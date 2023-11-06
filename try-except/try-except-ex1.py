# Enter your code here. Read input from STDIN. Print output to STDOUT
for i in range(int(input("enter number of lines: "))):
    try:
        a, b = map(int, input().split())
        print("{}".format(int(a / b)))
    except ZeroDivisionError:
        print("Error Code: integer division or modulo by zero")
    except ValueError as ve:
        print("Error Code:", ve)
    except TypeError as te:
        print("Error Code:", te)
    except Exception as e:
        print("Error Code:", e)
    finally:
        pass
