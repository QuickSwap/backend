from django.urls import path
from .views import ListPoolAprs, ListMaxPoolAprs, ListEternalFarmingsMaxAprs, ListEternalFarmingsAprs, ListLimitFarmingsTvl, ListLimitFarmingsAprs, DexData, ListEternalFarmingsTvl

urlpatterns = [
    path('APR/pools/', ListPoolAprs.as_view(), name='get_pools_apr'),
    path('APR/pools/max', ListMaxPoolAprs.as_view(), name='get_pools_max_apr'),
    path('APR/eternalFarmings/', ListEternalFarmingsAprs.as_view(), name='get_eternal_farmings_apr'),
    path('APR/eternalFarmings/max', ListEternalFarmingsMaxAprs.as_view(), name='get_eternal_farmings_max_apr'),
    path('APR/limitFarmings/', ListLimitFarmingsAprs.as_view(), name='get_limit_farmings_apr'),
    path('TVL/limitFarmings/', ListLimitFarmingsTvl.as_view(), name='get_limit_farmings_tvl'),
    path('TVL/eternalFarmings/', ListEternalFarmingsTvl.as_view(), name='get_eternal_farmings_tvl'),
    path('lendingData/',DexData.as_view(), name='get_dex_data')
]
