import math
import re
import time 

def magnitude(item):
    if isinstance(item, int):
        return item
    else:
        return 3*magnitude(item[0])+2*magnitude(item[1])

def process(s):
    # print(s)
    level = 0
    # Check explodes
    for i, c in enumerate(s):
        if c == '[': level += 1
        elif c == ']': level -= 1
        elif c.isnumeric():
            if level > 4:
                return process(explode(s, i-1))
    # Check splits
    for i, c in enumerate(s):
        if s[i:i+2].isnumeric():
            return process(split(s, i))
    return s

def explode(s, start):
    end = re.search(']',s[start:]).span()[0]  # Find end of pair
    pair = s[start:start+end+1]
    # print(f"Exploding pair {pair}")
    n,m = [int(i) for i in pair.strip('[]').split(',')]
    parts = ((s[:start], n, -1), (s[start+end+1:],  m, 0))
    modified = []
    for part, n, i in parts:
        m = list(re.finditer('\d+', part))
        if m:
            idx = m[i].span()
            modified.append(part[:idx[0]] + str(int(part[idx[0]:idx[1]])+n)+ part[idx[1]:])
        else:
            modified.append(part)
    return modified[0] + '0' + modified[1]

def split(s, start):
    # print(f"Splitting number {s[start:start+2]}")
    left_part = s[:start]
    right_part = s[start+2:]
    n = int(s[start:start+2])
    
    return left_part + '[' + str(math.floor(n/2)) + ',' + str(math.ceil(n/2)) + ']' + right_part

def add(s1,s2):
    return process('[' + s1 + ',' + s2 + ']')

def tolist(s):
    d = {}
    exec("x="+s, d)
    return d['x']

def part1(input):
    result = input[0]
    for line in input[1:]:
        result = add(result, line)
    result = tolist(result)
    return magnitude(result)

def part2(input):
    max_mag = 0
    for i in range(len(input)):
        for j in range(len(input)):
            if i != j:
                result = add(input[i], input[j])
                result = tolist(result)
                mag = magnitude(result)
                if mag > max_mag:
                    max_mag = mag
    return max_mag
    
input = [line for line in open(0).read().splitlines()]

result = input[0]
for line in input[1:]:
    result = add(result, line)
exec('result = ' + result)

t = time.time()
print(f"Day 18 solution: {part1(input)}. Execution time: {time.time() - t:.6f} seconds")

t = time.time()
print(f"Day 18 solution: {part2(input)}. Execution time: {time.time() - t:.6f} seconds")

