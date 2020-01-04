from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType

CARD_TYPE = {
    "无": 0,
    "黑桃": 1,
    "梅花": 2,
    "方片": 3,
    "红心": 4,
    0: "无",
    1: "黑桃",
    2: "梅花",
    3: "方片",
    4: "红心"
}

CARD_VALUE = ["A", "2", "3", "4", "5", "6", "7", "8",
              "9", "10", "J", "Q", "K", "小王", "大王"]


def convert(card_type, card_val):
    '''
    牌信息转化

    :param  card_type:  string      花色
    :param  card_val:   string      牌值

    :return:    [string, string]      [明文, 编码]         
    '''

    if not card_type or not card_val:
        return ['', '']
    
    types = [t for t in card_type.split(",") if t]
    values = [int(v) for v in card_val.split(",") if v]

    items = ["小王", "大王"]
    for i in range(len(types)):
        for item in items:
            if item == types[i].strip():
                types[i] = "无"
                values[i] = CARD_VALUE.index(item) + 1

    cards_name = ["{}-{}".format(types[i], CARD_VALUE[values[i] - 1]) for i in range(len(types))]
    cards_value = ["{}-{}".format(CARD_TYPE[types[i]], values[i]) for i in range(len(types))]

    return [','.join(cards_name), ','.join(cards_value)]


def regist_udf(ss, logger):
    '''
    注册UDF
    
    :param  ss: spark session
    '''
    logger.info("注册cards_convert_udf UDF", event="regist_udf")
    cards_convert_udf = udf(lambda card_type, card_val: convert(card_type, card_val), ArrayType(StringType()))
    ss.udf.register("cards_convert_udf", cards_convert_udf)
    return cards_convert_udf