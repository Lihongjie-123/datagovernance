from django.http import HttpResponse
import json
import logging
from src.DataPreprocess.update_data_preprocess import UpdateDataPrerprocess
from src.ErrorCenter.error_center import ErrorCenter


def check_params(func):
    def wrapper(
            db_type,
            db_name,
            table_name,
            update_value,
            where_value,
            check_flag
    ):
        try:
            assert db_type
            assert not "Hive".__eq__(db_type)
            assert all([update_value, where_value])
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
            update_value,
            where_value,
            check_flag
        )
    return wrapper


@check_params
def check_input_params(
        _db_type,
        _db_name,
        _table_name,
        _update_value,
        _where_value,
        check_flag=True
):
    return check_flag


def data_content_update(request):
    if request.POST:
        db_type = request.POST.get("DBType", 0)
        db_name = request.POST.get("DBName", 0)
        table_name = request.POST.get("TableName", 0)
        update_value_str = request.POST.get("UpdateValue", 0)
        where_value_str = request.POST.get("WhereValue", 0)
        try:
            update_value = json.loads(update_value_str)
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
        logging.info("input parameter UpdateValue is [ %s ]" %
                     update_value_str)
        logging.info("input parameter WhereValue is [ %s ]" % where_value_str)
        if not check_input_params(
                db_type,
                db_name,
                table_name,
                update_value,
                where_value,
                True
        ):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))

        update_data_process = UpdateDataPrerprocess(db_type)
        if update_data_process.data_content_update(
                db_name,
                table_name,
                update_value,
                where_value
        ):
            return HttpResponse(
                '{"msg": "update %s %s.%s data successful"}' % (
                    db_type, db_name, table_name
                )
            )
        else:
            return HttpResponse(json.dumps(
                {
                    "msg": str(ErrorCenter.UPDATE_DATA_TO_DB_FAILED.value) % (
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
