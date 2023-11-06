import re

for i in range(int(input())):
    try:
        pattern = bool(re.compile("r'("+ input() +")'"))
        print(pattern)
    except re.error:
        print("False")
