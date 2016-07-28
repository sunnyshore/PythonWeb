import config_default


class SimpleDict(dict):
    """
    Simple dict that support access as x.y style
    """
    def __init__(self, names=(), values=(), **kw):
        super(SimpleDict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'SimpleDict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(default, override):
    r = {}
    for k, v in default.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def to_dict(d):
    D = SimpleDict()
    for k, v in d.items():
        D[k] = to_dict(v) if isinstance(v, dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass
