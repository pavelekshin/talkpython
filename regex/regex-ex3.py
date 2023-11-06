import re


# Squaring numbers
def replace(match):
    return "and" if match.group() == "&&" else "or"


def re_replace(INPUT):
    p = re.compile(
        r"""
    (           # first group
    (?<=\s)     # the next searched symbol should start from whitespace
    \&\&        # the mathech symbol &&
    (?=\s)      # previously matched symbol should end with whitespace
    )           # close first match group
    |           # logical OR
    (           # second group
    (?<=\s)     # the next searched symbol should start from whitespace
    \|\|        # the match symbol ||
    (?=\s)      # previously matched symbol should end with whitespace
    )           # close second match group
    """,
        re.VERBOSE,
    )
    n = N
    for _ in range(int(n)):
        l = INPUT
        print(re.sub(p, replace, l))


if __name__ == "__main__":
    INPUT = """11
    a = 1;
    b = input();

    if a + b > 0 && a - b < 0:
            start()
    elif a*b > 10 || a/b < 1:
            stop()
    print set(list(a)) | set(list(b))
    #Note do not change &&& or ||| or & or |
    #Only change those '&&' which have space on both sides.
    #Only change those '|| which have space on both sides."""
    OUTPUT = """
    a = 1;
    b = input();

    if a + b > 0 and a - b < 0:
            start()
    elif a*b > 10 or a/b < 1:
            stop()
    print set(list(a)) | set(list(b))
    #Note do not change &&& or ||| or & or |
    #Only change those '&&' which have space on both sides.
    #Only change those '|| which have space on both sides."""

    print(len(INPUT.split("\n"))
    assert re_replace(INPUT) == OUTPUT
