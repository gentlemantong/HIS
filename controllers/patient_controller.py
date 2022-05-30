# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-13 16:55
"""
from models import excel_client
from models.mysql_client import MySQLClient
import logging


def get_patient_detail(data_id):
    """
    获取人员基本信息
    :param data_id: 人员id
    :return: 人员基本信息
    """
    result = {}
    code = 0
    msg = 'OK'
    try:
        # 获取基础信息
        query = "SELECT `name`,`age`,`id_no`,`phone`,`town`,`address`,`basic_disease`,`out_treatment`," \
                "`first_positive_date`,`last_positive_date`,`source`,`occupation`,`work_unit` FROM `bench`.`patient`" \
                " WHERE `id`={0}".format(data_id)
        data = MySQLClient.find_one('his', query)

        # 获取同住人信息
        query = "SELECT `name`,`id_no` FROM `bench`.`roommate` WHERE `pid`={0}".format(data_id)
        temp_roommates = MySQLClient.find('his', query)
        roommates = [{'name': i[0], 'id_no': i[1]} for i in temp_roommates]

        # 组装最终结果
        result['name'] = data[0]
        result['age'] = data[1]
        result['id_no'] = data[2]
        result['phone'] = data[3]
        result['town'] = data[4]
        result['address'] = data[5]
        result['basic_disease'] = data[6]
        result['out_treatment'] = data[7]
        result['first_positive_date'] = data[8].strftime('%Y-%m-%d')
        result['last_positive_date'] = data[9].strftime('%Y-%m-%d')
        result['source'] = data[10]
        result['occupation'] = data[11]
        result['work_unit'] = data[12]
        result['roommates'] = roommates
    except Exception as e:
        code = -1
        msg = str(e)
        logging.exception(e)
    return {'code': code, 'msg': msg, 'data': result}


def execute_search(data):
    """
    执行搜索
    :param data: 搜索条件
    :return: 搜索结果
    """
    code = 0
    count = 0
    results = []
    msg = 'OK'
    page = int(data['page'])
    limit = int(data['limit'])
    try:
        count_sql_pre = "SELECT COUNT(`id`)"
        query_sql_pre = "SELECT `id`,`name`,`id_no`,`phone`,`town`,`source`"
        sql_steel = " FROM `bench`.`patient`"
        db_query = query_sql_pre + sql_steel
        count_query = count_sql_pre + sql_steel
        if data['name'] or data['id_no'] or data['phone']:
            db_query += " WHERE "
            count_query += " WHERE "
            key_strings = []
            for k, v in data.items():
                if k not in ['page', 'limit'] and v:
                    key_strings.append('`{0}` LIKE "%%{1}%%"'.format(k, v))
            count_query += ' AND '.join(key_strings)
            db_query += ' AND '.join(key_strings)
        db_query += ' LIMIT {0},{1}'.format((page-1)*limit, limit)
        count = MySQLClient.find_one('his', count_query)[0]
        temps = MySQLClient.find('his', db_query)
        if temps:
            results = [{'id': t[0], 'name': t[1], 'id_no': t[2], 'phone': t[3], 'town': t[4],
                        'source': t[5]} for t in temps]
    except Exception as e:
        code = -1
        msg = '数据异常：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': results, 'count': count}


def get_pid_by_id_no(id_no):
    """
    根据身份证号获取数据id
    :param id_no:
    :return:
    """
    db_query = "SELECT `id` FROM `bench`.`patient` WHERE `id_no`='{0}'".format(id_no)
    return MySQLClient.find_one('his', db_query)


def execute_add(data):
    """
    执行新增重点人员信息操作
    :param data: 重点人员数据
    :return: 操作结果
    """
    code = 0
    msg = 'OK'
    try:
        # 检查身份证号是否重复
        if get_pid_by_id_no(data['id_no']):
            raise Exception('身份证号重复')

        # 插入数据
        db_query = "INSERT INTO `bench`.`patient` SET `name`='{name}', `age`={age},`id_no`='{id_no}'," \
                   "`phone`='{phone}',`town`='{town}',`address`='{address}',`basic_disease`='{basic_disease}'," \
                   "`out_treatment`='{out_treatment}',`first_positive_date`='{first_positive_date}'," \
                   "`last_positive_date`='{last_positive_date}',`source`='{source}',`occupation`='{occupation}'," \
                   "`work_unit`='{work_unit}'".format(**data)
        MySQLClient.execute('his', db_query)

        # 插入同住人数据
        __insert_roommates(data)
    except Exception as e:
        code = -1
        msg = '数据错误：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg}


def __insert_roommates(data):
    """
    插入同住人信息
    :param data:
    :return:
    """
    try:
        if data['roommate_no']:
            pid = get_pid_by_id_no(data['id_no'])[0]
            db_query = "INSERT INTO `bench`.`roommate` (`pid`, `name`, `id_no`) VALUES "
            for i in data['roommate_no'].split(','):
                db_query = db_query + "({0},'{1}','{2}'),".format(
                    pid, data['roommate_name' + i], data['roommate_id_no' + i])
            db_query = db_query[:-1] + ';'
            MySQLClient.execute('his', db_query)
    except Exception as e:
        logging.exception(e)


def execute_update(data):
    """
    执行更新操作
    :param data:
    :return:
    """
    code = 0
    msg = 'OK'
    try:
        # 检查身份证号是否重复
        r = get_pid_by_id_no(data['id_no'])
        if r and r[0] != int(data['id']):
            raise Exception('修改后的身份证号有重复')

        # 更新数据
        db_query = "UPDATE `bench`.`patient` SET `name`='{name}', `age`={age},`id_no`='{id_no}'," \
                   "`phone`='{phone}',`town`='{town}',`address`='{address}',`basic_disease`='{basic_disease}'," \
                   "`out_treatment`='{out_treatment}',`first_positive_date`='{first_positive_date}'," \
                   "`last_positive_date`='{last_positive_date}',`source`='{source}',`occupation`='{occupation}'," \
                   "`work_unit`='{work_unit}' WHERE `id`={id}".format(**data)
        MySQLClient.execute('his', db_query)

        # 更新同住人数据
        MySQLClient.execute('his', "DELETE FROM `bench`.`roommate` WHERE `pid`={0}".format(data['id']))
        __insert_roommates(data)
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
            if len(row_data) == 15:
                # 姓名、身份证号
                if not row_data[1].strip() or not row_data[2].strip():
                    error_lines.append(row_data)
                    continue
                common_lines.append(row_data)
            else:
                raise Exception('表格列数与模板有出入，读取被中断')
        if common_lines:
            __batch_insert_update(common_lines)
            __batch_update_roommates(common_lines)
    except Exception as e:
        code = -1
        msg = '数据错误：{0}'.format(e)
        logging.exception(msg)
    return {'code': code, 'msg': msg, 'data': error_lines if error_lines else None}


def __batch_update_roommates(row_datas):
    """
    批量更新同住人
    :param row_datas:
    :return:
    """
    try:
        data_list = [{'id_no': row_data[2], 'roommate': row_data[9]} for row_data in row_datas]
        for row_data in data_list:
            pid = get_pid_by_id_no(row_data['id_no'])[0]
            MySQLClient.execute('his', "DELETE FROM `bench`.`roommate` WHERE `pid`={0}".format(pid))
            mate_arr = row_data['roommate'].split(';')
            db_query = "INSERT INTO `bench`.`roommate`(`pid`,`name`,`id_no`) VALUES "
            for mate in mate_arr:
                if mate.strip():
                    mate_items = mate.split(',')
                    db_query += "({0},'{1}','{2}'),".format(pid, mate_items[0].strip(), mate_items[1].strip())
            if db_query[-1] == ',':
                db_query = db_query[:-1] + ';'
                MySQLClient.execute('his', db_query)
    except Exception as e:
        logging.exception(e)


def __batch_insert_update(row_datas):
    """
    批量插入或更新数据
    :param row_datas: 行数据列表
    :return:
    """
    try:
        data_list = [{
            'name': row_data[1],
            'id_no': str(row_data[2]).split('.')[0],
            'age': str(row_data[3]).split('.')[0],
            'phone': str(row_data[4]).split('.')[0],
            'address': row_data[5],
            'town': row_data[6],
            'occupation': row_data[7],
            'work_unit': row_data[8],
            'basic_disease': row_data[10],
            'out_treatment': row_data[11],
            'first_positive_date': row_data[12] if row_data[12] else '1900-01-01',
            'last_positive_date': row_data[13] if row_data[12] else '1900-01-01',
            'source': row_data[14]
        } for row_data in row_datas]
        db_query = "INSERT INTO `bench`.`patient`(`name`,`id_no`,`age`,`phone`,`address`,`town`,`basic_disease`," \
                   "`out_treatment`,`first_positive_date`,`last_positive_date`,`source`,`occupation`,`work_unit`) VALUES "
        for row_data in data_list:
            temp = "('{name}','{id_no}',{age},'{phone}','{address}','{town}','{basic_disease}','{out_treatment}'," \
                        "'{first_positive_date}','{last_positive_date}','{source}','{occupation}'," \
                        "'{work_unit}'),".format(**row_data)
            db_query += temp
        db_query = db_query[:-1]
        db_query += " ON DUPLICATE KEY UPDATE `name`=VALUES(`name`),`id_no`=VALUES(`id_no`),`age`=VALUES(`age`)," \
                    "`phone`=VALUES(`phone`),`address`=VALUES(`address`),`town`=VALUES(`town`)," \
                    "`basic_disease`=VALUES(`basic_disease`),`out_treatment`=VALUES(`out_treatment`)," \
                    "`first_positive_date`=VALUES(`first_positive_date`),`last_positive_date`=VALUES(`last_positive_date`)," \
                    "`source`=VALUES(`source`),`occupation`=VALUES(`occupation`),`work_unit`=VALUES(`work_unit`);"
        MySQLClient.execute('his', db_query)
    except Exception as e:
        logging.exception(e)
