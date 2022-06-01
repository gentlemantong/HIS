# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-14 01:30
"""
from models.mysql_client import MySQLClient
from models import excel_client
import datetime
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
        query_sql_pre = "SELECT `a`.`id`,`b`.`name`,`b`.`id_no`,`a`.`orf`,`a`.`n`,`a`.`testing_date`,`a`.`treatment`"
        sql_steel = " FROM `bench`.`nucleic_acid_testing` `a` LEFT JOIN `bench`.`patient` `b` ON `a`.`pid`=`b`.`id` "
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
            results = [{'id': t[0], 'name': t[1], 'id_no': t[2], 'orf': t[3], 'n': t[4],
                        'testing_date': t[5].strftime('%Y-%m-%d'), 'treatment': t[6]} for t in temps]
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
        sql_steel = " FROM `bench`.`nucleic_acid_testing` WHERE `pid`={0}".format(data['pid'])
        # 获取数量
        count_query = "SELECT COUNT(`id`)" + sql_steel
        count = MySQLClient.find_one(count_query)[0]

        # 获取当前页数据
        db_query = "SELECT `orf`,`n`,`testing_date`,`treatment`" + sql_steel\
                   + ' LIMIT {0},{1}'.format((page - 1) * limit, limit)
        temps = MySQLClient.find(db_query)
        if temps:
            results = [{'orf': t[0], 'n': t[1], 'testing_date': t[2].strftime('%Y-%m-%d'), 'treatment': t[3]}
                       for t in temps]
    except Exception as e:
        code = -1
        msg = '数据异常：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': results, 'count': count}


def __get_every_day(begin_date, end_date):
    """
    获取两个日期间的所有日期列表
    :param begin_date:
    :param end_date:
    :return:
    """
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while begin_date <= end_date:
        date_str = begin_date.strftime('%Y-%m-%d')
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def __full_date_range(date_list):
    """
    填充日期范围
    :param date_list:
    :return:
    """
    min_date = date_list[0]
    max_date = date_list[-1]
    return __get_every_day(min_date, max_date)


def __get_ct_val(results, date_list, i):
    """
    获取ct值
    :param results:
    :param date_list:
    :param i:
    :return:
    """
    data = []
    for d in date_list:
        be_find = False
        for result in results:
            if result[2].strftime('%Y-%m-%d') == d:
                be_find = True
                data.append(result[i] if result[i] else '-')
                break
        if not be_find:
            data.append('-')
    return data


def get_chart_data(param):
    """
    获取折线图所需数据
    :param param:
    :return:
    """
    code = 0
    msg = 'OK'
    data = {'xAxis': [], 'ct_o': [], 'ct_n': []}
    try:
        db_query = "SELECT `orf`,`n`,`testing_date` FROM `bench`.`nucleic_acid_testing` WHERE `pid`={0} " \
                   "ORDER BY `testing_date` ASC".format(param['pid'])
        r = MySQLClient.find(db_query)
        if r:
            data['xAxis'] = __full_date_range([item[2].strftime('%Y-%m-%d') for item in r])
            data['ct_o'] = __get_ct_val(r, data['xAxis'], 0)
            data['ct_n'] = __get_ct_val(r, data['xAxis'], 1)
    except Exception as e:
        code = -1
        msg = '数据错误：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': data}


def get_nat_detail(data):
    """
    获取核酸检测
    :param data: 搜索条件
    :return: 搜索结果
    """
    code = 0
    msg = 'OK'
    result = {}
    try:
        data_query = "SELECT `b`.`name`,`b`.`id_no`,`a`.`orf`,`a`.`n`,`a`.`testing_date`,`a`.`treatment`" \
                     " FROM `bench`.`nucleic_acid_testing` `a` LEFT JOIN `bench`.`patient` `b` ON `a`.`pid`=`b`.`id`" \
                     " WHERE `a`.`id`={0};".format(data['id'])
        r = MySQLClient.find_one(data_query)
        result = {'name': r[0], 'id_no': r[1], 'orf': r[2], 'n': r[3],
                  'testing_date': r[4].strftime('%Y-%m-%d'), 'treatment': '' if r[5] is None else r[5]}
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
        db_query = "UPDATE `bench`.`nucleic_acid_testing` SET `orf`='{orf}',`n`='{n}',`testing_date`='{testing_date}'," \
                   "`treatment`='{treatment}' WHERE `id`={id};".format(**data)
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
                if not row_data[1].strip() or not row_data[2].strip() or (not row_data[3] and not row_data[4])\
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
    批量插入核酸检测数据
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
            'testing_date': line[5],
            'orf': line[3],
            'n': line[4],
            'treatment': line[6]
        } for line in common_lines]
        db_query = "INSERT INTO `bench`.`nucleic_acid_testing`(`pid`,`testing_date`,`orf`,`n`,`treatment`) VALUES "
        for nat in nat_list:
            db_query += "({pid},'{testing_date}','{orf}','{n}','{treatment}'),".format(**nat)
        db_query = db_query[:-1]
        db_query += " ON DUPLICATE KEY UPDATE `pid`=VALUES(`pid`),`testing_date`=VALUES(`testing_date`)," \
                    "`orf`=VALUES(`orf`),`n`=VALUES(`n`),`treatment`=VALUES(`treatment`);"
        MySQLClient.execute(db_query)
    except Exception as e:
        logging.exception(e)


def read_excel2(file):
    """
    上传原来的数据文件
    :param file:
    :return:
    """
    code = 0
    msg = 'OK'
    error_lines = []
    try:
        workbook, sheet_names = excel_client.read_excel(file.file.read())
        sheet, rows, cols = excel_client.read_sheet_by_name(workbook, sheet_names[0])
        index = 0
        common_lines = []
        while index < rows:
            row_data = excel_client.read_sheet_row_by_index(sheet, index)
            index += 1
            if row_data[0].strip():
                common_lines.append(row_data)
            else:
                error_lines.append(row_data)
        if common_lines:
            __batch_insert_update2(common_lines)
    except Exception as e:
        code = -1
        msg = '数据错误：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': error_lines if error_lines else None}


def __batch_insert_update2(common_lines):
    """

    :param common_lines:
    :return:
    """
    try:
        date_titles = common_lines.pop(0)[1:]
        db_query = "SELECT `id_no`,`id` FROM `bench`.`patient` WHERE `id_no` IN {0}".format(
            str([i[0] for i in common_lines]).replace('[', '(').replace(']', ')'))
        r = MySQLClient.find(db_query)
        if not r:
            raise Exception('请先上传人员基本信息')
        patient = {k: v for k, v in r}

        db_query = "INSERT INTO `bench`.`nucleic_acid_testing`(`pid`,`testing_date`,`orf`,`n`) VALUES "
        for line in common_lines:
            pid = patient.get(line[0].upper()) if patient.get(line[0].upper()) else patient.get(line[0].lower())
            for d in range(0, len(date_titles), 2):
                orf = str(line[d+1]).strip().replace('-', '').replace('—', '')
                n = str(line[d+2]).strip().replace('-', '').replace('—', '')
                if orf or n:
                    db_query += "({0},'{1}','{2}','{3}'),".format(pid, date_titles[d], line[d+1], line[d+2])
        db_query = db_query[:-1]
        db_query += " ON DUPLICATE KEY UPDATE `pid`=VALUES(`pid`),`testing_date`=VALUES(`testing_date`)," \
                    "`orf`=VALUES(`orf`),`n`=VALUES(`n`);"
        MySQLClient.execute(db_query)
    except Exception as e:
        logging.exception(e)
