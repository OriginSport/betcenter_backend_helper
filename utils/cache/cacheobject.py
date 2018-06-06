#coding=utf-8

import simplejson
from copy import deepcopy
from redis import Redis

from app_api.configs import settings


class CacheObjectError(Exception):
    pass

class CacheObjectCacheMissingError(Exception):
    pass

class CacheAdapter(object):

    def __init__(self, cache_client, cache_type, prefix="CO"):
        self.cache_client = cache_client
        self.cache_type = cache_type
        self._prefix = prefix
        
    def make_cache_key(self, obj_id):
        key = '%s:%s:%s'%(self._prefix, self.cache_type, obj_id)
        key = key.encode('utf-8')
        return key

    def bulk_query_cache(self, obj_ids):
        keys = [self.make_cache_key(obj_id) for obj_id in obj_ids]
        if isinstance(self.cache_client, Redis):
            return dict(zip(keys, self.cache_client.mget(keys)))
        else:
            return self.cache_client.get_multi(keys)

    def save_cache(self, cache_doc, timeout=None):
        if settings.DEBUG:
            return True
        doc_id = cache_doc.get('id')
            
        if not doc_id:
            return False
            #raise CacheObjectError('Adapter save cache object require _id.')
        
        if timeout:
            if isinstance(self.cache_client, Redis):
                self.cache_client.setex(self.make_cache_key(doc_id), simplejson.dumps(cache_doc), timeout)
            else:
                self.cache_client.set(self.make_cache_key(doc_id), simplejson.dumps(cache_doc), timeout)
        else:
            self.cache_client.set(self.make_cache_key(doc_id), simplejson.dumps(cache_doc))
    
    def fetch_cache_json(self, obj_id):
        if settings.DEBUG:
            return None
        doc = self.cache_client.get(self.make_cache_key(obj_id))
        if not doc:
            return None
            #raise CacheObjectCacheMissingError('Adapter cache missing object id: %s'%obj_id)
        return simplejson.loads(doc)


    def delete(self, obj_id):
        self.cache_client.delete(self.make_cache_key(obj_id))

class BaseObject(object):

    def __init__(self):
        self.__dict__['_properties'] = {}
        self.__dict__['_time'] = {}
        self._is_dummy = True


    def __setattr__(self, attr, value):
        if attr not in ['_properties', '_time', '_is_dummy']:
            self._properties[attr] = value
        else:
            self.__dict__[attr] = value

    def __getattr__(self, attr):
        if attr not in ['_properties', '_time', '_is_dummy']:
            value = self._properties.get(attr, None)
            if value:
                if attr in self._time:
                    return self._time[attr](value)
            return value
        else:
            return self.__dict__.get(attr, None)
                    
    def _fetch_data(self, data):
        if not data:
            self._is_dummy = True
            return self

        if not isinstance(data, dict):
            data = simplejson.loads(data)
        for k, v in data.items():
            self._properties[k] = v
        
        self._is_dummy = False
        return self
    
    def is_dummy(self):
        return self._is_dummy


class CacheObject(BaseObject):

    def __init__(self, adapter=None, timeout=None):
        self.__dict__['_properties'] = {}
        self._curry = {}
        self._time = {}
        self._adapter = adapter
        self._is_dummy = True
        self._timeout = timeout
    
    def __setattr__(self, attr, value):
        if attr not in ['_properties', '_adapter', '_curry', '_time', '_timeout', '_is_dummy']:
            if attr in self._curry:
                self._properties[attr] = self._curry[attr][1](value)
            else:
                self._properties[attr] = value
        else:
            self.__dict__[attr] = value

    def __getattr__(self, attr):
        if attr not in ['_adapter', '_curry', '_time', '_properties', '_timeout', '_is_dummy']:
            value = self._properties.get(attr, None)
            if attr in self._curry:
                return self._curry[attr][0](value)
            elif attr in self._time:
                return self._time[attr](value)
            else:
                return value
        else:
            return self.__dict__.get(attr, None)
            
    def set_doc(self, doc):
        if not isinstance(doc, dict):
            doc = simplejson.loads(doc)
        for k, v in doc.items():
            self._properties[k] = v
        
        self._is_dummy = False

    def store_cache(self, timeout=None):
        """
        save document into cache
        """
        if not timeout and self._timeout:
            timeout = self._timeout
        return self._adapter.save_cache(self._properties, timeout)
   
    def fetch_cache(self, obj_id):
        """
        fetch cache object by document id
        """
        doc = self._adapter.fetch_cache_json(obj_id)
        if doc:
            self.set_doc(doc)
        else:
            self._is_dummy = True
    
    def load_cache(self, cache_obj):
        """
            load cache object into cache object
        """
        doc = cache_obj.get_json()
        if doc:
            self.set_doc(doc)
        else:
            self._is_dummy = True
    
    def get_json(self):
        return deepcopy(self._properties)
    
    def get_doc(self):
        return self.get_json()
    
    def save(self):
        self.store_cache()
    
    def is_dummy(self):
        return self._is_dummy

    def delete(self):
        self._adapter.delete(self.id)


