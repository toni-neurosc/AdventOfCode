import time

dots = []
folds = []
for line in open(0).read().splitlines():
    if line and line[0].isnumeric():
        dots.append(([int(n) for n in line.strip().split(',')]))
    elif line:
        folds.append((0 if line[11] == 'x' else 1, int(line.split('=')[1])))

def print_dots(dots):
    xmax = max([dot[0] for dot in dots])
    ymax = max([dot[1] for dot in dots])
    grid = [['.'] * (xmax+1) for count in range(ymax+1)]
    for dot in dots:
        grid[dot[1]][dot[0]] = '#'
    for row in grid:
        print(''.join([str(n) for n in row]))

def fold(dots, part1 = False):
    for dim, pos in folds:
        # Mirror dots respect to fold line
        for dot in dots:
            if dot[dim] > pos:
                dot[dim] = 2*pos - dot[dim] # this mirrors the indexes around the fold line
        # Remove dots in fold line
        dots = [dot for dot in dots if dot[dim] != pos]
        # if the fold line is on the first half of the page, we get negative indexes
        # we have add the offset: <total lines> - 2 * <lines after fold> + 1 (we lost the fold line)
        l = max([dot[dim] for dot in dots])
        if pos < l // 2:
            offset = l - 2 * pos + 1
            for dot in dots:
                dot[dim] += offset
        if part1: break
    return dots

print(f"Day 13 Part 1 solution: {len(set([tuple(dot) for dot in fold(dots, part1=True)]))}")
print(f"Day 13 Part 2 solution:")
t = time.time()
print_dots(fold(dots))
print(f"Part 2 execution time: {time.time()-t:.6f} seconds")



    
#     for 
#     for i, c in enumerate(dots[dim]):
#         if c > f: dots[dim][i] 

# if f > d//2:

# print(dots, folds)
