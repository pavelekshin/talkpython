import time
import functools

DEFAULT_FMT = "[{elapsed:0.8f}s] {name}({args}) -> {result}"


class clock:
    def __init__(self,fmt=DEFAULT_FMT):
        self.fmt = fmt
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args):
            t0 = time.perf_counter()
            result = func(*args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            doc = func.__doc__
            arg_str = ", ".join(repr(arg) for arg in args)
            print(self.fmt.format(**locals()))
            return result

        return wrapper

@clock()
#@clock(fmt="{name} {doc} ({args!r}): dt ={elapsed:0.8f}s")
def snooze(seconds):
    """this is snooze func """
    time.sleep(seconds)


@clock(fmt="{name} ({args!r}) dt = [{elapsed:0.8f}]s -> {result!r}")
def factorial(n):
    """ this is fibonacci func """
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == "__main__":
    print(snooze.__name__)
    print(snooze.__doc__)
    print("*" * 40, "Calling snooze(.88)")
    snooze(0.888)
    print(snooze(0.888).__doc__)
    print("*" * 40, "Calling factorial(6)")
    print("5! =", factorial(5))
    print("test", "*" * 40)
    assert factorial(5) == 120
