#coding=utf-8

import logging
import datetime

import utils.errors as err

from utils.view_tools import ok_json, fail_json, get_args
from utils.timeutils import stamp_to_datetime
from utils.cache.page import PageCache

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt 

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class AbstractAPI(object):
    args = None

    def __init__(self, cache_args=[]):
        self.check_user = False
        self.cache_args = cache_args
        self.config_args()

    def config_args(self):
        self.args = {}

    def access_db(self, kwarg):
        return fail_json(err.ERROR_CODE_UNDEFINED)

    def format_data(self, data):
        if data is not None:
            if isinstance(data, models.query.QuerySet):
                return ok_json([d.get_json() for d in data])
            return ok_json(data.get_json())
        return fail_json(err.ERROR_CODE_DATABASE_ACCESS_ERROR)

    def cache_page(self, cache_key, data, timeout=settings.DEFAULT_PAGE_CACHE_TIMEOUT):
        if not settings.DEBUG:
            PageCache.set_page_key(cache_key, data, timeout)

    def make_cache_key(self, kwarg):
        arg_list = list(kwarg.items())
        arg_list.sort(key=lambda x:x[0])
        key = kwarg['request'].path
        for arg in arg_list:
            if arg[0] in self.cache_args:
                key += '?' + '%s=%s' %arg
        return key


    def wrap_func(self, cache_args=[]):
        @csrf_exempt
        def wrapper(request):
            args = get_args(request)
            kwarg ={'request': request}
            for k in self.args:
                if self.args[k] == 'r' and (k not in args or args[k] == ""):
                    return fail_json(err.ERROR_CODE_INVALID_ARGS, k)
                val = args.get(k, None)
                if not val and isinstance(self.args[k], tuple):
                    val = self.args[k][1]
                kwarg[k] = val

            if self.cache_args != [] and not settings.DEBUG:
                cache_key = self.make_cache_key(kwarg)
                cache_data = PageCache.get_page_key(cache_key)
                if cache_data:
                    return ok_json(cache_data)

            obj = self.access_db(kwarg)
            return self.format_data(obj)

        return wrapper


class ByIdQueryAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {'id': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model.objects.get(pk=kwarg['id'], is_active=True)
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None


class ByIdsQueryAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {'ids': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            objs = self.model.objects.filter(id__in=kwarg['ids'].split(','), is_active=True)
            return objs
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None



class DeleteAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {'id': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = None
            if self.model.delete.__self__ is not None: 
                obj = self.model.delete(id=kwarg['id'])
            else:
                obj = self.model.objects.get(pk=kwarg['id'], is_active=True)
                obj.is_active = False
                obj.save()
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def format_data(self, data):
        if not data:
            return fail_json(err.ERROR_CODE_DATABASE_DELETE_ERROR)
        return ok_json({'id':data.id})


class BatchDeleteAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {'ids': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            ids = kwarg['ids']
            if type(ids) is not list:
                ids = ids.split(',')
            if self.model.delete.__self__ is not None: 
                for id in ids:
                    self.model.delete(id=id)
                return ids 
            else:
                self.model.objects.filter(pk__in=[int(id) for id in ids], is_active=True).update(is_active=False)
                return ids 
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def format_data(self, data):
        if not data:
            return fail_json(err.ERROR_CODE_DATABASE_DELETE_ERROR)
        return ok_json(data)


class UpdateAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {'id': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model.objects.get(pk=kwarg['id'], is_active=True)
            for k in kwarg:
                if k is not 'id':
                    if type(obj.__dict__[k]) is datetime.datetime and type(kwarg[k]) is not datetime.datetime:
                        kwarg[k] = stamp_to_datetime(int(kwarg[k]))
                    if type(obj.__dict__[k]) is bool and type(kwarg[k]) is not bool:
                        kwarg[k] = str(kwarg[k]).lower() == 'true'
                    if kwarg[k] == '':
                        kwarg[k] = None
                    setattr(obj, k, kwarg[k])
            obj.save()
            return obj 
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def wrap_func(self):
        @csrf_exempt
        def wrapper(request):
            args = get_args(request)
            kwargs = {}
            for field in self.model._meta.fields:
                key_name = field.name
                key_name = field.column
                if field.name == 'user':
                    try:
                        s = Session.objects.get(pk=args['session_id'])
                        user_id = s.get_decoded().get('_auth_user_id')
                        user = User.objects.get(pk=user_id, is_active=True)
                        args['user_id'] = user_id
                        args['user'] = user
                    except:
                        import traceback; traceback.print_exc()
                        return fail_json(err.ERROR_CODE_INVALID_ARGS, field.name)

                if key_name in args:
                    if args.get(key_name):
                        kwargs[key_name] = args[key_name]
            obj = self.access_db(kwargs)
            return self.format_data(obj)
        return wrapper


class CreateAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model()
            for k in kwarg:
                if type(obj.__dict__[k]) is datetime.datetime and type(kwarg[k]) is not datetime.datetime:
                    kwarg[k] = stamp_to_datetime(int(kwarg[k]))
                if type(obj.__dict__[k]) is bool and type(kwarg[k]) is not bool:
                    kwarg[k] = str(kwarg[k]).lower() == 'true'
                if type(obj.__dict__[k]) is int and type(kwarg[k]) is not int:
                    kwarg[k] = int(kwarg[k])
                setattr(obj, k, kwarg[k])
            obj.save()
            return obj 
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def wrap_func(self):
        @csrf_exempt
        def wrapper(request):
            args = get_args(request)
            kwargs = {}
            for field in self.model._meta.fields:
                key_name = field.column
                if field.name in ['create_time', 'update_time', 'is_active', 'id']:
                    continue
                if field.name == 'user':
                    try:
                        s = Session.objects.get(pk=args['session_id'])
                        user_id = s.get_decoded().get('_auth_user_id')
                        user = User.objects.get(pk=user_id, is_active=True)
                        args['user_id'] = user_id
                        args['user'] = user
                    except:
                        import traceback; traceback.print_exc()
                        return fail_json(err.ERROR_CODE_INVALID_ARGS, field.name)

                if not field.null and key_name not in args and not field.has_default():
                    return fail_json(err.ERROR_CODE_INVALID_ARGS, field.name)

                if key_name in args:
                    if args.get(key_name):
                        kwargs[key_name] = args[key_name]
            obj = self.access_db(kwargs)
            return self.format_data(obj)
        return wrapper


class AssitListOrderAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model
    
    def config_args(self):
        self.args = {'parent_id': 'r',
                'target_id': 'r',
                'index': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model.update(int(kwarg['parent_id']), int(kwarg['target_id']), int(kwarg['index']))
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def format_data(self, data):
        if not data:
            return fail_json(err.ERROR_CODE_DATABASE_DELETE_ERROR)
        return ok_json(data)
