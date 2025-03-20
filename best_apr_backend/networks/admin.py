from django.contrib.admin import register, ModelAdmin

from .models import Network
from .models import LandingNetwork


# Register your models here.
@register(Network)
class NetworkModelAdmin(ModelAdmin):
    fields = (
        'title',
        'subgraph_url',
        'subgraph_blocks_urls',
        'subgraph_farming_url',
        'api_key',
        '_is_displayed',
    )
    list_display = (
        'id',
        'title',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'title',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'

@register(LandingNetwork)
class LandingNetworkModelAdmin(ModelAdmin):
    fields = (
        'title',
        'subgraph_url',
        'subgraph_blocks_urls',
        '_is_displayed',
    )
    list_display = (
        'id',
        'title',
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    list_filter = (
        '_created_at',
        '_updated_at',
        '_is_displayed',
    )
    search_fields = (
        '=id',
        'title',
    )
    ordering = (
        '-_created_at',
    )
    empty_value_display = '-empty-'
