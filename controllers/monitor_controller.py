# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-21 13:46
"""
from models.mysql_client import MySQLClient
from models import excel_client
import logging


def execute_search(data):
    """
    执行搜索
    :param data:
    :return:
    """
    code = 0
    count = 0
    results = []
    msg = 'OK'
    page = int(data['page'])
    limit = int(data['limit'])
    try:
        count_sql_pre = "SELECT COUNT(a.`id`)"
        query_sql_pre = "SELECT `a`.`id`,`b`.`name`,`b`.`id_no`,`a`.`health_condition`,`a`.`out_status`," \
                        "`a`.`submit_date`,`a`.`disposal_result`"
        sql_steel = " FROM `bench`.`monitor` `a` LEFT JOIN `bench`.`patient` `b` ON `a`.`pid`=`b`.`id` "
        db_query = query_sql_pre + sql_steel
        count_query = count_sql_pre + sql_steel
        if data['name'] or data['id_no']:
            db_query += " WHERE "
            count_query += " WHERE "
            key_strings = []
            for k, v in data.items():
                if k not in ['page', 'limit'] and v:
                    key_strings.append('`b`.`{0}` LIKE "%%{1}%%"'.format(k, v))
            count_query += ' AND '.join(key_strings)
            db_query += ' AND '.join(key_strings)
        db_query += ' LIMIT {0},{1}'.format((page - 1) * limit, limit)
        count = MySQLClient.find_one(count_query)[0]
        temps = MySQLClient.find(db_query)
        if temps:
            results = [{'id': t[0], 'name': t[1], 'id_no': t[2], 'health_condition': t[3], 'out_status': t[4],
                        'submit_date': t[5].strftime('%Y-%m-%d'), 'disposal_result': t[6]} for t in temps]
    except Exception as e:
        code = -1
        msg = '数据异常：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': results, 'count': count}


def execute_search_by_pid(data):
    """
    根据pid检索数据
    :param data:
    :return:
    """
    code = 0
    count = 0
    results = []
    msg = 'OK'
    page = int(data['page'])
    limit = int(data['limit'])
    try:
        sql_steel = " FROM `bench`.`monitor` WHERE `pid`={0}".format(data['pid'])
        # 获取数量
        count_query = "SELECT COUNT(`id`)" + sql_steel
        count = MySQLClient.find_one(count_query)[0]

        # 获取当前页数据
        db_query = "SELECT `submit_date`,`health_condition`,`out_status`,`disposal_result`" + sql_steel\
                   + ' LIMIT {0},{1}'.format((page - 1) * limit, limit)
        temps = MySQLClient.find(db_query)
        if temps:
            results = [{'submit_date': t[0].strftime('%Y-%m-%d'), 'health_condition': t[1], 'out_status': t[2],
                        'disposal_result': t[3]} for t in temps]
    except Exception as e:
        code = -1
        msg = '数据异常：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': results, 'count': count}


def get_monitor_detail(data):
    """
    获取每日上报
    :param data: 搜索条件
    :return: 搜索结果
    """
    code = 0
    msg = 'OK'
    result = {}
    try:
        data_query = "SELECT `b`.`name`,`b`.`id_no`,`a`.`health_condition`,`a`.`out_status`,`a`.`submit_date`," \
                     "`a`.`disposal_result` FROM `bench`.`monitor` `a` LEFT JOIN `bench`.`patient` `b` " \
                     "ON `a`.`pid`=`b`.`id` WHERE `a`.`id`={0};".format(data['id'])
        r = MySQLClient.find_one(data_query)
        result = {'name': r[0], 'id_no': r[1], 'health_condition': r[2], 'out_status': r[3],
                  'submit_date': r[4].strftime('%Y-%m-%d'), 'disposal_result': '' if r[5] is None else r[5]}
    except Exception as e:
        code = -1
        msg = '数据异常：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': result}


def execute_update(data):
    """
    执行更新操作
    :param data:
    :return:
    """
    code = 0
    msg = 'OK'
    try:
        db_query = "UPDATE `bench`.`monitor` SET `health_condition`='{health_condition}',`out_status`='{out_status}'," \
                   "`submit_date`='{submit_date}',`disposal_result`='{disposal_result}' WHERE `id`={id};".format(**data)
        MySQLClient.execute(db_query, None)
    except Exception as e:
        code = -1
        msg = '数据错误：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg}


def read_excel(file):
    """
    读取excel数据
    :param file:
    :return:
    """
    code = 0
    msg = 'OK'
    error_lines = []
    try:
        workbook, sheet_names = excel_client.read_excel(file.file.read())
        sheet, rows, cols = excel_client.read_sheet_by_name(workbook, sheet_names[0])
        index = 1
        common_lines = []
        while index < rows:
            row_data = excel_client.read_sheet_row_by_index(sheet, index)
            index += 1
            if len(row_data) == 7:
                # 姓名、身份证号、检测日期数据不能为空，O值与N值不能同时为空
                if not row_data[1].strip() or not row_data[2].strip() or not row_data[3].strip() \
                        or not row_data[5].strip():
                    error_lines.append(row_data)
                    continue
                common_lines.append(row_data)
            else:
                raise Exception('请按照模板上传')
        if common_lines:
            __batch_insert_update(common_lines)
    except Exception as e:
        code = -1
        msg = '数据错误：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': error_lines if error_lines else None}


def __batch_insert_update(common_lines):
    """
    批量插入每日上报数据
    :param common_lines:
    :return:
    """
    try:
        db_query = "SELECT `id_no`,`id` FROM `bench`.`patient` WHERE `id_no` IN {0}".format(
            str([i[2] for i in common_lines]).replace('[', '(').replace(']', ')'))
        r = MySQLClient.find(db_query)
        if not r:
            raise Exception('请先上传人员基本信息')
        patient = {k: v for k, v in r}
        nat_list = [{
            'pid': patient.get(line[2].upper()) if patient.get(line[2].upper()) else patient.get(line[2].lower()),
            'submit_date': line[5],
            'health_condition': line[3],
            'out_status': line[4],
            'disposal_result': line[6]
        } for line in common_lines]
        db_query = "INSERT INTO `bench`.`monitor`(`pid`,`submit_date`,`health_condition`,`out_status`,`disposal_result`) " \
                   "VALUES "
        for nat in nat_list:
            db_query += "({pid},'{submit_date}','{health_condition}','{out_status}','{disposal_result}'),".format(**nat)
        db_query = db_query[:-1]
        db_query += " ON DUPLICATE KEY UPDATE `pid`=VALUES(`pid`),`submit_date`=VALUES(`submit_date`)," \
                    "`health_condition`=VALUES(`health_condition`),`out_status`=VALUES(`out_status`)," \
                    "`disposal_result`=VALUES(`disposal_result`);"
        MySQLClient.execute(db_query)
    except Exception as e:
        logging.exception(e)
