from rest_framework import serializers

from .models import SKU
from django.contrib.auth.models import User


class SKUSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = SKU
        fields = ('s_id', 'name', 'desc', 'volume', 'volumeunits',
                  'volumeunitprice')


class SKUGetSerializer(SKUSerializer):
    pass
    # image_file = serializers.SerializerMethodField()
    # def get_image_file(self, instance):
    #     return generate_aws_url(instance.image_file)

# class UserSerializer(serializers.ModelSerializer):
#     devices = serializers.PrimaryKeyRelatedField(many=True, queryset=POS.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'device')
