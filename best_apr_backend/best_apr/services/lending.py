from datetime import datetime
from networks.models import LendingNetwork
from best_apr.models import DexDayData

def update_dex_data(network: LendingNetwork):
    daysData = network.getDexDaysData()

    dex_object = DexDayData.object.filter(network = network)
    if not dex_object:
        dex_object = DexDayData.objects.create(
            network=network
        )
    else:
        dex_object = dex_object[0]
    dex_object.days_data = daysData
    dex_object.save()

