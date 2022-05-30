# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2021-10-23 17:46
"""
SESSION_OPTS = {
    'session.type': 'file',                 # 以文件的方式保存session
    'session.cookie_expires': 3600,         # session过期时间为3600秒
    'session.data_dir': '/tmp/sessions',    # session存放路径
    'session.auto': True
}

DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'debian-sys-maint',
    'password': 'LMfjSXIDRaCefuNi',
    'db': 'bench',
    'charset': 'utf8'
}
