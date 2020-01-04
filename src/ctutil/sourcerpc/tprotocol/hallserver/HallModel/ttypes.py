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


class HallProtoc(object):
    """
    大厅结构体


    Attributes:
     - hallid
     - hallname
     - province
     - city
     - district
    """

    thrift_spec = None

    def __init__(self, hallid=None, hallname=None, province=None, city=None, district=None,):
        self.hallid = hallid
        self.hallname = hallname
        self.province = province
        self.city = city
        self.district = district

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
                    self.hallid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == -2:
                if ftype == TType.STRING:
                    self.hallname = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -3:
                if ftype == TType.STRING:
                    self.province = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -4:
                if ftype == TType.STRING:
                    self.city = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == -5:
                if ftype == TType.STRING:
                    self.district = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
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
        oprot.writeStructBegin('HallProtoc')
        if self.district is not None:
            oprot.writeFieldBegin('district', TType.STRING, -5)
            oprot.writeString(self.district.encode('utf-8') if sys.version_info[0] == 2 else self.district)
            oprot.writeFieldEnd()
        if self.city is not None:
            oprot.writeFieldBegin('city', TType.STRING, -4)
            oprot.writeString(self.city.encode('utf-8') if sys.version_info[0] == 2 else self.city)
            oprot.writeFieldEnd()
        if self.province is not None:
            oprot.writeFieldBegin('province', TType.STRING, -3)
            oprot.writeString(self.province.encode('utf-8') if sys.version_info[0] == 2 else self.province)
            oprot.writeFieldEnd()
        if self.hallname is not None:
            oprot.writeFieldBegin('hallname', TType.STRING, -2)
            oprot.writeString(self.hallname.encode('utf-8') if sys.version_info[0] == 2 else self.hallname)
            oprot.writeFieldEnd()
        if self.hallid is not None:
            oprot.writeFieldBegin('hallid', TType.I32, -1)
            oprot.writeI32(self.hallid)
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