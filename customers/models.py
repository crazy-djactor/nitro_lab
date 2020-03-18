from django.db import models


class Customers(models.Model):
    customer_id = models.TextField()
    """customer_id
    """

    payment_status = models.BooleanField()
    """payment_status
    """
