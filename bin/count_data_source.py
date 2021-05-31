"""
定时统计对接数据源中的数据入库条数信息，入到redis中
目前统计前一天入库量和最近一周入库量
"""
import _load  # nopep8
import logging
import src.main.count_data_source as main


if __name__ == "__main__":
    try:
        main.main()
    except Exception as e:
        logging.exception(e)
        exit(-1)
