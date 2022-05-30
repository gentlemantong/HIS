# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-15 00:48
"""
from bottle import route, request, static_file, FormsDict, template

from controllers import nat_controller


@route('/nat/index', method='GET')
def go_nat_index():
    """
    跳转核酸检测数据首页
    :return:
    """
    return static_file('index.html', './views/pages/nat')


@route('/nat/search', method='POST')
def do_search():
    """
    执行搜索
    :return:
    """
    return nat_controller.execute_search(FormsDict(request.forms).decode('utf-8'))


@route('/nat/searchByPid', method='POST')
def do_search_by_pid():
    """
    根据pid执行搜索
    :return:
    """
    return nat_controller.execute_search_by_pid(FormsDict(request.forms).decode('utf-8'))


@route('/nat/chart', method='POST')
def get_nat_chart_data():
    """
    获取折线图数据
    :return:
    """
    return nat_controller.get_chart_data(FormsDict(request.forms).decode('utf-8'))


@route('/nat/edit/<dataId:int>', method='GET')
def go_edit(**kwargs):
    """
    跳转至修改核酸检测信息页面
    :param kwargs:
    :return:
    """
    return template('natEdit.html', root='./views/pages/nat', dataId=kwargs['dataId'])


@route('/nat/edit', method='POST')
def do_edit():
    """
    执行更新
    :return:
    """
    return nat_controller.execute_update(FormsDict(request.forms).decode('utf-8'))


@route('/nat/detail', method='POST')
def get_nat_detail():
    """
    获取核酸检测数据
    :return: 搜索结果
    """
    return nat_controller.get_nat_detail(request.forms)


@route('/nat/batch', method='GET')
def go_batch():
    """
    跳转至批量更新页面
    :return:
    """
    return static_file('batch.html', './views/pages/nat')


@route('/nat/download/2.xlsx', method='GET')
def download2():
    """
    下载模板
    :return:
    """
    return static_file('2.xlsx', './views/files', download=True)


@route('/nat/download/4.xlsx', method='GET')
def download4():
    """
    下载模板
    :return:
    """
    return static_file('4.xlsx', './views/files', download=True)


@route('/nat/upload', method='POST')
def do_upload():
    """
    上传并解析文件
    :return:
    """
    upload_file = request.files.get('file')
    return nat_controller.read_excel(upload_file)


@route('/nat/upload2', method='POST')
def do_upload2():
    """
    上传并解析文件
    :return:
    """
    upload_file = request.files.get('file')
    return nat_controller.read_excel2(upload_file)
