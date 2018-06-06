#coding=utf-8

import os
import uuid

def auto_reload_module(module_name, globals_dict=globals(), locals_dict=locals()):
    module = __import__(module_name, globals_dict, locals_dict, [], -1)
    module_path = module.__file__
    if module_path.endswith('pyc'):
        module_path = module_path[:-1]
    try:
        if module.load_time < os.path.getmtime(module_path):
            reload(module)
            module.load_time = os.path.getmtime(module_path)
    except Exception:
        module.load_time = os.path.getmtime(module_path)
    return module


def generate_uuid4():
    return str(uuid.uuid4()).replace('-', '')
