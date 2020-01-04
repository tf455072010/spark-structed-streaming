'''
@Author:    wangzs@ct108.com
@Create:    2016/06/19
@Update:    2018/04/23
'''

import pymysql

class SqlHelper:
    '''
    mysql/mariadb 数据库帮助类
    '''

    __conn = None
    __cursor = None
    def __init__(self, host, port, username, password, db):
        '''
        初始化数据库帮助类
        '''

        if not self.__conn:
            self.__conn = pymysql.connect(
                host=host,
                port=port,
                user=username,
                passwd=password,
                db=db,
                charset="utf8")
            self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
      
    def close(self):
        '''
        关闭释放数据库链接
        '''
        try:
            if self.__cursor:
                self.__cursor.close()
        finally:
            self.__cursor = None

        try:
            if self.__conn:
                self.__conn.close()
        finally:
            self.__conn = None

    def __del__(self):
        '''
        关闭释放数据库链接
        '''

        self.close()

    def execute(self, sqlstr, params=None):
        '''
        执行语句，无返回结果

        Args:
            sqlstr  sql语句
            params  参数
        Returns:
            影响行数
        '''

        def handle(sqlstr, params):
            count = self.__cursor.execute(sqlstr, params)
            self.__conn.commit()
            return count
        return handle(sqlstr, params)

    def queryall(self, sqlstr, params=None):
        '''
        执行语句，有返回结果

        Args:
            sqlstr  sql语句
            params  参数

        Returns:
            dict
        '''
        def handle(sqlstr, params):
            self.__cursor.execute(sqlstr, params)
            return self.__cursor.fetchall()
        return handle(sqlstr, params)

    def query2cursor(self, sqlstr, params=None):
        '''
        执行语句，有返回结果

        Args:
            sqlstr  sql语句
            params  参数

        Returns:
            cursor
        '''

        def handle(sqlstr, params):
            self.__cursor.execute(sqlstr, params)
            return self.__cursor
        return handle(sqlstr, params)

    def executemany(self, sqlstr, params):
        '''
        执行语句，有返回结果

        Args:
            sqlstr  sql语句
            params  参数
        '''

        def handle(sqlstr, params):
            self.__cursor.executemany(sqlstr, params)
            self.__conn.commit()
        return handle(sqlstr, params)

    @staticmethod
    def transacted(func):
        """
        此装饰器用来使被装饰的函数支持事务

        当异常抛出时，被装饰的函数必须返回异常给装饰器，装饰器接收异常后事务会回滚，并将此异常返回给调用者。
        如果被装饰的函数返回值不是异常，装饰器会提交事务，并把接收到的返回值返回给调用者。
        """
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            conn.__conn.autocommit(False)
            ret = func(conn, *args, **kwargs)
            try:
                if isinstance(ret, Exception):
                    conn.__conn.rollback()
                else:
                    conn.__conn.commit()
            finally:
                conn.__conn.autocommit(True)
                return ret
        return wrapper


    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()