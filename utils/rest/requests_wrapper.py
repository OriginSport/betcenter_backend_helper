#coding=utf-8

import requests
import tempfile

from urllib import parse
from urllib.parse import urlencode
from django.conf import settings

def _get_absolute_url(relative_url, host):
    return parse.urljoin(host, relative_url)

def _debug_log(log):
    if settings.DEBUG:
        #if isinstance(log, bytes):
        #    log = log.decode("utf-8")
        print(log)

def local_fail_json(err=0, description=''):
    return {'ok': False, 'reason': {'err': err, 'desc': description}}

def get(relative_url, local_args, args, host=None, format='json'):
    data = {}
    for i in args:
        val = local_args.get(i, None)
        if val is not None:
            #if isinstance(val, unicode):
            #    val = val.encode('utf-8')
            data[i] = val
    compiled_url = '%s?%s' % (relative_url, urlencode(data))
    absolute_url = _get_absolute_url(compiled_url, host)
    req = requests.get(absolute_url)
    _debug_log(req.content)
    _debug_log(absolute_url)
    if req.status_code == 200:
        if format == 'json':
            return req.json()
        elif format == 'raw':
            return req.content
    return local_fail_json('20001', 'request error') 

def post(relative_url, locals, args, host=None, format='json'):
    data = {}
    for i in args:
        val = locals.get(i, None)
        if val is not None:
            #if isinstance(val, unicode):
            #    val = val.encode('utf-8')
            data[i] = val
    absolute_url = _get_absolute_url(relative_url, host)
    req = requests.post(absolute_url, data=data)
    _debug_log(req.content)
    _debug_log(absolute_url)
    _debug_log(data)
    if req.status_code == 200:
        if format == 'json':
            return req.json()
        elif format == 'raw':
            return req.content
    return local_fail_json('20001', 'request error') 

def post_file(relative_url, locals, args, filename, content, host=None, format='json'):
    data = {}
    for i in args:
        val = locals.get(i, None)
        if val is not None:
            #if isinstance(val, unicode):
            #    val = val.encode('utf-8')
            data[i] = val
    absolute_url = _get_absolute_url(relative_url, host)
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(content)
    temp.name = temp.name + "." +  filename.split('.')[-1]
    temp.seek(0)
    files = {'filedata': temp}
    req = requests.post(absolute_url, data=data, files=files)
    _debug_log(req.content)
    _debug_log(absolute_url)
    _debug_log(data)
    temp.close()
    if req.status_code == 200:
        if format == 'json':
            return req.json()
        elif format == 'raw':
            return req.content
    return local_fail_json('20001', 'request error') 

def delete(relative_url, id):
    return post(relative_url, locals(), ('id', ))
