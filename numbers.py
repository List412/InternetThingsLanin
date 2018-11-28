import roman
import re

file = open('input.txt', 'r', encoding='utf-8')
data = file.read()
file.close()

regexp = r"\b((?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}))[,\.»]?\b"
pattern = re.compile(regexp, re.UNICODE)

rom = re.findall(pattern, data)

for r in rom:
    print(r)
    if str(r[0]).__len__() > 0:
        data = data.replace(r[0], str(roman.fromRoman(r[0])))
        print(str(roman.fromRoman(r[0])))

print(data)
