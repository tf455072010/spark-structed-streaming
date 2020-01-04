from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
import json


def regist_udf_str2arr(ss,logger):
    logger.info("注册str2arr UDF", event="regist_udf")
    def string2array(str):
        if len(str) :
            return ','.join(json.loads(str))
            # arr = str.replace('\\"','').replace('\\[','').replace('\\]','')
            # return arr
        return None
    str2arr_udf = udf(lambda str : string2array(str),StringType())
    ss.udf.register("str2arr", string2array)




