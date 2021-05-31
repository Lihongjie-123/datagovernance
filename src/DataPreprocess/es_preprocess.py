import csv
import datetime
from elasticsearch import helpers
import io
import json
import logging
import requests
from src.config.load_config_map import get_config_conf
from src.DataSource.elasticsearch_source import EsSource
from src.DataSource.presto_source import PrestoSource
from src.utils.common_utils import CommonUtils
from src.utils.preprocess_utils import PreprocessUtil


class EsPreprocess(object):

    def __init__(self):
        self.config_map = get_config_conf()
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.before_7_days_date = self.today - datetime.timedelta(days=7)
        self.check_import_time_body = {
            "query": {
                "match_all": {}
            },
            "aggregations": {
                "update_time": {
                    "max": {
                        "field": "import_time"
                    }
                }
            }
        }
        self.query_create_time_url = \
            "http://%s:%s/_cat/indices?" \
            "h=h,s,i,id,p,r,dc,dd,ss,creation.date.string&format=json" % (
                self.config_map["es_server_hosts"][0],
                self.config_map["es_server_port"]
            )
        self.SELECT_DATA_SQL = "select * from %s limit %s"
        self.common_utils = CommonUtils()
        self.preprocess_utils = PreprocessUtil()

    def format_col_info(
            self,
            es_source,
            index_name,
            format_result_json
    ):
        try:
            index_state_info = \
                es_source.es_client.cluster.state(index=index_name)
            index_info = \
                index_state_info[
                    "metadata"]["indices"][
                    index_name]["mappings"][
                    "_doc"]["properties"]
            logging.info(index_info)
            col_info = self.get_col_list_by_index(index_name)
            logging.info("col_info is %s" % col_info)
            for col_name in col_info:

                if "import_time" == col_name and \
                        "date" == index_info[col_name]["type"]:

                    # 提取昨天入库量
                    yesterday_count = \
                        es_source.es_client.count(
                            index=index_name,
                            q='import_time:[ %sT00:00:00Z TO %sT00:00:00Z ]' %
                              (
                                  str(self.yesterday),
                                  str(self.today)
                              )
                        )
                    logging.info(yesterday_count)
                    format_result_json["numAddedYesterday"] = \
                        str(yesterday_count["count"])

                    # 提取最近一周入库量
                    sev_days_ago_count = \
                        es_source.es_client.count(
                            index=index_name,
                            q='import_time:[ %sT00:00:00Z TO %sT00:00:00Z ]' %
                              (
                                  str(self.before_7_days_date),
                                  str(self.today)
                              )
                        )
                    logging.info(sev_days_ago_count)
                    format_result_json["numAddedlastWeek"] = \
                        str(sev_days_ago_count["count"])

                    # 获取最近更新时间
                    max_update_time = \
                        es_source.es_client.search(
                            index=index_name,
                            body=self.check_import_time_body
                        )
                    format_result_json["lastUpdateTime"] = \
                        max_update_time[
                            'aggregations']['update_time']['value_as_string']

                format_result_json["col_name"].append({
                    "col_name": col_name,
                    "col_type": index_info[col_name]["type"],
                    "col_comment": "",
                })
        except Exception as e:
            logging.exception(e)
            format_result_json["col_name"] = []

    @staticmethod
    def format_detail_info(
            es_source,
            index_name,
            format_result_json
    ):
        try:
            index_info = \
                es_source.es_client.cat.indices(
                    index=index_name,
                    format='json'
                )[0]
            for key in index_info:
                if "docs.count" == key:
                    format_result_json["numRows"] = index_info[key]

                if "store.size" == key:
                    format_result_json["totalSize"] = index_info[key]

                format_result_json["detail_information"].append({
                    "index_name": index_name,
                    "info_field": key,
                    "info_value": index_info[key],
                })
        except Exception as e:
            logging.exception(e)
            format_result_json["detail_information"] = []

    def format_time_info(
            self,
            index_name,
            format_result_json
    ):
        try:
            # 获取创建时间
            req = requests.get(self.query_create_time_url)
            create_time_info_list = req.json()
            for sub_info in create_time_info_list:
                if index_name == sub_info["i"]:
                    format_result_json["createTime"] = \
                        sub_info["creation.date.string"]
            req.close()
        except Exception as e:
            logging.exception(e)

    def format_table_info(self, es_source, index_name):
        format_result_json = {
            "col_name": [],
            "detail_information": [],
            "dbName": "",
            "tableName": index_name,
            "numRows": "0",
            "totalSize": "0",
            "numAddedYesterday": "0",
            "numAddedlastWeek": "0",
            "lastUpdateTime": "",
            "createTime": "",
            "tableComment": ""
        }

        self.format_col_info(es_source, index_name, format_result_json)

        self.format_detail_info(es_source, index_name, format_result_json)

        self.format_time_info(index_name, format_result_json)

        return format_result_json

    @staticmethod
    def get_col_list_by_index(index_name):
        es_source = EsSource()
        es_source.create_connection()
        one_data_info = \
            es_source.es_client.search(index=index_name, size=1)
        if 1 == len(one_data_info["hits"]["hits"]):
            data_info = one_data_info["hits"]["hits"][0]["_source"]
        else:
            data_info = {}
        col_info = list(data_info.keys())
        es_source.close()
        return col_info

    def select_data(self, _db_name, table_name, select_count):
        presto_source = PrestoSource("elasticsearch")
        presto_source.create_connection()
        select_sql = self.SELECT_DATA_SQL % (
            table_name,
            select_count
        )
        logging.info("select sql is %s " % select_sql)
        presto_source.execute(select_sql)
        select_df = presto_source.fetch_all()
        logging.info(select_df)
        select_df = select_df[self.get_col_list_by_index(table_name)]
        logging.info(select_df)
        return_result = self.common_utils.format_df(select_df)
        presto_source.close()
        return return_result

    def parse_table_col_info(self, full_table_name):
        data_map = \
            json.loads(self.preprocess_utils.cache_data_select("ESDataMap"))
        col_info = []
        for i in data_map["es_source"]:
            if full_table_name == i["table_name"]:
                for col_name_info in i["col_name"]:
                    col_info.append(col_name_info["col_name"])
                break
        return col_info

    @staticmethod
    def format_data_to_es(index_name, value_list):
        format_values = []
        col_info = []
        first_line = True
        for line in value_list:
            if first_line:
                col_info = line
                first_line = False
                continue
            if 1 == len(line) and not line[0]:
                continue
            tmp_value = {
                "_index": index_name,
                "_source": {}
            }
            for index in range(len(col_info)):
                tmp_value["_source"][col_info[index]] = line[index]
            format_values.append(tmp_value)
        return format_values

    def data_content_to_db(self, db_name, db_table, input_content, separator):
        try:
            if "," == separator:
                content_obj = csv.reader(io.StringIO(input_content))
            else:
                content_obj = \
                    [x.split(separator) for x in
                     [j for j in input_content.split("\n")]]
            format_values = \
                self.format_data_to_es(
                    db_table,
                    content_obj
                )

            logging.info(format_values)
            es_source = EsSource()
            es_source.create_connection()
            helpers.bulk(es_source.es_client, format_values)
            es_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    @staticmethod
    def data_content_update(
            _db_name,
            table_name,
            update_value,
            where_value
    ):
        try:
            assert where_value.__contains__("_id")
            es_source = EsSource()
            es_source.create_connection()
            es_source.es_client.update(
                index=table_name,
                body={"doc": update_value},
                id=where_value["_id"]
            )
            es_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    @staticmethod
    def data_content_delete(
            _db_name,
            table_name,
            where_value
    ):
        try:
            assert where_value.__contains__("_id")
            es_source = EsSource()
            es_source.create_connection()
            es_source.es_client.delete(
                index=table_name,
                id=where_value["_id"]
            )
            es_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False
