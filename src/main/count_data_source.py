"""
spark streaming 程序，用于实时接收前端传过来的参数，并且计算结果返回
热词查询
"""
import datetime
import logging.config
from optparse import OptionParser
import os
from src.config import load_config_map
from src.DataSource.hive_source import HiveSource
from src.DataSource.redis_source import RedisSource

workdir = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))  # nopep8
if "lib" == os.path.basename(workdir):
    workdir = os.path.dirname(workdir)
config_map = load_config_map.get_config_conf()  # 存储配置
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
before_7_days_date = today - datetime.timedelta(days=7)
COUNT_COUNT_SQL = \
    "select count(1) from %s " \
    "where import_time > '%s' and import_time < '%s'"
COUNT_SUM_SQL = "select count(1) from %s"


def _handle_cmd_line(args=None):
    parser = OptionParser()

    parser.add_option("--id", dest="id", action="store",
                      type="string", default="0",
                      help="id use guard and create log file")
    parser.add_option("--logconfig", dest="logconfig", action="store",
                      type="string",
                      default=os.path.join(
                          workdir, 'etc',
                          'count_data_source.log.conf'),
                      help="log config file [%default]")
    (options, args) = parser.parse_args(args=args)
    return options, args


def _valid_options(_options):
    # TODO(lihongjie): 后面可能增加其他参数，用作参数检查
    return True


def hive_related(hive_source, redis_source):
    try:
        hive_source.execute("show databases")
        database_list = hive_source.fetch_all()
        for sub_db in database_list:
            if sub_db[0] in hive_source.hive_ignore_database:
                logging.info("database %s is ignored" % sub_db[0])
                continue
            hive_source.execute("show tables from %s" % sub_db[0])
            table_list = hive_source.fetch_all()
            for sub_table in table_list:
                full_table_name = "%s.%s" % (sub_db[0], sub_table[0])
                if full_table_name in hive_source.hive_ignore_table:
                    logging.info("table %s is ignored" % full_table_name)
                    continue

                hive_source.execute(
                    COUNT_SUM_SQL % (
                        full_table_name
                    )
                )
                sum_count = hive_source.fetch_all()[0][0]
                logging.info("sum count is %s" % sum_count)
                logging.info("redis key is %s" %
                             ("hive_sum_count-%s" % full_table_name))
                redis_source.hset(
                    name="hive_sum_count",
                    key="hive_sum_count-%s" % full_table_name,
                    value=sum_count
                )

                hive_source.execute("desc %s" % full_table_name)
                desc_info = hive_source.fetch_all()
                has_import_time = False
                for col_info in desc_info:
                    if "import_time".__eq__(col_info[0]):
                        has_import_time = True
                if not has_import_time:
                    continue
                logging.info("count data num from %s" % full_table_name)
                hive_source.execute(
                    COUNT_COUNT_SQL % (
                        full_table_name,
                        "%s 00:00:00" % str(yesterday),
                        "%s 00:00:00" % str(today)
                    )
                )
                yesterday_count = hive_source.fetch_all()[0][0]
                logging.info("yesterday count is %s" % yesterday_count)
                logging.info("redis key is %s" %
                             ("hive_yesterday_count-%s" % full_table_name))
                redis_source.hset(
                    name="hive_yesterday_count",
                    key="hive_yesterday_count-%s" % full_table_name,
                    value=yesterday_count
                )
                hive_source.execute(
                    COUNT_COUNT_SQL % (
                        full_table_name,
                        "%s 00:00:00" % str(before_7_days_date),
                        "%s 00:00:00" % str(today)
                    )
                )
                sev_daysago_count = hive_source.fetch_all()[0][0]
                logging.info("last week count is %s" % sev_daysago_count)
                logging.info("redis key is %s" %
                             ("hive_7days_ago_count-%s" % full_table_name))
                redis_source.hset(
                    name="hive_7days_ago_count",
                    key="hive_7days_ago_count-%s" % full_table_name,
                    value=str(sev_daysago_count)
                )

    except Exception as e:
        logging.exception(e)


def process():
    hive_source = HiveSource()
    hive_source.create_connection()
    redis_source = RedisSource()
    redis_source.create_connection()
    hive_related(hive_source, redis_source)
    hive_source.close()
    redis_source.close()


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
