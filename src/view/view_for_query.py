from django.http import HttpResponse
import json
from src.DataPreprocess.es_preprocess import EsPreprocess
from src.DataPreprocess.hive_preprocess import HivePreprocess
from src.DataPreprocess.mysql_preprocess import MysqlPreprocess
from src.ErrorCenter.error_center import ErrorCenter
from src.utils.common_utils import CommonUtils


def hive_data_query(request):
    if request.POST:
        db_name = request.POST.get("DbName", None)
        table_name = request.POST.get("TableName", None)
        query_rows_count = request.POST.get("QueryRowsCount", None)
        common_util = CommonUtils()

        if not all([
            common_util.check_params("DbName", db_name),
            common_util.check_params("TableName", table_name),
            common_util.check_params("QueryRowsCount", query_rows_count)
        ]):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))

        hive_process = HivePreprocess()
        select_data = \
            hive_process.select_data(
                db_name,
                table_name,
                query_rows_count
            )

        return HttpResponse(json.dumps(select_data))


def mysql_data_query(request):
    if request.POST:
        db_name = request.POST.get("DbName", None)
        table_name = request.POST.get("TableName", None)
        query_rows_count = request.POST.get("QueryRowsCount", None)
        common_util = CommonUtils()
        if not all([
            common_util.check_params("DbName", db_name),
            common_util.check_params("TableName", table_name),
            common_util.check_params("QueryRowsCount", query_rows_count)
        ]):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))
        mysql_process = MysqlPreprocess()
        select_data = \
            mysql_process.select_data(
                db_name,
                table_name,
                query_rows_count
            )

        return HttpResponse(json.dumps(select_data))


def es_data_query(request):
    if request.POST:
        db_name = request.POST.get("DbName", None)
        table_name = request.POST.get("TableName", None)
        query_rows_count = request.POST.get("QueryRowsCount", None)
        common_util = CommonUtils()

        if not all([
            common_util.check_params("TableName", table_name),
            common_util.check_params("QueryRowsCount", query_rows_count)
        ]):
            return HttpResponse(json.dumps({
                "message":
                    str(ErrorCenter.INPUT_PARAMS_WHICH_IS_EMPTY.value)
            }))

        es_process = EsPreprocess()
        select_data = \
            es_process.select_data(
                db_name,
                table_name,
                query_rows_count
            )

        return HttpResponse(json.dumps(select_data))
