# DataGovernance

数据治理相关

# 依赖环境：
	hdp3.x
	ElasticSearch
	Redis
	Neo4j
	Apache Presto





# 接口说明

## 实时查询接口

### 数据源摘要数据查询接口

- 接口说明：

  ```
  用于实时查询对接的hive、mysql、elasticsearch、redis、neo4j五种数据源的相关摘要数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  AbstractDataMap
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/AbstractDataMap"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "hive_abstract_data": [
      {
        "dbName": "fake_db",
        "tableName": "fake_copy_table_1",
        "numRows": "100",
        "totalSize": "8.031(KB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-19 11:25:30",
        "createTime": "2021-01-19 11:25:30",
        "tableComment": ""
      }
    ],
    "mysql_abstract_data": [
      {
        "dbName": "mysql_test_db",
        "tableName": "mysql_test_table",
        "numRows": 30003,
        "totalSize": "5.264(MB)",
        "numAddedYesterday": 0,
        "numAddedlastWeek": 0,
        "lastUpdateTime": "2021-02-07 17:25:54",
        "createTime": "2021-01-21 17:45:13",
        "tableComment": "the test table in mysql"
      }
    ],
    "redis_abstract_data": [
      {
        "dbName": "",
        "tableName": "",
        "numRows": "28",
        "totalSize": "15.296(MB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ],
    "es_abstract_data": [
      {
        "dbName": "",
        "tableName": "es_test_index",
        "numRows": "325021",
        "totalSize": "72.7mb",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "2021-01-22T08:42:16.198Z",
        "tableComment": ""
      }
    ],
    "neo_abstract_data": [
      {
        "dbName": "bolt://172.28.128.16:7687",
        "tableName": "NODE.Person",
        "numRows": 200,
        "totalSize": "0",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  - 无

- 接口调用返回字段说明：

  - hive_abstract_data： 和hive数据库相关的摘要信息
    - dbName： 数据库名称
    - tableName： 数据表名称
    - numRows： 数据总量
    - totalSize： 占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述
  - mysql_abstract_data： 和mysql数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**
  - redis_abstract_data： 和redis数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**
  - es_abstract_data： 和ElasticSearch数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**
  - neo_abstract_data： 和neo4j数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**

### Hive数据地图查询接口

- 接口说明：

  ```
  用于实时查询对接的hive数据源的相关摘要数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  HiveDataMap
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/HiveDataMap"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "hive_source": [
      {
        "col_name": [
          {
            "col_name": "name",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "cardno",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "moblie",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "company",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "location",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "import_time",
            "col_type": "string",
            "col_comment": "from deserializer"
          }
        ],
        "DetailedTableInformation": {
          "Database": [
            {
              "data_type": "fake_db_1",
              "comment": ""
            }
          ],
          "OwnerType": [
            {
              "data_type": "USER",
              "comment": ""
            }
          ],
          "Owner": [
            {
              "data_type": "root",
              "comment": ""
            }
          ],
          "CreateTime": [
            {
              "data_type": "Thu Jan 21 15:07:16 CST 2021",
              "comment": ""
            }
          ],
          "LastAccessTime": [
            {
              "data_type": "UNKNOWN",
              "comment": ""
            }
          ],
          "Retention": [
            {
              "data_type": "0",
              "comment": ""
            }
          ],
          "Location": [
            {
              "data_type": "hdfs://master.ambari3.0.com:8020/warehouse/tablespace/managed/hive/fake_db_1.db/fake_table_import_time",
              "comment": ""
            }
          ],
          "TableType": [
            {
              "data_type": "MANAGED_TABLE",
              "comment": ""
            }
          ],
          "TableParameters": [
            {
              "data_type": "COLUMN_STATS_ACCURATE",
              "comment": "{\\\"BASIC_STATS\\\":\\\"true\\\",\\\"COLUMN_STATS\\\":{\\\"cardno\\\":\\\"true\\\",\\\"company\\\":\\\"true\\\",\\\"import_time\\\":\\\"true\\\",\\\"location\\\":\\\"true\\\",\\\"moblie\\\":\\\"true\\\",\\\"name\\\":\\\"true\\\"}}"
            },
            {
              "data_type": "bucketing_version",
              "comment": "2"
            },
            {
              "data_type": "comment",
              "comment": "?????"
            },
            {
              "data_type": "numFiles",
              "comment": "0"
            },
            {
              "data_type": "numRows",
              "comment": "0"
            },
            {
              "data_type": "rawDataSize",
              "comment": "0"
            },
            {
              "data_type": "totalSize",
              "comment": "0"
            },
            {
              "data_type": "transactional",
              "comment": "true"
            },
            {
              "data_type": "transactional_properties",
              "comment": "insert_only"
            },
            {
              "data_type": "transient_lastDdlTime",
              "comment": "1611212836"
            }
          ]
        },
        "StorageInformation": {
          "SerDeLibrary": [
            {
              "data_type": "org.apache.hadoop.hive.serde2.OpenCSVSerde",
              "comment": ""
            }
          ],
          "InputFormat": [
            {
              "data_type": "org.apache.hadoop.mapred.TextInputFormat",
              "comment": ""
            }
          ],
          "OutputFormat": [
            {
              "data_type": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
              "comment": ""
            }
          ],
          "Compressed": [
            {
              "data_type": "No",
              "comment": ""
            }
          ],
          "NumBuckets": [
            {
              "data_type": "-1",
              "comment": ""
            }
          ],
          "BucketColumns": [
            {
              "data_type": "[]",
              "comment": ""
            }
          ],
          "SortColumns": [
            {
              "data_type": "[]",
              "comment": ""
            }
          ],
          "StorageDescParams": [
            {
              "data_type": "escapeChar",
              "comment": "\\\\"}, {"data_type": "quoteChar", "comment": "\\\""
            },
            {
              "data_type": "separatorChar",
              "comment": ","
            },
            {
              "data_type": "serialization.format",
              "comment": "1"
            }
          ]
        },
        "dbName": "fake_db_1",
        "tableName": "fake_table_import_time",
        "numRows": "0",
        "totalSize": "0(B)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-21 15:07:16",
        "createTime": "2021-01-21 15:07:16",
        "tableComment": "?????",
        "table_name": "fake_db_1.fake_table_import_time"
      }
    ],
    "abstract_data": [
      {
        "dbName": "fake_db_1",
        "tableName": "fake_table_import_time",
        "numRows": "0",
        "totalSize": "0(B)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-21 15:07:16",
        "createTime": "2021-01-21 15:07:16",
        "tableComment": "?????"
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - hive_source： hive数据库中每张表的详细信息，包含每张表的字段信息、表详细信息、表存储信息
    - col_name： 表字段信息
    - DetailedTableInformation： 表详细信息
    - StorageInformation： 表存储信息
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述
    - table_name： 完整表名
  - abstract_data： hive数据库中每张表的摘要信息，包含数据库名、数据表名、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述

### Mysql数据地图查询接口

- 接口说明：

  ```
  用于实时查询对接的Mysql数据源的相关摘要数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  MysqlDataMap
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/MysqlDataMap"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "mysql_source": [
      {
        "col_name": [
          {
            "col_name": "_id",
            "col_type": "varchar(100)",
            "col_comment": ""
          },
          {
            "col_name": "name",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "cardno",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "mobile",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "company",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "address",
            "col_type": "longtext",
            "col_comment": ""
          },
          {
            "col_name": "import_time",
            "col_type": "text",
            "col_comment": ""
          }
        ],
        "index_information": [
          
        ],
        "detail_information": [
          {
            "infoType": "DetailInformation",
            "infoField": "table_catalog",
            "infoValue": "def"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_schema",
            "infoValue": "mysql_test_db"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_name",
            "infoValue": "test_tabl_2"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_type",
            "infoValue": "BASE TABLE"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "engine",
            "infoValue": "InnoDB"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "version",
            "infoValue": 10
          },
          {
            "infoType": "DetailInformation",
            "infoField": "row_format",
            "infoValue": "Compact"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_rows",
            "infoValue": 6
          },
          {
            "infoType": "DetailInformation",
            "infoField": "avg_row_length",
            "infoValue": 2730
          },
          {
            "infoType": "DetailInformation",
            "infoField": "data_length",
            "infoValue": 16384
          },
          {
            "infoType": "DetailInformation",
            "infoField": "max_data_length",
            "infoValue": 0
          },
          {
            "infoType": "DetailInformation",
            "infoField": "index_length",
            "infoValue": 0
          },
          {
            "infoType": "DetailInformation",
            "infoField": "data_free",
            "infoValue": 10485760
          },
          {
            "infoType": "DetailInformation",
            "infoField": "auto_increment",
            "infoValue": null
          },
          {
            "infoType": "DetailInformation",
            "infoField": "create_time",
            "infoValue": "2021-01-21 16:08:57"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "update_time",
            "infoValue": ""
          },
          {
            "infoType": "DetailInformation",
            "infoField": "check_time",
            "infoValue": ""
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_collation",
            "infoValue": "utf8_general_ci"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "checksum",
            "infoValue": null
          },
          {
            "infoType": "DetailInformation",
            "infoField": "create_options",
            "infoValue": ""
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_comment",
            "infoValue": ""
          }
        ],
        "dbName": "mysql_test_db",
        "tableName": "test_tabl_2",
        "numRows": 6,
        "totalSize": "16.0(KB)",
        "numAddedYesterday": 0,
        "numAddedlastWeek": 0,
        "lastUpdateTime": "",
        "createTime": "2021-01-21 16:08:57",
        "tableComment": "",
        "table_name": "mysql_test_db.test_tabl_2"
      }
    ],
    "abstract_data": [
      {
        "dbName": "mysql_test_db",
        "tableName": "test_tabl_2",
        "numRows": 6,
        "totalSize": "16.0(KB)",
        "numAddedYesterday": 0,
        "numAddedlastWeek": 0,
        "lastUpdateTime": "",
        "createTime": "2021-01-21 16:08:57",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - mysql_source： mysql数据库中每张表的详细信息，包含字段信息、索引信息、表详细信息、数据库名、数据表名、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述、完整表名
    - col_name： 表字段信息
    - index_information： 表索引信息
    - detail_information： 表详细信息
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述
    - table_name： 完整表名
  - abstract_data： mysql数据库中每张表的摘要信息，包含数据库名、数据表名、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述

### ES数据地图查询接口

- 接口说明：

  ```
  用于实时查询对接的ES数据源的相关摘要数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、索引描述等
  ```

- 接口地址： 

  ```
  ESDataMap
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/ESDataMap"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "es_source": [
      {
        "col_name": [
          {
            "col_name": "uuid",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "name",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "ssn",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "phone_number",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "company",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "address",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "import_time",
            "col_type": "date",
            "col_comment": ""
          }
        ],
        "detail_information": [
          {
            "index_name": "es_test_index_2",
            "info_field": "health",
            "info_value": "yellow"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "status",
            "info_value": "open"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "index",
            "info_value": "es_test_index_2"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "uuid",
            "info_value": "y42mwJBRQ0SPqoaZRMptyg"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "pri",
            "info_value": "1"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "rep",
            "info_value": "1"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "docs.count",
            "info_value": "38141"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "docs.deleted",
            "info_value": "1"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "store.size",
            "info_value": "8.8mb"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "pri.store.size",
            "info_value": "8.8mb"
          }
        ],
        "dbName": "",
        "tableName": "es_test_index_2",
        "numRows": "38141",
        "totalSize": "8.8mb",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-26T14:19:04.000Z",
        "createTime": "2021-01-25T09:00:05.243Z",
        "tableComment": "",
        "table_name": "es_test_index_2"
      }
    ],
    "abstract_data": [
      {
        "dbName": "",
        "tableName": "es_test_index_2",
        "numRows": "38141",
        "totalSize": "8.8mb",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-26T14:19:04.000Z",
        "createTime": "2021-01-25T09:00:05.243Z",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - es_source： ElasticSearch数据库中每个索引的详细信息，包含字段信息、索引详细信息、数据库名、索引名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、索引描述、完整索引名称
    - col_name： 索引字段信息
    - detail_information： 索引详细信息
    - dbName： 数据库名
    - tableName： 索引名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 索引描述
    - table_name： 完整索引名称
  - abstract_data： ElasticSearch数据库中每个索引的摘要信息，包含数据库名、索引名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 索引名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 索引描述

### Redis数据地图查询接口

- 接口说明：

  ```
  用于实时查询对接的Redis数据源的相关摘要数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  RedisDataMap
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/RedisDataMap"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "redis_source": [
      {
        "resource_check": [
          {
            "clusterNode": "172.28.128.17:6381",
            "resourceField": "redis_version",
            "resourceValue": "6.0.8"
          },
        ],
        "dbName": "",
        "tableName": "",
        "numRows": "28",
        "totalSize": "15.296(MB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": "",
        "table_name": ""
      }
    ],
    "abstract_data": [
      {
        "dbName": "",
        "tableName": "",
        "numRows": "28",
        "totalSize": "15.296(MB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - redis_source： Redis数据库中每个索引的详细信息，包含字段信息、数据源详细信息、数据库名、数据表名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、数据表描述、完整数据表名称
    - resource_check：数据源详细信息，**这个字段会很多，并且会把每个redis节点的详细信息都返回，接口文档例子中只保留了一个字段**
    - dbName： 数据库名
    - tableName： 数据表名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述
    - table_name： 完整数据表名称
  - abstract_data： Redis数据库中每个索引的摘要信息，包含数据库名、数据表名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 数据表名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述

### Neo4j数据地图查询接口

- 接口说明：

  ```
  用于实时查询对接的Neo4j数据源的相关摘要数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  NeoDataMap
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/NeoDataMap"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "neo_source": [
      {
        "col_name": [
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "end_time",
            "attr_comment": ""
          },
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "begin_time",
            "attr_comment": ""
          },
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "payroll",
            "attr_comment": ""
          },
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "job",
            "attr_comment": ""
          }
        ],
        "dbName": "bolt://172.28.128.16:7687",
        "tableName": "RELATIONSHIP.\u5408\u4f5c",
        "numRows": 10,
        "totalSize": "0",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": "",
        "connect_url": "bolt://172.28.128.16:7687"
      }
    ],
    "abstract_data": [
      {
        "dbName": "bolt://172.28.128.16:7687",
        "tableName": "RELATIONSHIP.\u5408\u4f5c",
        "numRows": 10,
        "totalSize": "0",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - neo_source： Neo4j数据库中每个索引的详细信息，包含字段信息、数据源详细信息、数据库名、数据表名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、数据表描述、完整数据表名称
    - col_name：节点或边的属性列表
    - dbName： neo4j图数据库连接地址
    - tableName： 节点或边的完整名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述
    - connect_url：neo4j图数据库连接地址
  - abstract_data： Redis数据库中每个索引的摘要信息，包含neo4j图数据库连接地址、节点或边的完整名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： neo4j图数据库连接地址
    - tableName：节点或边的完整名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述

## 缓存查询接口

### 数据源摘要数据缓存查询接口

- 接口说明：

  ```
  用于查询对接的hive、mysql、elasticsearch、redis、neo4j五种数据源的相关摘要缓存数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  AbstractDataMapCache
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/AbstractDataMapCache"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "hive_abstract_data": [
      {
        "dbName": "fake_db",
        "tableName": "fake_copy_table_1",
        "numRows": "100",
        "totalSize": "8.031(KB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-19 11:25:30",
        "createTime": "2021-01-19 11:25:30",
        "tableComment": ""
      }
    ],
    "mysql_abstract_data": [
      {
        "dbName": "mysql_test_db",
        "tableName": "mysql_test_table",
        "numRows": 30003,
        "totalSize": "5.264(MB)",
        "numAddedYesterday": 0,
        "numAddedlastWeek": 0,
        "lastUpdateTime": "2021-02-07 17:25:54",
        "createTime": "2021-01-21 17:45:13",
        "tableComment": "the test table in mysql"
      }
    ],
    "redis_abstract_data": [
      {
        "dbName": "",
        "tableName": "",
        "numRows": "28",
        "totalSize": "15.296(MB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ],
    "es_abstract_data": [
      {
        "dbName": "",
        "tableName": "es_test_index",
        "numRows": "325021",
        "totalSize": "72.7mb",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "2021-01-22T08:42:16.198Z",
        "tableComment": ""
      }
    ],
    "neo_abstract_data": [
      {
        "dbName": "bolt://172.28.128.16:7687",
        "tableName": "NODE.Person",
        "numRows": 200,
        "totalSize": "0",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  - 无

- 接口调用返回字段说明：

  - hive_abstract_data： 和hive数据库相关的摘要信息
    - dbName： 数据库名称
    - tableName： 数据表名称
    - numRows： 数据总量
    - totalSize： 占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述
  - mysql_abstract_data： 和mysql数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**
  - redis_abstract_data： 和redis数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**
  - es_abstract_data： 和ElasticSearch数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**
  - neo_abstract_data： 和neo4j数据库相关的摘要信息，其下字段解释参考**hive_abstract_data**

### Hive数据地图缓存查询接口

- 接口说明：

  ```
  用于查询对接的hive数据源的相关摘要缓存数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  HiveDataMapCache
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/HiveDataMapCache"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "hive_source": [
      {
        "col_name": [
          {
            "col_name": "name",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "cardno",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "moblie",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "company",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "location",
            "col_type": "string",
            "col_comment": "from deserializer"
          },
          {
            "col_name": "import_time",
            "col_type": "string",
            "col_comment": "from deserializer"
          }
        ],
        "DetailedTableInformation": {
          "Database": [
            {
              "data_type": "fake_db_1",
              "comment": ""
            }
          ],
          "OwnerType": [
            {
              "data_type": "USER",
              "comment": ""
            }
          ],
          "Owner": [
            {
              "data_type": "root",
              "comment": ""
            }
          ],
          "CreateTime": [
            {
              "data_type": "Thu Jan 21 15:07:16 CST 2021",
              "comment": ""
            }
          ],
          "LastAccessTime": [
            {
              "data_type": "UNKNOWN",
              "comment": ""
            }
          ],
          "Retention": [
            {
              "data_type": "0",
              "comment": ""
            }
          ],
          "Location": [
            {
              "data_type": "hdfs://master.ambari3.0.com:8020/warehouse/tablespace/managed/hive/fake_db_1.db/fake_table_import_time",
              "comment": ""
            }
          ],
          "TableType": [
            {
              "data_type": "MANAGED_TABLE",
              "comment": ""
            }
          ],
          "TableParameters": [
            {
              "data_type": "COLUMN_STATS_ACCURATE",
              "comment": "{\\\"BASIC_STATS\\\":\\\"true\\\",\\\"COLUMN_STATS\\\":{\\\"cardno\\\":\\\"true\\\",\\\"company\\\":\\\"true\\\",\\\"import_time\\\":\\\"true\\\",\\\"location\\\":\\\"true\\\",\\\"moblie\\\":\\\"true\\\",\\\"name\\\":\\\"true\\\"}}"
            },
            {
              "data_type": "bucketing_version",
              "comment": "2"
            },
            {
              "data_type": "comment",
              "comment": "?????"
            },
            {
              "data_type": "numFiles",
              "comment": "0"
            },
            {
              "data_type": "numRows",
              "comment": "0"
            },
            {
              "data_type": "rawDataSize",
              "comment": "0"
            },
            {
              "data_type": "totalSize",
              "comment": "0"
            },
            {
              "data_type": "transactional",
              "comment": "true"
            },
            {
              "data_type": "transactional_properties",
              "comment": "insert_only"
            },
            {
              "data_type": "transient_lastDdlTime",
              "comment": "1611212836"
            }
          ]
        },
        "StorageInformation": {
          "SerDeLibrary": [
            {
              "data_type": "org.apache.hadoop.hive.serde2.OpenCSVSerde",
              "comment": ""
            }
          ],
          "InputFormat": [
            {
              "data_type": "org.apache.hadoop.mapred.TextInputFormat",
              "comment": ""
            }
          ],
          "OutputFormat": [
            {
              "data_type": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
              "comment": ""
            }
          ],
          "Compressed": [
            {
              "data_type": "No",
              "comment": ""
            }
          ],
          "NumBuckets": [
            {
              "data_type": "-1",
              "comment": ""
            }
          ],
          "BucketColumns": [
            {
              "data_type": "[]",
              "comment": ""
            }
          ],
          "SortColumns": [
            {
              "data_type": "[]",
              "comment": ""
            }
          ],
          "StorageDescParams": [
            {
              "data_type": "escapeChar",
              "comment": "\\\\"}, {"data_type": "quoteChar", "comment": "\\\""
            },
            {
              "data_type": "separatorChar",
              "comment": ","
            },
            {
              "data_type": "serialization.format",
              "comment": "1"
            }
          ]
        },
        "dbName": "fake_db_1",
        "tableName": "fake_table_import_time",
        "numRows": "0",
        "totalSize": "0(B)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-21 15:07:16",
        "createTime": "2021-01-21 15:07:16",
        "tableComment": "?????",
        "table_name": "fake_db_1.fake_table_import_time"
      }
    ],
    "abstract_data": [
      {
        "dbName": "fake_db_1",
        "tableName": "fake_table_import_time",
        "numRows": "0",
        "totalSize": "0(B)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-21 15:07:16",
        "createTime": "2021-01-21 15:07:16",
        "tableComment": "?????"
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - hive_source： hive数据库中每张表的详细信息，包含每张表的字段信息、表详细信息、表存储信息
    - col_name： 表字段信息
    - DetailedTableInformation： 表详细信息
    - StorageInformation： 表存储信息
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述
    - table_name： 完整表名
  - abstract_data： hive数据库中每张表的摘要信息，包含数据库名、数据表名、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述

### Mysql数据地图缓存查询接口

- 接口说明：

  ```
  用于查询对接的Mysql数据源的相关摘要缓存数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  MysqlDataMapCache
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/MysqlDataMapCache"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "mysql_source": [
      {
        "col_name": [
          {
            "col_name": "_id",
            "col_type": "varchar(100)",
            "col_comment": ""
          },
          {
            "col_name": "name",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "cardno",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "mobile",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "company",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "address",
            "col_type": "longtext",
            "col_comment": ""
          },
          {
            "col_name": "import_time",
            "col_type": "text",
            "col_comment": ""
          }
        ],
        "index_information": [
          
        ],
        "detail_information": [
          {
            "infoType": "DetailInformation",
            "infoField": "table_catalog",
            "infoValue": "def"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_schema",
            "infoValue": "mysql_test_db"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_name",
            "infoValue": "test_tabl_2"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_type",
            "infoValue": "BASE TABLE"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "engine",
            "infoValue": "InnoDB"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "version",
            "infoValue": 10
          },
          {
            "infoType": "DetailInformation",
            "infoField": "row_format",
            "infoValue": "Compact"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_rows",
            "infoValue": 6
          },
          {
            "infoType": "DetailInformation",
            "infoField": "avg_row_length",
            "infoValue": 2730
          },
          {
            "infoType": "DetailInformation",
            "infoField": "data_length",
            "infoValue": 16384
          },
          {
            "infoType": "DetailInformation",
            "infoField": "max_data_length",
            "infoValue": 0
          },
          {
            "infoType": "DetailInformation",
            "infoField": "index_length",
            "infoValue": 0
          },
          {
            "infoType": "DetailInformation",
            "infoField": "data_free",
            "infoValue": 10485760
          },
          {
            "infoType": "DetailInformation",
            "infoField": "auto_increment",
            "infoValue": null
          },
          {
            "infoType": "DetailInformation",
            "infoField": "create_time",
            "infoValue": "2021-01-21 16:08:57"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "update_time",
            "infoValue": ""
          },
          {
            "infoType": "DetailInformation",
            "infoField": "check_time",
            "infoValue": ""
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_collation",
            "infoValue": "utf8_general_ci"
          },
          {
            "infoType": "DetailInformation",
            "infoField": "checksum",
            "infoValue": null
          },
          {
            "infoType": "DetailInformation",
            "infoField": "create_options",
            "infoValue": ""
          },
          {
            "infoType": "DetailInformation",
            "infoField": "table_comment",
            "infoValue": ""
          }
        ],
        "dbName": "mysql_test_db",
        "tableName": "test_tabl_2",
        "numRows": 6,
        "totalSize": "16.0(KB)",
        "numAddedYesterday": 0,
        "numAddedlastWeek": 0,
        "lastUpdateTime": "",
        "createTime": "2021-01-21 16:08:57",
        "tableComment": "",
        "table_name": "mysql_test_db.test_tabl_2"
      }
    ],
    "abstract_data": [
      {
        "dbName": "mysql_test_db",
        "tableName": "test_tabl_2",
        "numRows": 6,
        "totalSize": "16.0(KB)",
        "numAddedYesterday": 0,
        "numAddedlastWeek": 0,
        "lastUpdateTime": "",
        "createTime": "2021-01-21 16:08:57",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - mysql_source： mysql数据库中每张表的详细信息，包含字段信息、索引信息、表详细信息、数据库名、数据表名、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述、完整表名
    - col_name： 表字段信息
    - index_information： 表索引信息
    - detail_information： 表详细信息
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述
    - table_name： 完整表名
  - abstract_data： mysql数据库中每张表的摘要信息，包含数据库名、数据表名、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 数据表名
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 表描述

### ES数据地图缓存查询接口

- 接口说明：

  ```
  用于查询对接的ES数据源的相关摘要缓存数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、索引描述等
  ```

- 接口地址： 

  ```
  ESDataMapCache
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/ESDataMapCache"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "es_source": [
      {
        "col_name": [
          {
            "col_name": "uuid",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "name",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "ssn",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "phone_number",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "company",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "address",
            "col_type": "text",
            "col_comment": ""
          },
          {
            "col_name": "import_time",
            "col_type": "date",
            "col_comment": ""
          }
        ],
        "detail_information": [
          {
            "index_name": "es_test_index_2",
            "info_field": "health",
            "info_value": "yellow"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "status",
            "info_value": "open"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "index",
            "info_value": "es_test_index_2"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "uuid",
            "info_value": "y42mwJBRQ0SPqoaZRMptyg"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "pri",
            "info_value": "1"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "rep",
            "info_value": "1"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "docs.count",
            "info_value": "38141"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "docs.deleted",
            "info_value": "1"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "store.size",
            "info_value": "8.8mb"
          },
          {
            "index_name": "es_test_index_2",
            "info_field": "pri.store.size",
            "info_value": "8.8mb"
          }
        ],
        "dbName": "",
        "tableName": "es_test_index_2",
        "numRows": "38141",
        "totalSize": "8.8mb",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-26T14:19:04.000Z",
        "createTime": "2021-01-25T09:00:05.243Z",
        "tableComment": "",
        "table_name": "es_test_index_2"
      }
    ],
    "abstract_data": [
      {
        "dbName": "",
        "tableName": "es_test_index_2",
        "numRows": "38141",
        "totalSize": "8.8mb",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "2021-01-26T14:19:04.000Z",
        "createTime": "2021-01-25T09:00:05.243Z",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - es_source： ElasticSearch数据库中每个索引的详细信息，包含字段信息、索引详细信息、数据库名、索引名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、索引描述、完整索引名称
    - col_name： 索引字段信息
    - detail_information： 索引详细信息
    - dbName： 数据库名
    - tableName： 索引名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 索引描述
    - table_name： 完整索引名称
  - abstract_data： ElasticSearch数据库中每个索引的摘要信息，包含数据库名、索引名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 索引名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 索引描述

### Redis数据地图缓存查询接口

- 接口说明：

  ```
  用于查询对接的Redis数据源的相关摘要缓存数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  RedisDataMapCache
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/RedisDataMapCache"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "redis_source": [
      {
        "resource_check": [
          {
            "clusterNode": "172.28.128.17:6381",
            "resourceField": "redis_version",
            "resourceValue": "6.0.8"
          },
        ],
        "dbName": "",
        "tableName": "",
        "numRows": "28",
        "totalSize": "15.296(MB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": "",
        "table_name": ""
      }
    ],
    "abstract_data": [
      {
        "dbName": "",
        "tableName": "",
        "numRows": "28",
        "totalSize": "15.296(MB)",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - redis_source： Redis数据库中每个索引的详细信息，包含字段信息、数据源详细信息、数据库名、数据表名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、数据表描述、完整数据表名称
    - resource_check：数据源详细信息，**这个字段会很多，并且会把每个redis节点的详细信息都返回，接口文档例子中只保留了一个字段**
    - dbName： 数据库名
    - tableName： 数据表名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述
    - table_name： 完整数据表名称
  - abstract_data： Redis数据库中每个索引的摘要信息，包含数据库名、数据表名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： 数据库名
    - tableName： 数据表名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述

### Neo4j数据地图缓存查询接口

- 接口说明：

  ```
  用于查询对接的Neo4j数据源的相关摘要缓存数据，如数据总量、数据占用空间、昨日新增数据量、最近一周新增数据量、最近更新时间、表描述等
  ```

- 接口地址： 

  ```
  NeoDataMapCache
  ```

- 接口类型：

  ```
  GET
  ```

- 接口参数：

  ```
  无
  ```

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/NeoDataMapCache"
  req = requests.get(url)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "neo_source": [
      {
        "col_name": [
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "end_time",
            "attr_comment": ""
          },
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "begin_time",
            "attr_comment": ""
          },
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "payroll",
            "attr_comment": ""
          },
          {
            "attr_type": "RELATIONSHIP.\u5408\u4f5c",
            "attr_name": "job",
            "attr_comment": ""
          }
        ],
        "dbName": "bolt://172.28.128.16:7687",
        "tableName": "RELATIONSHIP.\u5408\u4f5c",
        "numRows": 10,
        "totalSize": "0",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": "",
        "connect_url": "bolt://172.28.128.16:7687"
      }
    ],
    "abstract_data": [
      {
        "dbName": "bolt://172.28.128.16:7687",
        "tableName": "RELATIONSHIP.\u5408\u4f5c",
        "numRows": 10,
        "totalSize": "0",
        "numAddedYesterday": "0",
        "numAddedlastWeek": "0",
        "lastUpdateTime": "",
        "createTime": "",
        "tableComment": ""
      }
    ]
  }
  ```

- 接口调用提交字段说明：

  ```
  无
  ```

- 接口调用返回字段说明：

  - neo_source： Neo4j数据库中每个索引的详细信息，包含字段信息、数据源详细信息、数据库名、数据表名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、数据表描述、完整数据表名称
    - col_name：节点或边的属性列表
    - dbName： neo4j图数据库连接地址
    - tableName： 节点或边的完整名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述
    - connect_url：neo4j图数据库连接地址
  - abstract_data： Redis数据库中每个索引的摘要信息，包含neo4j图数据库连接地址、节点或边的完整名称、数据总量、数据占用空间大小、昨日新增数据量、最近一周新增数据量、最近更新时间、创建时间、表描述
    - dbName： neo4j图数据库连接地址
    - tableName：节点或边的完整名称
    - numRows： 数据总量
    - totalSize： 数据占用空间大小
    - numAddedYesterday： 昨日新增数据量
    - numAddedlastWeek： 最近一周新增数据量
    - lastUpdateTime： 最近更新时间
    - createTime： 创建时间
    - tableComment： 数据表描述

## 预览数据接口

### Hive预览数据接口

- 接口说明：

  ```
  该接口用来从hive数据库中查询指定条数的数据，达到预览数据的目的
  ```

- 接口地址： 

  ```
  HiveDataQuery
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DbName
  - TableName
  - QueryRowsCount

- 接口调用举例：

  ```
  import requests
  url = "http://172.28.128.16:8000/HiveDataQuery"
  data = {
      "DbName": "fake_db",
      "TableName": "fake_table_20210205_1",
      "QueryRowsCount": "10",
  }
  req = requests.post(url, data=data)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "select_result": [
      [
        "name",
        "cardno",
        "moblie",
        "company",
        "location",
        "import_time"
      ],
      [
        "汪婷5",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷6",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷7",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷3",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷4",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷3",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷4",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷5",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ],
      [
        "汪婷6",
        "410928197610108785",
        "18515947796",
        "昊嘉信息有限公司",
        "广西壮族自治区玉梅市高坪海门路Z座 224330",
        "2021-02-05 10:38:54"
      ]
    ]
  }
  ```

- 接口调用提交字段说明：

  - DbName： 需要查询的数据库名称
  - TableName： 需要查询的数据表名称
  - QueryRowsCount： 需要查询的数据条数，如果不传，则默认查询十条数据

- 接口调用返回字段说明：

  - select_result： 查询返回的预览数据，该字段是一个列表，列表第一个元素是预览数据的列名信息

### Mysql预览数据接口

- 接口说明：

  ```
  该接口用来从mysql数据库中查询指定条数的数据，达到预览数据的目的
  ```

- 接口地址： 

  ```
  MysqlDataQuery
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DbName
  - TableName
  - QueryRowsCount

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/MysqlDataQuery"
  data = {
      "DbName": "mysql_test_db",
      "TableName": "test_tabl_1",
      "QueryRowsCount": "10",
  }
  req = requests.post(url, data=data)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "select_result": [
      [
        "_id",
        "name",
        "cardno",
        "mobile",
        "company",
        "address",
        "import_time",
        "foo"
      ],
      [
        "00002cb8-5bbf-11eb-b7b1-548d5a43df81",
        "翁旭",
        "21122419320225972X",
        "13687456311",
        "时空盒数字信息有限公司",
        "香港特别行政区太原县秀英邱街B座 796295",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "00002cb9-5bbf-11eb-84ca-548d5a43df81",
        "孙丽丽",
        "540224196702086588",
        "13988714595",
        "中建创业信息有限公司",
        "上海市桂珍市普陀何街U座 967403",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "000052e4-5bbf-11eb-bb5f-548d5a43df81",
        "杨红梅",
        "140929199210277221",
        "13668722523",
        "创亿信息有限公司",
        "福建省齐齐哈尔县清城张路x座 172059",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "00007902-5bbf-11eb-ad7d-548d5a43df81",
        "许丽华",
        "510723195202163808",
        "13195056728",
        "开发区世创网络有限公司",
        "河北省上海市华龙北京路I座 647350",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "00009f2e-5bbf-11eb-a267-548d5a43df81",
        "郑晶",
        "420107195302059317",
        "15589844992",
        "凌云科技有限公司",
        "台湾省六盘水市门头沟颜街y座 744319",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "00009f2f-5bbf-11eb-a47f-548d5a43df81",
        "胡刚",
        "54012219540224182X",
        "18530425430",
        "维旺明信息有限公司",
        "江苏省成都市沈北新游街M座 276599",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "0000c554-5bbf-11eb-8cba-548d5a43df81",
        "倪建华",
        "420822198610292095",
        "13918526802",
        "联软传媒有限公司",
        "甘肃省东县兴山田路q座 655147",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "0000eb76-5bbf-11eb-8eb7-548d5a43df81",
        "沈宇",
        "632525194908141797",
        "13037841930",
        "维旺明科技有限公司",
        "江西省香港县高明乌鲁木齐街w座 220409",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "0001119e-5bbf-11eb-9166-548d5a43df81",
        "姚丽华",
        "130322199601318079",
        "15076994395",
        "九方传媒有限公司",
        "江西省萍市和平六盘水街u座 965492",
        "2021-01-21 16:02:26",
        0
      ],
      [
        "000137cc-5bbf-11eb-a0a6-548d5a43df81",
        "李强",
        "370681196711209057",
        "15939497876",
        "中建创业信息有限公司",
        "天津市武汉县朝阳永安路u座 560023",
        "2021-01-21 16:02:26",
        0
      ]
    ]
  }
  ```

- 接口调用提交字段说明：

  - DbName： 需要查询的数据库名称
  - TableName： 需要查询的数据表名称
  - QueryRowsCount： 需要查询的数据条数，如果不传，则默认查询十条数据

- 接口调用返回字段说明：

  - select_result： 查询返回的预览数据，该字段是一个列表，列表第一个元素是预览数据的列名信息

### ES预览数据接口

- 接口说明：

  ```
  该接口用来从elasticsearch数据库中查询指定条数的数据，达到预览数据的目的
  ```

- 接口地址： 

  ```
  EsDataQuery
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DbName
  - TableName
  - QueryRowsCount

- 接口调用举例：

  ```python
  import requests
  url = "http://172.28.128.16:8000/EsDataQuery"
  data = {
      "DbName": "",
      "TableName": "es_test_index_2",
      "QueryRowsCount": "10",
  }
  req = requests.post(url, data=data)
  print(req.json())
  ```

- 接口调用返回：

  ```json
  {
    "select_result": [
      [
        "uuid",
        "name",
        "ssn",
        "phone_number",
        "company",
        "address",
        "import_time"
      ],
      [
        "14886603-5eec-11eb-b92a-548d5a43df81",
        "郭璐",
        "511423197308071921",
        "15258652378",
        "通际名联信息有限公司",
        "贵州省济南县大兴张街A座 860152",
        "2021-01-25 17:02:41.000"
      ],
      [
        "14888c28-5eec-11eb-8fff-548d5a43df81",
        "蔡丹丹",
        "350302199811237125",
        "18874362558",
        "诺依曼软件科技有限公司",
        "四川省六盘水市高港李路M座 723412",
        "2021-01-25 17:02:41.000"
      ],
      [
        "14888c29-5eec-11eb-bff9-548d5a43df81",
        "罗辉",
        "451101196206245526",
        "18538525004",
        "维旺明信息有限公司",
        "浙江省潮州县高港王路r座 451231",
        "2021-01-25 17:02:41.000"
      ],
      [
        "1488b252-5eec-11eb-bc1b-548d5a43df81",
        "黄春梅",
        "131127195301150562",
        "15546136407",
        "银嘉网络有限公司",
        "浙江省广州县房山赵街s座 766959",
        "2021-01-25 17:02:41.000"
      ],
      [
        "1488b253-5eec-11eb-bc09-548d5a43df81",
        "张杰",
        "140221198109034192",
        "13918947412",
        "彩虹科技有限公司",
        "安徽省坤市龙潭王路K座 655114",
        "2021-01-25 17:02:41.000"
      ],
      [
        "1488d874-5eec-11eb-92a9-548d5a43df81",
        "李彬",
        "330101197708287618",
        "14533129161",
        "国讯信息有限公司",
        "山东省宜都县六枝特尹街v座 355070",
        "2021-01-25 17:02:41.000"
      ],
      [
        "1488d875-5eec-11eb-8dc2-548d5a43df81",
        "宋飞",
        "652323194704199970",
        "14535286967",
        "诺依曼软件网络有限公司",
        "甘肃省大冶市崇文韩街d座 557020",
        "2021-01-25 17:02:41.000"
      ],
      [
        "1488fe9a-5eec-11eb-92dc-548d5a43df81",
        "凌秀梅",
        "621024196410216344",
        "15616608960",
        "立信电子科技有限公司",
        "广西壮族自治区深圳市淄川广州街Y座 565323",
        "2021-01-25 17:02:41.000"
      ],
      [
        "1488fe9b-5eec-11eb-9dd6-548d5a43df81",
        "赵勇",
        "451223196603032907",
        "18280707388",
        "富罳网络有限公司",
        "天津市合肥县房山福州街g座 351808",
        "2021-01-25 17:02:41.000"
      ],
      [
        "148924c2-5eec-11eb-9258-548d5a43df81",
        "史小红",
        "350725196205036086",
        "13157263730",
        "超艺传媒有限公司",
        "吉林省巢湖县丰都梧州路P座 926769",
        "2021-01-25 17:02:41.000"
      ]
    ]
  }
  ```

- 接口调用提交字段说明：

  - DbName： es查询不需要传该字段，传空即可
  - TableName： 需要查询的索引名称
  - QueryRowsCount： 需要查询的数据条数，如果不传，则默认查询十条数据

- 接口调用返回字段说明：

  - select_result： 查询返回的预览数据，该字段是一个列表，列表第一个元素是预览数据的列名信息

## 新增数据接口

### 新增文本数据接口

- 接口说明：

  ```
  该接口用于上传文本数据到指定的数据源，目前支持的数据源有：hive、mysql、elasticsearch、redis、neo4j
  ```

- 接口地址： 

  ```
  DataContentAdd
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DBType
  - DBName
  - TableName
  - InputeContent
  - Separator

- 接口调用举例：

  - 新增数据到hive数据库

    ```python
    # 以"\t"作为分隔符
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Hive",
        "DBName": "fake_db",
        "TableName": "test_merge_data",
        "InputeContent": "路人甲\t1111111\t22222222\n"
                         "路人乙\t3333333\t44444444\n"
                         "路人丙\t5555555\t66666666\n",
        "Separator": "\t"
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 分隔符Separator字段不传值，或传","，都按照csv来解析
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Hive",
        "DBName": "fake_db",
        "TableName": "test_merge_data",
        "InputeContent": "路人甲,1111111,22222222\n"
                         "路人乙,3333333,44444444\n"
                         "路人丙,5555555,66666666\n",
        "Separator": ""
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 新增数据到mysql数据库

    ```python
    # 以"\t"作为分隔符
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Mysql",
        "DBName": "mysql_test_db",
        "TableName": "test_merge_data",
        "InputeContent": "路人甲\t1111111\t22222222\n"
                         "路人乙\t3333333\t44444444\n"
                         "路人丙\t5555555\t66666666\n",
        "Separator": "\t"
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 分隔符Separator字段不传值，或传","，都按照csv来解析
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Mysql",
        "DBName": "mysql_test_db",
        "TableName": "test_merge_data",
        "InputeContent": "路人甲,1111111,22222222\n"
                         "路人乙,3333333,44444444\n"
                         "路人丙,5555555,66666666\n",
        "Separator": ""
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 新增数据到elasticsearch数据库

    ```python
    # 以"\t"作为分隔符，注意！ES增加数据需要把列名作为第一行传入
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "ElasticSearch",
        "DBName": "",
        "TableName": "test_merge_data",
        "InputeContent": "name\tssn\tphone_number\n"
                         "路人甲\t1111111\t22222222\n"
                         "路人乙\t3333333\t44444444\n"
                         "路人丙\t5555555\t66666666\n",
        "Separator": "\t"
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 分隔符Separator字段不传值，或传","，都按照csv来解析，注意！ES增加数据需要把列名作为第一行传入
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "ElasticSearch",
        "DBName": "",
        "TableName": "test_merge_data",
        "InputeContent": "name,ssn,phone_number\n"
                         "路人甲,1111111,22222222\n"
                         "路人乙,3333333,44444444\n"
                         "路人丙,5555555,66666666\n",
        "Separator": ""
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 新增数据到redis数据库

    ```python
    # 以"\t"作为分隔符，注意！Redis增加数据需要有三列，第一列是name 第二列是key 第三列是value
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Redis",
        "DBName": "",
        "TableName": "",
        "InputeContent": "tender_info\t1111111\t22222222\n"
                         "tender_info\t3333333\t44444444\n"
                         "tender_info\t5555555\t66666666\n",
        "Separator": "\t"
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 分隔符Separator字段不传值，或传","，都按照csv来解析，注意！Redis增加数据需要有三列，第一列是name 第二列是key 第三列是value
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Redis",
        "DBName": "",
        "TableName": "",
        "InputeContent": "tender_info,1111111,aaaaaaaa\n"
                         "tender_info,3333333,bbbbbbbb\n"
                         "tender_info,5555555,cccccccc\n",
        "Separator": ""
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 新增数据到neo4j数据库

    ```python
    # 以"\t"作为分隔符，注意！neo4j增加数据需要有三列，第一列是点信息,第二列是边信息,第三列是点信息
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "InputeContent": '{"label_type":"学生","attrs":{"name":"小明","sex":"男","age":"12","mobile":"123456789","ssn":"320323198506252035","address":"测试1省测试1市测试1区测试1街道测试1小区测试1单元101"}}\t'
                         '{"relation_type":"在读","attrs":{"begin_time":"2021-03-02","end_time":"-","class":"一(1)","job":"普通学生"}}\t'
                         '{"label_type":"学校","attrs":{"name":"江苏省南京市琅琊路实验小学","principal":"张三", "master_sex":"男","master_age":"25","master_mobile":"123456789","master_ssn":"320323198506252035","company_address":"测试1省测试1市测试1区测试1街道测试1小区测试1单元101"}}',
        "Separator": "\t"
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 分隔符Separator字段不传值，或传","，都按照csv来解析，注意！neo4j增加数据需要有三列，第一列是点信息,第二列是边信息,第三列是点信息
    import requests
    url = "http://172.28.128.16:8000/DataContentAdd"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "InputeContent": '"{""label_type"":""员工"",""attrs"":{""name"":""张三"",""sex"":""男"",""age"":""25"",""mobile"":""123456789"",""ssn"":""320323198506252035"",""address"":""测试1省测试1市测试1区测试1街道测试1小区测试1单元102""}}"'
                         ',"{""relation_type"":""任职"",""attrs"":{""begin_time"":""2021-03-02"",""end_time"":""-"",""payroll"":""21K"",""job"":""校长""}}",'
                         '"{""label_type"":""学校"",""attrs"":{""name"":""江苏省南京市琅琊路实验小学"",""principal"":""张三"", ""master_sex"":""男"",""master_age"":""25"",""master_mobile"":""123456789"",""master_ssn"":""320323198506252035"",""company_address"":""测试1省测试1市测试1区测试1街道测试1小区测试1单元101""}}',
        "Separator": ""
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

- 接口调用返回：

  ```json
  {'msg': 'data to xxx successful'}
  ```

- 接口调用提交字段说明：

  - DBType： 需要添加数据的数据源类型，目前支持： Hive,Mysql,Redis,ElasticSearch,Neo4j
  - DBName： 需要添加的数据库名称
    - Hive和Mysql填写数据库的名称
    - ElasticSearch不填
    - Redis不填
    - Neo4j填写图数据库的连接url
  - TableName： 需要添加的数据表名称
    - Hive和Mysql填写数据表的名称
    - ElasticSearch填写索引的名称
    - Redis和Neo4j不填
  - InputeContent：需要添加的数据源的文本数据
    - 如果添加的到Hive和Mysql里，就按照正常二维表数据输入即可，具体看调用示例
    - 如果添加到ElasticSearch里，需要把列名作为第一行传入，按照正常二维表形式传入即可，具体看调用示例
    - 如果添加到Redis里，数据需要有三列，第一列是name 第二列是key 第三列是value，按照正常二维表形式传入即可，具体看调用示例
    - 如果添加到Neo4j里，数据需要有三列，第一列是点信息,第二列是边信息,第三列是点信息，且每一列都是json字符串，具体格式参考调用示例
      - 第一列点信息的json字符串需要有的key为：
        - label_type： 点类型
        - attrs： 点属性
      - 第二列边信息的json字符串需要有的key为：
        - relation_type： 边类型
        - attrs： 边属性
      - 第三列点信息的json字符串需要有的key为：
        - label_type： 点类型
        - attrs： 点属性
  - Separator： 指定文本的列分隔符，如果传空或者传英文逗号，则按照csv格式解析

- 接口调用返回字段说明：

  - msg： 添加数据结果描述

### 新增文件数据接口

- 接口说明：

  ```
  该接口用于上传文件到指定的数据源，目前支持的数据源有：hive、mysql、elasticsearch、redis、neo4j
  ```

- 接口地址： 

  ```
  DataFileAdd
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DBType
  - DBName
  - TableName
  - File
  - Separator

- 接口调用举例：

  - 新增数据到hive数据库

    ```python
    # 假设上传文件名为：test_data， 文件内容为：
    路人甲\t1111111\t22222222
    路人乙\t3333333\t44444444
    路人丙\t5555555\t66666666
    # 以"\t"作为分隔符
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Hive",
        "DBName": "fake_db",
        "TableName": "test_merge_data",
        "Separator": "\t"
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    
    # 假设上传文件名为：test_data， 文件内容为：
    路人甲,1111111,22222222
    路人乙,3333333,44444444
    路人丙,5555555,66666666
    # 分隔符Separator字段不传值，或传","，都按照csv来解析
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Hive",
        "DBName": "fake_db",
        "TableName": "test_merge_data",
        "Separator": ""
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    ```

  - 新增数据到mysql数据库

    ```python
    # 假设上传文件名为：test_data， 文件内容为：
    路人甲\t1111111\t22222222
    路人乙\t3333333\t44444444
    路人丙\t5555555\t66666666
    # 以"\t"作为分隔符
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Mysql",
        "DBName": "mysql_test_db",
        "TableName": "test_merge_data",
        "Separator": "\t"
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    
    # 假设上传文件名为：test_data， 文件内容为：
    路人甲,1111111,22222222
    路人乙,3333333,44444444
    路人丙,5555555,66666666
    # 分隔符Separator字段不传值，或传","，都按照csv来解析
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Mysql",
        "DBName": "mysql_test_db",
        "TableName": "test_merge_data",
        "Separator": ""
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    ```

  - 新增数据到elasticsearch数据库

    ```python
    # 假设上传文件名为：test_data， 文件内容为：
    name\tssn\tphone_number
    路人甲\t1111111\t22222222
    路人乙\t3333333\t44444444
    路人丙\t5555555\t66666666
    # 以"\t"作为分隔符，注意！ES增加数据需要把列名作为第一行传入
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "ElasticSearch",
        "DBName": "",
        "TableName": "test_merge_data",
        "Separator": "\t"
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    
    # 假设上传文件名为：test_data， 文件内容为：
    name,ssn,phone_number
    路人甲,1111111,22222222
    路人乙,3333333,44444444
    路人丙,5555555,66666666
    # 分隔符Separator字段不传值，或传","，都按照csv来解析，注意！ES增加数据需要把列名作为第一行传入
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "ElasticSearch",
        "DBName": "",
        "TableName": "test_merge_data",
        "Separator": ""
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    ```

  - 新增数据到redis数据库

    ```python
    # 假设上传文件名为：test_data， 文件内容为：
    tender_info\t1111111\t22222222
    tender_info\t3333333\t44444444
    tender_info\t5555555\t66666666
    # 以"\t"作为分隔符，注意！Redis增加数据需要有三列，第一列是name 第二列是key 第三列是value
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Redis",
        "DBName": "",
        "TableName": "",
        "Separator": "\t"
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    
    # 假设上传文件名为：test_data， 文件内容为：
    tender_info,1111111,aaaaaaaa
    tender_info,3333333,bbbbbbbb
    tender_info,5555555,cccccccc
    # 分隔符Separator字段不传值，或传","，都按照csv来解析，注意！Redis增加数据需要有三列，第一列是name 第二列是key 第三列是value
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Redis",
        "DBName": "",
        "TableName": "",
        "Separator": ""
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    ```

  - 新增数据到neo4j数据库

    ```python
    # 假设上传文件名为：test_data， 文件内容为：
    {"label_type":"学生","attrs":{"name":"小明","sex":"男","age":"12","mobile":"123456789","ssn":"320323198506252035","address":"测试1省测试1市测试1区测试1街道测试1小区测试1单元101"}}\t{"relation_type":"在读","attrs":{"begin_time":"2021-03-02","end_time":"-","class":"一(1)","job":"普通学生"}}\t{"label_type":"学校","attrs":{"name":"江苏省南京市琅琊路实验小学","principal":"张三", "master_sex":"男","master_age":"25","master_mobile":"123456789","master_ssn":"320323198506252035","company_address":"测试1省测试1市测试1区测试1街道测试1小区测试1单元101"}}
    # 以"\t"作为分隔符，注意！neo4j增加数据需要有三列，第一列是点信息,第二列是边信息,第三列是点信息
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "Separator": "\t"
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    
    # 假设上传文件名为：test_data， 文件内容为：
    "{""label_type"":""员工"",""attrs"":{""name"":""张三"",""sex"":""男"",""age"":""25"",""mobile"":""123456789"",""ssn"":""320323198506252035"",""address"":""测试1省测试1市测试1区测试1街道测试1小区测试1单元102""}}","{""relation_type"":""任职"",""attrs"":{""begin_time"":""2021-03-02"",""end_time"":""-"",""payroll"":""21K"",""job"":""校长""}}","{""label_type"":""学校"",""attrs"":{""name"":""江苏省南京市琅琊路实验小学"",""principal"":""张三"", ""master_sex"":""男"",""master_age"":""25"",""master_mobile"":""123456789"",""master_ssn"":""320323198506252035"",""company_address"":""测试1省测试1市测试1区测试1街道测试1小区测试1单元101""}}
    # 分隔符Separator字段不传值，或传","，都按照csv来解析，注意！neo4j增加数据需要有三列，第一列是点信息,第二列是边信息,第三列是点信息
    import requests
    url = "http://172.28.128.16:8000/DataFileAdd"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "Separator": ""
    }
    files = {'File': open('test_data', 'rb')}
    req = requests.post(url, files=files, data=data)
    print(req.json())
    ```

- 接口调用返回：

  ```json
  {'msg': 'data to xxx successful'}
  ```

- 接口调用提交字段说明：

  - DBType： 需要添加数据的数据源类型，目前支持： Hive,Mysql,Redis,ElasticSearch,Neo4j
  - DBName： 需要添加的数据库名称
    - Hive和Mysql填写数据库的名称
    - ElasticSearch不填
    - Redis不填
    - Neo4j填写图数据库的连接url
  - TableName： 需要添加的数据表名称
    - Hive和Mysql填写数据表的名称
    - ElasticSearch填写索引的名称
    - Redis和Neo4j不填
  - File：需要添加的数据源的文件对象
    - 如果添加的到Hive和Mysql里，就按照正常二维表数据输入即可，具体看调用示例
    - 如果添加到ElasticSearch里，需要把列名作为第一行传入，按照正常二维表形式传入即可，具体看调用示例
    - 如果添加到Redis里，数据需要有三列，第一列是name 第二列是key 第三列是value，按照正常二维表形式传入即可，具体看调用示例
    - 如果添加到Neo4j里，数据需要有三列，第一列是点信息,第二列是边信息,第三列是点信息，且每一列都是json字符串，具体格式参考调用示例
      - 第一列点信息的json字符串需要有的key为：
        - label_type： 点类型
        - attrs： 点属性
      - 第二列边信息的json字符串需要有的key为：
        - relation_type： 边类型
        - attrs： 边属性
      - 第三列点信息的json字符串需要有的key为：
        - label_type： 点类型
        - attrs： 点属性
  - Separator： 指定文本的列分隔符，如果传空或者传英文逗号，则按照csv格式解析

- 接口调用返回字段说明：

  - msg： 添加数据结果描述

## 修改数据接口

### 修改数据接口

- 接口说明：

  ```
  该接口用于修改指定数据源的数据，目前支持的数据源有： Hive,Mysql.ElasticSearch,Redis,Neo4j
  ```

- 接口地址： 

  ```
  DataContentUpdate
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DBType
  - DBName
  - TableName
  - UpdateValue
  - WhereValue

- 接口调用举例：

  - 更新Hive数据

    ```
    Hive不支持更新数据
    ```

  - 更新Mysql数据

    ````python
    import requests
    url = "http://172.28.128.16:8000/DataContentUpdate"
    data = {
        "DBType": "Mysql",
        "DBName": "mysql_test_db",
        "TableName": "test_tabl_1",
        "UpdateValue": '{"name": "李桂芳2", "company": "南康传媒有限公司2"}',
        "WhereValue":
            '{"_id": "00000694-5bbf-11eb-bbad-548d5a43df81", "mobile": "15276171206"}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ````

  - 更新ElasticSearch数据

    ```python
    import requests
    url = "http://172.28.128.16:8000/DataContentUpdate"
    data = {
        "DBType": "ElasticSearch",
        "DBName": "",
        "TableName": "es_test_index_2",
        "UpdateValue": '{"uuid":"14886602-5eec-11eb-9567-548d5a43df81","name":"杨桂珍2"}',
        "WhereValue":
            '{"_id": "0rjHOHcBP63OC6Zx-aI7"}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 更新Redis数据

    ```python
    import requests
    url = "http://172.28.128.16:8000/DataContentUpdate"
    data = {
        "DBType": "Redis",
        "DBName": "",
        "TableName": "",
        "UpdateValue": '{"name":"测试姓名","ssn":"123456789876543210"}',
        "WhereValue":
            '{"name": "tender_info", "key": "tender_info-uuid_126515646853455"}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 更新Neo4j数据

    ```python
    # 修改节点信息
    import requests
    url = "http://172.28.128.16:8000/DataContentUpdate"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "UpdateValue": '{"update_obj_type": "员工", "update_value": {"name": "张三111","homwtown": "江苏省徐州市"}}',
        "WhereValue":
            '{"update_type": "Node", "src_node": {"label_type": "员工", "attrs":{"name": "张三11"}}, "tgt_node": ""}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 修改边信息
    import requests
    url = "http://172.28.128.16:8000/DataContentUpdate"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "UpdateValue": '{"update_obj_type": "合作", "update_value": {"job": "UI设计工程师", "homwtown": "江苏省徐州市"}}',
        "WhereValue":
            '{"update_type": "RelationShip", "src_node": {"label_type": "员工", "attrs":{"name": "张三"}}, "tgt_node": {"label_type": "公司", "attrs":{"name": "测试2有限公司"}}}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

- 接口调用返回：

  ```
  {'msg': 'update Neo4j bolt://172.28.128.16:7687. data successful'}
  ```

- 接口调用提交字段说明：

  - DBType： 需要修改的数据源类型，目前支持的数据源有： Mysql.ElasticSearch,Redis,Neo4j
  - DBName： 需要修改的数据库名称
    - 修改Mysql 数据的话，填写对应的数据库名称
    - 修改ElasticSearch数据的话，此字段不用填写
    - 修改redis数据的话，此字段不用填写
    - 修改Neo4j数据的话，此字段填写图数据库的连接地址，参考调用示例
  - TableName： 需要修改的数据表名称
    - 修改Mysql 数据的话，填写对应的数据库名称
    - 修改ElasticSearch数据的话，此字段填写索引名称
    - 修改Redis数据的话，此字段不用填写
    - 修改Neo4j数据的话，此字段不用填写
  - UpdateValue，需要修改的信息，该字段为json字符串
    - 修改Mysql数据的话，该json字符串中的key和value对应需要修改的字段和字段值
    - 修改ElasticSearch数据的话，该json字符串中的key和value对应需要修改的字段和字段值
    - 修改Redis数据的话，该son字符串为需要存储在redis数据库中完整的value
    - 修改Neo4j数据的话，该son字符串需要包含如下key
      - update_obj_type： 需要更新的对象的类型
      - update_value： 需要更新的属性，如果想把某个属性去掉，将那个属性的值传None即可
  - WhereValue： 条件信息，用来查出待修改的数据，该字段为json字符串
    - 修改Mysql数据的话，该json字符串中的key和value对应筛选条件中的key和value，参考调用举例
    - 修改ElasticSearch数据的话，该json字符串中的key需要包含如下字段
      - _id： 该字段为文档在ES中的id
    - 修改Redis数据的话，该json字符串中的key需要包含如下字段
      - name： 数据在redis存储的name
      - key： 数据在redis存储name下的key
    - 修改Neo4j数据的话，需要包含如下字段
      - update_type：需要更新的对象种类，只能在Node和RelationShip中选择，即更新点还是边
      - src_node： 第一个node的相关属性信息，需要包含如下字段
        - label_type： 节点的label类型
        - attrs： 节点用来筛选的属性名称
      - tgt_node： 第二个node的相关属性信息，当update_type为Node时，该字段为空，需要包含如下key
        - label_type： 节点的label类型
        - attrs： 节点用来筛选的属性名称

- 接口调用返回字段说明：

  - msg： 修改数据结果描述

## 删除数据接口

### 删除数据接口

- 接口说明：

  ```
  该接口用来删除指定条件查出的数据，目前支持的数据源有: Mysql,ElasticSearch,Redis,Neo4j
  ```

- 接口地址： 

  ```
  DataContentDelete
  ```

- 接口类型：

  ```
  POST
  ```

- 接口参数：

  - DBType
  - DBName
  - TableName
  - WhereValue

- 接口调用举例：

  - 删除Hive数据

    ```python
    Hive不支持删除数据
    ```
    
  - 删除Mysql数据

    ```python
    import requests
    url = "http://172.28.128.16:8000/DataContentDelete"
    data = {
        "DBType": "Mysql",
        "DBName": "mysql_test_db",
        "TableName": "test_tabl_1",
        "WhereValue":
            '{"_id": "00000694-5bbf-11eb-bbad-548d5a43df81", "mobile": "15276171206"}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 删除ElasticSearch数据

    ```python
    import requests
    url = "http://172.28.128.16:8000/DataContentDelete"
    data = {
        "DBType": "ElasticSearch",
        "DBName": "",
        "TableName": "es_test_index_2",
        "WhereValue":
            '{"_id": "0rjHOHcBP63OC6Zx-aI7"}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 删除Redis数据

    ```python
    import requests
    url = "http://172.28.128.16:8000/DataContentDelete"
    data = {
        "DBType": "Redis",
        "DBName": "",
        "TableName": "",
        "WhereValue":
            '{"name": "tender_info", "key": "tender_info-uuid_126515646853455"}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

  - 删除Neo4j数据

    ```python
    # 删除边
    import requests
    url = "http://172.28.128.16:8000/DataContentDelete"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "WhereValue":
            '{"delete_type": "RelationShip", "delete_obj_type": "合作", "src_node": {"label_type": "员工", "attrs":{"name": "张三"}}, "tgt_node": {"label_type": "公司", "attrs":{"name": "测试2有限公司"}}}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    # 删除点
    import requests
    url = "http://172.28.128.16:8000/DataContentDelete"
    data = {
        "DBType": "Neo4j",
        "DBName": "bolt://172.28.128.16:7687",
        "TableName": "",
        "WhereValue":
            '{"delete_type": "Node", "delete_obj_type": "公司", "src_node": {"label_type": "公司", "attrs":{"name": "测试2有限公司"}}, "tgt_node": ""}'  # nopep8
    }
    req = requests.post(url, data=data)
    print(req.json())
    ```

- 接口调用返回：

  ```
  {'msg': 'delete Neo4j bolt://172.28.128.16:7687. data successful'}
  ```

- 接口调用提交字段说明：

  - DBType： 需要删除数据的数据源类型，目前支持的数据源类型有： Mysql、ElasticSearch、Redis、Neo4j
  - DBName： 需要删除数据的数据库名称
    - 删除Mysql数据时，该字段填写数据库名称
    - 删除Redis数据时，该字段不填
    - 删除ElasticSearch数据时，该字段不填
    - 删除Neo4j数据时，该字段填写图数据库的连接地址
  - TableName： 需要删除数据的数据表名称
    - 删除Mysql数据时，该字段填写数据表名称
    - 删除Redis数据时，该字段不填
    - 删除ElasticSearch数据时，该字段填写索引名称
    - 删除Neo4j数据，该字段不填
  - WhereValue： 用来筛选出待删除数据的筛选信息，该字段为json字符串格式
    - 删除Mysql数据时，该json字符串中的key和value对应需要删除数据的筛选条件的key和value
    - 删除Redis数据时，该json字符串中需要包含如下key
      - name： 该字段为redis中的用来hash存储的name
      - key：该字段为redis中hash存储的对应的key
    - 删除ElasticSearch数据时，该json字符串中需要包含如下key
      - _id： 该字段为文档在ES中的唯一标识
    - 删除Neo4j数据时，该json字符串中需要包含如下key
      - delete_type：该字段用于标识删除的是节点还是边，如果是节点，该字段为Node，如果是边，该字段为RelationShip
      - delete_obj_type： 该字段用于标识删除对象的类型，如节点类型或者关系类型
      - src_node： 第一个node的相关属性信息，需要包含如下字段
        - label_type： 节点的label类型
        - attrs： 节点用来筛选的属性名称
      - tgt_node： 第二个node的相关属性信息，当delete_type为Node时，该字段为空，需要包含如下key
        - label_type： 节点的label类型
        - attrs： 节点用来筛选的属性名称

- 接口调用返回字段说明：

  - msg： 删除数据结果描述

