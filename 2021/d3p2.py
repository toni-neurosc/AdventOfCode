import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

def findrate(values, pos = 0, most = True):
    print(values)
    if len(values) == 1:
        return values[0]
    else:
        l = len(values)
        s = sum([int(v[pos]) for v in values])
        if s == l/2:
            c = '1' if most else '0'
        else:
            c = round(s/l)
            c = c if most else abs(c-1)
            c = str(c)
        print('most common', c)
        values = [v for v in values if v[pos] == c]
        return findrate(values, pos+1, most)




lines = args.file.readlines()
values = [l.strip() for l in lines]

o = findrate(values, most = True)
c = findrate(values, most = False)

print(o, c)
print(int(o, 2) * int(c, 2))
