from itertools import chain
from functools import reduce


def merge_iterables(*lsts):
    return chain.from_iterable(lsts)


def merge_dicts(*dikts):
    return dict(list(merge_iterables(*[d.items() for d in dikts])))


def merge_keys(*dikts):
    return chain.from_iterable([tuple(d.keys()) for d in dikts])


def merge_dicts_deep(*dikts):
    obj = dict()
    for key in merge_keys(*dikts):
        foo = [dd for dd in [
            prop(key)(d) for d in dikts if key in d.keys()] if isinstance(dd, dict)]
        bar = [prop(key)(d) for d in dikts if key in d.keys()]
        obj = assoc(key, merge_dicts(*foo) if len(foo) >
                    0 else bar if len(bar) > 1 else bar[0])(obj)
    return obj


def maybe_callable(value, obj):
    return value if not callable(value) else value(obj)


def resolve_assignments(kwargs, obj):
    return dict([(key, maybe_callable(value, obj)) for key, value in kwargs.items()])


def assign(**kwargs):
    return lambda dikt: merge_dicts(dikt, resolve_assignments(kwargs, dikt))


def prop(name):
    return lambda obj: obj[name] if isinstance(obj, dict) else getattr(obj, name)


def pipe(*fns):
    return lambda initial_value: reduce(lambda prev_result, fn: fn(prev_result), fns, initial_value)


def extend(obj, extension):
    return assign(**extension)(obj)


def assoc(key):
    return lambda value: lambda obj: assign(**{key: value})(obj)


def assoc_path(path):
    return lambda obj: pipe(*map(prop, path))(obj)


_AXIS = dict(
    gridcolor='rgba(255,255,255,0.2)',
    zerolinecolor='rgba(255,255,255,0.7)',
)
_DEFAULT_LAYOUT = dict(
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,.2)',
    xaxis=_AXIS,
    yaxis=_AXIS,
)

SCATTER_OPTS = {
    '.': 'markers',
    '-': 'lines',
    '.-': 'lines+markers',
    'markers': 'markers',
    'lines': 'lines',
    'lines+markers': 'lines+markers',
}

RESOLVERS = dict(
    markersize=lambda value: dict(marker=dict(size=value)),
    alpha=lambda value: dict(opacity=value),
    linesize=lambda value: dict
)

_RESOLVER_ALIASES = dict(
    ms=prop('markersize'),
    ls=prop('linesize'),
)

RESOLVERS = extend(RESOLVERS, _RESOLVER_ALIASES)


def resolve_alias(key, value):
    if key not in RESOLVERS:
        out = {key: value}
        print(out)
        return out
    else:
        return RESOLVERS[key](value)


def scatter(x, y, line_marker_desc='.', *args, **kwargs):
    options = merge_dicts(*[resolve_alias(key, value)
                            for key, value in kwargs.items()])
    trace = dict(
        x=x,
        y=y,
        mode=SCATTER_OPTS[line_marker_desc],
        **options,
    )
    return dict(
        data=[trace],
        layout=_DEFAULT_LAYOUT,
    )
