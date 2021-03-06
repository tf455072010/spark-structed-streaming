#
# Autogenerated by Thrift Compiler (0.10.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
import sys

from thrift.transport import TTransport


class GameProtoc(object):
    """
    游戏结构体


    Attributes:
     - id
     - name
     - code
     - clazz
    """

    thrift_spec = None

    def __init__(self, id=None, name=None, code=None, clazz=None,):
        self.id = id
        self.name = name
        self.code = code
        self.clazz = clazz

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.I32:
                    self.id = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -2:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -3:
                if ftype == TType.STRING:
                    self.code = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -4:
                if ftype == TType.I32:
                    self.clazz = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('GameProtoc')
        if self.clazz is not None:
            oprot.writeFieldBegin('clazz', TType.I32, -4)
            oprot.writeI32(self.clazz)
            oprot.writeFieldEnd()
        if self.code is not None:
            oprot.writeFieldBegin('code', TType.STRING, -3)
            oprot.writeString(self.code.encode('utf-8') if sys.version_info[0] == 2 else self.code)
            oprot.writeFieldEnd()
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, -2)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I32, -1)
            oprot.writeI32(self.id)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class AppProtoc(object):
    """
    移动应用结构体


    Attributes:
     - appid
     - gameid
     - platform
     - appname
     - gamecode
     - type
     - appcode
    """

    thrift_spec = None

    def __init__(self, appid=None, gameid=None, platform=None, appname=None, gamecode=None, type=None, appcode=None,):
        self.appid = appid
        self.gameid = gameid
        self.platform = platform
        self.appname = appname
        self.gamecode = gamecode
        self.type = type
        self.appcode = appcode

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.I64:
                    self.appid = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == -2:
                if ftype == TType.I32:
                    self.gameid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -3:
                if ftype == TType.I32:
                    self.platform = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -4:
                if ftype == TType.STRING:
                    self.appname = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -5:
                if ftype == TType.STRING:
                    self.gamecode = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -6:
                if ftype == TType.I32:
                    self.type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -7:
                if ftype == TType.STRING:
                    self.appcode = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('AppProtoc')
        if self.appcode is not None:
            oprot.writeFieldBegin('appcode', TType.STRING, -7)
            oprot.writeString(self.appcode.encode('utf-8') if sys.version_info[0] == 2 else self.appcode)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.I32, -6)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        if self.gamecode is not None:
            oprot.writeFieldBegin('gamecode', TType.STRING, -5)
            oprot.writeString(self.gamecode.encode('utf-8') if sys.version_info[0] == 2 else self.gamecode)
            oprot.writeFieldEnd()
        if self.appname is not None:
            oprot.writeFieldBegin('appname', TType.STRING, -4)
            oprot.writeString(self.appname.encode('utf-8') if sys.version_info[0] == 2 else self.appname)
            oprot.writeFieldEnd()
        if self.platform is not None:
            oprot.writeFieldBegin('platform', TType.I32, -3)
            oprot.writeI32(self.platform)
            oprot.writeFieldEnd()
        if self.gameid is not None:
            oprot.writeFieldBegin('gameid', TType.I32, -2)
            oprot.writeI32(self.gameid)
            oprot.writeFieldEnd()
        if self.appid is not None:
            oprot.writeFieldBegin('appid', TType.I64, -1)
            oprot.writeI64(self.appid)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TcyappAppProtoc(object):
    """
    同城游移动应用结构体


    Attributes:
     - code
     - playtype
     - appname
     - packagename
     - os
    """

    thrift_spec = None

    def __init__(self, code=None, playtype=None, appname=None, packagename=None, os=None,):
        self.code = code
        self.playtype = playtype
        self.appname = appname
        self.packagename = packagename
        self.os = os

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.STRING:
                    self.code = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -2:
                if ftype == TType.I32:
                    self.playtype = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -3:
                if ftype == TType.STRING:
                    self.appname = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -4:
                if ftype == TType.STRING:
                    self.packagename = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -5:
                if ftype == TType.I32:
                    self.os = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('TcyappAppProtoc')
        if self.os is not None:
            oprot.writeFieldBegin('os', TType.I32, -5)
            oprot.writeI32(self.os)
            oprot.writeFieldEnd()
        if self.packagename is not None:
            oprot.writeFieldBegin('packagename', TType.STRING, -4)
            oprot.writeString(self.packagename.encode('utf-8') if sys.version_info[0] == 2 else self.packagename)
            oprot.writeFieldEnd()
        if self.appname is not None:
            oprot.writeFieldBegin('appname', TType.STRING, -3)
            oprot.writeString(self.appname.encode('utf-8') if sys.version_info[0] == 2 else self.appname)
            oprot.writeFieldEnd()
        if self.playtype is not None:
            oprot.writeFieldBegin('playtype', TType.I32, -2)
            oprot.writeI32(self.playtype)
            oprot.writeFieldEnd()
        if self.code is not None:
            oprot.writeFieldBegin('code', TType.STRING, -1)
            oprot.writeString(self.code.encode('utf-8') if sys.version_info[0] == 2 else self.code)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class YaodouGameProtoc(object):
    """
    妖豆游戏游戏列表结构体


    Attributes:
     - gameid
     - gamename
     - gamepinyin
    """

    thrift_spec = None

    def __init__(self, gameid=None, gamename=None, gamepinyin=None,):
        self.gameid = gameid
        self.gamename = gamename
        self.gamepinyin = gamepinyin

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.I32:
                    self.gameid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -2:
                if ftype == TType.STRING:
                    self.gamename = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -3:
                if ftype == TType.STRING:
                    self.gamepinyin = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('YaodouGameProtoc')
        if self.gamepinyin is not None:
            oprot.writeFieldBegin('gamepinyin', TType.STRING, -3)
            oprot.writeString(self.gamepinyin.encode('utf-8') if sys.version_info[0] == 2 else self.gamepinyin)
            oprot.writeFieldEnd()
        if self.gamename is not None:
            oprot.writeFieldBegin('gamename', TType.STRING, -2)
            oprot.writeString(self.gamename.encode('utf-8') if sys.version_info[0] == 2 else self.gamename)
            oprot.writeFieldEnd()
        if self.gameid is not None:
            oprot.writeFieldBegin('gameid', TType.I32, -1)
            oprot.writeI32(self.gameid)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class JointAppProtoc(object):
    """
    手游列表结构体


    Attributes:
     - appid
     - appcode
     - appname
     - hallgameid
    """

    thrift_spec = None

    def __init__(self, appid=None, appcode=None, appname=None, hallgameid=None,):
        self.appid = appid
        self.appcode = appcode
        self.appname = appname
        self.hallgameid = hallgameid

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.I32:
                    self.appid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -2:
                if ftype == TType.STRING:
                    self.appcode = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -3:
                if ftype == TType.STRING:
                    self.appname = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -4:
                if ftype == TType.I32:
                    self.hallgameid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('JointAppProtoc')
        if self.hallgameid is not None:
            oprot.writeFieldBegin('hallgameid', TType.I32, -4)
            oprot.writeI32(self.hallgameid)
            oprot.writeFieldEnd()
        if self.appname is not None:
            oprot.writeFieldBegin('appname', TType.STRING, -3)
            oprot.writeString(self.appname.encode('utf-8') if sys.version_info[0] == 2 else self.appname)
            oprot.writeFieldEnd()
        if self.appcode is not None:
            oprot.writeFieldBegin('appcode', TType.STRING, -2)
            oprot.writeString(self.appcode.encode('utf-8') if sys.version_info[0] == 2 else self.appcode)
            oprot.writeFieldEnd()
        if self.appid is not None:
            oprot.writeFieldBegin('appid', TType.I32, -1)
            oprot.writeI32(self.appid)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
