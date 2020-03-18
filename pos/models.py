from django.db import models
from .storage_backends import PrivateMediaStorage


class POS(models.Model):

    p_id = models.CharField(primary_key=True, max_length=3)
    """POS_ID
    """

    location = models.TextField()
    """POS_Location
    """

    deploy_state = models.BooleanField()
    """POS_DeployStatus
    """

    wifinetwork = models.TextField()
    """POS_Location
    """

    wifiusername = models.TextField()
    """POS_Location
    """

    wifipassword = models.TextField()
    """POS_Location
    """
