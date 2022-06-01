# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-23 17:45
"""
import pymysql

from settings import DATABASE_CONFIG


class MySQLClient(object):
    """初步封装的MySQL相关方法类"""

    @staticmethod
    def __get_client(schema):
        """
        get client
        :param schema:
        :return:
        """
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
            return client
        else:
            raise Exception(u"Failed to connect to mysql - {0}".format(config[u'host']))

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
            client.close()

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
            client.close()

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
            client.close()
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
            client.close()
        return result_list
