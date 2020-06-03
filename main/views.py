import uuid
from secrets import token_hex

from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from main.line import reserve_payment, check_payment_status, confirm, pay_preapproved, expire_reg_key, void_transaction
from main.models import POS, SKU, Service, OrderLog, Customer, Promo, Matching, LocationProduct, Transaction, Discount
from main.permissions import IsAuthenticated, IsPosAuthenticated
from main.serializers import SKUSerializer, POSSerializer, ServiceSerializer, AdminSerializer, CustomerSerializer, \
    MatchingSerializer, ServiceLogSerializer


class POSView(GenericAPIView):
    serializer_class = POSSerializer

    def get_queryset(self):
        try:
            pos = POS.objects.get(pos_sn=self.kwargs.get('pos_sn'))
        except POS.DoesNotExist:
            return None
        return pos

    def get(self, request, *args, **kwargs):
        pos = self.get_queryset()
        if pos is None:
            content = {
                'status': 'Not Found POS'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(pos, data={'pos_auth_string': token_hex(16)}, partial=True)
        if serializer.is_valid():
            serializer.save()

        data = {
            'pos_id': pos.pos_id,
            'pos_auth_string': serializer.validated_data['pos_auth_string']
        }
        return Response(data, status=status.HTTP_200_OK)


class SKUView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = SKUSerializer
    permission_classes = (IsAdminUser, )
    queryset = SKU.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        _filter = {"sku_id": self.request.data['sku_id']}
        obj = get_object_or_404(queryset, **_filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        _location_product = {
            'personnel_id': request.user.id,
            'pos_id': request.data['pos_id'],
            'sku_id': request.data['sku_id'],
            'batch_no': request.data['batch_no']
        }
        new_log = LocationProduct.objects.create(**_location_product)
        new_log.save()
        return super(SKUView, self).partial_update(request, *args, **kwargs)


class SKUPOSView(RetrieveAPIView):

    serializer_class = SKUSerializer
    permission_classes = (IsPosAuthenticated,)

    def get_queryset(self):
        try:
            sku = SKU.objects.filter(pos__pos_id=self.kwargs.get('pos_id'))
            matching = Matching.objects.filter(matched_pos=self.kwargs.get('pos_id'))
        except SKU.DoesNotExist:
            return None, None
        return sku, matching

    def get(self, request, *args, **kwargs):
        sku_query, matching_query = self.get_queryset()

        serializer = self.serializer_class(sku_query, context={'user': request.user}, many=True)
        matching_sz = MatchingSerializer(matching_query, context={'user': request.user}, many=True)
        response_data = serializer.data.copy()
        for _sku in response_data:
            for _match in matching_sz.data:
                if _sku['sku_id'] == _match['sku']:
                    _sku['side'] = _match['side']
                    break
        return Response(response_data, status=status.HTTP_200_OK)


class CustomerView(CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = ()


class ServiceView(ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_queryset(self):
        services = Service.objects.filter(personnel__username=self.request.user.username)
        return services

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set, many=True)
        available_data = serializer.data
        all_query = Service.objects.all()
        serializer = self.serializer_class(all_query, many=True)
        all_data = serializer.data
        return Response({'available': available_data,
                         'all': all_data}, status=status.HTTP_200_OK)


class ServiceLogView(CreateAPIView):
    serializer_class = ServiceLogSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def create(self, request, *args, **kwargs):
        request.data['personnel'] = request.user.id
        return super().create(request, *args, **kwargs)


class PaymentReserveView(CreateAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        pos_id = request.data['pos_id']
        sku_id = request.data['sku_id']
        customer_id = request.data.get('customer_id')
        promo_code = request.data.get('promo_code')

        sku = SKU.objects.get(sku_id=sku_id)
        order_id = str(uuid.uuid4())
        ret, msg = reserve_payment(order_id=order_id, product_id=sku_id, product_name=sku.name,
                                   image_url=sku.image_path)
        if ret:
            _info = {
                'transaction_id': msg['info']['transactionId'],
                'sku_id': sku_id,
                'pos_id': pos_id,
                'order_id': order_id,
                'web_link': msg['info']['paymentUrl']['web'],
                'app_link': msg['info']['paymentUrl']['app'],
                'payment_access_token': msg['info']['paymentAccessToken']
            }
            if customer_id:
                customer = Customer.objects.get(customer_id=customer_id)
                if customer is not None:
                    _info['customer_id'] = customer_id
            promo = Promo.check_promo(promo_code=promo_code)
            if promo is not None:
                _info['promo_id'] = promo.code

            transaction = Transaction.objects.create(**_info)
            transaction.save()

            res = {
                'transaction_id': _info['transaction_id'],
                'customer_id': _info.get('customer_id'),
                'app_link': _info['app_link'],
                'web_link': _info['web_link']
            }
            return Response(status=status.HTTP_200_OK, data=res)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=msg)


MAX_CUP_CAPACITY = 500


class PaymentCheckView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        transaction_id = int(kwargs['transaction_id'])
        ret, check_msg = check_payment_status(transaction_id=transaction_id)
        if ret:
            ret, confirm_msg = confirm(transaction_id=transaction_id)
            if ret and confirm_msg['returnCode'] == '0000':
                # Try Pay Preapproved payment to see if customer's payment is available.
                reg_key = confirm_msg['info']['regKey']
                transaction = Transaction.objects.get(transaction_id=transaction_id)
                sku = SKU.objects.get(sku_id=transaction.sku_id)
                max_amount = MAX_CUP_CAPACITY * sku.volume_unit_price_guest / sku.volume_units
                ret, pay_msg = pay_preapproved(reg_key=reg_key, amount=max_amount, product_name=sku.name,
                                               order_id=str(uuid.uuid4()), capture=False)
                if ret and pay_msg['returnCode'] == '0000':
                    ret, void_msg = void_transaction(transaction_id=pay_msg['info']['transactionId'])
                    if ret and void_msg['returnCode'] == '0000':
                        pay_info = confirm_msg['info']['payInfo'][0]
                        transaction.status = "CONFIRMED"
                        transaction.payment_method = pay_info['method']
                        transaction.credit_card_nick_name = pay_info.get('creditCardNickname', "")
                        transaction.credit_card_brand = pay_info.get('creditCardBrand', '')
                        transaction.reg_key = confirm_msg['info']['regKey']
                        transaction.save()
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data=void_msg)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=pay_msg)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=confirm_msg)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentPayView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        transaction_id = request.data['transaction_id']
        volume = request.data['volume']
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        sku = SKU.objects.get(sku_id=transaction.sku_id)

        unit_price = sku.volume_unit_price_customer if transaction.customer_id else sku.volume_unit_price_guest
        total_price = volume / sku.volume_units * unit_price

        discount_total = 0
        msg_discount = "No discount"
        if transaction.promo_id:
            promo = Promo.objects.get(code=transaction.promo_id)
            discount = Discount.objects.get(discount_id=promo.discount_id)
            if discount.discount_current_uses < discount.discount_total_uses:
                if discount.discount_total_order:
                    discount_total = total_price
                    msg_discount = "Skip payment"
                elif discount.discount_percent:
                    discount_total = total_price * discount.discount_percent / 100
                    msg_discount = f"{discount.discount_percent}% discount"
                elif discount.discount_amount:
                    discount_total = discount.discount_amount
                    msg_discount = f"{discount.discount_amount} BAHT discount)"
        else:
            discount = None

        charged_price = total_price - discount_total
        reg_key = transaction.reg_key
        ret, msg = pay_preapproved(reg_key=reg_key,
                                   amount=charged_price,
                                   product_name=sku.name,
                                   order_id=transaction.order_id)
        if ret:
            expire_reg_key(reg_key=reg_key)
            _order_log = {
                'transaction_id': transaction_id,
                'sku_id': transaction.sku_id,
                'pos_id': transaction.pos_id,
                'customer_id': transaction.customer_id,
                'promo_id': transaction.promo_id,
                'order_id': transaction.order_id,
                'transaction_status': transaction.status,
                'order_volume': volume,
                'order_value': total_price,
                'discount_total': discount_total,
                'customer_payment_net': charged_price,
                'customer_payment_base': round(charged_price / 1.07, 2),
                'customer_payment_vat': round(charged_price * (1 - 1 / 1.07), 2)
            }
            order_log = OrderLog.objects.create(**_order_log)
            order_log.save()
            if discount is not None:
                discount.discount_current_uses = discount.discount_current_uses + 1
                discount.save()
            return Response(status=status.HTTP_200_OK, data={'price': charged_price, "discount": msg_discount})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=msg)


# ========= Log in ==========
class AdminView(TokenViewBase):
    authentication_classes = ()
    serializer_class = AdminSerializer
