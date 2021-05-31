"""
spark streaming 程序，用于实时接收前端传过来的参数，并且计算结果返回
热词查询
"""
import json
import logging.config
from optparse import OptionParser
import os
import re
import requests
from src.config import load_config_map
from src.DataSource.mysql_source import MysqlSource
import time
import uuid

workdir = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))  # nopep8
if "lib" == os.path.basename(workdir):
    workdir = os.path.dirname(workdir)
config_map = load_config_map.get_config_conf()  # 存储配置
mysql_insert_sql = \
    "insert into %s.%s(" \
    "primary_id,interface_type,data,import_time) values(%s)"
query_url = "http://%s:%s/%s"


def _handle_cmd_line(args=None):
    parser = OptionParser()

    parser.add_option("--id", dest="id", action="store",
                      type="string", default="0",
                      help="id use guard and create log file")
    parser.add_option("--logconfig", dest="logconfig", action="store",
                      type="string",
                      default=os.path.join(
                          workdir, 'etc',
                          'query_data_source.log.conf'),
                      help="log config file [%default]")
    (options, args) = parser.parse_args(args=args)
    return options, args


def _valid_options(_options):
    # TODO(lihongjie): 后面可能增加其他参数，用作参数检查
    return True


def data_to_mysql(interface_type, input_data, mysql_source):
    try:
        value_list = [
            uuid.uuid1().__str__(),
            interface_type,
            re.escape(json.dumps(input_data)),
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ]
        value = "'%s'" % ("','".join(value_list))
        insert_sql = \
            mysql_insert_sql % (
                config_map["statistics_data_db_name"],
                config_map["statistics_data_table_name"],
                value
            )
        mysql_source.execute(insert_sql)
        mysql_source.commit()
    except Exception as _e:
        logging.exception(_e)


def _format_url(interface_type):
    return (
        query_url % (
            config_map["django_server_ip"],
            config_map["django_server_port"],
            interface_type
        ), interface_type
    )


def format_all_url():
    return [
        _format_url("AbstractDataMap"),
        _format_url("HiveDataMap"),
        _format_url("MysqlDataMap"),
        _format_url("RedisDataMap"),
        _format_url("ESDataMap"),
        _format_url("NeoDataMap"),
    ]


def process():
    all_url_info = format_all_url()
    mysql_source = MysqlSource()
    mysql_source.create_connection()
    for url_info in all_url_info:
        logging.info("now query interface : %s" % url_info[1])
        req = requests.get(url_info[0])
        query_data = req.json()
        data_to_mysql(url_info[1], query_data, mysql_source)
    mysql_source.close()


def main():
    try:
        options, _args = _handle_cmd_line()
        if options.logconfig:
            defaults = {"id": options.id}
            logging.config.fileConfig(options.logconfig, defaults)
        if not _valid_options(options):
            logging.error("options:\n" +
                          '\n'.join('%s = %s' %
                                    (d, getattr(options, d))
                                    for d in options.__dict__))
            return
        logging.info("start to count data source")
        process()
        logging.info("end to count data source")

    except Exception as exception:
        logging.exception(exception)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
        exit(-1)
