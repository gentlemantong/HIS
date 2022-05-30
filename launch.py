# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-21 09:55
"""
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
    app = default_app()
    app = SessionMiddleware(app, SESSION_OPTS)
    serve(app, host='0.0.0.0', port=9000)
