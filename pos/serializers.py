from rest_framework import serializers

from pos.utils import generate_aws_url
from .models import POS
from django.contrib.auth.models import User


class POSSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = POS
        fields = ('p_id', 'location', 'deploy_state', 'wifinetwork', 'wifiusername',
                  'wifipassword')


class POSGetSerializer(POSSerializer):
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
