from pyspark import SparkConf, SparkContext
from pyspark.sql.session import SparkSession


class SparkBase:
    def __init__(self):
        self.__sc = SparkContext()
        self.__sc.setLogLevel("WARN")
        self.__spark = SparkSession.builder.enableHiveSupport().getOrCreate()

    def get_spark_context(self):
        return self.__sc, self.__spark

    def get_applicationId(self):
        return self.__sc.applicationId

    def get_structured_streaming_kafka(self, bootstrap_servers, topic, max_offsets_per_trigger=None, security_protocol=None, sasl_mechanism=None, starting_offsets="earliest"):
        '''
        获取来源于kafka的dataframe对象

        :param  bootstrap_servers:   str     kafka broker地址
        :param  topic:  str     topic
        :param  security_protocol:  str     认证协议
        :param  sasl_mechanism: str     认证信息

        :return:    dataframe
        '''
        if security_protocol:
            return self.__spark.readStream.format("kafka") \
                .option("kafka.bootstrap.servers", bootstrap_servers)  \
                .option("kafka.security.protocol", security_protocol) \
                .option("kafka.sasl.mechanism", sasl_mechanism) \
                .option("subscribe", topic) \
                .option("failOnDataLoss", "true") \
                .option("startingOffsets", starting_offsets) \
                .option("includeTimestamp", True) \
                .option("maxOffsetsPerTrigger", max_offsets_per_trigger)
        else:
            return self.__spark.readStream.format("kafka") \
                .option("kafka.bootstrap.servers", bootstrap_servers)  \
                .option("subscribe", topic) \
                .option("failOnDataLoss", "true") \
                .option("startingOffsets", starting_offsets) \
                .option("includeTimestamp", True) \
                .option("maxOffsetsPerTrigger", max_offsets_per_trigger)


    def close(self):
        self.__sc.stop()
        self.__spark.stop()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
