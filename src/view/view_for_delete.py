from django.http import HttpResponse
import json
import logging

from src.DataPreprocess.delete_data_preprocess import DeleteDataPrerprocess
from src.ErrorCenter.error_center import ErrorCenter


def check_params(func):
    def wrapper(
            db_type,
            db_name,
            table_name,
            where_value,
            check_flag
    ):
        try:
            assert db_type
            assert not "Hive".__eq__(db_type)
            assert where_value
            if "Mysql".__eq__(db_type):
                assert all([db_name, table_name])
            if "ElasticSearch".__eq__(db_type):
                assert table_name
            if "Neo4j".__eq__(db_type):
                assert db_name
        except Exception as e:
            logging.exception(e)
            check_flag = False

        return func(
            db_type,
            db_name,
            table_name,
            where_value,
            check_flag
        )
    return wrapper


@check_params
def check_input_params(
        _db_type,
        _db_name,
        _table_name,
        _where_value,
        check_flag=True
):
    return check_flag


def data_content_delete(request):
    if request.POST:
        db_type = request.POST.get("DBType", 0)
        db_name = request.POST.get("DBName", 0)
        table_name = request.POST.get("TableName", 0)
        where_value_str = request.POST.get("WhereValue", 0)
        try:
            where_value = json.loads(where_value_str)
        except Exception as e:
            logging.exception(e)
            return HttpResponse(json.dumps(
                {
                    "msg": str(ErrorCenter.VALUE_IS_NOT_JSON_STYLE.value)
                })
            )
        logging.info("input parameter DBType is [ %s ]" % db_type)
        logging.info("input parameter DBName is [ %s ]" % db_name)
        logging.info("input parameter TableName is [ %s ]" % table_name)
        logging.info("input parameter WhereValue is [ %s ]" % where_value_str)
        if not check_input_params(
                db_type,
                db_name,
                table_name,
                where_value,
                True
        ):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))

        delete_data_process = DeleteDataPrerprocess(db_type)
        if delete_data_process.data_content_delete(
                db_name,
                table_name,
                where_value
        ):
            return HttpResponse(
                '{"msg": "delete %s %s.%s data successful"}' % (
                    db_type, db_name, table_name
                )
            )
        else:
            return HttpResponse(json.dumps(
                {
                    "msg": str(ErrorCenter.DELETE_DATA_TO_DB_FAILED.value) % (
                        db_type, db_name, table_name
                    )
                }
            )
            )
    else:
        return HttpResponse(json.dumps(
            {
                "msg": str(ErrorCenter.NOT_USE_POST_METHOD.value)
            }
        )
        )
