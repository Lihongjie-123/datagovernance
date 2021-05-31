from src.DataPreprocess.es_preprocess import EsPreprocess
from src.DataPreprocess.hive_preprocess import HivePreprocess
from src.DataPreprocess.mysql_preprocess import MysqlPreprocess
from src.DataPreprocess.neo_preprocess import NeoPreprocess
from src.DataPreprocess.redis_preprocess import RedisPreprocess


class UpdateDataPrerprocess(object):

    def __init__(self, db_type):
        self.db_type = db_type

    def __new__(cls, *args, **kwargs):
        if "Hive" == args[0]:
            return HivePreprocess()
        elif "Mysql" == args[0]:
            return MysqlPreprocess()
        elif "Redis" == args[0]:
            return RedisPreprocess()
        elif "ElasticSearch" == args[0]:
            return EsPreprocess()
        elif "Neo4j" == args[0]:
            return NeoPreprocess()
        else:
            return super(UpdateDataPrerprocess, cls).__new__(cls)

    def data_content_update(
            self,
            db_name,
            table_name,
            update_value,
            where_value
    ):
        pass
