from django.db import models
from django.contrib.auth.models import User


class Discounts(models.Model):
    class Meta:
        db_table = 'nitro_discounts'

    discount_id = models.CharField(max_length=150, unique=True)
    discount_name = models.CharField(max_length=150)
    discount_percent = models.FloatField()
    discount_amount = models.FloatField()
    discount_torder = models.BooleanField()
    discount_tuses = models.IntegerField()
    discount_usespuser = models.IntegerField()


class POS(models.Model):
    class Meta:
        db_table = 'nitro_pos'

    p_id = models.CharField(unique=True, max_length=3)
    location = models.CharField(max_length=255, null=True)
    deploy_state = models.BooleanField()
    wifinetwork = models.CharField(max_length=255, null=True)
    wifiusername = models.CharField(max_length=255, null=True)
    wifipassword = models.CharField(max_length=50)


class UserProfile(models.Model):
    class Meta:
        db_table = 'nitro_profile'
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)


class PaymentDataStream(models.Model):
    class Meta:
        db_table = 'nitro_paymentdtstream'
    payment_ID = models.TextField()
    payment_status = models.BooleanField()


class SKU(models.Model):
    class Meta:
        db_table = 'nitro_sku'
    s_id = models.CharField(unique=True, max_length=4)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    volume = models.IntegerField()
    volumeunits = models.IntegerField()
    volumeunitprice = models.FloatField()


class OrderLog(models.Model):
    class Meta:
        db_table = 'nitro_orderlog'

    o_id = models.CharField(unique=True, max_length=9)
    o_date = models.DateField()
    o_time = models.DateTimeField()
    p_id = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='pos_id')
    payment_ID = models.ForeignKey(PaymentDataStream, on_delete=models.CASCADE, related_name='pay_id')
    payment_status = models.ForeignKey(PaymentDataStream, on_delete=models.CASCADE, related_name='pay_status')
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cus_id')
    s_id = models.ForeignKey(SKU, on_delete=models.CASCADE, related_name='sku_id')
    ordervolume = models.IntegerField()
    ordervalue = models.FloatField()
    discount_id = models.ForeignKey(Discounts, on_delete=models.CASCADE)

