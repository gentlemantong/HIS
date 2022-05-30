# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2022-05-19 03:06
"""
# -*- coding: utf-8 -*-
import xlrd


def read_excel(file):
    """
    读取excel文件
    :param file: 文件
    :return: Excel文件对象 | sheet名列表
    """
    # 打开文件
    workbook = xlrd.open_workbook(file_contents=file)
    # 获取所有sheet
    sheet_names = workbook.sheet_names()
    return workbook, sheet_names


def read_sheet_by_name(workbook, sheet_name):
    """
    读取指定名称的sheet的内容
    :param workbook: Excel文件对象
    :param sheet_name: sheet名
    :return: sheet对象 | 行数 | 列数
    """
    sheet = workbook.sheet_by_name(sheet_name)
    return sheet, sheet.nrows, sheet.ncols


def read_sheet_by_index(workbook, index):
    """
    读取指定索引的sheet的内容
    :param workbook: Excel文件对象
    :param index: sheet索引
    :return: sheet对象 | 行数 | 列数
    """
    sheet = workbook.sheet_by_index(index)
    return sheet, sheet.nrows, sheet.ncols


def read_sheet_row_by_index(sheet, index):
    """
    根据索引获取sheet指定行的数据
    :param sheet: sheet对象
    :param index: 行索引
    :return: 行数据
    """
    return sheet.row_values(index)


def read_sheet_col_by_index(sheet, index):
    """
    根据索引获取sheet指定列的数据
    :param sheet: sheet对象
    :param index: 列索引
    :return: 列数据
    """
    return sheet.col_values(index)
