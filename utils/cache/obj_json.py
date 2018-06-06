#coding=utf-8

import simplejson
from .base import mcache
from django.conf import settings

class CacheObjJson(object):
    KEY_PREFIX = 'OBJJSON#:'

    @classmethod
    def _make_key(cls, obj_type, obj_id):
        return "%s:%s:%s" % (cls.KEY_PREFIX , obj_type , obj_id)

    @classmethod
    def delete_json(cls, obj_type, obj_id):
        key = cls._make_key(obj_type, obj_id)
        mcache.delete(key)

    @classmethod
    def set_json(cls, obj_type, obj_id, data, timeout=settings.DEFAULT_OBJ_JSON_TIMEOUT):
        key = cls._make_key(obj_type, obj_id)
        if isinstance(data, dict):
            data = simplejson.dumps(data)
        mcache.set(key, data, timeout)

    @classmethod
    def get_json(cls, obj_type, obj_id):
        key = cls._make_key(obj_type, obj_id)
        data = mcache.get(key)
        if data:
            if isinstance(data, str):
                return simplejson.loads(data)
            else:
                return data

class GameDetail(object):
    KEY_PREFIX = 'GAMEDETAIL#'

    @classmethod
    def _make_key(cls, game_id):
        return "%s:%s" % (cls.KEY_PREFIX, game_id)

    @classmethod
    def delete_json(cls, game_id):
        key = cls._make_key(game_id)
        mcache.delete(key)

    @classmethod
    def set_json(cls, game_id, data, timeout=300):
        key = cls._make_key(game_id)
        if isinstance(data, dict):
            data = simplejson.dumps(data)
        mcache.set(key, data, timeout)

    @classmethod
    def get_json(cls, game_id):
        key = cls._make_key(game_id)
        data = mcache.get(key)
        if data:
            if isinstance(data, str):
                return simplejson.loads(data)
            else:
                return data

