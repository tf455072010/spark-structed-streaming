from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType, BooleanType
from ctutil import iputil
import traceback


def regist_long2ip_udf(ss, logger):
    '''将long类型转化成ip字符串'''
    def handle(iplong):
        if not iplong:
            return None
        try:
            if iplong == 0:
                return None
            return iputil.long2ip(iplong)
        except:
            logger.error(traceback.format_exc(), event="long2ip_udf")
            return None

    long2ip_udf = udf(lambda iplong: handle(iplong), StringType())
    ss.udf.register("long2ip_udf", long2ip_udf)
    return long2ip_udf


def regist_is_ipv4_udf(ss, logger):
    '''判断是是否是ipv4'''
    is_ipv4_udf = udf(lambda ipstr: iputil.is_ipv4(ipstr), BooleanType())
    ss.udf.register("is_ipv4_udf", is_ipv4_udf)
    return is_ipv4_udf


def regist_is_ipv6_udf(ss, logger):
    '''判断是否是ipv6'''
    is_ipv6_udf = udf(lambda ipstr: iputil.is_ipv6(ipstr), BooleanType())
    ss.udf.register("is_ipv6_udf", is_ipv6_udf)
    return is_ipv6_udf