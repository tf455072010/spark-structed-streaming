# coding=utf-8
import threading
import time

from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from ctutil.sourcerpc import error
from ctutil.sourcerpc.tprotocol.areaserver.AreaService import AreaService
from ctutil.sourcerpc.util import format_checker, iputils, lock, mem

mutext_lock = threading.Semaphore(value=1)
SERVICE_NAME = "AreaService"


class AreaClient:
    '''
    地区服务客户端实现类
    '''

    def __init__(self, host, port, authkey, timeout=100000000):
        self.__host = host
        self.__port = port
        self.__timeout = timeout
        self.__authkey = authkey

        self.__connect()
        self.__authrize()

    def close(self):
        '''
        关闭thrift链接
        '''
        if self.__transport:
            self.__transport.close()
        self.__client = None
        self.__transport = None
 
    def __connect(self):
        '''
        创建客户端链接
        '''

        self.__transport = TSocket.TSocket(host=self.__host, port=self.__port)
        self.__transport.setTimeout(self.__timeout)
        self.__transport = TTransport.TFramedTransport(self.__transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.__transport)
        tMultiplexedProtocol = TMultiplexedProtocol.TMultiplexedProtocol(
            protocol, SERVICE_NAME)
        self.__client = AreaService.Client(tMultiplexedProtocol)
        self.__transport.open()
        self.__connectts = time.time() * 1000

    def __authrize(self):
        '''
        验证帐号
        '''

        if not self.__getclient().authorize(self.__authkey):
            raise error.AuthenticationError()

    def __getclient(self):
        '''
        获取thrift客户端
        '''

        nowts = time.time() * 1000

        @lock.auto_shared_lock(mutext_lock)
        def __connect_handle():
            nowts = time.time() * 1000
            if not self.__client or not self.__transport or not self.__transport.isOpen or nowts - self.__connectts >= self.__timeout:
                self.__connect()
                self.__authrize()

        if not self.__client or not self.__transport or not self.__transport.isOpen or nowts - self.__connectts >= self.__timeout:
            __connect_handle()
        if self.__client:
            return self.__client
        raise error.InvalidClientError()

    def ip2area(self, ipaddr):
        '''
        ip转化成地区信息

        Args：
            ipaddr  string  ip地址(122.224.230.90)
        Returns：
            {
                "provinceID":"06", 
                "provinceName":"浙江省",
                "cityID":"0601",            #没有地级市就没有这个字段
                "cityName":"杭州市",         #没有地级市就没有这个字段
                "districtID":"060101",      #没有县区就没有这个字段
                "districtName":"上城区"      #没有县区就没有这个字段
            }
        '''

        if not isinstance(ipaddr, str) or not format_checker.is_ipv4(ipaddr):
            raise error.InvalidValueError("无效的ip：%s" % str(ipaddr))

        protoc = self.__getclient().ip2area(ipaddr)
        if not protoc or not protoc.provinceID:
            return None
        area = {"provinceID": protoc.provinceID,
                "provinceName": protoc.provinceName}
        if protoc.cityID:
            area["cityID"] = protoc.cityID
            area["cityName"] = protoc.cityName
        else:
            return area
        if protoc.districtID:
            area["districtID"] = protoc.districtID
            area["districtName"] = protoc.districtName
        return area

    def ips2area(self, listip):
        '''
        批量ip转化成地区信息

        Args：
            listip  array<string>  ip地址列表[122.224.230.90, 122.224.230.91]
        Returns：
            dict
        {
            "122.224.230.90": {
                "provinceID":"06",
                "provinceName":"浙江省",
                "cityID":"0601",            #没有地级市就没有这个字段
                "cityName":"杭州市",         #没有地级市就没有这个字段
                "districtID":"060101",      #没有县区就没有这个字段
                "districtName":"上城区"      #没有县区就没有这个字段
            },"122.224.230.91": {
                "provinceID":"06",
                "provinceName":"浙江省",
                "cityID":"0601",            #没有地级市就没有这个字段
                "cityName":"杭州市",         #没有地级市就没有这个字段
                "districtID":"060101",      #没有县区就没有这个字段
                "districtName":"上城区"      #没有县区就没有这个字段
            }
        }
        '''

        if not isinstance(listip, list) and not isinstance(listip, tuple):
            raise error.InvalidValueError("无效的ip列表")
        ips = []
        for ipaddr in listip:
            if not isinstance(ipaddr, str) or not format_checker.is_ipv4(ipaddr):
                raise error.InvalidValueError("无效的ip：%s" % str(ipaddr))
            ips.append(ipaddr)

        protocs = self.__getclient().ips2area(ips)
        result = {}
        if not protocs or len(protocs) == 0:
            return None
        for ipaddr, protoc in protocs.items():
            area = None
            if protoc and protoc.provinceID:
                area = {"provinceID": protoc.provinceID,
                        "provinceName": protoc.provinceName}
                if protoc.cityID:
                    area["cityID"] = protoc.cityID
                    area["cityName"] = protoc.cityName
                elif protoc.districtID:
                    area["districtID"] = protoc.districtID
                    area["districtName"] = protoc.districtName
            result[ipaddr] = area
        return result

    def listprovinces(self):
        '''
        获取所有省份列表

        Returns：
            Array
            [
                {"provinceID":"06", "provinceName":"浙江"},
                {"provinceID":"01", "provinceName":"北京"},
            ]
        '''

        listprotoc = self.__getclient().listProvinces()
        provinces = []
        if not listprotoc:
            return provinces
        for protoc in listprotoc:
            province = {"provinceID": protoc.provinceID,
                        "provinceName": protoc.provinceName}
            provinces.append(province)
        return provinces

    def getprovince(self, provinceID):
        '''
        根据省份ID获取省份信息

        Returns：
            {"provinceID":"06", "provinceName":"浙江"}
        '''

        protoc = self.__getclient().getProvince(provinceID)
        if not protoc or not protoc.provinceID:
            return None
        province = {"provinceID": protoc.provinceID,
                    "provinceName": protoc.provinceName}
        return province

    def listcities(self):
        '''
        获取所有地级市列表

        Returns：
            Array
            [
                {
                    "provinceID":"06",
                    "provinceName":"浙江",
                    "cityID":"0601",
                    "cityName":"杭州"
                },
                {
                    "provinceID":"01",
                    "provinceName":"北京"
                    "cityID":"0101",
                    "cityName":"北京"
                },
            ]
        '''

        listprotoc = self.__getclient().listCities()
        cities = []
        if not listprotoc:
            return cities
        for protoc in listprotoc:
            city = {"provinceID": protoc.provinceID, "provinceName": protoc.provinceName, "cityID": protoc.cityID,
                    "cityName": protoc.cityName}
            cities.append(city)
        return cities

    @mem.autocache("CTDC.SOURCERPC.AREA.CITIES", 90000)  # 缓存25小时
    def __list_cities(self):
        '''
        获取所有地级市列表

        Returns：
            Array
            [
                {
                    "provinceID":"06",
                    "provinceName":"浙江",
                    "cityID":"0601",
                    "cityName":"杭州"
                },
                {
                    "provinceID":"01",
                    "provinceName":"北京"
                    "cityID":"0101",
                    "cityName":"北京"
                },
            ]
        '''

        return self.listcities()

    def getcity(self, cityID):
        '''
        根据地级市ID获取地级市信息

        Returns：
            {
                "provinceID":"06",
                "provinceName":"浙江",
                "cityID":"0601",
                "cityName":"杭州"
            }
        '''

        protoc = self.__getclient().getCity(cityID)
        if not protoc or not protoc.cityID:
            return None
        city = {"provinceID": protoc.provinceID, "provinceName": protoc.provinceName, "cityID": protoc.cityID,
                "cityName": protoc.cityName}
        return city

    def listdistricts(self):
        '''
        获取所有县区列表

        Returns：
            Array
            [
                {
                    "provinceID":"06",
                    "provinceName":"浙江",
                    "cityID":"0601",
                    "cityName":"杭州"
                    "districtID":"060101",
                    "districtName":"上城区"
                },
                {
                    "provinceID":"01",
                    "provinceName":"北京"
                    "cityID":"0101",
                    "cityName":"北京"
                    "districtID":"0101",
                    "districtName":"北京"
                }
            ]
        '''

        listprotoc = self.__getclient().listDistricts()
        districts = []
        if not listprotoc:
            return districts
        for protoc in listprotoc:
            district = {"provinceID": protoc.provinceID, "provinceName": protoc.provinceName, "cityID": protoc.cityID,
                        "cityName": protoc.cityName, "districtID": protoc.districtID,
                        "districtName": protoc.districtName}
            districts.append(district)
        return districts

    def getdistrict(self, districtID):
        '''
        根据县区ID获取县区信息

        Returns：
                {
                    "provinceID":"06",
                    "provinceName":"浙江",
                    "cityID":"0601",
                    "cityName":"杭州",
                    "districtID":"060101",
                    "districtName":"上城区"
                }
        '''

        protoc = self.__getclient().getDistrict(districtID)
        if not protoc or not protoc.districtID:
            return None
        district = {"provinceID": protoc.provinceID, "provinceName": protoc.provinceName, "cityID": protoc.cityID,
                    "cityName": protoc.cityName, "districtID": protoc.districtID, "districtName": protoc.districtName}
        return district

    def address2area(self, province, city=None, district=None):
        '''
        地区名称转化成地区信息

        Args：
            province    string  省份信息
            city        string  地级市信息
            district    string  县区信息
        Returns：
            {
                "provinceID":"06",
                "provinceName":"浙江省",
                "cityID":"0601",            #没有地级市就没有这个字段
                "cityName":"杭州市",         #没有地级市就没有这个字段
                "districtID":"060101",      #没有县区就没有这个字段
                "districtName":"上城区"      #没有县区就没有这个字段
            }
        '''
        if not province:
            province = ""
        if not city:
            city = ""
        if not district:
            district = ""
        protoc = self.__getclient().address2area(province, city, district)
        if not protoc or not protoc.provinceID:
            return None
        area = {"provinceID": protoc.provinceID,
                "provinceName": protoc.provinceName}
        if protoc.cityID:
            area["cityID"] = protoc.cityID
            area["cityName"] = protoc.cityName
        if protoc.districtID:
            area["districtID"] = protoc.districtID
            area["districtName"] = protoc.districtName
        return area

    def loc2area(self, lng, lat):
        '''
        经纬度转化成地区信息

        Args：
            lng    double  经度
            lat    double  纬度
        Returns：
            {
                "provinceID":"06",
                "provinceName":"浙江省",
                "cityID":"0601",            #没有地级市就没有这个字段
                "cityName":"杭州市",         #没有地级市就没有这个字段
                "districtID":"060101",      #没有县区就没有这个字段
                "districtName":"上城区"      #没有县区就没有这个字段
            }
        '''

        if not isinstance(lng, float) or not isinstance(lat, float):
            raise error.InvalidValueError("无效的经纬度信息")
        protoc = self.__getclient().loc2area(lng, lat)
        if not protoc or not protoc.provinceID:
            return None
        area = {"provinceID": protoc.provinceID,
                "provinceName": protoc.provinceName}
        if protoc.cityID:
            area["cityID"] = protoc.cityID
            area["cityName"] = protoc.cityName
        if protoc.districtID:
            area["districtID"] = protoc.districtID
            area["districtName"] = protoc.districtName
        return area

    def ip2area_(self, ipaddr):
        '''
        ip转化成地区信息(加速版，会格外消耗客户端内存和cpu资源)

        Args：
            ipaddr  string  ip地址(122.224.230.90)
        Returns：
            {
                "provinceID":"06",
                "provinceName":"浙江省",
                "cityID":"0601",            #没有地级市就没有这个字段
                "cityName":"杭州市",         #没有地级市就没有这个字段
                "districtID":"060101",      #没有县区就没有这个字段
                "districtName":"上城区"      #没有县区就没有这个字段
            }
        '''

        if not isinstance(ipaddr, str) or not format_checker.is_ipv4(ipaddr):
            raise error.InvalidValueError("无效的ip：%s" % str(ipaddr))

        iplong = iputils.ip2long(ipaddr)

        ips = self.__listip()

        def bst_search(array, index_l, index_r, value):
            if index_l == index_r:
                return None

            index = int((index_l + index_r) / 2)
            index_pre = index - 1 if index - 1 >= 0 else 0
            index_next = index + 1 if index + \
                1 <= len(array) - 1 else len(array) - 1

            if array[index][0] <= value:
                if array[index_next][0] >= value:
                    return array[index_next][1]
                return bst_search(array, index + 1, index_r, value)
            else:
                if array[index_pre][0] <= value:
                    return array[index][1]
                return bst_search(array, index_l, index, value)

        cityid = bst_search(ips, 0, len(ips) - 1, iplong)

        @mem.autocache("CTDC.SOURCERPC.CITIES.DICT", 90000000)  # 缓存25小时
        def __all_city_dict():
            return {city["cityID"]: city for city in self.__list_cities()}

        if cityid and cityid in __all_city_dict():
            return __all_city_dict()[cityid]
        return None

    @mem.autocache("CTDC.SOURCERPC.AREA.IPS", 90000000)  # 缓存25小时
    @lock.auto_shared_lock(mutext_lock)
    @mem.autocache("CTDC.SOURCERPC.AREA.IPS", 90000000)  # 缓存25小时
    def __listip(self):
        '''
        获取ip列表

        Returns：
        [
            (0, "0101"),
            {1, "0201"}
        ]
        '''
        protocs = self.__getclient().listIp()
        if not protocs:
            raise error.InvalidValueError("无效的IP列表")
        ips_dict = {}
        for protoc in protocs:
            ips_dict[protoc.ipStart] = protoc.cityID
            ips_dict[protoc.ipEnd] = protoc.cityID
        ips = sorted(ips_dict.items(), key=lambda item: item[0])
        return ips

    def listip(self):
        '''
        获取ip列表

        Returns：
        [
            (0, "0101"),
            {1, "0201"}
        ]
        '''

        protocs = self.__getclient().listIp()
        if not protocs:
            raise error.InvalidValueError("无效的IP列表")
        ips = []
        for protoc in protocs:
            item = (protoc.ipStart, protoc.ipEnd, protoc.cityID)
            ips.append(item)
        return ips

    def __enter__(self):
        return self

    def __exit__(self, *exc_info): 
        self.close()
