from django.db import models

from customers.models import Customers
from discounts.models import Discounts
from paymentdatastream.models import PaymentDataStream
from pos.models import POS
from sku.models import SKU


class OrderLog(models.Model):

    o_id = models.CharField(max_length=9)
    """Order_ID
    """

    o_date = models.DateField()
    """Order_Date
    """

    o_time = models.DateTimeField()
    """Order_Date
    """

    p_id = models.ForeignKey(POS,  on_delete=models.CASCADE)
    """foreign key POS_ID
    """

    payment_ID = models.ForeignKey(PaymentDataStream,  on_delete=models.CASCADE)
    """foreign key Payment ID
    """

    payment_status = models.ForeignKey(PaymentDataStream,  on_delete=models.CASCADE)
    """foreign key payment status
    """

    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    """foreign key customer_id
    """

    s_id = models.ForeignKey(SKU, on_delete=models.CASCADE)
    """foreign key sku_id
    """

    ordervolume = models.IntegerField()
    """OrderVolume in ML
    """

    ordervalue = models.FloatField()
    """OrderValue = (OV/SKU_VU)*SKU_VUP
    """

    discount_id = models.ForeignKey(Discounts, on_delete=models.CASCADE)