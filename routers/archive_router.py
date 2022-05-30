# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-15 00:35
"""
from bottle import route, template, static_file


@route('/archive/index', method='GET')
def go_archive_index():
    """
    前往档案首页
    :return:
    """
    return static_file('index.html', root='./views/pages/archive')


@route('/archive/<dataId:int>', method='GET')
def patient_detail(**kwargs):
    """
    前往个人档案详情页
    :param kwargs:
    :return:
    """
    return template('detail', root='./views/pages/archive', dataId=kwargs['dataId'])
