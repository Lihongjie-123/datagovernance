from django.http import HttpResponse
from src.utils.preprocess_utils import PreprocessUtil

# Create your views here.


def abstract_data_map_cache(request):
    preprocess_utils = PreprocessUtil()
    map_data = preprocess_utils.cache_data_select_by_orm("AbstractDataMap")
    return HttpResponse(map_data)


def hive_data_map_cache(request):
    preprocess_utils = PreprocessUtil()
    map_data = preprocess_utils.cache_data_select_by_orm("HiveDataMap")
    return HttpResponse(map_data)


def mysql_data_map_cache(request):
    preprocess_utils = PreprocessUtil()
    map_data = preprocess_utils.cache_data_select_by_orm("MysqlDataMap")
    return HttpResponse(map_data)


def redis_data_map_cache(request):
    preprocess_utils = PreprocessUtil()
    map_data = preprocess_utils.cache_data_select_by_orm("RedisDataMap")
    map_data = map_data.replace("\\", "")
    return HttpResponse(map_data)


def es_data_map_cache(request):
    preprocess_utils = PreprocessUtil()
    map_data = preprocess_utils.cache_data_select_by_orm("ESDataMap")
    return HttpResponse(map_data)


def neo_data_map_cache(request):
    preprocess_utils = PreprocessUtil()
    map_data = preprocess_utils.cache_data_select_by_orm("NeoDataMap")
    return HttpResponse(map_data)
