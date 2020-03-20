from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import POS, SKU


class POSSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = ('p_id', 'location', 'deploy_state', 'wifinetwork', 'wifiusername',
                  'wifipassword')

    def create(self, validated_data):
        _p_id = validated_data.get('p_id')
        _location = validated_data.get('location')
        _deploy_state = validated_data.get('deploy_state')
        _wifinetwork = validated_data.get('wifinetwork')
        _wifiusername = validated_data.get('wifiusername')
        _wifipassword = validated_data.get('wifipassword')

        new_pos_dict = {
            "p_id": _p_id,
            "location": _location,
            "deploy_state": _deploy_state,
            "wifinetwork": _wifinetwork,
            "wifiusername": _wifiusername,
            "wifipassword": _wifipassword,
        }

        try:
            pos = POS.objects.create(**new_pos_dict)
        except Exception as e:
            print(e)
            return None
        return pos

    def update(self, instance, validated_data):
        """
        Update and return an existing `SKU` instance, given the validated data.
        """
        instance.p_id = validated_data.get('p_id', instance.p_id)
        instance.location = validated_data.get('location', instance.location)
        instance.deploy_state = validated_data.get('deploy_state', instance.deploy_state)
        instance.wifinetwork = validated_data.get('wifinetwork', instance.wifinetwork)
        instance.wifiusername = validated_data.get('wifiusername', instance.wifiusername)
        instance.wifipassword = validated_data.get('wifipassword', instance.wifipassword)
        instance.save()
        return instance


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('s_id', 'name', 'desc', 'volume', 'volumeunits',
                  'volumeunitprice')

    def create(self, validated_data):
        _sid = validated_data.get('s_id')
        _name = validated_data.get('name')
        _desc = validated_data.get('desc')
        _volume = validated_data.get('volume')
        _volumeunits = validated_data.get('volumeunits')
        _volumeunitprice = validated_data.get('volumeunitprice')

        new_sku_dict = {
            "s_id": _sid,
            "name": _name,
            "desc": _desc,
            "volume": _volume,
            "volumeunits": _volumeunits,
            "volumeunitprice": _volumeunitprice,
        }
        try:
            sku = SKU.objects.create(**new_sku_dict)
        except Exception as e:
            print(e)
            return None
        return sku

    def update(self, instance, validated_data):
        """
        Update and return an existing `SKU` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.volume = validated_data.get('volume', instance.volume)
        instance.volumeunits = validated_data.get('volumeunits', instance.volumeunits)
        instance.volumeunitprice = validated_data.get('volumeunitprice', instance.volumeunitprice)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    def get_phone_number(self, obj):
        return obj.profile.phone_number

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
