# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-21 20:07
"""
from bottle import route, static_file


@route('/track/index', method='GET')
def go_index():
    """
    跳转轨迹数据首页
    :return:
    """
    return static_file('index.html', root='./views/pages/track')
