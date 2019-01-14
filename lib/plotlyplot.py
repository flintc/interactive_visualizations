import plotly.graph_objs as go
import lib.core as core
from inspect import getmembers, isfunction

functions_list = [o for o in getmembers(core) if isfunction(o[1])]
def as_figurewidget(fn):
    def wrapper(*args, **kwargs):
        return go.FigureWidget(**fn(*args,**kwargs))
    return wrapper


globals().update(dict([ (name, as_figurewidget(fn)) for name, fn in functions_list ]))

def as_figurewidget(fn):
    def wrapper(*args, **kwargs):
        return go.FigureWidget(**fn(*args,**kwargs))
    return wrapper


globals().update(dict([ (name, as_figurewidget(fn)) for name, fn in functions_list ]))


