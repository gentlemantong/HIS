# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-13 14:11
"""
from models.mysql_client import MySQLClient
import logging


def execute_login(username, password):
    """
    执行登录
    :return:
    """
    data_id = MySQLClient.find_one('SELECT `id` FROM `bench`.`user` WHERE `name`=%s AND `pwd`=%s', (username, password))
    return {'code': 1, 'msg': '登录成功'} if data_id else {'code': 0, 'msg': '用户名或密码错误'}


def execute_change_pwd(user, old_pwd, new_pwd):
    """
    修改密码
    :param user: 用户名
    :param old_pwd: 旧密码
    :param new_pwd: 新密码
    :return: 状态码
    """
    try:
        current_pwd = MySQLClient.find_one('SELECT `pwd` FROM `bench`.`user` WHERE `name`=%s', (user,))
        if current_pwd[0] != old_pwd:
            return {'code': -1, 'msg': '原密码错误'}
        MySQLClient.execute('UPDATE `bench`.`user` SET `pwd`=%s WHERE `name`=%s', (new_pwd, user))
        return {'code': 0, 'msg': 'OK'}
    except Exception as e:
        logging.exception(e)
        return {'code': -2, 'msg': e.__context__}
