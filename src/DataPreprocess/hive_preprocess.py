import csv
import datetime
import io
import json
import logging
from src.DataSource.hive_source import HiveSource
from src.DataSource.presto_source import PrestoSource
from src.utils.common_utils import CommonUtils
from src.utils.preprocess_utils import PreprocessUtil
import time


class HivePreprocess(object):
    def __init__(self):
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.before_7_days_date = self.today - datetime.timedelta(days=7)
        self.COUNT_COUNT_SQL = \
            "select count(1) from %s " \
            "where import_time > '%s' and import_time < '%s'"
        self.CREATE_TIME_RE = "%a %b %d %H:%M:%S CST %Y"
        self.SELECT_DATA_SQL = "select * from %s.%s limit %s"
        self.INSERT_DATA_SQL = "INSERT INTO %s.%s (%s) VALUES %s"
        self.common_utils = CommonUtils()
        self.preprocess_utils = PreprocessUtil()

    def get_date(self, timestamp):
        logging.info("format timestamp is %s" % timestamp)
        if timestamp.isdigit():
            # 转为cst时间 +8小时
            time_local = time.localtime(int(timestamp) + 28800)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            return dt
        else:
            return datetime.datetime.strptime(
                timestamp, self.CREATE_TIME_RE
            ).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_col_name_list(
            col_name_list,
            redis_source,
            full_table_name,
            format_result_json
    ):
        for sub_row in col_name_list:
            if 0 == col_name_list.index(sub_row):
                continue
            if not sub_row[0].strip() and not sub_row[1] and not sub_row[2]:
                continue
            if "import_time".__eq__(sub_row[0].strip()):
                # 如果有import_time字段，统计昨天入库量以及最近一周入库量
                # redis里的统计数据是由定时任务来完成的
                # 统计昨天入库量
                yesterday_count = \
                    redis_source.redisconn.hget(
                        "hive_yesterday_count",
                        "hive_yesterday_count-%s" % full_table_name
                    )
                logging.info("yesterday count is %s" % yesterday_count)
                format_result_json["numAddedYesterday"] = yesterday_count

                # 统计最近一周入库量
                sev_daysago_count = \
                    redis_source.redisconn.hget(
                        "hive_7days_ago_count",
                        "hive_7days_ago_count-%s" % full_table_name
                    )
                logging.info("sev_daysago_count is %s" % sev_daysago_count)
                format_result_json["numAddedlastWeek"] = sev_daysago_count
            format_result_json["col_name"].append({
                "col_name": sub_row[0],
                "col_type": sub_row[1],
                "col_comment": sub_row[2],
            })

    def format_detailed_table_information_list(
            self,
            detailed_table_information_list,
            redis_source,
            full_table_name,
            format_result_json
    ):
        for sub_row in detailed_table_information_list:
            if 0 == detailed_table_information_list.index(sub_row):
                continue
            if not sub_row[0].strip() and not sub_row[1] and not sub_row[2]:
                continue

            if sub_row[0].strip() and \
                    "Table Parameters:" != sub_row[0].strip():

                if "CreateTime" == sub_row[0].strip(": "):
                    format_result_json["createTime"] = \
                        self.get_date(sub_row[1].strip())

                format_result_json[
                    "DetailedTableInformation"][
                    sub_row[0].strip(": ").replace(" ", "")] = [
                    {
                        "data_type": ""
                        if not sub_row[1] else sub_row[1].strip(),
                        "comment": ""
                        if not sub_row[2] else sub_row[2].strip(),
                    }]
            elif "Table Parameters:" == sub_row[0].strip():
                format_result_json[
                    "DetailedTableInformation"]["TableParameters"] = []
            else:
                if "comment" == sub_row[1].strip():
                    format_result_json["tableComment"] = sub_row[2].strip()
                # 数据总量
                if "numRows" == sub_row[1].strip():
                    sum_count = \
                        redis_source.redisconn.hget(
                            "hive_sum_count",
                            "hive_sum_count-%s" % full_table_name
                        )
                    logging.info("sum count is %s" % sum_count)
                    format_result_json["numRows"] = sum_count

                if "totalSize" == sub_row[1].strip():
                    total_size = int(sub_row[2].strip())
                    if 0 <= total_size <= 1024:
                        format_result_json["totalSize"] = "%s(B)" % total_size
                    elif 1024 < total_size <= 1048576:
                        format_result_json["totalSize"] = \
                            "%s(KB)" % (round(total_size / 1024, 3))
                    elif 1048576 < total_size <= 1073741824:
                        format_result_json["totalSize"] = \
                            "%s(MB)" % (round(total_size / 1048576, 3))
                    elif 1073741824 < total_size <= 1099511627776:
                        format_result_json["totalSize"] = \
                            "%s(GB)" % (round(total_size / 1073741824, 3))
                    elif 1099511627776 < total_size <= 1125899906842624:
                        format_result_json["totalSize"] = \
                            "%s(TB)" % (round(total_size / 1099511627776, 3))
                    else:
                        format_result_json["totalSize"] = \
                            "%s(PB)" % (
                                round(total_size / 1125899906842624, 3))

                if "transient_lastDdlTime" == sub_row[1].strip():
                    format_result_json["lastUpdateTime"] = \
                        self.get_date(sub_row[2].strip())

                format_result_json[
                    "DetailedTableInformation"]["TableParameters"].append(
                    {
                        "data_type": ""
                        if not sub_row[1] else sub_row[1].strip(),
                        "comment": ""
                        if not sub_row[2] else sub_row[2].strip(),
                    }
                )

    @staticmethod
    def fortmat_storage_information_list(
            storage_information_list,
            format_result_json
    ):
        for sub_row in storage_information_list:
            if 0 == storage_information_list.index(sub_row):
                continue
            if not sub_row[0].strip() and not sub_row[1] and not sub_row[2]:
                continue
            if sub_row[0].strip() and \
                    "Storage Desc Params:" != sub_row[0].strip():
                format_result_json[
                    "StorageInformation"][
                    sub_row[0].strip(": ").replace(" ", "")] = [
                    {
                        "data_type": ""
                        if not sub_row[1] else sub_row[1].strip(),
                        "comment": ""
                        if not sub_row[2] else sub_row[2].strip(),
                    }]
            elif "Storage Desc Params:" == sub_row[0].strip():
                format_result_json[
                    "StorageInformation"]["StorageDescParams"] = []
            else:
                format_result_json[
                    "StorageInformation"]["StorageDescParams"].append(
                    {
                        "data_type": ""
                        if not sub_row[1] else sub_row[1].strip(),
                        "comment": ""
                        if not sub_row[2] else sub_row[2].strip(),
                    }
                )

    def format_table_info(self, table_info, full_table_name, redis_source):
        format_result_json = {
            "col_name": [],
            "DetailedTableInformation": {},
            "StorageInformation": {},
            "dbName": full_table_name.split(".")[0],
            "tableName": full_table_name.split(".")[1],
            "numRows": "0",
            "totalSize": "0",
            "numAddedYesterday": "0",
            "numAddedlastWeek": "0",
            "lastUpdateTime": "",
            "createTime": "",
            "tableComment": ""
        }
        col_name_list = \
            table_info[0:table_info.index(
                ('# Detailed Table Information', None, None)
            )
            ]
        detailed_table_information_list = \
            table_info[table_info.index(
                ('# Detailed Table Information', None, None)
            ):table_info.index(
                ('# Storage Information', None, None)
            )
            ]
        storage_information_list = \
            table_info[table_info.index(
                ('# Storage Information', None, None)
            ):]
        self.format_col_name_list(
            col_name_list,
            redis_source,
            full_table_name,
            format_result_json
        )

        self.format_detailed_table_information_list(
            detailed_table_information_list,
            redis_source,
            full_table_name,
            format_result_json
        )

        self.fortmat_storage_information_list(
            storage_information_list,
            format_result_json
        )

        return format_result_json

    def select_data(self, db_name, table_name, select_count):
        presto_source = PrestoSource("hive")
        presto_source.create_connection()
        select_sql = self.SELECT_DATA_SQL % (
            db_name,
            table_name,
            select_count
        )
        presto_source.execute(select_sql)
        select_df = presto_source.fetch_all()
        return_result = self.common_utils.format_df(select_df)
        presto_source.close()
        return return_result

    def parse_table_col_info(self, full_table_name):
        data_map = \
            json.loads(self.preprocess_utils.cache_data_select("HiveDataMap"))
        col_info = []
        for i in data_map["hive_source"]:
            if full_table_name == i["table_name"]:
                for col_name_info in i["col_name"]:
                    col_info.append(col_name_info["col_name"])
                break
        return col_info

    def data_content_to_db(self, db_name, db_table, input_content, separator):
        try:
            if "," == separator:
                content_obj = csv.reader(io.StringIO(input_content))
            else:
                content_obj = \
                    [x.split(separator) for x in [j for j in input_content.split("\n")]]  # nopep8
            col_info = self.parse_table_col_info("%s.%s" % (db_name, db_table))
            value_list = []
            for line in content_obj:
                if 1 == len(line) and not line[0]:
                    continue
                value_list.append("'%s'" % ("','".join(line)))
            insert_sql = self.INSERT_DATA_SQL % (
                db_name,
                db_table,
                ",".join(col_info),
                "(%s)" % ("),(".join(value_list))
            )
            # 这里跑一次创建一次连接，防止冲突
            hive_source = HiveSource()
            hive_source.create_connection()
            hive_source.execute(insert_sql)
            hive_source.close()
            logging.info("data merge to hive successful")
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def data_content_update(
            self,
            db_name,
            table_name,
            update_value,
            where_value
    ):
        pass

    def data_content_delete(
            self,
            db_name,
            table_name,
            where_value
    ):
        pass
