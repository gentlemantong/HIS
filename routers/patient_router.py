# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-14 23:23
"""
from bottle import route, request, FormsDict, static_file, template

from controllers import patient_controller


@route('/patient/index', method='GET')
def go_index():
    """
    跳转重点人员首页
    :return:
    """
    return static_file('index.html', root='./views/pages/patient')


@route('/patient/search', method='POST')
def do_search():
    """
    执行搜索
    :return: 搜索结果
    """
    return patient_controller.execute_search(FormsDict(request.forms).decode('utf-8'))


@route('/patient/add', method='GET')
def go_add():
    """
    跳转新增重点人员页面
    :return:
    """
    return static_file('add.html', root='./views/pages/patient')


@route('/patient/edit/<dataId:int>', method='GET')
def go_edit(**kwargs):
    """
    跳转至修改人员信息页面
    :return:
    """
    return template('edit.html', root='./views/pages/patient', dataId=kwargs['dataId'])


@route('/patient/edit', method='POST')
def do_edit():
    """
    修改重点人员信息
    :return:
    """
    return patient_controller.execute_update(FormsDict(request.forms).decode('utf-8'))


@route('/patient/add', method='POST')
def do_add():
    """
    新增重点人员信息
    :return:
    """
    return patient_controller.execute_add(FormsDict(request.forms).decode('utf-8'))


@route('/patient/detail', method='POST')
def get_patient_detail():
    """
    获取重点人员基本信息
    :return: 基本信息
    """
    return patient_controller.get_patient_detail(request.forms.get('data_id'))


@route('/patient/batch', method='GET')
def go_patient_batch():
    """
    跳转至批量页面
    :return:
    """
    return static_file('batch.html', root='./views/pages/patient')


@route('/patient/download/1.xlsx', method='GET')
def download():
    """
    下载模板
    :return:
    """
    return static_file('1.xlsx', './views/files', download=True)


@route('/patient/upload', method='POST')
def do_upload():
    """
    上传并解析文件
    :return:
    """
    upload_file = request.files.get('file')
    return patient_controller.read_excel(upload_file)
