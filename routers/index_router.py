# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-23 20:59
"""
from bottle import route, template

from routers.basic_router import check_login_status


@route('/', method='GET')
def index():
    """
    加载首面
    :return: 静态文件
    """
    user = check_login_status()
    return template('index', user=user)
