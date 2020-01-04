from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from ctutil import convert


def regist_datetime_int_format_udf(ss, logger):
    '''
    注册UDF
    
    :param  ss: spark session
    '''
    logger.info("注册datetime_int_format_udf UDF", event="regist_udf")
    datetime_int_format_udf = udf(lambda dateint, timeint: convert.datetime_int_format(dateint, timeint), StringType())
    ss.udf.register("datetime_int_format_udf", datetime_int_format_udf)
    return datetime_int_format_udf