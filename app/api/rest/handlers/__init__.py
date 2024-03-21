import os
import importlib
from fastapi.routing import APIRoute


__globals = globals()

# autoload:
for file in os.listdir(os.path.dirname(__file__)):
    if file.startswith('__'):
        continue
    mod_name = file[:-3]   # strip .py at the end
    mod = importlib.import_module('.' + mod_name, package=__name__)
    items = dir(mod)
    for item in items:
        obj = getattr(mod, item)
        if isinstance(obj, APIRoute):
            __globals[mod_name] = obj
