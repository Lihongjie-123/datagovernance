import pandas as pd
from sqlalchemy.engine import create_engine
from src.DataSource.data_source import DataSource


class PrestoSource(DataSource):

    def __init__(self, data_source_type):
        super().__init__()
        self.source_type = "presto"
        self.select_result_df = None
        self.data_source_type = data_source_type

    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        self.presto_engine = \
            create_engine('presto://%s:%s/%s/default' % (
                self.config_map["presto_server_ip"],
                self.config_map["presto_server_port"],
                self.data_source_type
            ))

    def commit(self):
        """
        提交更新
        :return:
        """
        pass

    def execute(self, input_sql):
        """
        执行sql
        :param input_sql:
        :return:
        """
        self.select_result_df = pd.read_sql(input_sql, self.presto_engine)

    def fetch_all(self):
        """
        获取查询结果
        :return:
        """
        return self.select_result_df

    def close(self):
        """
        关闭连接
        :return:
        """
        self.presto_engine = None
