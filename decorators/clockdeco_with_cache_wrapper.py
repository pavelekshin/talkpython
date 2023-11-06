import time
import functools


def clock(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        doc = func.__doc__
        arg_list = [repr(arg) for arg in args]
        arg_list.extend(f"{k}:{v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_list)
        print(f"[{elapsed:0.8f}]s {doc} {name}({arg_str}) -> {result!r}")
        return result

    return wrapper


@clock
def snooze(seconds, k1, k2):
    """this is sleep func"""
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


@clock
@functools.cache
def fibonacci(n):
    """this is fibonacci func"""
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == "__main__":
    print(snooze.__name__)
    print(snooze.__doc__)
    print("*" * 40, "Calling snooze(.456)")
    snooze(0.456, **{"k1": "asd", "k2": "123"})
    print("*" * 40, "Calling fibonacci(6)")
    print(fibonacci(8))
