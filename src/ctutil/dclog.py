import json
import logging
import os
import platform
import socket
import sys
import time
import traceback
import config
from config import base

import ctutil

NAME2LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}

LEVEL2NAME = {
    logging.CRITICAL: 'CRITICAL',
    logging.ERROR: 'ERROR',
    logging.WARNING: 'WARNING',
    logging.INFO: 'INFO',
    logging.DEBUG: 'DEBUG',
    logging.NOTSET: 'NOTSET',
}


SOCK_ADDR = ("dclog2.tcy365.net", 9099)
SOCK_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LEVEL_LIMIT = logging.INFO

LOG_BASE_INFO = {
    "app": config.APPLICATION_NAME,
    "env": base.APPLICAITON_ENV,
    "vers": config.APPLICATION_VERS,
    "ctutil-vers":  ctutil.VERSION,
    "proj-type": "python",
    "py-vers": platform.python_version(),
    "applicationId": "unkown"
}

def set_app_info(app, env, vers, level_limit, applicationId=None):
    '''
    设置当前应用服务信息
    '''
    global LOG_BASE_INFO,  LEVEL_LIMIT
    LOG_BASE_INFO["app"] = app
    LOG_BASE_INFO["env"] = env
    LOG_BASE_INFO["vers"] = vers
    LOG_BASE_INFO["applicationId"] = applicationId if applicationId else "unkown"
    LEVEL_LIMIT = level_limit

def set_applicationId(applicationId):
    '''
    设置当前applicationId
    '''
    global LOG_BASE_INFO
    LOG_BASE_INFO["applicationId"] = applicationId if applicationId else "unkown"


def find_caller(srcfile):
    '''
    发现当前调用的堆栈信息
    '''
    def __current_frame():
        try:
            raise Exception()
        except:
            return sys.exc_info()[2].tb_frame.f_back.f_back.f_back

    frame = __current_frame()
    if frame:
        frame=frame.f_back
    fln = "(unkown file)",0,"(undown function)"
    while hasattr(frame, "f_code"):
        code = frame.f_code
        filename = os.path.normcase(code.co_filename)
        if filename == srcfile:
            frame = frame.f_back
            continue
        fln = (code.co_filename, frame.f_lineno, code.co_name)
        break
    return fln


class DcLogger:
    '''
    使用udp发送日志
    '''

    def __init__(self):
        self.__srcfile = os.path.normcase(self.__init__.__code__.co_filename)

    def notset(self, content,  event=None, **kwargs):
        self.__send(logging.NOTSET, content, event=event, **kwargs)

    def debug(self, content,  event=None, **kwargs):
        self.__send(logging.DEBUG, content, event=event, **kwargs)

    def info(self, content,  event=None, **kwargs):
        self.__send(logging.INFO, content, event=event, **kwargs)

    def warn(self, content,  event=None, **kwargs):
        self.__send(logging.WARNING, content, event=event, **kwargs)

    def error(self, content,  event=None, **kwargs):
        self.__send(logging.ERROR, content, event=event, **kwargs)

    def critical(self, content,  event=None, **kwargs):
        self.__send(logging.CRITICAL, content, event=event, **kwargs)

    def __send(self, level, content, event, **kwargs):
        '''
        发送日志

        Args:
            level   str     日志级别
            log     obj     日志内容
        '''
        if not SOCK_UDP:
            return

        if level < LEVEL_LIMIT:
            return

        message = LOG_BASE_INFO.copy()
        message.update({
            "level": LEVEL2NAME[level].lower().replace("ing", ''),
        })
        if isinstance(content, str):
            message["content"] = content
        elif isinstance(content, dict):
            try:
                message["content"] = json.dumps(content)
            except:
                message["content"] = "failed to json_dumps!!"
        else:
            message["content"] = ""

        if isinstance(event, str):
            message["event"] = event
        else:
            return

        co_filename, f_lineno, co_name = find_caller(self.__srcfile)

        message["srcfile"] = co_filename
        message["lineno"] = f_lineno
        message["defname"] = co_name

        for key in kwargs:
            filed = str(key).lower()
            if filed in ["num", "duration"] and (
                    isinstance(kwargs.get(key), int) or isinstance(kwargs.get(key), float)):
                message[filed] = kwargs.get(key)
            else:
                message["extends.%s" % filed] = kwargs.get(key)

        message["opts"] = int(time.time() * 1000)

        try:
            SOCK_UDP.sendto(json.dumps(message).encode('utf-8'), SOCK_ADDR)
        except:
            traceback.print_exc()
            pass
