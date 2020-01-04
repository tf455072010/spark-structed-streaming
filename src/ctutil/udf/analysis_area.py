from ctutil import analysis_area
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, LongType, StringType

def load_broadcast_ips(ss, logger):
    '''
    加载广播变量(ip解析源)
    '''

    ips_df = ss.sql(
        "select ip_start, ip_end, province_code, province_name, city_code, city_name from dwd.dim_ip_area")
    ips = []
    for row in ips_df.collect():
        ips.append((row["ip_start"], row["province_code"],
                    row["province_name"], row["city_code"], row["city_name"]))
        ips.append((row["ip_end"], row["province_code"],
                    row["province_name"], row["city_code"], row["city_name"]))
    ips.sort(key=lambda k: k[0], reverse=False)
    logger.info("当前获取源：{} 条".format(len(ips)), event="load_broadcast_ips")
    return ips

def load_broadcast_region(ss, logger):
    '''加载广播变量（地区信息）'''
    region_df = ss.sql(
        "select province_code, province_name, city_code, city_name, district_code, district_name from dwd.dim_region_dict")
    region = {}
    for row in region_df.collect():
        if not row["city_code"]:
            continue
        province_name_ = analysis_area.areaname_handle(row["province_name"])
        city_name_ = analysis_area.areaname_handle(row["city_name"])
        if not row["district_code"]:
            region["{}_{}".format(province_name_, city_name_)] = {
                "province_code": row["province_code"],
                "province_name": row["province_name"],
                "city_code": row["city_code"],
                "city_name": row["city_name"],
                "district_code": "",
                "district_name": ""
            }
        else:
            district_name_ = analysis_area.areaname_handle(row["district_name"])
            region["{}_{}_{}".format(province_name_, city_name_, district_name_)] = {
                "province_code": row["province_code"],
                "province_name": row["province_name"],
                "city_code": row["city_code"],
                "city_name": row["city_name"],
                "district_code": row["district_code"],
                "district_name": row["district_name"],
            }
    logger.info("当前获取源：{} 条".format(len(region)), event="load_broadcast_region")
    return region


def load_broadcast_group(ss, logger):
    '''加载广播变量（大厅对应地区信息）'''
    region_df = ss.sql("select hall_id, province_code, province_name, city_code, city_name, district_code, district_name from dwd.dim_group_dict where hall_id is not null ")
    region = {}
    for row in region_df.collect():
        hall_id = row['hall_id']
        province_code = row['province_code']
        city_code = row['city_code']
        district_code = row['district_code']
        province_name = row["province_name"]
        city_name = row["city_name"]
        district_name = row["district_name"]
        region[hall_id] = [province_code, province_name, city_code, city_name, district_code, district_name]
    logger.info("当前获取源：{} 条".format(len(region)), event="load_broadcast_region")
    return region    



def regist_udf(ss, logger):
    '''地区解析'''
    broadcast_ips = ss.sparkContext.broadcast(load_broadcast_ips(ss, logger))
    broadcast_region = ss.sparkContext.broadcast(load_broadcast_region(ss, logger))
    broadcast_group = ss.sparkContext.broadcast(load_broadcast_group(ss, logger))

    def handle(address, groupid, ipv4, ipv6, ips_source, region_source, group_source):
        return analysis_area.handle(address, groupid, ipv4, ipv6, ips_source.value, region_source.value, group_source.value)

    logger.info("注册analysis_area_udf UDF", event="regist_udf")
    analysis_area_udf = udf(lambda address, groupid, ipv4, ipv6: handle(address, groupid, ipv4, ipv6, broadcast_ips, broadcast_region, broadcast_group), ArrayType(StringType()))
    ss.udf.register("analysis_area_udf", analysis_area_udf)
    return analysis_area_udf
