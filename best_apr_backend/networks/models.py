from time import time

from django.conf import settings
from django.db.models import (
    CharField,
    URLField,
    JSONField
)

from base.models import AbstractBaseModel
from base.requests import send_post_request
import logging

logging.basicConfig(level=logging.DEBUG)

# Create your models here.
class Network(AbstractBaseModel):
    title = CharField(
        max_length=255,
        verbose_name='Title',
    )
    subgraph_url = URLField(
        help_text='Subgraph about main contracts'
    )
    subgraph_blocks_urls = URLField(
        help_text='Subgraph about blockchain'
    )
    subgraph_farming_url = URLField(
        help_text='Subgraph about farmings'
    )

    api_key = CharField(
        max_length=255,
        verbose_name='Sentio api key',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'networks'
        ordering = '-_created_at',

    def __str__(self) -> str:
        return f'{self.title} (id: {self.id})'

    def get_token_info_by_address(self, address):
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}
        ids_json = send_post_request(self.subgraph_url, json={'query': """query {
          tokens(where:{id:"%s"}){
            derivedMatic
            decimals
          }
        }""" % address}, headers=headers)

        return ids_json['data']['tokens']

    def get_eternal_farmings_info(self, ):
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}
        ids_json = send_post_request(self.subgraph_farming_url, json={'query': """query {
          eternalFarmings{
            id
            rewardToken
            bonusRewardToken
            rewardRate
            bonusRewardRate
          }
        }"""}, headers=headers)

        return ids_json['data']['eternalFarmings']

    def get_limit_farmings_info(self, ):
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}
        ids_json = send_post_request(self.subgraph_farming_url, json={'query': """query {
          limitFarmings{
            id
            rewardToken
            bonusRewardToken
            reward
            bonusReward
            startTime
            endTime
          }
        }"""}, headers=headers)

        return ids_json['data']['limitFarmings']

    def get_positions_in_eternal_farming(self, farming_id):
        result = []
        i = 0

        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}

        while True:
            ids_json = send_post_request(self.subgraph_farming_url, json={'query': """query {
              deposits(where:{eternalFarming:"%s"}, first:1000, skip:%s){
                id
              }
            }""" % (farming_id, str(i*1000))}, headers=headers)

            result += ids_json['data']['deposits']

            if len(ids_json['data']['deposits']) < 1000:
                break

        return result

    def get_positions_in_limit_farming(self, farming_id):
        result = []
        i = 0

        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}


        while True:
            ids_json = send_post_request(self.subgraph_farming_url, json={'query': """query {
              deposits(where:{limitFarming:"%s"}, first:1000, skip:%s){
                id
              }
            }""" % (farming_id, str(i*1000))}, headers=headers)

            result += ids_json['data']['deposits']

            if len(ids_json['data']['deposits']) < 1000:
                break

        return result

    def get_positions_by_id(self, ids):
        ids_array = [i['id'] for i in ids]

        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}
        result = []
        i = 0

        while True:
            positions_json = send_post_request(self.subgraph_url, json={'query': """query {
              positions(where:{id_in:%s}, first:1000, skip:%s){
                id
                liquidity
                tickLower{
                  tickIdx
                }
                tickUpper{
                  tickIdx
                }
                pool{
                  token0{
                    name
                    decimals
                    derivedMatic
                  }
                  token1{
                    name
                    decimals
                    derivedMatic
                  }
                  tick
                }
              }
            }""" % (str(ids_array).replace("'", '"'), str(i*1000))}, headers=headers)

            result += positions_json['data']['positions']

            if len(positions_json['data']['positions']) < 1000:
                break

        return result

    # def get_position_snapshots_from_subgraph(self, ):
    #     positions_json = send_post_request(self.subgraph_url, json={'query': """query {
    #   positionSnapshots{
    #     liquidity,
    #     feeGrowthInside0LastX128,
    #     feeGrowthInside1LastX128,
    #     position{
    #       id
    #       tickLower{
    #         tickIdx
    #       }
    #       tickUpper{
    #         tickIdx
    #       }
    #     }
    #   }
    # }"""})
    #     return positions_json['data']['positionSnapshots']

    def get_positions_of_integral_pool(self, pool):
        result = []
        i = 0
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}

        while True:
            positions_json = send_post_request(self.subgraph_url, json={'query': """query {
                poolPositions(first:1000, skip:%s, where:{liquidity_gt:0, pool:"%s"}){
                lowerTick{
                    tickIdx
                }
                upperTick{
                    tickIdx
                }
                liquidity
                pool{
                  id
                  token0Price
                }
              }
            }""" % (str(i*1000), pool)},  headers=headers)
            ##logging.debug("model01=%s", positions_json)
            data = positions_json['data']
            ##logging.debug("model02=%s", data)
            if data is not None:
              pool_positions = data['poolPositions']
              ##logging.debug("model03=%s", pool_positions)
              result += pool_positions
              ##logging.debug("pool positions lenght=%s", len(pool_positions))
              if len(pool_positions) < 1000:
                  ##logging.debug("result=%s", result)
                  break
            else:
                ##logging.debug("result=%s", result)
                break

        return result

    def get_positions_of_pool(self, pool):
        result = []
        i = 0
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}

        while True:
            positions_json = send_post_request(self.subgraph_url, json={'query': """query {
                positions(first:1000, skip:%s, where:{liquidity_gt:0, pool:"%s"}){
                tickLower{
                    tickIdx
                }
                tickUpper{
                    tickIdx
                }
                liquidity
                depositedToken0
                depositedToken1
                token0{
                  decimals
                }
                token1{
                  decimals
                }
                pool{
                  id
                  token0Price
                }
              }
            }""" % (str(i*1000), pool)},  headers=headers)
            ##logging.debug("model01=%s", positions_json)
            data = positions_json['data']
            ##logging.debug("model02=%s", data)
            if data is not None:
              pool_positions = data['positions']
              ##logging.debug("model03=%s", pool_positions)
              result += pool_positions
              ##logging.debug("pool positions lenght=%s", len(pool_positions))
              if len(pool_positions) < 1000:
                  ##logging.debug("result=%s", result)
                  break
            else:
                ##logging.debug("result=%s", result)
                break

        return result

    def get_previous_block_number(self):
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}
        previous_date = int(time()) - settings.APR_DELTA
        block_json = send_post_request(self.subgraph_blocks_urls, json={'query': """query {
            blocks(first: 1, orderBy: timestamp, orderDirection: desc, where:{timestamp_lt:%s, timestamp_gt:%s}) {
                number
              }
        }""" % (str(previous_date), str(previous_date - settings.BLOCK_DELTA))},  headers=headers)
        return block_json['data']['blocks'][0]['number']

    def get_current_pools_info(self):
        headers = None
        if self.api_key != None:  
          headers={"api-key": self.api_key}
        pools_json_previous_raw = send_post_request(self.subgraph_url, json={'query': """query {
        pools(block:{number:%s},first: 1000, orderBy: totalValueLockedUSD orderDirection: desc where:{
        totalValueLockedUSD_gt: "10000" feesUSD_gt: "100"
  }){
            feesToken0
            feesToken1
            liquidity
            id
            token0{
            decimals
            name
            }
            token1{
            decimals
            name
            }
            token0Price
            tick
         }
            }""" % self.get_previous_block_number()}, headers=headers)

        pools_json_previous = {}

        for pool in pools_json_previous_raw['data']['pools']:
            pools_json_previous[pool['id']] = {'feesToken0': pool['feesToken0'], 'feesToken1': pool['feesToken1'], 'liquidity': pool['liquidity']}

        pools_json = send_post_request(self.subgraph_url, json={'query': """query {
        pools(first: 1000, orderBy: totalValueLockedUSD orderDirection: desc where:{
        totalValueLockedUSD_gt: "10000" feesUSD_gt: "100"
  }){
            feesToken0
            feesToken1
            feesUSD
            totalValueLockedUSD                                                    
            liquidity
            id
            token0{
            decimals
            name
            }
            token1{
            decimals
            name
            }
            token0Price
            tick
         }
            }"""},  headers=headers)

        pools_json = pools_json['data']['pools']

        for i in range(len(pools_json)):
            try:
                pools_json[i]['feesToken0'] = \
                    float(pools_json[i]['feesToken0']) - float(pools_json_previous[pools_json[i]['id']]['feesToken0'])
                pools_json[i]['feesToken1'] = \
                    float(pools_json[i]['feesToken1']) - float(pools_json_previous[pools_json[i]['id']]['feesToken1'])
            except KeyError:
                pools_json[i]['feesToken0'] = float(pools_json[i]['feesToken0'])
                pools_json[i]['feesToken1'] = float(pools_json[i]['feesToken1'])

        return pools_json
 

class LandingNetwork(AbstractBaseModel):
    title = CharField(
        max_length=255,
        verbose_name='Title',
    )
    subgraph_url = URLField(
        help_text='Subgraph about main contracts'
    )
    subgraph_blocks_urls = URLField(
        help_text='Subgraph about blockchain'
    )


    class Meta:
        db_table = 'landingNetworks'
        ordering = '-_created_at',

    def __str__(self) -> str:
        return f'{self.title} (id: {self.id})'

    def getDexDaysData(self):
        data = []
        MAX_VALUE = 5000000000
        if self.title == "Thena BNB" or self.title == "Thena opBNB":
            dexDaysData_json = send_post_request(self.subgraph_url, json={'query': """query {
              fusionDayDatas(first: 365, orderBy: date, orderDirection: desc) {  
                          date
                          tvlUSD
                          volumeUSD
                          feesUSD
                      }}"""})
            data = dexDaysData_json['data']['fusionDayDatas']
        else:
            dexDaysData_json = send_post_request(self.subgraph_url, json={'query': """query {
              algebraDayDatas(first: 365, orderBy: date, orderDirection: desc) {  
                          date
                          tvlUSD
                          volumeUSD
                          feesUSD
                      }}"""})
            data = dexDaysData_json['data']['algebraDayDatas']
        for i in range(len(data)):
            if float(data[i]["tvlUSD"]) > MAX_VALUE or float(data[i]["volumeUSD"]) > MAX_VALUE:
                data[i]["tvlUSD"] = data[i-1]["tvlUSD"]
                data[i]["volumeUSD"] = data[i-1]["volumeUSD"]
                data[i]["feesUSD"] = data[i-1]["feesUSD"]
        return data
        
    def getDexDataForTimestamp(self, timestamp):
        MAX_VALUE = 200000000000
        block_json = send_post_request(self.subgraph_blocks_urls, json={'query': """query {
          blocks(first: 1, orderBy: timestamp, orderDirection: desc, where:{timestamp_lt:%s}) {
              number
            }
          }""" % (str(timestamp+60))})
        block = block_json['data']['blocks'][0]['number']
        
        dexData_json = send_post_request(self.subgraph_url, json={'query': """query {
            factories(block: {number:%s}) {  
                    totalVolumeUSD
                    totalValueLockedUSD
                    totalFeesUSD
            }}""" % (block)})
        data = dexData_json['data']['factories']
        if float(data[0]['totalVolumeUSD']) > MAX_VALUE or float(data[0]['totalValueLockedUSD']) > MAX_VALUE:
            return None
        else:
            return data
