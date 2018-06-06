#coding=utf-8

import simplejson
from .base import mcache

class PageCache(object):
    KEY_PREFIX = 'PAGE#:'

    @classmethod
    def set_page_key(cls, key, data, timeout):
        if isinstance(data, dict):
            data = simplejson.dumps(data)
        mcache.set(cls.KEY_PREFIX+key, data, timeout)

    @classmethod
    def get_page_key(cls, key):
        data = mcache.get(cls.KEY_PREFIX +  key)
        if data:
            if isinstance(data, str):
                return simplejson.loads(data)
            else:
                return data

