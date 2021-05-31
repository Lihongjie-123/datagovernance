from django.http import HttpResponse
import json
import logging
from src.DataPreprocess.add_data_preprocess import AddDataPrerprocess
from src.ErrorCenter.error_center import ErrorCenter
from src.utils.common_utils import CommonUtils


def check_params(func):
    def wrapper(
            db_type,
            db_name,
            table_name,
            separator,
            common_utils,
            check_flag
    ):
        try:
            assert common_utils.check_params("DBType", db_type)
            if ["Hive", "Mysql"].__contains__(db_type):
                assert all([
                    common_utils.check_params("DBName", db_name),
                    common_utils.check_params("TableName", table_name),
                    common_utils.check_params("Separator", separator)
                ])
            elif "ElasticSearch".__eq__(db_type):
                assert all([
                    common_utils.check_params("TableName", table_name),
                    common_utils.check_params("Separator", separator)
                ])
            elif "Neo4j".__eq__(db_type):
                assert all([
                    common_utils.check_params("DBName", db_name),
                    common_utils.check_params("Separator", separator)
                ])
            elif "Redis".__eq__(db_type):
                assert common_utils.check_params("Separator", separator)
        except Exception as e:
            logging.exception(e)
            check_flag = False

        return func(
            db_type,
            db_name,
            table_name,
            separator,
            common_utils,
            check_flag
        )
    return wrapper


@check_params
def check_input_params(
        _db_type,
        _db_name,
        _table_name,
        _separator,
        _common_utils,
        check_flag=True
):
    return check_flag


def data_content_add(request):
    if request.POST:
        db_type = request.POST.get("DBType", 0)
        db_name = request.POST.get("DBName", 0)
        table_name = request.POST.get("TableName", 0)
        input_content = request.POST.get("InputeContent", 0)
        separator = request.POST.get("Separator", 0)
        common_utils = CommonUtils()
        if not input_content:
            return HttpResponse(json.dumps(
                {
                    "msg": str(ErrorCenter.CONTENT_IS_NONE_OR_EMPTY.value)
                }
            )
            )
        if not separator:
            separator = ","
        if not check_input_params(
            db_type,
            db_name,
            table_name,
            separator,
            common_utils,
            True
        ):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))
        add_data_process = AddDataPrerprocess(db_type)
        if add_data_process.data_content_to_db(
                db_name, table_name, input_content, separator):
            return HttpResponse(
                '{"msg": "data to %s %s.%s successful"}' % (
                    db_type, db_name, table_name
                )
            )
        else:
            return HttpResponse(json.dumps(
                {
                    "msg": str(ErrorCenter.ADD_DATA_TO_DB_FAILED.value) % (
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


def data_file_add(request):
    if request.POST:
        db_type = request.POST.get("DBType", 0)
        db_name = request.POST.get("DBName", 0)
        table_name = request.POST.get("TableName", 0)
        separator = request.POST.get("Separator", 0)
        # TODO(lihongjie): 这个方法有风险，如果文件过大，
        #  则会有可能导致内存溢出，暂未想到好方法
        input_file = request.FILES.get("File").read()
        common_utils = CommonUtils()
        if not separator:
            separator = ","
        if not check_input_params(
                db_type,
                db_name,
                table_name,
                separator,
                common_utils,
                True
        ):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))
        add_data_process = AddDataPrerprocess(db_type)
        if add_data_process.data_content_to_db(
                db_name,
                table_name,
                str(input_file, encoding="utf-8"),
                separator
        ):
            return HttpResponse(
                '{"msg": "data to %s %s.%s successful"}' % (
                    db_type, db_name, table_name
                )
            )
        else:
            return HttpResponse(json.dumps(
                {
                    "msg": str(ErrorCenter.ADD_DATA_TO_DB_FAILED.value) % (
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
