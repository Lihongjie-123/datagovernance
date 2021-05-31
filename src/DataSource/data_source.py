import abc
from src.config.load_config_map import get_config_conf


class DataSource(object):
    """
    该类为所有数据源连接的父类，定义一些方法由子类去实现，抽出所有子类公用的方法
    这里不能做成单例模式，如果多个人共同请i去的话，单例模式会有问题
    """
    __metaclass__ = abc.ABCMeta  # nopep8

    def __init__(self):
        self.config_map = get_config_conf()
        self.hive_client = None
        self.hive_cursor = None
        self.mysql_db = None
        self.mysql_cursor = None
        self.source_type = None
        self.redisconn = None
        self.es_client = None
        self.graph = None
        self.presto_engine = None
        self.hive_ignore_database = []
        self.hive_ignore_table = []
        self.mysql_ignore_database = []
        self.mysql_ignore_table = []

    @abc.abstractmethod
    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        pass

    @abc.abstractmethod
    def commit(self):
        """
        提交更新
        :return:
        """
        pass

    @abc.abstractmethod
    def execute(self, input_sql):
        """
        执行sql
        :param input_sql:
        :return:
        """
        pass

    @abc.abstractmethod
    def fetch_all(self):
        """
        获取查询结果
        :return:
        """
        pass

    @abc.abstractmethod
    def close(self):
        """
        关闭连接
        :return:
        """
        pass
