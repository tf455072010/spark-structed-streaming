
#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Desc:      thrfit错误
@Author:    wangzs@ct108.com
@Create:    2017/06/22
@Update:    2017/06/22
'''

class InvalidClientError(Exception):
    '''
    无效的客户端
    '''
    pass

class AuthenticationError(Exception):
    '''
    无效的验证异常
    '''
    pass

class InvalidValueError(Exception):
    '''
    无效的参数异常
    '''
    pass