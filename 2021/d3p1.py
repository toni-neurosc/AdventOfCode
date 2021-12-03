import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

lines = args.file.readlines()

values = [l.strip() for l in lines]
n = len(values[0])
g = ''
e = ''

for i in range(n):
    s = sum([int(v[i]) for v in values])
    if s > len(values)/2:
        g += '1'
        e += '0'
    else:
        e += '1'
        g += '0'

print(g, e)
print(int(g, 2) * int(e, 2))
