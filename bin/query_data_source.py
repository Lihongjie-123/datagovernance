"""
定时查询hive、mysql、redis、es、neo4js，将查询结果入到mysql中
"""

import _load  # nopep8
import logging
import src.main.query_data_source as main


if __name__ == "__main__":
    try:
        main.main()
    except Exception as e:
        logging.exception(e)
        exit(-1)
