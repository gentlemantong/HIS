# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-21 13:46
"""
from bottle import route, request, static_file, FormsDict, template

from controllers import monitor_controller


@route('/monitor/index', method='GET')
def go_monitor_index():
    """
    跳转每日上报数据首页
    :return:
    """
    return static_file('index.html', './views/pages/monitor')


@route('/monitor/search', method='POST')
def do_search():
    """
    执行搜索
    :return:
    """
    return monitor_controller.execute_search(FormsDict(request.forms).decode('utf-8'))


@route('/monitor/searchByPid', method='POST')
def do_search_by_pid():
    """
    根据pid执行搜索
    :return:
    """
    return monitor_controller.execute_search_by_pid(FormsDict(request.forms).decode('utf-8'))


@route('/monitor/edit/<dataId:int>', method='GET')
def go_edit(**kwargs):
    """
    跳转至修改每日上报信息页面
    :param kwargs:
    :return:
    """
    return template('monitorEdit.html', root='./views/pages/monitor', dataId=kwargs['dataId'])


@route('/monitor/edit', method='POST')
def do_edit():
    """
    执行更新
    :return:
    """
    return monitor_controller.execute_update(FormsDict(request.forms).decode('utf-8'))


@route('/monitor/detail', method='POST')
def get_monitor_detail():
    """
    获取核酸检测数据
    :return: 搜索结果
    """
    return monitor_controller.get_monitor_detail(request.forms)


@route('/monitor/batch', method='GET')
def go_batch():
    """
    跳转至批量更新页面
    :return:
    """
    return static_file('batch.html', './views/pages/monitor')


@route('/monitor/download/3.xlsx', method='GET')
def download():
    """
    下载模板
    :return:
    """
    return static_file('3.xlsx', './views/files', download=True)


@route('/monitor/upload', method='POST')
def do_upload():
    """
    上传并解析文件
    :return:
    """
    upload_file = request.files.get('file')
    return monitor_controller.read_excel(upload_file)
