# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-21 09:55
"""
import logging
from logging.handlers import RotatingFileHandler
from waitress import serve
import bottle
from bottle import default_app
from beaker.middleware import SessionMiddleware
from routers import basic_router, index_router, user_router, patient_router, archive_router,\
    nat_router, monitor_router, track_router
from settings import SESSION_OPTS
bottle.TEMPLATE_PATH = [
    './', './views/', './views/pages/', './views/pages/archive', './views/pages/patient', './views/pages/nat',
    './views/pages/monitor']

if __name__ == '__main__':
    # 设置日志输出
    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s %(processName)s %(module)s.%(funcName)s Line:%(lineno)d - %(message)s')
    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)
    console_handler.setLevel(logging.DEBUG)
    # 文件输出
    file_handler = RotatingFileHandler(filename='launch.log', maxBytes=50*1024*1024, backupCount=5)
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.INFO)

    # 运行
    app = default_app()
    app = SessionMiddleware(app, SESSION_OPTS)
    serve(app, host='0.0.0.0', port=9000)
