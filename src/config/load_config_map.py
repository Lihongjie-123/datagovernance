import configparser
import logging
import os

workdir = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))  # nopep8
if "lib" == os.path.basename(workdir):
    workdir = os.path.dirname(workdir)


def get_config_conf():
    try:
        config_map = {}
        config = configparser.ConfigParser()

        config.read(os.path.join(workdir,
                                 'etc', 'config.conf'),
                    encoding='utf-8')
        # hive 配置
        config_map["hive_jdbc_ip"] = \
            config.get('hive_setting', 'hive_jdbc_ip')
        config_map["hive_jdbc_port"] = \
            config.get('hive_setting', 'hive_jdbc_port')
        config_map["hive_ignore_databases"] = \
            config.get('hive_setting', 'hive_ignore_databases').split(",")
        config_map["hive_ignore_tables"] = \
            config.get('hive_setting', 'hive_ignore_tables').split(",")

        # redis 配置
        config_map["redis_server_hosts"] = \
            config.get('redis_setting', 'redis_server_hosts').split(",")
        config_map["redis_server_ports"] = \
            config.get('redis_setting', 'redis_server_ports').split(",")

        # mysql 配置
        config_map["mysql_ip"] = \
            config.get('mysql_setting', 'mysql_ip')
        config_map["mysql_username"] = \
            config.get('mysql_setting', 'mysql_username')
        config_map["mysql_password"] = \
            config.get('mysql_setting', 'mysql_password')
        config_map["mysql_database"] = \
            config.get('mysql_setting', 'mysql_database')
        config_map["mysql_ignore_databases"] = \
            config.get('mysql_setting', 'mysql_ignore_databases').split(",")
        config_map["mysql_ignore_tables"] = \
            config.get('mysql_setting', 'mysql_ignore_tables').split(",")
        config_map["mysql_cache_database"] = \
            config.get('mysql_setting', 'mysql_cache_database')

        # ES 配置
        config_map["es_server_hosts"] = \
            config.get('es_setting', 'es_server_hosts').split(",")
        config_map["es_server_port"] = \
            config.get('es_setting', 'es_server_port')

        # neo4j 配置
        config_map["neo_connect_urls"] = \
            config.get('neo4j_setting', 'neo_connect_urls').split(",")
        config_map["neo_usernames"] = \
            config.get('neo4j_setting', 'neo_usernames').split(",")
        config_map["neo_passwords"] = \
            config.get('neo4j_setting', 'neo_passwords').split(",")

        # presto 配置
        config_map["presto_server_ip"] = \
            config.get('presto_setting', 'presto_server_ip')
        config_map["presto_server_port"] = \
            config.get('presto_setting', 'presto_server_port')

        # other 配置
        config_map["django_server_ip"] = \
            config.get('other_setting', 'django_server_ip')
        config_map["django_server_port"] = \
            config.get('other_setting', 'django_server_port')
        config_map["statistics_data_db_name"] = \
            config.get('other_setting', 'statistics_data_db_name')
        config_map["statistics_data_table_name"] = \
            config.get('other_setting', 'statistics_data_table_name')
        config_map["allowed_hosts"] = \
            config.get('other_setting', 'allowed_hosts').split(",")

        return config_map
    except Exception as exception:
        logging.exception(exception)
        exit(-1)
