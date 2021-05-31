import logging
from src.config.load_config_map import get_config_conf
from src.DataSource.mysql_source import MysqlSource
from src.models import StatisticsDataInfo
from src.utils.common_utils import CommonUtils


class PreprocessUtil(object):
    def __init__(self):
        self.common_utils = CommonUtils()
        self.config_map = get_config_conf()
        self.mysql_source = MysqlSource()

    def cache_data_select(self, interface_type):
        """
        比较传统的查询方法，不用了
        :param interface_type:
        :return:
        """
        select_result = None
        try:
            select_sql = \
                self.common_utils.MYSQL_CACHE_DATA_SELECT_SQL % (
                    self.config_map["statistics_data_db_name"],
                    self.config_map["statistics_data_table_name"],
                    interface_type
                )
            logging.info("[ %s ] request sql is [ %s ]" % (
                interface_type,
                select_sql
            ))
            # 查presto
            # self.cache_select_presto_client.execute(select_sql)
            # select_dict = self.cache_select_presto_client.fetch_all().to_dict()  # nopep8
            # select_result = select_dict["data"][0]
            # 查mysql
            self.mysql_source.create_connection()
            self.mysql_source.execute(select_sql)
            select_result = self.mysql_source.fetch_all()[0][0]
            self.mysql_source.close()
        except Exception as e:
            logging.exception(e)
        return select_result

    @staticmethod
    def cache_data_select_by_orm(interface_type):
        statistics_info = \
            StatisticsDataInfo.objects.filter(
                interface_type=interface_type
            ).order_by("-import_time")
        query_result = statistics_info.values("data").first()
        return query_result["data"]
