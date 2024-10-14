from django.contrib.admin import ModelAdmin, register, display

# Register your models here.
from .models import Pool, EternalFarming, LimitFarming, DexDayData


@register(Pool)
class PoolAdmin(ModelAdmin):
    fields = (
        'title',
        'address',
        'last_apr',
        'max_apr',
    )
    list_display = (
        'title',
        'network',
        'address',
        'last_apr',
        'max_apr'
    )
    list_filter = (
        'network__title',
    )
    search_fields = (
        '=address',
    )
    ordering = (
        '-last_apr',
    )
    sortable_by = (
        'last_apr',
        'network',
    )
    empty_value_display = '-empty-'


@register(EternalFarming)
class EternalFarmingAdmin(ModelAdmin):
    fields = (
        'hash',
        'native_amount',
        'last_apr',
        'max_apr'
    )
    list_display = (
        'hash',
        'native_amount',
        'network',
        'last_apr',
        'max_apr'
    )
    list_filter = (
        'network__title',
    )
    search_fields = (
        '=hash',
    )
    ordering = (
        '-last_apr',
    )
    sortable_by = (
        'last_apr',
        'network'
    )
    empty_value_display = '-empty-'


@register(LimitFarming)
class LimitFarmingAdmin(ModelAdmin):
    fields = (
        'hash',
        'native_amount',
        'last_apr'
    )
    list_display = (
        'hash',
        'native_amount',
        'network',
        'last_apr'
    )
    list_filter = (
        'network__title',
    )
    search_fields = (
        '=hash',
    )
    ordering = (
        '-last_apr',
    )
    sortable_by = (
        'last_apr',
        'network'
    )
    empty_value_display = '-empty-'

@register(DexDayData)
class DexDayDataAdmin(ModelAdmin):
    fields = (
        'network',
        'days_data',
        
    )
    list_display = (
        'days_data',
        'network'
    )
    list_filter = (
        'network__title',
    )
    ordering = (
        'network__title',
    )
    sortable_by = (
        'network'
    )
    empty_value_display = '-empty-'