# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-23 16:06
"""
from bottle import route, request, static_file, redirect

from controllers import user_controller
from routers.basic_router import check_login_status


@route('/user/login', method='GET')
def login():
    """
    加载登录页面
    :return: 静态文件
    """
    user = check_login_status(False)
    if not user:
        return static_file('login.html', root='./views/pages/user')
    else:
        redirect('/')


@route('/user/login', method='POST')
def do_login():
    """
    执行登录操作
    :return:
    """
    username = request.forms.get('username')
    password = request.forms.get('password')
    status = user_controller.execute_login(username, password)
    if status['code'] == 1:
        session = request.environ.get('beaker.session')
        session['user'] = username
    return status


@route('/user/logout', method='GET')
def logout():
    """
    退出登录
    :return:
    """
    session = request.environ.get('beaker.session')
    if session.get('user'):
        session.pop('user')
    redirect('/user/login')


@route('/user/changePass', method='GET')
def change_pass():
    """
    加载修改密码页面
    :return:
    """
    return static_file('changePass.html', root='./views/pages/user')


@route('/user/changePass', method='POST')
def do_change_pass():
    """
    执行修改密码
    :return: 修改结果
    """
    old_pwd = request.forms.get('oldPass')
    new_pwd = request.forms.get('newPass')
    user = check_login_status(False)
    return user_controller.execute_change_pwd(user, old_pwd, new_pwd)
