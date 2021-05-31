from py2neo import Graph
from src.DataSource.data_source import DataSource


class NeoSource(DataSource):

    def __init__(self):
        super().__init__()
        self.source_type = "neo4j"
        self.graph_exec_result = None

    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        pass

    def create_connection_auth(
            self,
            neo_connect_url,
            neo_username,
            neo_password
    ):
        """
        创建数据源连接
        :return:
        """
        self.graph = Graph(
            neo_connect_url,
            user=neo_username,
            password=neo_password
        )

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
        self.graph_exec_result = self.graph.run(input_sql).data()

    def fetch_all(self):
        """
        获取查询结果
        :return:
        """
        return self.graph_exec_result

    def close(self):
        """
        关闭连接
        :return:
        """
        self.graph = None
