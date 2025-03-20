from math import sqrt

from datetime import datetime
from networks.models import Network
from best_apr.models import Pool, EternalFarming, LimitFarming
from backend.consts import DEFAULT_CRYPTO_ADDRESS
import logging

logging.basicConfig(level=logging.DEBUG)

def tick_to_sqrt_price(tick):
    return sqrt(pow(1.0001, tick))


def get_amounts(liquidity, tickLower, tickUpper, currentTick):
    currentPrice = tick_to_sqrt_price(currentTick)
    lowerPrice = tick_to_sqrt_price(tickLower)
    upperPrice = tick_to_sqrt_price(tickUpper)
    if currentPrice < lowerPrice:
        amount1 = 0
        amount0 = liquidity * (1 / lowerPrice - 1 / upperPrice)
    elif lowerPrice <= currentPrice <= upperPrice:
        amount1 = liquidity * (currentPrice - lowerPrice)
        amount0 = liquidity * (1 / currentPrice - 1 / upperPrice)
    else:
        amount1 = liquidity * (upperPrice - lowerPrice)
        amount0 = 0
    return amount0, amount1


def update_pools_apr(network: Network):
    pools_json = network.get_current_pools_info()
    logging.debug("network=%s", network.title)
    ##logging.debug("pools_length=%s", len(pools_json))
    pools_tick = {}
    pools_current_tvl = {}
    pools_fees = {}

    for pool in pools_json:
        pools_tick[pool['id']] = int(pool['tick'])
        pools_current_tvl[pool['id']] = 0
        days = 7
        try:
            pools_fees[pool['id']] += pool['feesToken0']
        except KeyError:
            pools_fees[pool['id']] = pool['feesToken0']
        pools_fees[pool['id']] += pool['feesToken1'] * float(pool['token0Price'])
        positions_json = []
        logging.debug("pool id=%s", pool['id'])
        positions_json = network.get_pool_day_data(pool['id'], days)
        ##logging.debug("position00=%s", positions_json)
        # Calculate total fees earned
        total_fees_earned = sum(float(position["feesUSD"]) for position in positions_json)

        last_n_days_tvl = sum(float(position["tvlUSD"]) for position in positions_json)

        apr = (total_fees_earned / (last_n_days_tvl)) * 365 * 100

        pool_object = Pool.objects.filter(address=pool['id'])
        ##logging.debug("pool02=%s", pool)
        if not pool_object:
            pool_object = Pool.objects.create(
                title=pool['token0']['name'] + ' : ' + pool['token1']['name'],
                address=pool['id'],
                network=network
            )
        else:
            pool_object = pool_object[0]
        if apr:
            pool_object.last_apr = apr
        else:
            pool_object.last_apr = 0.0
        pool_object.save()
    
def update_max_pools_apr(network: Network):
    pools_json = network.get_current_pools_info()

    pools_tick = {}
    pools_liquidity = {}
    pools_current_tvl = {}
    pools_fees = {}
    max_apr = 0

    for pool in pools_json:
        pools_tick[pool['id']] = int(pool['tick'])
        pools_liquidity[pool['id']] = float(pool['liquidity'])
        pools_current_tvl[pool['id']] = 0
        try:
            pools_fees[pool['id']] += pool['feesToken0']
        except KeyError:
            pools_fees[pool['id']] = pool['feesToken0']
        pools_fees[pool['id']] += pool['feesToken1'] * float(pool['token0Price'])

        positions_json = network.get_positions_of_pool(pool['id'])

        for position in positions_json:
            current_tick = pools_tick[position['pool']['id']]
            if int(position['lowerTick']['tickIdx']) < current_tick < int(position['upperTick']['tickIdx']):
                (amount0, amount1) = get_amounts(
                    int(position['liquidity']),
                    int(position['lowerTick']['tickIdx']),
                    int(position['upperTick']['tickIdx']),
                    current_tick,
                )
                amount0 = amount0 / pow(10, int(pool['token0']['decimals']))
                amount1 = (amount1 / pow(10, int(pool['token1']['decimals'])))

                pos_fees = pools_fees[pool['id']] * float(position['liquidity']) / float(pools_liquidity[pool['id']]) 

                pos_tvl = amount0 + amount1 * float(position['pool']['token0Price'])
                
                if pos_tvl > 0:
                    apr = pos_fees * 100 * 365 / pos_tvl 
                    if apr > max_apr:
                        max_apr = apr

        pool_object = Pool.objects.filter(address=pool['id'])
        if not pool_object:
            pool_object = Pool.objects.create(
                title=pool['token0']['name'] + ' : ' + pool['token1']['name'],
                address=pool['id'],
                network=network
            )
        else:
            pool_object = pool_object[0]
        pool_object.max_apr = max_apr
        pool_object.save()
        max_apr = 0

def update_eternal_farmings_apr(network: Network):
    farmings = network.get_eternal_farmings_info()
    for farming in farmings:
        token_ids = network.get_positions_in_eternal_farming(farming['id'])
        token0 = network.get_token_info_by_address(farming['rewardToken'])[0]
        total_native_amount = 0.0
        positions = network.get_positions_by_id(token_ids)
        for position in positions:
            (amount0, amount1) = get_amounts(
                int(position['liquidity']),
                int(position['tickLower']['tickIdx']),
                int(position['tickUpper']['tickIdx']),
                int(position['pool']['tick']),
            )
            total_native_amount += amount0 * \
                                  float(position['pool']['token0']['derivedMatic']) \
                                  / 10 ** int(position['pool']['token0']['decimals'])
            total_native_amount += amount1 \
                                  * float(position['pool']['token1']['derivedMatic']) \
                                  / 10 ** int(position['pool']['token1']['decimals'])

        reward_per_second = int(farming['rewardRate']) * float(token0['derivedMatic']) / 10 ** int(token0['decimals'])
        if farming['bonusRewardToken'] != DEFAULT_CRYPTO_ADDRESS:
            token1 = network.get_token_info_by_address(farming['bonusRewardToken'])[0]
            reward_per_second += int(farming['bonusRewardRate']) * float(token1['derivedMatic']) / 10 ** int(
                token1['decimals'])
        apr = (reward_per_second) \
              / total_native_amount * 60 * 60 * 24 * 365 * 100 if total_native_amount > 0 else \
            -1.0

        farming_object = EternalFarming.objects.filter(hash=farming['id'])
        if not farming_object:
            farming_object = EternalFarming.objects.create(
                hash=farming['id'],
                network=network
            )
        else:
            farming_object = farming_object[0]
        farming_object.last_apr = apr
        farming_object.native_amount = total_native_amount
        farming_object.save()

def update_eternal_farmings_max_apr(network: Network):
    farmings = network.get_eternal_farmings_info()
    for farming in farmings:
        token_ids = network.get_positions_in_eternal_farming(farming['id'])
        token0 = network.get_token_info_by_address(farming['rewardToken'])[0]
        total_native_amount = 0.0
        max_apr = 0.0
        total_active_liquidity_farm = 0.0
        positions = network.get_positions_by_id(token_ids)

        for position in positions:
            if int(position['tickLower']['tickIdx']) < int(position['pool']['tick']) < int(position['tickUpper']['tickIdx']):
                total_active_liquidity_farm += float(position['liquidity'])

        reward_per_second = int(farming['rewardRate']) * float(token0['derivedMatic']) / 10 ** int(token0['decimals'])
        if farming['bonusRewardToken'] != DEFAULT_CRYPTO_ADDRESS:
            token1 = network.get_token_info_by_address(farming['bonusRewardToken'])[0]
            reward_per_second += int(farming['bonusRewardRate']) * float(token1['derivedMatic']) / 10 ** int(
                token1['decimals'])

        for position in positions:
            total_native_amount = 0
            if int(position['tickLower']['tickIdx']) < int(position['pool']['tick']) < int(position['tickUpper']['tickIdx']):
                (amount0, amount1) = get_amounts(
                    int(position['liquidity']),
                    int(position['tickLower']['tickIdx']),
                    int(position['tickUpper']['tickIdx']),
                    int(position['pool']['tick']),
                )
                total_native_amount = amount0 * \
                                    float(position['pool']['token0']['derivedMatic']) \
                                    / 10 ** int(position['pool']['token0']['decimals'])
                total_native_amount += amount1 \
                                    * float(position['pool']['token1']['derivedMatic']) \
                                    / 10 ** int(position['pool']['token1']['decimals'])
            
            if total_native_amount > 0 and total_active_liquidity_farm > 0:  
                apr = (reward_per_second) * 86400 * 365 * 100 * float(position['liquidity']) / total_active_liquidity_farm \
                    / total_native_amount 
            else:
                apr = 0

            if apr > max_apr:
                max_apr = apr

        farming_object = EternalFarming.objects.filter(hash=farming['id'])
        if not farming_object:
            farming_object = EternalFarming.objects.create(
                hash=farming['id'],
                network=network
            )
        else:
            farming_object = farming_object[0]
        farming_object.max_apr = max_apr
        farming_object.save()

def update_limit_farmings_apr(network: Network):
    farmings = network.get_limit_farmings_info()
    for farming in farmings:
        token_ids = network.get_positions_in_limit_farming(farming['id'])
        token0 = network.get_token_info_by_address(farming['rewardToken'])[0]
        token1 = network.get_token_info_by_address(farming['bonusRewardToken'])[0]
        total_native_amount = 0.0
        positions = network.get_positions_by_id(token_ids)
        for position in positions:
            (amount0, amount1) = get_amounts(
                int(position['liquidity']),
                int(position['tickLower']['tickIdx']),
                int(position['tickUpper']['tickIdx']),
                int(position['pool']['tick']),
            )
            total_native_amount += amount0 * \
                                  float(position['pool']['token0']['derivedMatic']) \
                                  / 10 ** int(position['pool']['token0']['decimals'])
            total_native_amount += amount1 \
                                  * float(position['pool']['token1']['derivedMatic']) \
                                  / 10 ** int(position['pool']['token1']['decimals'])

        duration = 86400 * 365 / (int(farming['endTime']) - int(farming['startTime']))
        rewards_amount_0 = int(farming['reward']) * float(token0['derivedMatic']) / \
                           10 ** int(token0['decimals'])
        rewards_amount_1 = int(farming['bonusReward']) * float(token1['derivedMatic']) / \
                           10 ** int(token1['decimals'])

        apr = (rewards_amount_0 + rewards_amount_1) * duration / total_native_amount * 100 \
            if total_native_amount > 0 and int(farming['endTime']) > int(datetime.now().timestamp()) else -1

        farming_object = LimitFarming.objects.filter(hash=farming['id'])
        if not farming_object:
            farming_object = LimitFarming.objects.create(
                hash=farming['id'],
                network=network
            )
        else:
            farming_object = farming_object[0]
        farming_object.native_amount = total_native_amount
        farming_object.last_apr = apr
        farming_object.save()
