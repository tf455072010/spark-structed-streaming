# !/usr/bin/python3
# -*- coding: utf-8 -*-

'''
@Desc:      简易本地缓存
@Author:    wangzs@ct108.com
@Create:    2016/06/17
@Update:    2017/04/11
'''

import time


class MemoryCache:
    '''
    利用内存进行python的缓存管理
    '''

    CACHE_DICT = {}
    KEY_EXPIRE_TS = "expireTs"
    KEY_CACHE_OBJ = "obj"

    @staticmethod
    def build_cache_obj(value, timeout):
        '''
        获取过期时间

        Args:
            value： 缓存对象
            timeout: 缓存超时时间，单位毫秒
        '''

        return {MemoryCache.KEY_EXPIRE_TS: time.time() * 1000 + timeout, MemoryCache.KEY_CACHE_OBJ: value}

    @staticmethod
    def has_expired(cacheobj):
        '''
        判断是否已经过期

        Args:
            cacheobj 缓存object
        '''

        if not cacheobj:
            return True
        valid = MemoryCache.KEY_EXPIRE_TS in cacheobj
        valid = valid and (time.time() * 1000 <= cacheobj[MemoryCache.KEY_EXPIRE_TS])
        return not valid

    @staticmethod
    def set(key, value, timeout):
        '''
        设置缓存，如果key存在，则覆盖现有缓存

        Args:
            key: 缓存键
            value： 缓存对象
            timeout: 缓存超时时间，单位毫秒
        '''

        MemoryCache.CACHE_DICT[key] = MemoryCache.build_cache_obj(value, timeout)

    @staticmethod
    def clear(key):
        '''
        清空缓存

        Args:
            key: 缓存键
        '''
        if key in MemoryCache.CACHE_DICT:
            del MemoryCache.CACHE_DICT[key]

    @staticmethod
    def clearall():
        '''
        清空所有内存缓存
        '''

        MemoryCache.CACHE_DICT = {}

    @staticmethod
    def get(key):
        '''
        获取缓存, 如果缓存失效或者没有缓存，则返回None

        Args:
            key: 缓存键
        Returns:
            缓存对象
        '''

        if key not in MemoryCache.CACHE_DICT:
            return None
        cacheobj = MemoryCache.CACHE_DICT[key]
        if MemoryCache.has_expired(cacheobj):
            del MemoryCache.CACHE_DICT[key]
            return None
        else:
            return cacheobj[MemoryCache.KEY_CACHE_OBJ]


def autocache(key, timeout):
    '''
    自动设置缓存，如果key存在，则覆盖现有缓存

    Args:
        key: 缓存键
        timeout: 缓存超时时间，单位毫秒
    Returns:
        object
    '''
    def __autocache(func):
        def __autocache_handle(*args, **kwargs):
            key_ = key
            if len(args) > 0 and hasattr(args[0], "getcachekey"):
                key_ = "%s#%s" % (key, args[0].getcachekey())

            value = MemoryCache.get(key_)
            if value:
                return value
            else:
                value = func(*args, **kwargs)
                if value:
                    MemoryCache.set(key_, value, timeout)
            return value

        return __autocache_handle

    return __autocache
