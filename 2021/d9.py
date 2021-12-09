# %%
import sys, time
import numpy as np

input = [[int(n) for n in list(line.strip())] for line in sys.stdin.readlines()]
# input = [[int(n) for n in list(line.strip())] for line in open('d9_input.txt').readlines()]
# input = [[int(n) for n in list(line.strip())] for line in open('d9_test.txt').readlines()]

def getrisk(heightmap):
    risk = 0
    low_points = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            up = heightmap[i-1][j] if i-1>=0 else float('inf')
            down = heightmap[i+1][j] if i+1<len(heightmap) else float('inf')
            right = heightmap[i][j+1] if j+1<len(heightmap[i]) else float('inf')
            left = heightmap[i][j-1] if j-1>=0 else float('inf')
            if heightmap[i][j] < min(up, down, right, left):
                risk += heightmap[i][j]+1
                low_points.append((i,j))
    return risk, low_points

def get_basins(heightmap):
    basin_array = np.zeros((len(heightmap), len(heightmap[0])), dtype=int)
    basin_counter = 0
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j] == 9:continue
            up = heightmap[i-1][j] if i-1>=0 else 9
            left = heightmap[i][j-1] if j-1>=0 else 9
            if up == 9 and left == 9:
                basin_counter +=1
                basin_array[i,j] = basin_counter
                # basin_array[i,j] = np.max(basin_array) + 1
            elif up != 9 and left == 9:
                basin_array[i,j] = basin_array[i-1, j]
            elif up == 9 and left != 9:
                basin_array[i,j] = basin_array[i, j-1]
            elif up != 9 and left != 9:
                basin_array[np.where(basin_array == basin_array[i, j-1])] = basin_array[i-1, j]
                basin_array[i,j] = basin_array[i-1, j]
    return basin_array

def part2(heightmap):
    basins = get_basins(heightmap)
    basin_sizes = []
    for i in range(1, np.max(basins)+1):
        basin_sizes.append(np.sum(basins == i))
    basin_sizes.sort(reverse=True)
    return np.prod(basin_sizes[:3])


t = time.time()
print(f"Day 9 Part 1 solution: {getrisk(input)[0]}. Execution time: {time.time()-t:.6f} seconds")

t = time.time()
print(f"Day 9 Part 2 solution: {part2(input)}. Execution time: {time.time()-t:.6f} seconds")

from matplotlib import pyplot as plt
basin_map = np.array(get_basins(input), dtype=float)
basin_map[basin_map==9]=np.nan
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
ax.pcolormesh(basin_map, vmin=-1, vmax=1)
