from rediscluster import RedisCluster
from src.DataSource.data_source import DataSource


class RedisSource(DataSource):

    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        redis_nodes = []
        for sub_ip in self.config_map["redis_server_hosts"]:
            redis_nodes.append({
                "host": sub_ip,
                "port": self.config_map["redis_server_ports"][self.config_map[
                    "redis_server_hosts"].index(sub_ip)]
            })
        self.redisconn = \
            RedisCluster(
                startup_nodes=redis_nodes,
                decode_responses=True
            )

    def hset(self, name, key, value):
        self.redisconn.hset(
            name,
            key,
            str(value)
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
        self.redisconn.close()
