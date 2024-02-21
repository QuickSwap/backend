from django.db import models

from base.models import AbstractBaseModel
from networks.models import Network, LandingNetwork


class Pool(AbstractBaseModel):
    title = models.CharField(max_length=64)
    address = models.CharField(max_length=42)
    last_apr = models.FloatField(blank=True, null=True)
    max_apr = models.FloatField(blank=True, null=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class EternalFarming(AbstractBaseModel):
    hash = models.CharField(max_length=66, unique=True)
    native_amount = models.FloatField(blank=True, null=True)
    last_apr = models.FloatField(blank=True, null=True)
    max_apr = models.FloatField(blank=True, null=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class LimitFarming(AbstractBaseModel):
    hash = models.CharField(max_length=66, unique=True)
    native_amount = models.FloatField(blank=True, null=True)
    last_apr = models.FloatField(blank=True, null=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class DexDayData(AbstractBaseModel):
    network = models.ForeignKey(LandingNetwork, on_delete= models.CASCADE)
    now = models.JSONField(blank=True, null=True)
    day_ago = models.JSONField(blank=True, null=True)
    two_days_ago = models.JSONField(blank=True, null=True)
    days_data = models.JSONField(blank=True, null=True)

class BuyBackData(AbstractBaseModel):
    buy_back_data = models.JSONField(blank=True,null=True)