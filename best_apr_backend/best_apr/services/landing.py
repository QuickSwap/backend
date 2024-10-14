from datetime import datetime, timedelta
from networks.models import LandingNetwork
from best_apr.models import DexDayData, BuyBackData

from base.requests import send_post_request

def update_dex_data(network: LandingNetwork):
    daysData = network.getDexDaysData()

    day_ago_timestamp = round((datetime.now() - timedelta(days=1)).timestamp())
    two_days_ago_timestamp = round((datetime.now() - timedelta(days=2)).timestamp())
    now_timestamp = round(datetime.now().timestamp()) - 180

    now = network.getDexDataForTimestamp(now_timestamp)
    day_ago = network.getDexDataForTimestamp(day_ago_timestamp)
    two_days_ago = network.getDexDataForTimestamp(two_days_ago_timestamp)

    if now == None or day_ago == None or two_days_ago == None: 
        return
    dex_object = DexDayData.objects.filter(network = network)
    if not dex_object:
        dex_object = DexDayData.objects.create(
            network=network
        )
    else:
        dex_object = dex_object[0]
    dex_object.days_data = daysData
    dex_object.now = now
    dex_object.day_ago = day_ago
    dex_object.two_days_ago = two_days_ago
    dex_object.save()



def update_bb_data():

    ALGB_BUYBACK_TIMESTAMP = 1706612656 
    algb_rewards_api = 'https://api.studio.thegraph.com/query/50593/rewards/v0.0.1'
    def is_same_day(first_timestamp, second_timestamp):
        d1 = datetime.fromtimestamp(first_timestamp)
        d2 = datetime.fromtimestamp(second_timestamp)
        return (d1.year, d1.month, d1.day) == (d2.year, d2.month, d2.day)

    response = send_post_request(algb_rewards_api, json={
        'query': '''
            query algbRewards {
                histories(first: 1000, orderBy: id, orderDirection: asc) {    
                    id
                    rewardsAdded
                    burned
                    ALGBPrice
                }   
            }
        '''
    })


    histories = response['data']['histories']

    def process_history(history):
        algb_amount = (float(history['rewardsAdded']) + (float(history['burned']) / 2 if int(history['id']) > ALGB_BUYBACK_TIMESTAMP else float(history['burned']))) / 10 ** 18
        return {
            'time': int(history['id']),
            'value': algb_amount * float(history['ALGBPrice'])
        }

    processed_data = []
    for i, history in enumerate(histories):
        processed_history = process_history(history)
        if i == 0 or not is_same_day(processed_history['time'], processed_data[-1]['time']):
            processed_data.append(processed_history)
        else:
            processed_data[-1]['value'] += processed_history['value']

    bb_object = BuyBackData.objects.first()
    if not bb_object:
        bb_object = BuyBackData.objects.create(
            buy_back_data = processed_data
        )
    else:
        bb_object.buy_back_data = processed_data
    bb_object.save()
