import roman
import re


def replace(m):
    print(m)
    if m.group(1).__len__() > 0:
        return str(roman.fromRoman(m.group(1)))
    else:
        return m.group(1)


file = open('input.txt', 'r', encoding='utf-8')
data = file.read()
file.close()

regexp = r"\b((?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}))[,\.»]?\b"
pattern = re.compile(regexp, re.UNICODE)

data = re.sub(pattern, replace, data)

file = open('output.txt', 'w', encoding='utf-8')
file.write(data)
file.close()

