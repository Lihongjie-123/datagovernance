import csv
import io
import json
import logging
from src.DataSource.redis_source import RedisSource


class RedisPreprocess(object):

    def __init__(self):
        pass

    @staticmethod
    def format_table_info(redis_source):

        format_json = {
            "resource_check": [],
            "dbName": "",
            "tableName": "",
            "numRows": "0",
            "totalSize": "0",
            "numAddedYesterday": "0",
            "numAddedlastWeek": "0",
            "lastUpdateTime": "",
            "createTime": "",
            "tableComment": ""
        }
        # redis_source = RedisSource()
        # redis_source.create_collection()
        hkeys_name_list = redis_source.redisconn.keys("*")
        sum_count = 0
        total_size = 0
        for sub_hkey_name in hkeys_name_list:
            keys_list = redis_source.redisconn.hkeys(sub_hkey_name)
            sum_count += len(keys_list)
        format_json["numRows"] = str(sum_count)
        cluster_info = redis_source.redisconn.info()
        for cluster_node in cluster_info:
            for resource_field in cluster_info[cluster_node]:
                if "used_memory" == resource_field:
                    total_size += \
                        int(cluster_info[cluster_node][resource_field])
                format_json["resource_check"].append({
                    "clusterNode": cluster_node,
                    "resourceField": resource_field,
                    "resourceValue":
                        cluster_info[cluster_node][resource_field]
                })
        if 0 <= total_size <= 1024:
            format_json["totalSize"] = "%s(B)" % total_size
        elif 1024 < total_size <= 1048576:
            format_json["totalSize"] = \
                "%s(KB)" % (round(total_size / 1024, 3))
        elif 1048576 < total_size <= 1073741824:
            format_json["totalSize"] = \
                "%s(MB)" % (round(total_size / 1048576, 3))
        elif 1073741824 < total_size <= 1099511627776:
            format_json["totalSize"] = \
                "%s(GB)" % (round(total_size / 1073741824, 3))
        elif 1099511627776 < total_size <= 1125899906842624:
            format_json["totalSize"] = \
                "%s(TB)" % (round(total_size / 1099511627776, 3))
        else:
            format_json["totalSize"] = \
                "%s(PB)" % (
                    round(total_size / 1125899906842624, 3))
        # redis_source.close()
        return format_json

    @staticmethod
    def data_content_to_db(_db_name, _db_table, input_content, separator):
        """
        redis上传数据，需要有三列，name key value
        :param _db_name:
        :param _db_table:
        :param input_content:
        :param separator:
        :return:
        """
        try:
            if "," == separator:
                content_obj = csv.reader(io.StringIO(input_content))
            else:
                content_obj = \
                    [x.split(separator) for x in
                     [j for j in input_content.split("\n")]]
            logging.info(content_obj)
            data_list = \
                [
                    {"name": x[0], "key": x[1], "value": x[2]}
                    for x in content_obj if [""] != x
                ]
            redis_source = RedisSource()
            redis_source.create_connection()
            for sub_row in data_list:
                logging.info(sub_row)
                redis_source.redisconn.hset(
                    name=sub_row["name"],
                    key=sub_row["key"],
                    value=sub_row["value"]
                )
            redis_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    @staticmethod
    def data_content_update(
            _db_name,
            _table_name,
            update_value,
            where_value
    ):
        try:
            assert all([
                where_value.__contains__("name"),
                where_value.__contains__("key")
            ])
            redis_source = RedisSource()
            redis_source.create_connection()
            redis_source.redisconn.hset(
                name=where_value["name"],
                key=where_value["key"],
                value=json.dumps(update_value)
            )
            redis_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    @staticmethod
    def data_content_delete(
            _db_name,
            _table_name,
            where_value
    ):
        try:
            assert all([
                where_value.__contains__("name"),
                where_value.__contains__("key")
            ])
            redis_source = RedisSource()
            redis_source.create_connection()
            redis_source.redisconn.hdel(
                where_value.__getitem__("name"),
                where_value.__getitem__("key")
            )
            redis_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False
