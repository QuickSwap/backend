from django.urls import path
from .views import ListPoolAprs,TotalDexData, LandingDayData, BuybackData, ListMaxPoolAprs, ListEternalFarmingsMaxAprs, ListEternalFarmingsAprs, ListLimitFarmingsTvl, ListLimitFarmingsAprs, DexData, ListEternalFarmingsTvl

urlpatterns = [
    path('APR/pools/', ListPoolAprs.as_view(), name='get_pools_apr'),
    path('APR/pools/max', ListMaxPoolAprs.as_view(), name='get_pools_max_apr'),
    path('APR/eternalFarmings/', ListEternalFarmingsAprs.as_view(), name='get_eternal_farmings_apr'),
    path('APR/eternalFarmings/max', ListEternalFarmingsMaxAprs.as_view(), name='get_eternal_farmings_max_apr'),
    path('APR/limitFarmings/', ListLimitFarmingsAprs.as_view(), name='get_limit_farmings_apr'),
    path('TVL/limitFarmings/', ListLimitFarmingsTvl.as_view(), name='get_limit_farmings_tvl'),
    path('TVL/eternalFarmings/', ListEternalFarmingsTvl.as_view(), name='get_eternal_farmings_tvl'),
    path('landingData/', DexData.as_view(), name='get_dex_data'),
    path('buybackData/', BuybackData.as_view(), name='get_bb_data'),
    path('totalData/', TotalDexData.as_view(), name='get_total_data'),
    path('landingDayData/', LandingDayData.as_view(), name='get_landing_day_data')
]
