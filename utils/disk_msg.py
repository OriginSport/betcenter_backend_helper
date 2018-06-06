#coding=utf-8

import fcntl
import os
import time
import datetime
import simplejson

from .timeutils import stamp_to_datetime

from app_api.configs import settings

def get_msg_time(msg):
    """
    从消息中提取消息时间
    """
    if msg.get('create_time') and isinstance(msg['create_time'], int):
        msg_time = stamp_to_datetime(msg['create_time'])
    else:
        msg_time = datetime.datetime.now()
    return msg_time

def make_daily_path(msg):
    msg_type = msg['doc_type']
    time_str = get_msg_time(msg).strftime('%Y%m%d')
    return '%s/%s_%s_%s.txt'%(msg_type, msg_type.lower(), settings.SITE_IP, time_str)

def make_hourly_path(msg):
    msg_type = msg['doc_type']
    time_str = get_msg_time(msg).strftime('%Y%m%d%H')
    return '%s/%s_%s_%s.txt'%(msg_type, msg_type.lower(), settings.SITE_IP, time_str)

def write_disk_msg(msg, path=None, version='ttqzone'):
    if version:
        msg['v'] = version
    if path is None:
        if settings.APP_DISK_MSG_SPLIT == 'daily':
            path = make_daily_path(msg)
        elif settings.APP_DISK_MSG_SPLIT == 'hourly':
            path = make_hourly_path(msg)

    abs_path = os.path.join(settings.APP_DISK_MSG_DIR, path)
    
    abs_dir = os.path.split(abs_path)[0]
    # 确保路径可写
    if not os.path.isdir(abs_dir):
        os.makedirs(abs_dir)

    # 写入消息的json字符串
    for i in range(10):
        try:
            f = open(abs_path, 'a')
            fcntl.lockf(f, fcntl.LOCK_EX)
            f.write('%s\n'%simplejson.dumps(msg))
            fcntl.lockf(f, fcntl.LOCK_UN)
            f.close()
            break
        except:
            import traceback; traceback.print_exc()
            time.sleep(0.0001)
