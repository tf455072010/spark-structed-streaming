# -*- coding: utf-8 -*-
import threading
import time
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from ctutil.sourcerpc import error
from ctutil.sourcerpc.tprotocol.enumserver.EnumsService import EnumsService

mutext_lock = threading.Semaphore(value=1)
SERVICE_NAME = "EnumsService"


class EnumClient:
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
        self.__client = EnumsService.Client(tMultiplexedProtocol)
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

    def all_enums(self, key):
        '''
        获取所有游戏  处理逻辑
        '''

        listprotocol = self.__getclient().allEnums(key)
        games = []
        if not listprotocol:
            return games
        for protoc in listprotocol:
            print(protoc)


    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
