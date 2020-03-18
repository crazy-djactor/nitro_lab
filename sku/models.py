from django.db import models


class SKU(models.Model):

    s_id = models.CharField(primary_key=True, max_length=4)
    """SKU_ID
    """

    name = models.TextField()
    """SKU_Name
    """

    desc = models.TextField()
    """SKU_Description
    """

    volume = models.IntegerField()
    """SKU_Volume
    """

    volumeunits = models.IntegerField()
    """SKU_VolumeUnits
    0 = 1mL
    1 = 1L
    """

    volumeunitprice = models.FloatField()
    """SKU_VolumeUnitPrice
    """
