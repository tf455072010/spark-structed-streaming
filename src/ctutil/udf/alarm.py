import time

from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

from ctutil import dclog

logger = dclog.DcLogger()

interval_minutes = 5
defaut_alarm_diff_minutes = 30
def regist_kafka_consume_speed_alarm_udf(ss, logger):
    def __alarm(kafka_timestamp, topic):
        if not isinstance(kafka_timestamp, int):
            return 0
        if kafka_timestamp > 1000000000000:
            kafka_timestamp = int(kafka_timestamp / 1000)
        diff_ms = int(time.time() - kafka_timestamp)
        if diff_ms > defaut_alarm_diff_minutes * 60:
            logger.warn("KAFKA消费进度告警\nTOPIC:{}\n延后误差：{} 秒".format(topic, diff_ms))
            return -1
        return 1


    logger.info("regist_kafka_consume_speed_alarm_udf", event="regist_udf")
    udf_ = udf(lambda kafka_timestamp, topic: __alarm(kafka_timestamp, topic), IntegerType())
    ss.udf.register("kafka_consume_speed_alarm_udf", udf_)
    return udf_
