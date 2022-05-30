# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-23 10:38
"""
from bottle import route, static_file, request, redirect, error


@error(404)
def err404(error):
    """
    自定义404页面
    :param error:
    :return:
    """
    return static_file('404.html', './views/pages')


@route('/imgs/<filename:path>', method='GET')
def load_img(filename):
    """
    加载图片文件
    :param filename: 文件名
    :return: 静态文件
    """
    return static_file(filename, root='./views/imgs')


@route('/layui/<filename:path>', method='GET')
def load_layui(filename):
    """
    加载layui文件
    :param filename: 文件名
    :return: 静态文件
    """
    return static_file(filename, root='./views/components/layui')


@route('/js/<filename:path>', method='GET')
def load_js(filename):
    """
    加载js文件
    :param filename:
    :return:
    """
    return static_file(filename, root='./views/js')


@route('/css/<filename:path>', method='GET')
def load_css(filename):
    """
    加载css文件
    :param filename:
    :return:
    """
    return static_file(filename, root='./views/css')


@route('/components/<filename:path>', method='GET')
def load_component(filename):
    """
    加载component文件
    :param filename:
    :return:
    """
    return static_file(filename, root='./views/components')


def check_login_status(do_jump=True):
    """
    检查登录状态，若未登录则重定向至登录页
    :param do_jump: 是否跳转
    :return:
    """
    session = request.environ.get('beaker.session')
    user = session.get('user')
    if not user and do_jump:
        return redirect('/user/login')
    else:
        return user
