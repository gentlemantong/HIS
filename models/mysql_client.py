# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-23 17:45
"""
import sys

from settings import DATABASE_CONFIG

if sys.version_info < (3, 4):
    import thread
else:
    import _thread as thread
import pymysql
import copy


class MySQLClient(object):
    """初步封装的MySQL相关方法类"""

    __CONNECTION_POOL = dict()
    __mutex = thread.allocate_lock()

    @staticmethod
    def __init_instance(schema):
        """
        init instance
        :param schema:
        :return:
        """
        if schema not in MySQLClient.__CONNECTION_POOL.keys():
            MySQLClient.__mutex.acquire()
            config = DATABASE_CONFIG
            client = pymysql.connect(
                host=config[u'host'],
                user=config[u'user'],
                password=config[u'password'],
                db=config[u'db'],
                port=config[u'port'],
                charset=config[u'charset']
            )
            if client.cursor():
                MySQLClient.__CONNECTION_POOL[schema] = client
            else:
                raise Exception(u"Failed to connect to mysql - {0}".format(config[u'host']))
            MySQLClient.__mutex.release()
        return

    @staticmethod
    def __get_client(schema):
        """
        get client
        :param schema:
        :return:
        """
        MySQLClient.__init_instance(schema)
        return MySQLClient.__CONNECTION_POOL.get(schema)

    @staticmethod
    def execute(schema, db_query, params=None):
        """
        update、insert类操作
        :param schema:
        :param db_query:
        :param params:
        :return:
        """
        client = MySQLClient.__get_client(schema)
        if client:
            cursor = client.cursor()
            cursor.execute(db_query, params)
            client.commit()
            cursor.close()
        return

    @staticmethod
    def execute_many(schema, db_query, params):
        """
        执行多个update、insert类操作
        :param schema:
        :param db_query:
        :param params:
        :return:
        """
        client = MySQLClient.__get_client(schema)
        if client:
            cursor = client.cursor()
            cursor.executemany(db_query, params)
            client.commit()
            cursor.close()
        return

    @staticmethod
    def find_one(schema, db_query, params=None):
        """
        查询满足条件的第一条数据
        :param schema:
        :param db_query:
        :param params:
        :return:
        """
        result = None
        client = MySQLClient.__get_client(schema)
        if client:
            cursor = client.cursor()
            cursor.execute(db_query, params)
            result = cursor.fetchone()
            cursor.close()
        return result

    @staticmethod
    def find(schema, db_query, params=None):
        """
        查询满足条件的所有数据
        :param schema:
        :param db_query:
        :param params:
        :return:
        """
        result_list = list()
        client = MySQLClient.__get_client(schema)
        if client:
            cursor = client.cursor()
            cursor.execute(db_query, params)
            result_list = cursor.fetchall()
            cursor.close()
        return result_list

    @staticmethod
    def reconnect(schema):
        """
        重启连接
        :param schema:
        :return:
        """
        MySQLClient.close(schema)
        MySQLClient.__init_instance(schema)
        return

    @staticmethod
    def close(schema):
        """
        关闭指定schema的连接
        :param schema:
        :return:
        """
        client = MySQLClient.__get_client(schema)
        if client:
            client.close()
            MySQLClient.__CONNECTION_POOL.__delitem__(schema)
        return

    @staticmethod
    def close_all():
        """
        关闭所有连接
        :return:
        """
        keys = copy.deepcopy(list(MySQLClient.__CONNECTION_POOL.keys()))
        for schema in keys:
            MySQLClient.close(schema)
        return
