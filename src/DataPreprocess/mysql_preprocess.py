import csv
import datetime
import io
import json
import logging
from src.DataSource.mysql_source import MysqlSource
from src.DataSource.presto_source import PrestoSource
from src.utils.common_utils import CommonUtils
from src.utils.preprocess_utils import PreprocessUtil


class MysqlPreprocess(object):

    def __init__(self):
        self.SELECT_BASE_INFO_SQL = \
            "select * from information_schema.tables " \
            "where table_schema='%s' and table_name='%s'"
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.before_7_days_date = self.today - datetime.timedelta(days=7)
        self.COUNT_COUNT_SQL = \
            "select count(1) from %s " \
            "where import_time > '%s' and import_time < '%s'"
        self.SELECT_DATA_SQL = "select * from %s.%s limit %s"
        self.common_utils = CommonUtils()
        self.TIME_TEMPLATE = "%s 00:00:00"
        self.preprocess_utils = PreprocessUtil()
        self.INSERT_DATA_SQL = "INSERT INTO %s.%s (%s) VALUES %s"
        self.UPDATE_DATA_SQL = "update %s.%s set %s where %s"
        self.DELETE_DATA_SQL = "delete from %s.%s where %s"

    def format_col_info(
            self,
            full_table_name,
            format_result_json,
            mysql_source
    ):
        mysql_source.execute("show full columns from %s" % full_table_name)
        full_col_info_list = mysql_source.fetch_all()
        for sub_col_info in full_col_info_list:
            logging.info(sub_col_info)
            if "import_time" == sub_col_info[0]:
                mysql_source.execute(
                    self.COUNT_COUNT_SQL % (
                        full_table_name,
                        self.TIME_TEMPLATE % str(self.yesterday),
                        self.TIME_TEMPLATE % str(self.today)
                    ))
                yesterday_count = mysql_source.fetch_all()[0][0]
                format_result_json["numAddedYesterday"] = yesterday_count

                mysql_source.execute(
                    self.COUNT_COUNT_SQL % (
                        full_table_name,
                        self.TIME_TEMPLATE % str(self.before_7_days_date),
                        self.TIME_TEMPLATE % str(self.today)
                    ))
                sev_days_ago_count = mysql_source.fetch_all()[0][0]
                format_result_json["numAddedlastWeek"] = sev_days_ago_count

            format_result_json["col_name"].append(
                {
                    "col_name": sub_col_info[0],
                    "col_type": sub_col_info[1],
                    "col_comment": sub_col_info[8],
                }
            )

    @staticmethod
    def format_index_information(
            full_table_name,
            format_result_json,
            mysql_source
    ):
        mysql_source.execute("show index from %s" % full_table_name)
        full_col_info_list = mysql_source.fetch_all()
        for sub_col_info in full_col_info_list:
            logging.info(sub_col_info)
            format_result_json["index_information"].append(
                {
                    "table_name": sub_col_info[0],
                    "index_name": sub_col_info[2],
                    "index_field": sub_col_info[4],
                }
            )

    def format_detail_information(
            self,
            full_table_name,
            format_result_json,
            mysql_source
    ):
        mysql_source.execute(self.SELECT_BASE_INFO_SQL % (
            full_table_name.split(".")[0],
            full_table_name.split(".")[1]
        ))
        full_info_list = mysql_source.fetch_all()
        sub_info = full_info_list[0]
        logging.info(sub_info)
        format_result_json["detail_information"] = [{
            "infoType": "DetailInformation",
            "infoField": "table_catalog",
            "infoValue": sub_info[0]
        }, {
            "infoType": "DetailInformation",
            "infoField": "table_schema",
            "infoValue": sub_info[1]
        }, {
            "infoType": "DetailInformation",
            "infoField": "table_name",
            "infoValue": sub_info[2]
        }, {
            "infoType": "DetailInformation",
            "infoField": "table_type",
            "infoValue": sub_info[3]
        }, {
            "infoType": "DetailInformation",
            "infoField": "engine",
            "infoValue": sub_info[4]
        }, {
            "infoType": "DetailInformation",
            "infoField": "version",
            "infoValue": sub_info[5]
        }, {
            "infoType": "DetailInformation",
            "infoField": "row_format",
            "infoValue": sub_info[6]
        }, {
            "infoType": "DetailInformation",
            "infoField": "table_rows",
            "infoValue": sub_info[7]
        }, {
            "infoType": "DetailInformation",
            "infoField": "avg_row_length",
            "infoValue": sub_info[8]
        }, {
            "infoType": "DetailInformation",
            "infoField": "data_length",
            "infoValue": sub_info[9]
        }, {
            "infoType": "DetailInformation",
            "infoField": "max_data_length",
            "infoValue": sub_info[10]
        }, {
            "infoType": "DetailInformation",
            "infoField": "index_length",
            "infoValue": sub_info[11]
        }, {
            "infoType": "DetailInformation",
            "infoField": "data_free",
            "infoValue": sub_info[12]
        }, {
            "infoType": "DetailInformation",
            "infoField": "auto_increment",
            "infoValue": sub_info[13]
        }, {
            "infoType": "DetailInformation",
            "infoField": "create_time",
            "infoValue": str(sub_info[14]) if sub_info[14] else ""
        }, {
            "infoType": "DetailInformation",
            "infoField": "update_time",
            "infoValue": str(sub_info[15]) if sub_info[15] else ""
        }, {
            "infoType": "DetailInformation",
            "infoField": "check_time",
            "infoValue": str(sub_info[16]) if sub_info[16] else ""
        }, {
            "infoType": "DetailInformation",
            "infoField": "table_collation",
            "infoValue": sub_info[17]
        }, {
            "infoType": "DetailInformation",
            "infoField": "checksum",
            "infoValue": sub_info[18]
        }, {
            "infoType": "DetailInformation",
            "infoField": "create_options",
            "infoValue": sub_info[19]
        }, {
            "infoType": "DetailInformation",
            "infoField": "table_comment",
            "infoValue": sub_info[20]
        }]
        format_result_json["tableComment"] = sub_info[20]
        # 最近更新时间
        format_result_json["lastUpdateTime"] = \
            str(sub_info[15]) if sub_info[15] else ""
        # 创建时间
        format_result_json["createTime"] = \
            str(sub_info[14]) if sub_info[14] else ""
        # 占用空间大小
        total_size = int(sub_info[9])
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
        if "MyISAM" == sub_info[4]:
            format_result_json["numRows"] = sub_info[7]
        elif "InnoDB" == sub_info[4]:
            mysql_source.execute(
                "select count(1) from %s" % full_table_name
            )
            format_result_json["numRows"] = mysql_source.fetch_all()[0][0]
            logging.info(format_result_json["numRows"])

    def format_table_info(
            self,
            full_table_name,
            mysql_source
    ):
        format_result_json = {
            "col_name": [],
            "index_information": [],
            "detail_information": [],
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

        self.format_col_info(full_table_name, format_result_json, mysql_source)

        self.format_index_information(
            full_table_name,
            format_result_json,
            mysql_source
        )

        self.format_detail_information(
            full_table_name,
            format_result_json,
            mysql_source
        )

        return format_result_json

    def select_data(self, db_name, table_name, select_count):
        presto_source = PrestoSource("mysql")
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
            json.loads(self.preprocess_utils.cache_data_select("MysqlDataMap"))
        col_info = []
        for i in data_map["mysql_source"]:
            if full_table_name == i["table_name"]:
                for col_name_info in i["col_name"]:
                    col_info.append(col_name_info["col_name"])
                break
        return col_info

    @staticmethod
    def exec_sql(input_sql):
        # 这里跑一次创建一次连接，防止冲突
        mysql_source = MysqlSource()
        mysql_source.create_connection()
        mysql_source.execute(input_sql)
        mysql_source.commit()
        mysql_source.close()

    def data_content_to_db(self, db_name, db_table, input_content, separator):
        try:
            if "," == separator:
                content_obj = csv.reader(io.StringIO(input_content))
            else:
                content_obj = \
                    [x.split(separator) for x in
                     [j for j in input_content.split("\n")]]
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

            self.exec_sql(insert_sql)
            logging.info("data merge to mysql successful")
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
        """
        数据更新
        :param db_name: 数据库名
        :param table_name: 数据表名
        :param update_value: 更新字段，json格式
        :param where_value: 条件，json格式
        :return: True or False
        """
        try:
            # 先format更新字段
            set_value = \
                ", ".join(
                    ["%s='%s'" % (set_key, update_value[set_key])
                     for set_key in update_value]
                )
            # format 条件字段
            where_value = \
                " and ".join(
                    ["%s='%s'" % (where_key, where_value[where_key])
                     for where_key in where_value]
                )
            update_sql = \
                self.UPDATE_DATA_SQL % (
                    db_name,
                    table_name,
                    set_value,
                    where_value
                )
            logging.info("update sql is %s" % update_sql)

            self.exec_sql(update_sql)
            logging.info("data update in mysql successful")
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def data_content_delete(
            self,
            db_name,
            table_name,
            where_value
    ):
        try:
            where_format_value = \
                " and ".join(
                    ["%s='%s'" % (
                        key, where_value.__getitem__(key)
                    ) for key in where_value])
            delete_sql = \
                self.DELETE_DATA_SQL % (
                    db_name,
                    table_name,
                    where_format_value
                )
            logging.info("delete mysql data sql is %s" % delete_sql)
            self.exec_sql(delete_sql)
            logging.info("data delete in mysql successful")
            return True
        except Exception as e:
            logging.exception(e)
            return False
