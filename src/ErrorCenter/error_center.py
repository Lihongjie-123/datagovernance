from enum import Enum


class ErrorCenter(Enum):
    # 创建数据源连接失败
    CREATE_DATA_SOURCE_CONNECT_FAILED = \
        " create [ %s ] data source connect failed."
    # 执行sql失败
    EXEC_SQL_FAILED = "[ %s ] execute sql failed."
    # 未初始化变量
    VARIABLE_NOT_INITIAL_ERROR = "variable [ %s ] not be init."
    # 获取执行结果失败
    FETCH_EXEC_RESULT_FAILED = "get [ %s ] execute result failed."
    # 关闭数据库连接失败
    CLOSE_DB_CONNECT_FAILED = "close [ %s ] connection failed."
    # 某个输入参数为空
    INPUT_PARAMS_WHICH_IS_EMPTY = \
        "input parameters which is None or empty,please check it."
    # 字段为空
    FIELD_IS_EMPTY = "field %s value is None or empty."
    # 输入的参数并非json格式的字符串
    VALUE_IS_NOT_JSON_STYLE = \
        "UpdateValue and WhereValue should be a json style,please check it."
    # 更新数据到数据库失败
    UPDATE_DATA_TO_DB_FAILED = "update %s %s.%s data failed"
    # 删除数据到数据库失败
    DELETE_DATA_TO_DB_FAILED = "delete %s %s.%s data failed"
    # 添加数据到数据库失败
    ADD_DATA_TO_DB_FAILED = "add %s %s.%s data failed"
    # 没有使用POST方法
    NOT_USE_POST_METHOD = "please use POST method."
    # 输入的文本为空
    CONTENT_IS_NONE_OR_EMPTY = "input content is None or empty."
    # ES更新数据接口调用，传过来的条件参数里没有_id字段
    ES_UPDATE_NOT_SET__ID = "ES update where value must set _id "
    # REDIS更新数据接口调用，传过来的条件参数里没有_id字段
    REDIS_UPDATE_NOT_SET_NAME_KEY = \
        "REDIS update where value must set name and key"
