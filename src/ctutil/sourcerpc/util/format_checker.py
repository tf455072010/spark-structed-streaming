
#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Desc:      格式检查帮助类
@Author:    wangzs@ct108.com
@Create:    2017/06/22
@Update:    2018/03/08
'''

import re

class InvalidValueError(Exception):
    '''
    无效的参数异常
    '''
    pass

def is_ipv4(text):
    '''
    是否是正确的IP格式
    '''

    if not isinstance(text, str):
        raise InvalidValueError("输入参数不是字符串格式")

    rex = r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
    pattern = re.compile(rex)
    match = pattern.match(text)
    if match and match.group():
        return True
    else:
        return False

def is_number(text):
    '''
    是否是数字
    '''

    if not isinstance(text, str):
        raise InvalidValueError("输入参数不是字符串格式")

    rex = r'^(\d)*$'
    pattern = re.compile(rex)
    match = pattern.match(text)
    if match and match.group():
        return True
    else:
        return False

def is_email(text):
    '''
    是否是邮件格式
    '''

    if not isinstance(text, str):
        raise InvalidValueError("输入参数不是字符串格式")

    rex = r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$'
    pattern = re.compile(rex)
    match = pattern.match(text)
    if match and match.group():
        return True
    else:
        return False

def is_IDcard(text):
    '''
    是否是省份证号
    '''

    if not isinstance(text, str):
        raise InvalidValueError("输入参数不是字符串格式")

    rex1 = r'^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$'
    rex2 = r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$'
    pattern1 = re.compile(rex1)
    pattern2 = re.compile(rex2)
    match1 = pattern1.match(text)
    match2 = pattern2.match(text)
    if match1 or match2:
        if match1.group():
            return True
        elif match2.group():
            return True
    return False


def is_empty(text):
    '''
    是否为空
    '''

    if not isinstance(text, str):
        raise InvalidValueError("输入参数不是字符串格式")

    return True if text else False