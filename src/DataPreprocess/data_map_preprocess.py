import logging
from src.config.load_config_map import get_config_conf
from src.DataPreprocess.es_preprocess import EsPreprocess
from src.DataPreprocess.hive_preprocess import HivePreprocess
from src.DataPreprocess.mysql_preprocess import MysqlPreprocess
from src.DataPreprocess.neo_preprocess import NeoPreprocess
from src.DataPreprocess.redis_preprocess import RedisPreprocess
from src.DataSource.elasticsearch_source import EsSource
from src.DataSource.hive_source import HiveSource
from src.DataSource.mysql_source import MysqlSource
from src.DataSource.neo_source import NeoSource
from src.DataSource.presto_source import PrestoSource
from src.DataSource.redis_source import RedisSource
from src.utils.common_utils import CommonUtils


class DataMapPreprocess(object):

    def __init__(self):
        self.config_map = get_config_conf()
        self.common_utils = CommonUtils()
        self.cache_select_presto_client = PrestoSource("mysql")
        self.mysql_source = MysqlSource()
        self.hive_info = []
        self.mysql_info = []
        self.redis_info = []
        self.es_info = []
        self.neo_info = []
        self.cache_select_presto_client.create_connection()

    def hive_parse_related(self):
        # hive数据信息查询
        hive_source = HiveSource()
        hive_process = HivePreprocess()
        hive_source.create_connection()
        redis_source = RedisSource()
        redis_source.create_connection()
        hive_source.execute("show databases")
        database_list = hive_source.fetch_all()
        for sub_db in database_list:
            if sub_db[0] in hive_source.hive_ignore_database:
                logging.info("database %s is ignored" % sub_db[0])
                continue
            logging.info("parse data map from database %s" % sub_db[0])
            hive_source.execute("show tables from %s" % sub_db[0])
            table_list = hive_source.fetch_all()
            for sub_table in table_list:
                full_table_name = "%s.%s" % (sub_db[0], sub_table[0])
                if full_table_name in hive_source.hive_ignore_table:
                    logging.info("table %s is ignored" % full_table_name)
                    continue
                logging.info("parse data map from table %s" % full_table_name)
                hive_source.execute("desc formatted %s" % full_table_name)
                table_info = hive_source.fetch_all()
                format_json = \
                    hive_process.format_table_info(
                        table_info,
                        full_table_name,
                        redis_source
                    )
                format_json["table_name"] = full_table_name
                self.hive_info.append(format_json)
        hive_source.close()
        redis_source.close()

    def mysql_parse_related(self):
        self.mysql_source.create_connection()
        redis_source = RedisSource()
        redis_source.create_connection()
        mysql_process = MysqlPreprocess()

        self.mysql_source.execute("show databases")
        database_list = self.mysql_source.fetch_all()
        for sub_database in database_list:
            if sub_database[0] in self.mysql_source.mysql_ignore_database:
                logging.info("database %s is ignored" % sub_database[0])
                continue
            logging.info("parse database: %s" % sub_database)
            self.mysql_source.execute("show tables from %s" % sub_database[0])
            table_list = self.mysql_source.fetch_all()
            for sub_table in table_list:
                full_table_name = "%s.%s" % (sub_database[0], sub_table[0])
                if full_table_name in self.mysql_source.mysql_ignore_table:
                    logging.info("table %s is ignored" % full_table_name)
                    continue
                format_json = \
                    mysql_process.format_table_info(
                        full_table_name,
                        self.mysql_source
                    )
                format_json["table_name"] = full_table_name
                self.mysql_info.append(format_json)
        self.mysql_source.close()
        redis_source.close()

    def redis_parse_related(self):
        redis_process = RedisPreprocess()
        redis_source = RedisSource()
        redis_source.create_connection()
        format_json = redis_process.format_table_info(redis_source)
        format_json["table_name"] = ""
        self.redis_info.append(format_json)
        redis_source.close()

    def es_parse_related(self):
        es_source = EsSource()
        es_source.create_connection()
        es_process = EsPreprocess()
        # es_source.es_client.cat.indices(headers="h,s,i,id,p,r,dc,dd,ss,creation.date.string")  # nopep8
        for index_name in es_source.es_client.indices.get("*"):
            format_json = es_process.format_table_info(es_source, index_name)
            format_json["table_name"] = index_name
            self.es_info.append(format_json)
        es_source.close()

    def neo_parse_related(self):
        neo_source = NeoSource()
        neo_process = NeoPreprocess()
        for sub_auth_url in self.config_map["neo_connect_urls"]:

            neo_source.create_connection_auth(
                sub_auth_url,
                self.config_map["neo_usernames"][
                    self.config_map["neo_connect_urls"].index(sub_auth_url)],
                self.config_map["neo_passwords"][
                    self.config_map["neo_connect_urls"].index(sub_auth_url)],
            )
            format_result = \
                neo_process.format_result_json(
                    neo_source,
                    sub_auth_url
                )
            self.neo_info.extend(format_result)
            neo_source.close()

    def abstract_parse_related(self):
        """
        解析各个数据源的数据信息
        :return:
        """

        return_result = {}
        self.hive_parse_related()
        hive_parse_result = self.hive_fetch_data_map()
        return_result["hive_abstract_data"] = \
            hive_parse_result["abstract_data"]
        self.mysql_parse_related()
        mysql_parse_result = self.mysql_fetch_data_map()
        return_result["mysql_abstract_data"] = \
            mysql_parse_result["abstract_data"]
        self.redis_parse_related()
        redis_parse_result = self.redis_fetch_data_map()
        return_result["redis_abstract_data"] = \
            redis_parse_result["abstract_data"]
        self.es_parse_related()
        redis_parse_result = self.es_fetch_data_map()
        return_result["es_abstract_data"] = \
            redis_parse_result["abstract_data"]
        self.neo_parse_related()
        redis_parse_result = self.neo_fetch_data_map()
        return_result["neo_abstract_data"] = \
            redis_parse_result["abstract_data"]

        # TODO(lihongjie): 后续其他数据源解析数据
        return return_result

    def hive_fetch_data_map(self):
        return_result = {
            "hive_source": self.hive_info,
            "abstract_data": []
        }
        for sub_table_info in self.hive_info:
            return_result["abstract_data"].append(
                {
                    "dbName": sub_table_info["dbName"],
                    "tableName": sub_table_info["tableName"],
                    "numRows": sub_table_info["numRows"],
                    "totalSize": sub_table_info["totalSize"],
                    "numAddedYesterday": sub_table_info["numAddedYesterday"],
                    "numAddedlastWeek": sub_table_info["numAddedlastWeek"],
                    "lastUpdateTime": sub_table_info["lastUpdateTime"],
                    "createTime": sub_table_info["createTime"],
                    "tableComment": sub_table_info["tableComment"],
                }
            )

        return return_result

    def mysql_fetch_data_map(self):
        return_result = {
            "mysql_source": self.mysql_info,
            "abstract_data": []
        }
        for sub_table_info in self.mysql_info:
            return_result["abstract_data"].append(
                {
                    "dbName": sub_table_info["dbName"],
                    "tableName": sub_table_info["tableName"],
                    "numRows": sub_table_info["numRows"],
                    "totalSize": sub_table_info["totalSize"],
                    "numAddedYesterday": sub_table_info["numAddedYesterday"],
                    "numAddedlastWeek": sub_table_info["numAddedlastWeek"],
                    "lastUpdateTime": sub_table_info["lastUpdateTime"],
                    "createTime": sub_table_info["createTime"],
                    "tableComment": sub_table_info["tableComment"],
                }
            )
        return return_result

    def redis_fetch_data_map(self):
        return_result = {
            "redis_source": self.redis_info,
            "abstract_data": []
        }
        for sub_table_info in self.redis_info:
            return_result["abstract_data"].append(
                {
                    "dbName": sub_table_info["dbName"],
                    "tableName": sub_table_info["tableName"],
                    "numRows": sub_table_info["numRows"],
                    "totalSize": sub_table_info["totalSize"],
                    "numAddedYesterday": sub_table_info["numAddedYesterday"],
                    "numAddedlastWeek": sub_table_info["numAddedlastWeek"],
                    "lastUpdateTime": sub_table_info["lastUpdateTime"],
                    "createTime": sub_table_info["createTime"],
                    "tableComment": sub_table_info["tableComment"],
                }
            )
        return return_result

    def es_fetch_data_map(self):
        return_result = {
            "es_source": self.es_info,
            "abstract_data": []
        }
        for sub_table_info in self.es_info:
            return_result["abstract_data"].append(
                {
                    "dbName": sub_table_info["dbName"],
                    "tableName": sub_table_info["tableName"],
                    "numRows": sub_table_info["numRows"],
                    "totalSize": sub_table_info["totalSize"],
                    "numAddedYesterday": sub_table_info["numAddedYesterday"],
                    "numAddedlastWeek": sub_table_info["numAddedlastWeek"],
                    "lastUpdateTime": sub_table_info["lastUpdateTime"],
                    "createTime": sub_table_info["createTime"],
                    "tableComment": sub_table_info["tableComment"],
                }
            )
        return return_result

    def neo_fetch_data_map(self):
        return_result = {
            "neo_source": self.neo_info,
            "abstract_data": []
        }
        for sub_table_info in self.neo_info:
            return_result["abstract_data"].append(
                {
                    "dbName": sub_table_info["dbName"],
                    "tableName": sub_table_info["tableName"],
                    "numRows": sub_table_info["numRows"],
                    "totalSize": sub_table_info["totalSize"],
                    "numAddedYesterday": sub_table_info["numAddedYesterday"],
                    "numAddedlastWeek": sub_table_info["numAddedlastWeek"],
                    "lastUpdateTime": sub_table_info["lastUpdateTime"],
                    "createTime": sub_table_info["createTime"],
                    "tableComment": sub_table_info["tableComment"],
                }
            )
        return return_result
