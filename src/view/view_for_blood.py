from django.http import HttpResponse
import json
import logging
from src.config.load_config_map import get_config_conf
from src.ErrorCenter.error_center import ErrorCenter

config_map = get_config_conf()
url_map = {
    "entity_detail_info_show": "http://%s:%s/api/atlas/v2/types/typedefs",
    "entity_brief_info_show":
        "http://%s:%s/api/atlas/v2/types/typedefs/headers",
    "all_hive_info_show": "http://%s:%s/api/atlas/v2/search/basic?typeName=%s",
    "entity_info_by_name_show":
        "http://%s:%s/api/atlas/v2/search/basic?query=%s&typeName=%s",
    "add_new_entity": "http://%s:%s/api/atlas/v2/entity",
    "": "http://node01:21000/api/atlas/v2/entity/bulk?minExtInfo=yes&guid=5c870fa6-b743-4634-acef-0ce3cdadb91d"
}


def entity_detail_info_show(request):
    if request.GET:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def entity_brief_info_show(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def all_hive_info_show(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def entity_info_by_name_show(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def add_new_entity(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def query_relation_by_guid(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def query_entity_define_by_guid(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def query_blood_relation_for_entity_by_guid(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )


def query_blood_relation_create(request):
    if request.POST:
        pass
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )
