# -*- coding: utf-8 -*-
import threading
import time

from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from ctutil.sourcerpc import error
from ctutil.sourcerpc.tprotocol.gameservice.UnifyGameService import UnifyGameService
from ctutil.sourcerpc.util import format_checker, iputils, lock, mem

mutext_lock = threading.Semaphore(value=1)
SERVICE_NAME = "GameService"


class GameClient:
    '''
   应用游戏服务客户端实现类
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
        tMultiplexedProtocol = TMultiplexedProtocol.TMultiplexedProtocol(protocol, SERVICE_NAME)
        self.__client = UnifyGameService.Client(tMultiplexedProtocol)
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
        Returns：
            Array
            [
                {
                    "appId":"234",
                    "classID":"xx游戏",
                    "codeName":"lagt",
                    "gameCost":"1",
                    "countyID":"aaa|bbbb",
                    "gameID":"1",
                    "gameKind":"1",
                    "gameName":"1",
                    "osType":"1",
                    "publishKind":"1",
                    "terminalMode":"1",
                    "gameMode":"1",
                },
            ]
        '''

        listprotocol = self.__getclient().allGames()
        games = []
        if not listprotocol:
            return games
        for protoc in listprotocol:
            app_id = protoc.appId
            class_id = protoc.classID
            game_code = protoc.codeName
            county_id = protoc.countyID
            game_id = protoc.gameID
            game_name = protoc.gameName
            os_type = protoc.osType
            game_kind = protoc.gameKind
            publish_kind = protoc.publishKind
            terminal_mode = protoc.terminalMode
            game_mode = protoc.gameMode
            game = (app_id, class_id, game_code, county_id,
                    game_id, game_name, os_type, game_kind,
                    publish_kind, terminal_mode, game_mode)
            games.append(game)
        return games

    def listmapp(self):
        '''
        获取所有应用
        Returns：
            Array
            [
                {
                    "appId":"234",
                    "classID":"xx游戏",
                    "codeName":"lagt",
                    "gameCost":"1",
                    "countyID":"aaa|bbbb",
                    "gameID":"1",
                    "gameKind":"1",
                    "gameName":"1",
                    "osType":"1",
                    "publishKind":"1",
                    "terminalMode":"1",
                    "gameMode":"1",
                },
            ]
        '''
        listprotocol = self.__getclient().allGames()
        apps = []
        if not listprotocol:
            return apps
        for protoc in listprotocol:
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

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
