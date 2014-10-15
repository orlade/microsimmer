
def get_thrift_methods(cls):
    if hasattr(cls, 'Iface'):
        cls = cls.Iface
    names = [f for f in dir(cls) if '__' not in f]
    funcs = [cls.__dict__[name] for name in names]
    return {f.func_name: f.func_code.co_varnames[1:] for f in funcs}