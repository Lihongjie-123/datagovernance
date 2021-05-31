import pymysql
from src.DataSource.data_source import DataSource


class MysqlSource(DataSource):

    def __init__(self):
        super().__init__()
        self.source_type = "hive"
        self.mysql_ignore_database = self.config_map["mysql_ignore_databases"]
        self.mysql_ignore_table = self.config_map["mysql_ignore_tables"]

    def create_connection(self):
        """
        创建数据源连接
        :return:
        """
        self.mysql_db = pymysql.connect(
            host=self.config_map["mysql_ip"],
            port=3306,
            user=self.config_map["mysql_username"],
            password=self.config_map["mysql_password"],
            database=self.config_map["mysql_database"],
            charset='utf8'
        )
        self.mysql_cursor = self.mysql_db.cursor()

    def commit(self):
        """
        提交更新
        :return:
        """
        self.mysql_db.commit()

    def execute(self, input_sql):
        """
        执行sql
        :param input_sql:
        :return:
        """
        self.mysql_cursor.execute(input_sql)

    def fetch_all(self):
        """
        获取查询结果
        :return:
        """
        return self.mysql_cursor.fetchall()

    def close(self):
        """
        关闭连接
        :return:
        """
        self.mysql_cursor.close()
        self.mysql_db.close()
