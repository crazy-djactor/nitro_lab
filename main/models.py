from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class POS(models.Model):
    """
    Show POS info.
    """
    class Meta:
        db_table = 'nitro_pos'

    pos_id = models.CharField(primary_key=True, max_length=3)
    pos_sn = models.CharField(max_length=255)
    pos_auth_string = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    deploy_state = models.BooleanField()


class SKU(models.Model):
    """
    It is model for SKU. SKU can be attached on POS.
    So the relationship between SKU and POS is `Many To Many`
    """
    class Meta:
        db_table = 'nitro_sku'

    sku_id = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    volume = models.IntegerField()
    volume_units = models.IntegerField()
    volume_unit_price_customer = models.FloatField()
    volume_unit_price_guest = models.FloatField()
    image_path = models.CharField(max_length=255, null=True)
    image_path2 = models.CharField(max_length=255, null=True)
    last_change = models.DateTimeField(null=True, auto_now=True)
    batch_no = models.CharField(max_length=255, null=True)
    pos = models.ManyToManyField(POS, related_name='skus', through='Matching')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.last_change = datetime.now()
        super(SKU, self).save(force_insert=force_insert, force_update=force_update, using=using,
                              update_fields=update_fields)


class Matching(models.Model):
    """
    It is created by `through` on Pos model.
    Matching model is for `side` option that shows on where the SKU is attached on Pos.
    For example, 0 - left and 1 - right.
    """
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    matched_pos = models.ForeignKey(POS, on_delete=models.CASCADE)
    side = models.IntegerField()

    class Meta:
        db_table = "nitro_sku_pos"


class Discount(models.Model):
    class Meta:
        db_table = 'nitro_discount'

    discount_id = models.CharField(max_length=150, primary_key=True)
    discount_name = models.CharField(max_length=150)
    discount_percent = models.FloatField()                      # Percentage of discount
    discount_amount = models.FloatField()                       # Absolute amount of discount
    discount_total_order = models.BooleanField(default=False)   # True: Totally free
    discount_total_uses = models.IntegerField()                 # Limit number of discounts that can be applied.
    discount_current_uses = models.IntegerField(default=0)      # Current number of discounts that was applied so far.


class Customer(models.Model):
    class Meta:
        db_table = 'nitro_customer'
    customer_id = models.CharField(max_length=32, unique=True)
    customer_name = models.CharField(max_length=32, blank=True)
    customer_email = models.EmailField(unique=True)
    customer_phone = models.CharField(max_length=16, blank=True)
    customer_pin = models.CharField(max_length=255)
    discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING, related_name='customer')


class LocationProduct(models.Model):
    """
    Location Product model
    """
    class Meta:
        db_table = 'nitro_location_product'

    location_product_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now=True)
    personnel = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='location_product')
    pos = models.ForeignKey(POS, on_delete=models.DO_NOTHING, related_name='location_product')
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING, related_name='location_product')
    batch_no = models.CharField(max_length=255)


class Service(models.Model):
    """
    Service Model
    Every personnel can serve only for his own
    """
    class Meta:
        db_table = 'nitro_service'
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=255)
    service_description = models.TextField()
    personnel = models.ManyToManyField(User, related_name='service', through="ServicePersonnel")


class ServicePersonnel(models.Model):
    class Meta:
        db_table = 'nitro_service_personnel'
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service')
    personnel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personnel')


class ServiceLog(models.Model):
    """
    Service Log Model
    """
    class Meta:
        db_table = 'nitro_service_log'

    service_log_id = models.AutoField(primary_key=True)
    service_datetime = models.DateTimeField(auto_now=True)
    personnel = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='service_log')
    pos = models.ForeignKey(POS, on_delete=models.DO_NOTHING, related_name='service_log')
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, related_name='service_log')


class Promo(models.Model):
    class Meta:
        db_table = 'nitro_promo'

    code = models.CharField(unique=True, max_length=32, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.ForeignKey(Discount, on_delete=models.DO_NOTHING, related_name='promo')

    @staticmethod
    def check_promo(promo_code):
        try:
            promo = Promo.objects.get(code=promo_code)
            if promo and promo.start_date <= datetime.date(datetime.now()) < promo.end_date:
                return promo
        except Exception as exc:
            print(exc)
        return None


class Transaction(models.Model):

    class Meta:
        db_table = 'nitro_transaction'

    transaction_id = models.BigIntegerField(primary_key=True)
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING, related_name='transaction')
    pos = models.ForeignKey(POS, on_delete=models.DO_NOTHING, related_name='transaction')
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='transaction', null=True)
    promo = models.ForeignKey(Promo, on_delete=models.DO_NOTHING, related_name='transaction', null=True)
    order_id = models.UUIDField()
    web_link = models.URLField()
    app_link = models.URLField()
    payment_access_token = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="NOT_APPROVED", auto_created=True)
    amount = models.FloatField(null=True, default=0)
    payment_method = models.CharField(max_length=50, null=True)
    credit_card_nick_name = models.CharField(max_length=127, null=True)
    credit_card_brand = models.CharField(max_length=20, null=True)
    reg_key = models.CharField(max_length=20, null=True)
    transaction_date = models.DateTimeField(null=True)


class OrderLog(models.Model):
    class Meta:
        db_table = 'nitro_orderlog'

    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING, related_name='orderlog')
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING, related_name='orderlog')
    pos = models.ForeignKey(POS, on_delete=models.DO_NOTHING, related_name='orderlog')
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='orderlog', null=True)
    promo = models.ForeignKey(Promo, on_delete=models.DO_NOTHING, related_name='orderlog', null=True)
    order_id = models.UUIDField()
    transaction_status = models.CharField(max_length=20)
    order_volume = models.IntegerField(null=True)
    order_value = models.FloatField(null=True)
    discount_total = models.FloatField(null=True)
    customer_payment_net = models.FloatField(null=True)
    customer_payment_base = models.FloatField(null=True)
    customer_payment_vat = models.FloatField(null=True)
    order_timeout = models.BooleanField(null=True)
    order_datetime = models.DateTimeField(auto_now=True)
