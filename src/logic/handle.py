from logic.application import ss, sc, spark
from ctutil import dclog
from logic import logic_dalink_v2, logic_dalink_v2_test
from ctutil.udf import iputil, analysis_area
from logic.udf import string2array


logger = dclog.DcLogger()


def execute():
    '''
    程序执行入口
    '''

    logger.warn('datalink basicsdk服务开启', event='service start')

    # 注册udf
    iputil.regist_is_ipv6_udf(ss,logger)
    iputil.regist_is_ipv4_udf(ss,logger)
    analysis_area.regist_udf(ss,logger)
    string2array.regist_udf_str2arr(ss,logger)


    # 处理逻辑
    ss.sql("set spark.sql.orc.impl = native")
    logic_dalink_v2.handle(ss, spark)

    ss.streams.awaitAnyTermination()


    pass