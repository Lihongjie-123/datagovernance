import csv
import io
import json
import logging
from src.config.load_config_map import get_config_conf
from src.DataSource.neo_source import NeoSource


class NeoPreprocess(object):

    def __init__(self):
        self.config_map = get_config_conf()
        self.MATCH_ALL_NODE_LABEL = "MATCH (n) RETURN distinct labels(n)"
        self.MATCH_ALL_RELATIONSHIP_TYPE = \
            "match (n)-[r]-() return distinct type(r)"
        self.COUNT_NODE_BY_LABEL = "match (n:%s) return count(n)"
        self.COUNT_RELATIONSHIP_BY_TYPE = \
            "match (n)-[r:%s]->(m) return count(r)"
        self.MATCH_ATTR_BY_LABEL = "match (n:%s) return n limit 1"
        self.MATCH_ATTR_BY_TYPE = "match (n)-[r:%s]->(m) return r limit 1"

        self.MATCH_NODE_EXIST_CMD = \
            "match(n:%s{%s}) return n"
        self.CREATE_NODE_CMD = "create (n:%s{%s}) return n"
        self.CREATE_RELATION_SHIP_CMD = \
            "match (n:%s{%s})," \
            "(m:%s{%s}) create " \
            "(n)-[r:%s{%s}]->(m) return r"
        self.MATCH_RELATION_EXIST_CMD = \
            "match (n:%s{%s})-[r:%s]-(m:%s{%s}) where " \
            "%s RETURN r"
        self.UPDATE_NODE_ATTRS_CMD = \
            "MERGE (n:%s {%s}) SET n += {%s} RETURN n"
        self.UPDATE_RELATION_ATTRS_CMD = \
            "MATCH (n:%s {%s})-[r:%s]-(m:%s {%s}) SET %s Return r"
        self.DELETE_NODE_CMD = "match (n:%s{%s}) delete n"
        self.DELETE_RELATION_CMD = \
            "match (n:%s{%s})-[r:%s]-(m:%s{%s}) delete r"

    @staticmethod
    def init_format_json(sub_auth_url):
        return {
            "col_name": [],
            "dbName": "",
            "tableName": "",
            "numRows": "0",
            "totalSize": "0",
            "numAddedYesterday": "0",
            "numAddedlastWeek": "0",
            "lastUpdateTime": "",
            "createTime": "",
            "tableComment": "",
            "connect_url": sub_auth_url
        }

    def format_result_json(self, neo_source, sub_auth_url):
        final_result = []
        # 查询node相关信息
        neo_source.execute(self.MATCH_ALL_NODE_LABEL)
        all_node_label = neo_source.fetch_all()
        for sub_label_info in all_node_label:
            format_info_json = self.init_format_json(sub_auth_url)
            format_info_json["dbName"] = sub_auth_url
            format_info_json["tableName"] = \
                "%s.%s" % ("NODE", sub_label_info["labels(n)"][0])
            neo_source.execute(
                self.COUNT_NODE_BY_LABEL % sub_label_info["labels(n)"][0]
            )
            node_count = neo_source.fetch_all()
            format_info_json["numRows"] = node_count[0]["count(n)"]
            # 获取每个node 的属性，这里假设同一种label的node，属性相同
            neo_source.execute(
                self.MATCH_ATTR_BY_LABEL % sub_label_info["labels(n)"][0]
            )
            node_attrs = neo_source.fetch_all()[0]["n"].keys()
            for sub_attr in node_attrs:
                format_info_json["col_name"].append({
                    "attr_type": format_info_json["tableName"],
                    "attr_name": sub_attr,
                    "attr_comment": ""
                })
            final_result.append(format_info_json)
        # 查询relationship相关信息
        neo_source.execute(self.MATCH_ALL_RELATIONSHIP_TYPE)
        all_relation_type = neo_source.fetch_all()
        for sub_type in all_relation_type:
            format_info_json = self.init_format_json(sub_auth_url)
            format_info_json["dbName"] = sub_auth_url
            format_info_json["tableName"] = \
                "%s.%s" % ("RELATIONSHIP", sub_type["type(r)"])
            neo_source.execute(
                self.COUNT_RELATIONSHIP_BY_TYPE % sub_type["type(r)"]
            )
            relation_count = neo_source.fetch_all()
            format_info_json["numRows"] = relation_count[0]["count(r)"]

            neo_source.execute(
                self.MATCH_ATTR_BY_TYPE % sub_type["type(r)"]
            )
            relation_attrs = neo_source.fetch_all()[0]["r"].keys()
            for sub_attr in relation_attrs:
                format_info_json["col_name"].append({
                    "attr_type": format_info_json["tableName"],
                    "attr_name": sub_attr,
                    "attr_comment": ""
                })
            final_result.append(format_info_json)
        return final_result

    @staticmethod
    def _get_attr_info(type_name, node_msg):
        node_type = node_msg[type_name]
        attr_list = []
        for attr_name in node_msg["attrs"].keys():
            attr_list.append(
                "%s:'%s'" % (
                    attr_name,
                    node_msg["attrs"][attr_name]
                )
            )
        attr_value = ",".join(attr_list)
        return node_type, attr_value

    def format_match_node_exist_cmd(self, node_msg):
        return self.MATCH_NODE_EXIST_CMD % (
            self._get_attr_info("label_type", node_msg)
        )

    def format_create_node_cmd(self, node_msg):
        return self.CREATE_NODE_CMD % (
            self._get_attr_info("label_type", node_msg)
        )

    def format_create_relation_ship_cmd(
            self,
            row_info
    ):
        node1_info = self._get_attr_info("label_type", row_info[0])
        node2_info = self._get_attr_info("label_type", row_info[2])
        relation_info = self._get_attr_info("relation_type", row_info[1])
        return self.CREATE_RELATION_SHIP_CMD % (
            node1_info[0], node1_info[1],
            node2_info[0], node2_info[1],
            relation_info[0], relation_info[1]
        )

    def format_match_relation_exist_cmd(self, row_info):
        node1_info = self._get_attr_info("label_type", row_info[0])
        node2_info = self._get_attr_info("label_type", row_info[2])
        relation_type = row_info[1]["relation_type"]
        where_value = []
        for attr_info in row_info[1]["attrs"].keys():
            where_value.append(
                "r.%s='%s'" % (
                    attr_info,
                    row_info[1]["attrs"][attr_info]
                )
            )
        where_value = " and ".join(where_value)
        return self.MATCH_RELATION_EXIST_CMD % (
            node1_info[0], node1_info[1],
            relation_type,
            node2_info[0], node2_info[1],
            where_value
        )

    def one_data_to_neo(self, neo_source, row_info):
        # 检查该节点是否存在，如果不存在，则创建
        if not neo_source.graph.run(
                self.format_match_node_exist_cmd(row_info[0])).data():
            neo_source.graph.run(self.format_create_node_cmd(row_info[0]))
        # 检查该节点是否存在，如果不存在，则创建
        if not neo_source.graph.run(
                self.format_match_node_exist_cmd(row_info[2])).data():
            neo_source.graph.run(self.format_create_node_cmd(row_info[2]))
        # 创建两个节点的关系
        if not neo_source.graph.run(
                self.format_match_relation_exist_cmd(row_info)).data():
            neo_source.graph.run(
                self.format_create_relation_ship_cmd(row_info)
            )

    def data_content_to_db(self, db_name, _db_table, input_content, separator):
        """
        neo4j上传文本和文件内容，要有三列，node relation node
        且每一列都是一个json字符串，包含name 等一些属性
        :param db_name:
        :param _db_table:
        :param input_content:
        :param separator:
        :return:
        """
        try:
            if "," == separator:
                content_obj = csv.reader(io.StringIO(input_content))
            else:
                content_obj = \
                    [x.split(separator) for x in
                     [j for j in input_content.split("\n")]]

            data_list = [
                [json.loads(x[0]), json.loads(x[1]), json.loads(x[2])]
                for x in content_obj if [''] != x
            ]
            neo_source = NeoSource()
            if not self.config_map["neo_connect_urls"].__contains__(db_name):
                logging.error("input neo4j connect address is invaild.")
                return False
            neo_source.create_connection_auth(
                db_name,
                self.config_map["neo_usernames"][
                    self.config_map["neo_connect_urls"].index(db_name)],
                self.config_map["neo_passwords"][
                    self.config_map["neo_connect_urls"].index(db_name)],
            )
            for sub_info in data_list:
                self.one_data_to_neo(neo_source, sub_info)

            neo_source.commit()
            neo_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def update_node_attrs(self, neo_source, update_value, where_value):

        assert where_value.__getitem__("src_node").__contains__("label_type")
        assert where_value.__getitem__("src_node").__contains__("attrs")

        label_type = \
            update_value.__getitem__("update_obj_type")
        where_attrs = \
            ", ".join(
                [
                    "%s: '%s'" %
                    (
                        key,
                        where_value.__getitem__(
                            "src_node").__getitem__("attrs").__getitem__(key)
                    )
                    for key in
                    where_value.__getitem__("src_node").__getitem__("attrs")
                ]
            )
        update_attrs = \
            ", ".join(
                ["%s: '%s'" %
                 (key, update_value.__getitem__("update_value").__getitem__(key))  # nopep8
                 for key in update_value.__getitem__("update_value")]
            )
        exec_cmd = \
            self.UPDATE_NODE_ATTRS_CMD % (
                label_type, where_attrs, update_attrs
            )
        logging.info("update node attrs exec_cmd is %s" % exec_cmd)
        neo_source.execute(exec_cmd)
        neo_source.commit()

    def update_relation_attrs(self, neo_source, update_value, where_value):

        assert where_value.__getitem__("src_node").__contains__("label_type")
        assert where_value.__getitem__("src_node").__contains__("attrs")
        assert where_value.__getitem__("tgt_node").__contains__("label_type")
        assert where_value.__getitem__("tgt_node").__contains__("attrs")

        src_label_type = \
            where_value.__getitem__("src_node").__getitem__("label_type")
        src_where_attrs = \
            ", ".join(
                [
                    "%s: '%s'" %
                    (
                        key,
                        where_value.__getitem__(
                            "src_node").__getitem__("attrs").__getitem__(key)
                    )
                    for key in
                    where_value.__getitem__("src_node").__getitem__("attrs")
                ]
            )
        relation_type = update_value.__getitem__("update_obj_type")
        tgt_label_type = \
            where_value.__getitem__("tgt_node").__getitem__("label_type")
        tgt_where_attrs = \
            ", ".join(
                [
                    "%s: '%s'" %
                    (
                        key,
                        where_value.__getitem__(
                            "tgt_node").__getitem__("attrs").__getitem__(key)
                    )
                    for key in
                    where_value.__getitem__("tgt_node").__getitem__("attrs")
                ]
            )
        update_attrs = \
            ", ".join(
                [
                    "r.%s='%s'" % (
                        key,
                        update_value.__getitem__(
                            "update_value").__getitem__(key)
                    )
                    for key in
                    update_value.__getitem__("update_value")
                ]
            )

        exec_cmd = self.UPDATE_RELATION_ATTRS_CMD % (
            src_label_type,
            src_where_attrs,
            relation_type,
            tgt_label_type,
            tgt_where_attrs,
            update_attrs
        )
        logging.info("update relation attrs exec_cmd is %s" % exec_cmd)
        neo_source.execute(exec_cmd)
        neo_source.commit()

    def data_content_update(
            self,
            db_name,
            _table_name,
            update_value,
            where_value
    ):
        try:
            logging.info(update_value.__getitem__("update_value"))
            logging.info(bool(update_value.__getitem__("update_value")))
            # 先做入参检查
            assert all([
                self.config_map.__getitem__(
                    "neo_connect_urls").__contains__(db_name),
                where_value.__contains__("update_type"),
                bool(where_value.__getitem__("update_type")),
                ["Node", "RelationShip"].__contains__(
                    where_value.__getitem__("update_type")
                ),
                where_value.__contains__("src_node"),
                bool(where_value.__getitem__("src_node")),
                where_value.__contains__("tgt_node"),
                bool(where_value.__getitem__("tgt_node"))
                if "RelationShip".__eq__(
                    where_value.__getitem__("update_type"))
                else not bool(where_value.__getitem__("tgt_node")),
                update_value.__contains__("update_obj_type"),
                bool(update_value.__getitem__("update_obj_type")),
                update_value.__contains__("update_value"),
                bool(update_value.__getitem__("update_value"))
            ])

            logging.info("update_value is %s" % json.dumps(update_value))
            logging.info("where_value is %s" % json.dumps(where_value))
            neo_source = NeoSource()

            neo_source.create_connection_auth(
                db_name,
                self.config_map["neo_usernames"][
                    self.config_map["neo_connect_urls"].index(db_name)],
                self.config_map["neo_passwords"][
                    self.config_map["neo_connect_urls"].index(db_name)],
            )
            # 分类型做属性更新
            if "Node".__eq__(where_value.__getitem__("update_type")):
                self.update_node_attrs(
                    neo_source, update_value, where_value
                )
            else:
                self.update_relation_attrs(
                    neo_source, update_value, where_value
                )
            neo_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def delete_node(self, neo_source, where_value):
        label_type = \
            where_value.__getitem__(
                "src_node").__getitem__("label_type")
        where_attrs = \
            ", ".join(
                [
                    "%s: '%s'" %
                    (
                        key,
                        where_value.__getitem__(
                            "src_node").__getitem__("attrs").__getitem__(key)
                    )
                    for key in
                    where_value.__getitem__("src_node").__getitem__("attrs")
                ]
            )
        exec_cmd = self.DELETE_NODE_CMD % (
            label_type,
            where_attrs
        )
        logging.info("delete node exec_cmd is %s" % exec_cmd)
        neo_source.execute(exec_cmd)
        neo_source.commit()

    def delete_relation(self, neo_source, where_value):
        assert where_value.__getitem__("src_node").__contains__("label_type")
        assert where_value.__getitem__("src_node").__contains__("attrs")
        assert where_value.__getitem__("tgt_node").__contains__("label_type")
        assert where_value.__getitem__("tgt_node").__contains__("attrs")

        src_label_type = \
            where_value.__getitem__("src_node").__getitem__("label_type")
        src_where_attrs = \
            ", ".join(
                [
                    "%s: '%s'" %
                    (
                        key,
                        where_value.__getitem__(
                            "src_node").__getitem__("attrs").__getitem__(key)
                    )
                    for key in
                    where_value.__getitem__("src_node").__getitem__("attrs")
                ]
            )
        relation_type = where_value.__getitem__("delete_obj_type")
        tgt_label_type = \
            where_value.__getitem__("tgt_node").__getitem__("label_type")
        tgt_where_attrs = \
            ", ".join(
                [
                    "%s: '%s'" %
                    (
                        key,
                        where_value.__getitem__(
                            "tgt_node").__getitem__("attrs").__getitem__(key)
                    )
                    for key in
                    where_value.__getitem__("tgt_node").__getitem__("attrs")
                ]
            )

        exec_cmd = self.DELETE_RELATION_CMD % (
            src_label_type,
            src_where_attrs,
            relation_type,
            tgt_label_type,
            tgt_where_attrs,
        )
        logging.info("delete relation exec_cmd is %s" % exec_cmd)
        neo_source.execute(exec_cmd)
        neo_source.commit()

    def data_content_delete(
            self,
            db_name,
            _table_name,
            where_value
    ):
        try:
            # 先做入参检查
            assert all([
                self.config_map.__getitem__(
                    "neo_connect_urls").__contains__(db_name),
                where_value.__contains__("delete_type"),
                bool(where_value.__getitem__("delete_type")),
                ["Node", "RelationShip"].__contains__(
                    where_value.__getitem__("delete_type")
                ),
                where_value.__contains__("src_node"),
                bool(where_value.__getitem__("src_node")),
                where_value.__contains__("tgt_node"),
                bool(where_value.__getitem__("tgt_node"))
                if "RelationShip".__eq__(
                    where_value.__getitem__("delete_type"))
                else not bool(where_value.__getitem__("tgt_node")),
                where_value.__contains__("delete_obj_type")
            ])

            logging.info("where_value is %s" % json.dumps(where_value))
            neo_source = NeoSource()

            neo_source.create_connection_auth(
                db_name,
                self.config_map["neo_usernames"][
                    self.config_map["neo_connect_urls"].index(db_name)],
                self.config_map["neo_passwords"][
                    self.config_map["neo_connect_urls"].index(db_name)],
            )
            # 分类型做属性更新
            if "Node".__eq__(where_value.__getitem__("delete_type")):
                self.delete_node(
                    neo_source, where_value
                )
            else:
                self.delete_relation(
                    neo_source, where_value
                )
            neo_source.close()
            return True
        except Exception as e:
            logging.exception(e)
            return False
