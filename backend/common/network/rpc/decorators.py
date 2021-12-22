from functools import wraps
from inspect import getfullargspec

from backend.common.network.rpc.dataclass import RPCMethod
from backend.common.network.rpc.local import methods


def method(func: callable):
    args = getfullargspec(func).annotations
    
    argument_type = None
    for key, value in args.items():
        if key != 'return' and key != 'session':
            argument_type = value
    
    methods[func.__name__] = RPCMethod(
        func=func,
        argument_model=argument_type,
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    return wrapper
