import sys
from datetime import datetime, timedelta

from ctutil import convert, dclog

logger = dclog.DcLogger()


def date_args(func):
    yesterday = datetime.today() + timedelta(days=-1)
    date_yesterday = yesterday.year * 10000 + yesterday.month * 100 + yesterday.day
    date_start = yesterday
    date_end = yesterday

    args = sys.argv
    if args:
        logger.info("发现传入参数：{}".format(args), event="args")
        if ".py" in args[0]:
            if len(args) > 1:
                args = args[1:]
            else:
                args = []

        if len(args) == 1:
            date = convert.str2date(args[0])
            if not date:
                sys.exit(1)
            elif date <= yesterday:
                date_start = date
                date_end = date
            else:
                logger.error("当前能处理的最大的日期:{}, 输入参数为{}".format(
                    date_yesterday, args[0]), event="invalid_date")
                sys.exit(1)

        if len(args) >= 2:
            date_start = convert.str2date(args[0])
            date_end = convert.str2date(args[1])
            if not date_start or not date_end:
                sys.exit(1)
            if date_start > date_end:
                logger.error("起始日期[{}]不能大于结束日期[{}]".format(
                    args[0], args[1]), event="invalid_date_range")
                sys.exit(1)
            if date_end > yesterday:
                logger.error("当前能处理的最大的日期:{}, 输入参数的结束日期为{}".format(
                    date_yesterday, args[1]), event="invalid_date")
                sys.exit(1)

    def __wrapper():
        return func(date_start, date_end)

    return __wrapper
