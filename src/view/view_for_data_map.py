from django.http import HttpResponse
import json
from src.DataPreprocess.data_map_preprocess import DataMapPreprocess

# Create your views here.


def abstract_data_map(request):
    data_map_prerprocess = DataMapPreprocess()
    map_data = data_map_prerprocess.abstract_parse_related()
    return HttpResponse(json.dumps(map_data))


def hive_data_map(request):
    data_map_prerprocess = DataMapPreprocess()
    data_map_prerprocess.hive_parse_related()
    map_data = data_map_prerprocess.hive_fetch_data_map()
    return HttpResponse(json.dumps(map_data))


def mysql_data_map(request):
    data_map_prerprocess = DataMapPreprocess()
    data_map_prerprocess.mysql_parse_related()
    map_data = data_map_prerprocess.mysql_fetch_data_map()
    return HttpResponse(json.dumps(map_data))


def redis_data_map(request):
    data_map_prerprocess = DataMapPreprocess()
    data_map_prerprocess.redis_parse_related()
    map_data = data_map_prerprocess.redis_fetch_data_map()
    return HttpResponse(json.dumps(map_data))


def es_data_map(request):
    data_map_prerprocess = DataMapPreprocess()
    data_map_prerprocess.es_parse_related()
    map_data = data_map_prerprocess.es_fetch_data_map()
    return HttpResponse(json.dumps(map_data))


def neo_data_map(request):
    data_map_prerprocess = DataMapPreprocess()
    data_map_prerprocess.neo_parse_related()
    map_data = data_map_prerprocess.neo_fetch_data_map()
    return HttpResponse(json.dumps(map_data))
