cube = lambda x: x**3  # complete the lambda function

def fibonacci(n):
    a, b = 0, 1
    for i in range(0, n):
        yield a
        a, b = b, a + b

# return a list of fibonacci numbers
if __name__ == "__main__":
    n = int(6)
    print(list(map(cube, fibonacci(n))))
