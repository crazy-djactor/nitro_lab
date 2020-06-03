from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


from main.models import POS, SKU, Service, ServiceLog, Matching, Customer


class POSSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = ('pos_id', 'location', 'deploy_state', 'pos_sn', 'pos_auth_string')

    def create(self, validated_data):
        _pos_id = validated_data.get('pos_id')
        _pos_sn = validated_data.get('pos_sn')
        _location = validated_data.get('location')
        _deploy_state = validated_data.get('deploy_state')

        new_pos_dict = {
            "pos_id": _pos_id,
            "pos_sn": _pos_sn,
            "location": _location,
            "deploy_state": _deploy_state,
            "pos_auth_string": ""
        }

        try:
            pos = POS.objects.create(**new_pos_dict)
        except Exception as e:
            print(e)
            return None
        return pos

    def update(self, instance, validated_data):
        """
        Update and return an existing `POS` instance, given the validated data.
        """
        instance.pos_id = validated_data.get('pos_id', instance.pos_id)
        instance.pos_sn = validated_data.get('pos_sn', instance.pos_sn)
        instance.location = validated_data.get('location', instance.location)
        instance.deploy_state = validated_data.get('deploy_state', instance.deploy_state)
        instance.pos_auth_string = validated_data.get('pos_auth_string', instance.pos_auth_string)
        instance.save()
        return instance


class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = '__all__'


class SKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ('sku_id', 'name', 'desc', 'volume', 'volume_units', 'volume_unit_price_guest',
                  'volume_unit_price_customer', 'image_path', 'image_path2', 'batch_no', 'last_change')
        read_only_fields = ('last_change', 'image_path', 'image_path2')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service_id', 'service_name', 'service_description')


class ServiceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLog
        fields = '__all__'


class AdminSerializer(TokenObtainSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        login_user = User.objects.get(username=attrs['username'])

        refresh = self.get_token(self.user)

        data['is_admin'] = login_user.is_staff
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
