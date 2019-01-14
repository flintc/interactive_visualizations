from copy import deepcopy
from functools import reduce


def get_prop_names(prop_path):
    return prop_path.split('.') if isinstance(prop_path, str) else prop_path


def prop(name):
    return lambda obj: obj[name] if isinstance(obj, dict) else getattr(obj, name)


def path(prop_path):
    prop_names = get_prop_names(prop_path)
    return lambda obj: reduce(lambda cobj, name: prop(name)(cobj), prop_names, obj)


def assoc(name, value):
    return lambda obj: type(obj)([(name, value)]+[(k, v) if k != name else (k, value) for k, v in obj.items()])


def assoc_path(prop_path, value):
    def wrapper(obj):
        #new_obj = deepcopy(obj)
        #new_obj = obj
        prop_names = get_prop_names(prop_path)
        pobj = path(prop_names[0:-1])(obj)
        pobj[prop_names[-1]] = value
        return obj
    return wrapper
