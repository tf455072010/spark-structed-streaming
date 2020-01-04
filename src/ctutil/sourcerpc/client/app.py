# -*- coding: utf-8 -*-
import threading
import time
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from ctutil.sourcerpc import error
from ctutil.sourcerpc.tprotocol.appserver.AppService import AppService

mutext_lock = threading.Semaphore(value=1)
SERVICE_NAME = "AppService"


class AppClient:
    '''
   应用游戏服务客户端实现类
    '''

    def __init__(self, host, port, authkey, timeout=100000000):
        self.__host =host
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
        tMultiplexedProtocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, SERVICE_NAME)
        self.__client = AppService.Client(tMultiplexedProtocol)
        self.__transport.open()
        self.__connectts = time.time() * 1000

    def __authrize(self):
        '''
        验证帐号
        '''

        if not self.__getclient().authorization(self.__authkey):
            raise error.AuthenticationError()

    def __getclient(self):
        '''
        获取thrift客户端
        '''
        if not self.__client:
            self.__connect()
        if self.__client:
            return self.__client
        raise error.InvalidClientError()

    def listgame(self):
        '''
        获取所有游戏  处理逻辑
        '''

        listprotocol = self.__getclient().allgames()
        games = []
        if not listprotocol:
            return games
        for protoc in listprotocol:
            # game: id=7000255, name='萌将三国', code='mjsgsy', clazz=0
            id = protoc.id
            name = protoc.name
            code = protoc.code
            clazz = protoc.clazz
            game = {'id':id, 'name':name, 'code':code, 'clazz':clazz}
            games.append(game)
        return games

    def listmapp(self):
        listprotocol = self.__getclient().allmapps()
        apps = []
        if not listprotocol:
            return apps
        for protoc in listprotocol:
            # appid=1880106, gameid=106, platform=0, appname='茂名拖拉机', gamecode='mmsh', type=2, appcode='mmsh'
            appid = protoc.appid
            name = ""
            for protoc2 in listprotocol:
                if protoc2.appid == appid:
                    name = name + "|" + protoc2.appname if name else protoc2.appname
            app = {"appid": protoc.appid, "appcode": protoc.appcode, "appname": protoc.appname, "gameid": protoc.gameid,
                   "gamecode": protoc.gamecode, "type": protoc.type, "platform": protoc.platform, "joinname": name, }
            apps.append(app)
        return apps

    def listcode(self):
        '''
        获取所有缩写
        Returns：
            Array
            [
                {
                    "code": "asdf",
                    "playtype": 1,
                    "appname": "aaaaaa",
                    "packagename": "asdasd.asdasds",
                    "os": 1,
                },
                {
                    "code": "asdf",
                    "playtype": 2,
                    "appname": "aaaaaa",
                    "packagename": "asdasd.asdasds",
                    "os": 1,
                }
            ]
        '''
        listprotocol = self.__getclient().allcode()
        codes = []
        if not listprotocol:
            return codes
        for protoc in listprotocol:
            code = {"code": protoc.code, "playtype": protoc.playtype, "appname": protoc.appname,
                    "packagename": protoc.packagename, "os": protoc.os, }
            codes.append(code)
        return codes

    def listyaodougame(self):
        '''
        '''
        listprotocol = self.__getclient().allyaodougame()
        games = []
        if not listprotocol:
            return games
        for protoc in listprotocol:
            gameid = protoc.gameid
            gamepinyin = protoc.gamepinyin
            gamename = protoc.gamename
            game = {'gameid':gameid, 'gamepinyin':gamepinyin, 'gamename':gamename}
            games.append(game)
        return games

    def listjointapp(self):
        listprotocol = self.__getclient().alljointapp()
        games = []
        if not listprotocol:
            return games
        for protoc in listprotocol:
            # appid=7000126, appcode='zjzesy', appname='终结者2：审判日', hallgameid=7000126
            appid = protoc.appid
            appcode = protoc.appcode
            appname = protoc.appname
            hallgameid = protoc.hallgameid
            game = ({'appid':appid, 'appcode':appcode, 'appname':appname, 'hallgameid':hallgameid})
            games.append(game)
        return games

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
