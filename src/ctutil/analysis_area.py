import re
import socket
import struct as ip_struct
import traceback

from ctutil import iputil


def ipaddr_handle(ipv4, ipv6):
    '''
    udf处理入口

    :param  ipv4:   str     ipv4地址
    :param  ipv6:   str     ipv6地址

    :return:    bigint iplog
    '''
    if not iputil.is_ipv4(ipv4):
        return 0
    return iputil.ip2long(ipv4)


def address_split(address):
    '''
    udf处理入口

    :param  address:    str     详细地址

    :return: (province_name, city_name, district_name)
    '''
    if not address:
        return None, None, None

    chartered_cities = ["北京", "上海", "天津", "重庆", "香港", "澳门"]
    for city in chartered_cities:
        if city in address:
            address = address.replace(city, city + "省" + city, 1)
            break
    split_items = ['省', '市', '特别行政区', '自治区',
                   '自治县', '县区', '区县', '县', '区', '旗', '市']

    items = []
    addr_tmp = address
    for item in split_items:
        if item in addr_tmp:
            addr_tmp_ = addr_tmp.replace(item, ",", 1)
            items_ = addr_tmp_.split(',')
            items.append(items_[0])
            addr_tmp = items_[1]
    items.append(addr_tmp)

    if len(items) >= 3:
        return items[0], items[1], items[2]

    if len(items) >= 2:
        return items[0], items[1], None

    return None, None, None


def areaname_handle(area_name):
    if not area_name:
        return area_name

    split_items = ['省', '市', '自治区', '自治县', '特别行政区', '县区', '区县', '县', '区', '旗']
    for item in split_items:
        if area_name.endswith(item):
            return area_name[:-1 * len(item)]
    return area_name


def ip2area(iplong, ips_source):
    ips = ips_source

    def bst_search(array, index_l, index_r, value):
        if index_l == index_r:
            return None

        index = int((index_l + index_r) / 2)
        index_pre = index - 1 if index - 1 >= 0 else 0
        index_next = index + 1 if index + \
            1 <= len(array) - 1 else len(array) - 1

        if array[index][0] <= value:
            if array[index_next][0] >= value:
                return array[index_next]
            return bst_search(array, index + 1, index_r, value)
        else:
            if array[index_pre][0] <= value:
                return array[index]
            return bst_search(array, index_l, index, value)

    area_info = bst_search(ips, 0, len(ips) - 1, iplong)
    if area_info:
        return [
            area_info[1],
            area_info[2],
            area_info[3],
            area_info[4],
            None,
            None
        ]

    return [
        None,
        None,
        None,
        None,
        None,
        None
    ]


def handle(address, group_id, ipv4, ipv6, ips_source, region_source, group_source):
    '''解析地区'''

    if group_id and group_id > 0:
        area_info = group_source.get(group_id)
        if area_info and area_info[2] and int(area_info[2]) > 0:
            return [
                area_info[0],
                area_info[1],
                area_info[2],
                area_info[3],
                area_info[4],
                area_info[5]
            ]
    if address:
        region = region_source
        province_name, city_name, district_name = address_split(address)
        area_info = region.get("{}_{}_{}".format(
            province_name, city_name, district_name))
        if area_info:
            return [
                area_info["province_code"],
                area_info["province_name"],
                area_info["city_code"],
                area_info["city_name"],
                area_info["district_code"],
                area_info["district_name"]
            ]
        area_info = region.get("{}_{}".format(province_name, city_name))
        if area_info:
            return [
                area_info["province_code"],
                area_info["province_name"],
                area_info["city_code"],
                area_info["city_name"],
                None,
                None
            ]
    if isinstance(ipv4, str) and iputil.is_ipv4(ipv4):
        area_info = ip2area(iputil.ip2long(ipv4), ips_source)
        if area_info:
            return area_info
    return [
        None,
        None,
        None,
        None,
        None,
        None
    ]
