from functools import *
from itertools import *

def test(a, b, c, *args, **kwargs):
    pass


if __name__ == '__main__':
    func = test
    # get metafunction
    r = func.__code__
    print("-------first--------------")
    print("r.co_kwonlyargcount=",r.co_kwonlyargcount)
    print("r.co_posonlyargcount=",r.co_posonlyargcount)
    print("r.co_filename=",r.co_filename)
    print("r.co_name=",r.co_name)
    print("\n------second----------")
    print("r.co_stacksize",r.co_stacksize)
    print("r.co_argcount=",r.co_argcount)
    print("r.co_cellvars=",r.co_cellvars)
    print("r.co_code=",r.co_code)
    print("\n-------third--------------")
    print("r.co_consts=",r.co_consts)
    print("r.co_flags=",r.co_flags)
    print("r.co_freevars=", r.co_freevars)
    print("r.co_lnotab=",r.co_lnotab)
    print("\n--------------fourth---------")
    print("r.co_names=",r.co_names)
    print("r.co_nlocals=",r.co_nlocals)
    print("r.co_varnames=",r.co_varnames)
    print("r.replace=",r.replace)