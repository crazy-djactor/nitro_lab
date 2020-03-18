from django.db import models


class PaymentDataStream(models.Model):
    payment_ID = models.TextField()
    """payment_ID
    """

    payment_status = models.BooleanField()
    """payment_status
    """
