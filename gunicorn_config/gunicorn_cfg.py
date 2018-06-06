#coding=utf-8

import multiprocessing
import os, sys

path = os.path.abspath('')
sys.path.append(path)

app = "betcenter_backend_helper"
procname = app

abs_path = os.path.abspath(__file__)

project_path = os.path.join('/'.join(abs_path.split('/')[:-3]), app)

sys.path.insert(0, project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "betcenter_backend_helper.settings")

from django.conf import settings

bind = "%s:%s" % (settings.HOST, settings.PORT)
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
max_requests = 1000
timeout = 10
debug = False
daemon = False
loglevel = 'debug'
reload = True
