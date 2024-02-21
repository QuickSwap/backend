from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pool, EternalFarming, LimitFarming, DexDayData, BuyBackData
from logging import debug


# Create your views here.

class ListPoolAprs(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for pool in Pool.objects.filter(network__title=network_name):
            result[pool.address] = pool.last_apr
        return Response(result)

class ListMaxPoolAprs(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for pool in Pool.objects.filter(network__title=network_name):
            result[pool.address] = pool.max_apr
        return Response(result)


class ListEternalFarmingsTvl(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for farming in EternalFarming.objects.filter(network__title=network_name):
            result[farming.hash] = farming.native_amount
        return Response(result)


class ListEternalFarmingsAprs(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for farming in EternalFarming.objects.filter(network__title=network_name):
            result[farming.hash] = farming.last_apr
        return Response(result)

class ListEternalFarmingsMaxAprs(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for farming in EternalFarming.objects.filter(network__title=network_name):
            result[farming.hash] = farming.max_apr
        return Response(result)


class ListLimitFarmingsTvl(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for farming in LimitFarming.objects.filter(network__title=network_name):
            result[farming.hash] = farming.native_amount
        return Response(result)


class ListLimitFarmingsAprs(APIView):
    def get(self, request, format=None):
        result = {}

        try:
            network_name = request.GET['network']
        except KeyError:
            network_name = 'Polygon'

        for farming in LimitFarming.objects.filter(network__title=network_name):
            result[farming.hash] = farming.last_apr
        return Response(result)


class DexData(APIView):
    def get(self, request, format=None):
        result = {}

        totalData = {}

        for dex in DexDayData.objects.all():
            data = {}
            data["now"] = dex.now
            data["dayAgo"] = dex.day_ago
            data["twoDaysAgo"] = dex.two_days_ago
            data["daysData"] = dex.days_data
            daysData = dex.days_data
            for day in daysData:
                if totalData.get(day["date"]) == None:
                    totalData[day["date"]] = { "date":day["date"], "tvlUSD": float(day["tvlUSD"]), "volumeUSD": float(day["volumeUSD"]), "feesUSD": float(day["feesUSD"])} 
                else:
                    totalData[day["date"]]["tvlUSD"] +=  float(day["tvlUSD"])
                    totalData[day["date"]]["volumeUSD"] +=  float(day["volumeUSD"])        
                    totalData[day["date"]]["feesUSD"] +=  float(day["feesUSD"])                              
            result[dex.network.title] = data
        totalData = sorted(totalData.items(), reverse=True)
        date, result["Total"] = list(zip(*totalData))
        return Response(result)

class BuybackData(APIView):
    def get(self, request, format=None):
        result = {}
        try:
            result["buybackHistory"] = BuyBackData.objects.all()[0].buy_back_data
        except KeyError:
            result["buybackHistory"] = ""
        return Response(result)