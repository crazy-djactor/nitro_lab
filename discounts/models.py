from django.db import models

class Discounts(models.Model):

    discount_id = models.TextField(primary_key=True)
    """Discount_ID
    """

    discount_name = models.TextField()
    """Discount_Name
    """

    discount_percent = models.FloatField()
    """Discount_Percent
    """

    discount_amount = models.FloatField()
    """Discount_Amount
    """

    discount_torder = models.BooleanField()
    """Discount_TotalOrder
    """

    discount_tuses = models.IntegerField()
    """Discount_TotalUses
    """

    discount_usespuser = models.IntegerField()
    """Discount_UsesPerUser
    """