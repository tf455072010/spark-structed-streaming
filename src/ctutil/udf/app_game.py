from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType


def load_broadcast_game_app(ss, logger):
    '''
    加载应用游戏字典表
    '''
    df = ss.sql(
        'SELECT game_id,app_id from dwd.dim_app_game_dict GROUP BY game_id,app_id')
    data = {row['game_id']: row['app_id'] for row in df.collect()}
    logger.info("当前获取数据：{}".format(len(data)), event='load_broadcast_game_app')
    return data


def regist_gameid2appid_udf(ss, logger):
    '''
    从资源库中通过key查找value
    '''
    broadcast_game_app = ss.sparkContext.broadcast(
        load_broadcast_game_app(ss, logger))

    def gameid2appid(gameid, source):
        return source.value.get(gameid)

    logger.info("注册gameid2appid_udf UDF", event="regist_udf")
    gameid2appid_udf = udf(lambda gameid: gameid2appid(
        gameid, broadcast_game_app), IntegerType())
    ss.udf.register("gameid2appid_udf", gameid2appid_udf)
    return gameid2appid_udf
