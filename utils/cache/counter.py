#coding=utf-8

from base import mcache, counter_rclient

class MemcacheCounter(object):

    def __init__(self, name):
        self.key = 'MCR:' + name

    def get_count(self):
        value = mcache.get(self.key)
        if value is None:
            return 0
        else:
            return value

    def set_count(self, value):
        mcache.set(self.key, value)

    def delete_count(self):
        mcache.delete(self.key)

    count = property(get_count, set_count, delete_count)

    def increment(self, incr=1):
        value = mcache.get(self.key)
        if value:
            mcache.set(self.key, incr+int(value))
        else:
            mcache.set(self.key, incr)

class RedisCounter(object):

    def __init__(self, name):
        self.key = 'RCR:' + name

    def get_count(self):
        value = counter_rclient.get(self.key)
        if value is None:
            return 0
        else:
            return int(value)

    def set_count(self, value):
        counter_rclient.set(self.key, '%s'%value)

    def delete_count(self):
        counter_rclient.delete(self.key)

    count = property(get_count, set_count, delete_count)

    def increment(self, incr=1):
        return int(counter_rclient.incr(self.key, incr))
        
user_id_counter = RedisCounter('user_id')

