from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.db import IntegrityError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, \
    GenericAPIView
from rest_framework import status
from allauth.account.utils import complete_signup
from rest_auth.models import TokenModel
from rest_auth.views import LoginView
from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes

from main.models import UserProfile, POS, SKU
from main.permissions import IsAuthenticated, IsAdminOrAuthenticated, IsAuthenticatedOrReadOnly
from main.serializers import SKUSerializer, POSSerializer, UserSerializer, CreateUserSerializer


# ================= PROFILE ZONE ====================#
# UserProfile
class GetProfile(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        # queryset = User.objects.all()
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.save()
        user.profile.phone_number = request.data['phone_number']
        user.profile.save()
        return Response(data=self.get_serializer(user).data)


class CreateUserProfile(CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Some fields are missing', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'],
                                            first_name=data['first_name'], last_name=data['last_name'], is_active=True)
            profile = UserProfile.objects.create(phone_number=data['phone_number'], user_id=user.id)
        except IntegrityError:
            return Response({
                'message': 'Email already exists.',
                'errors': {'email': 'Email already exists.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)


# ================= POS ZONE ====================#
class PostPOS(CreateAPIView):
    serializer_class = POSSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)

    def post(self, request, *args, **kwargs):
        serializer = POSSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Some fields are missing', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        sku = serializer.save()
        return Response(data=POSSerializer(sku).data, status=status.HTTP_201_CREATED)


class GetPutPatchDeletePOS(GenericAPIView):
    serializer_class = POSSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        try:
            pos = POS.objects.get(p_id=self.kwargs.get('p_id'))
        except SKU.DoesNotExist:
            return None
        return pos

    def get(self, request, *args, **kwargs):
        pos = self.get_queryset()
        if pos is None:
            content = {
                'status': 'Not Found POS'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        serializer = POSSerializer(pos)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pos = self.get_queryset()
        if pos is None:
            content = {
                'status': 'Not Found POS'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        serializer = POSSerializer(pos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pos = self.get_queryset()
        serializer = POSSerializer(pos)
        return Response(serializer.data, status=status.HTTP_200_OK)


# get_pos_list
class GetPOSList(RetrieveAPIView):
    serializer_class = POSSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        query_set = POS.objects.all()
        serializer = POSSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ================= SKU ZONE ====================#
class PostSKU(CreateAPIView):
    serializer_class = SKUSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)

    def post(self, request, *args, **kwargs):
        serializer = SKUSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Some fields are missing', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        sku = serializer.save()
        return Response(data=SKUSerializer(sku).data, status=status.HTTP_201_CREATED)


class GetPutPatchDeleteSKU(GenericAPIView):
    serializer_class = SKUSerializer
    permission_classes = (IsAdminOrAuthenticated,)

    def get_queryset(self):
        try:
            sku = SKU.objects.get(s_id=self.kwargs.get('s_id'))
        except SKU.DoesNotExist:
            return None
        return sku

    def get(self, request, *args, **kwargs):
        sku = self.get_queryset()
        if sku is None:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        serializer = SKUSerializer(sku)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        sku = self.get_queryset()
        if sku is None:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        serializer = SKUSerializer(sku, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pos = self.get_queryset()
        serializer = SKUSerializer(pos)
        return Response(serializer.data, status=status.HTTP_200_OK)


# get_sku_list
class GetSKUList(RetrieveAPIView):
    serializer_class = SKUSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        query_set = SKU.objects.all()
        serializer = SKUSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
