from django.db import models

from base.models import AbstractBaseModel
from networks.models import Network
from networks.models import LendingNetwork


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
    network = models.ForeignKey(LendingNetwork, on_delete= models.CASCADE)
    fees_now = models.FloatField(blank=True, null=True)
    volume_now = models.FloatField(blank=True, null=True)
    tvl_now = models.FloatField(blank=True, null=True)
    fees_day = models.FloatField(blank=True, null=True)
    volume_day = models.FloatField(blank=True, null=True)
    tvl_day = models.FloatField(blank=True, null=True)
    fees_2days = models.FloatField(blank=True, null=True)
    volume_2days = models.FloatField(blank=True, null=True)
    tvl_2days = models.FloatField(blank=True, null=True)
    days_data = models.JSONField(blank=True, null=True)