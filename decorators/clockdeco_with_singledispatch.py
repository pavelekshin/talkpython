import time
import functools
import numbers


@functools.singledispatch
def clock(args, **kwargs : object):
    content = "this is base func " + repr(args)
    print(content,args)
    return f"{repr(args)}"

@clock.register
def _(arg: str) -> str:
    content = "this is str func " + repr(arg)
    print(content,arg)
    return f"{type(arg)}"


@clock.register
def _(arg : int) -> str:
    content = "this is number func " + repr(arg)
    print(content,arg)
    return f"{type(arg)}"

@clock.register(float)
def _(arg) -> str:
    content = "this is number func " + repr(arg)
    print(content,arg)
    return f"{type(arg)}"


if __name__ == "__main__":
    print(clock(11.5))
    print(clock("25"))
