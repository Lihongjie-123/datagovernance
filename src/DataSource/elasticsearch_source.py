from elasticsearch import Elasticsearch
from src.DataSource.data_source import DataSource


class EsSource(DataSource):

    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        es_nodes = []
        for sub_ip in self.config_map["es_server_hosts"]:
            es_nodes.append({
                "host": sub_ip,
                "port": self.config_map["es_server_port"]
            })
        self.es_client = Elasticsearch(
            hosts=es_nodes
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
        pass

    def fetch_all(self):
        """
        获取查询结果
        :return:
        """
        pass

    def close(self):
        """
        关闭连接
        :return:
        """
        self.es_client.close()
