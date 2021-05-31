import logging
import threading

from src.ErrorCenter.error_center import ErrorCenter


class CommonUtils(object):
    """
    一些通用函数,单例模式
    """

    _instance_lock = threading.Lock()

    def __init__(self):
        # 查询mysql缓存数据的sql模板
        self.MYSQL_CACHE_DATA_SELECT_SQL = \
            "select data from %s.%s where interface_type='%s' " \
            "order by import_time desc limit 1"

    def __new__(cls, *args, **kwargs):
        if not hasattr(CommonUtils, "_instance"):
            with CommonUtils._instance_lock:
                CommonUtils._instance = \
                    super(CommonUtils, cls).__new__(cls, *args, **kwargs)
        return CommonUtils._instance

    @staticmethod
    def format_df(select_df):
        """
        df to json
        :param select_df:
        :return:
        """
        select_result = {
            "select_result": []
        }
        select_dict = select_df.to_dict()
        select_data_keys = list(select_dict.keys())
        select_result["select_result"].append(select_data_keys)
        for i in range(len(select_dict[select_data_keys[0]])):
            tmp_list = []
            for key in select_data_keys:
                tmp_list.append(
                    select_dict[key][i]
                )
            select_result["select_result"].append(tmp_list)
        return select_result

    @staticmethod
    def check_params(field_name, field_value):
        if field_value:
            logging.info("field %s value is %s" % (field_name, field_value))
            return True
        else:
            logging.error(ErrorCenter.FIELD_IS_EMPTY.value % field_name)
            return False
