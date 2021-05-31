"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from src.view import \
    view_for_data_map, view_for_test, \
    view_for_show, view_for_query, \
    view_for_data_map_cache, view_for_add, view_for_update, view_for_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^test$', view_for_test.api_test),
    url('^AbstractDataMap$', view_for_data_map.abstract_data_map),
    url('^HiveDataMap$', view_for_data_map.hive_data_map),
    url('^MysqlDataMap$', view_for_data_map.mysql_data_map),
    url('^RedisDataMap$', view_for_data_map.redis_data_map),
    url('^ESDataMap$', view_for_data_map.es_data_map),
    url('^NeoDataMap$', view_for_data_map.neo_data_map),
    url('^DataGovernance$', view_for_show.index),
    url('^DataGovernanceTableShow$', view_for_show.table_show),

    # 接口隔离原则,尽量独立，不做聚合
    url('^AbstractDataMapCache$',
        view_for_data_map_cache.abstract_data_map_cache),
    url('^HiveDataMapCache$', view_for_data_map_cache.hive_data_map_cache),
    url('^MysqlDataMapCache$', view_for_data_map_cache.mysql_data_map_cache),
    url('^RedisDataMapCache$', view_for_data_map_cache.redis_data_map_cache),
    url('^ESDataMapCache$', view_for_data_map_cache.es_data_map_cache),
    url('^NeoDataMapCache$', view_for_data_map_cache.neo_data_map_cache),

    # 查询数据
    url('^HiveDataQuery$', view_for_query.hive_data_query),
    url('^MysqlDataQuery$', view_for_query.mysql_data_query),
    url('^EsDataQuery$', view_for_query.es_data_query),

    # 添加数据
    url('^DataContentAdd$', view_for_add.data_content_add),
    url('^DataFileAdd$', view_for_add.data_file_add),

    # 修改数据
    url('^DataContentUpdate$', view_for_update.data_content_update),

    # 删除数据
    url('^DataContentDelete$', view_for_delete.data_content_delete),
]
