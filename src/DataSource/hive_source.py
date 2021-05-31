import logging
from pyhive import hive
from src.DataSource.data_source import DataSource
from src.ErrorCenter.error_center import ErrorCenter


class HiveSource(DataSource):

    def __init__(self):
        super().__init__()
        self.source_type = "hive"
        self.hive_ignore_database = self.config_map["hive_ignore_databases"]
        # 库名.表名，如： fake_db.fake_ignore_table
        self.hive_ignore_table = self.config_map["hive_ignore_tables"]

    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        try:
            self.hive_client = hive.connect(
                host=self.config_map["hive_jdbc_ip"],
                port=self.config_map["hive_jdbc_port"]
            )
            self.hive_cursor = self.hive_client.cursor()
        except Exception as e:
            logging.error(
                ErrorCenter.CREATE_DATA_SOURCE_CONNECT_FAILED %
                self.source_type
            )
            logging.exception(e)

    def commit(self):
        """
        提交更新
        :return:
        """
        if not self.hive_client:
            logging.error(
                ErrorCenter.VARIABLE_NOT_INITIAL_ERROR % "self.client"
            )
        else:
            self.hive_client.commit()

    def execute(self, input_sql):
        """
        执行sql
        :param input_sql:
        :return:
        """
        try:
            logging.info("exec sql is %s" % input_sql)
            self.hive_cursor.execute(input_sql)
        except Exception as e:
            logging.error(ErrorCenter.EXEC_SQL_FAILED % self.source_type)
            logging.exception(e)

    def fetch_all(self):
        """
        获取查询结果
        :return:
        """
        return self.hive_cursor.fetchall()

    def close(self):
        """
        关闭连接
        :return:
        """
        try:
            self.hive_cursor.close()
            self.hive_client.close()
        except Exception as e:
            logging.error(
                ErrorCenter.CLOSE_DB_CONNECT_FAILED %
                self.source_type
            )
            logging.exception(e)
