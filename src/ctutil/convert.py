from datetime import datetime, timedelta


def datetime_int_format(date, time):
    '''
    将dateint和timeint转化成指定格式的datetime字符串
    '''
    datetime_int = date * 1000000 + time
    dateobj = datetime.strptime(str(datetime_int), "%Y%m%d%H%M%S")
    return dateobj.strftime("%Y-%m-%d %H:%M:%S")


def str2date(date_str):
    '''
    将字符串转换成日期格式 e.g.20190101

    :param  date_str:   str     待转换字符串

    :return:    datetime
    '''

    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except:
        return None


def date2int(date):
    '''
    将日期转换成数字

    :param  date:   datetime     日期

    :return:    int
    '''

    return date.year * 10000 + date.month * 100 + date.day
