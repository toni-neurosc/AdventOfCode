import argparse, time
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('steps', type=int)
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('maxiter', type=int, nargs='?', default=5000)
args = parser.parse_args()

def printmap(a):
    return np.array2string(a).translate(str.maketrans({'[':'', ']':'', ',':''}))

def simulate_step(grid):
    flashes = 0
    # Increment energy of all octopuses and start with the ones that reach the threshold of 10
    grid += 1
    queue = [pair for pair in zip(*np.where(grid==10))]
    while queue:
        # Get the position of first octopus in the queue 
        x,y = queue.pop(0)
        # Visit it and its neigbours, flash when energy threshold reached, otherwise increase
        # energy by 1 and add to queue if that makes the octopus reach threshold
        for i in range(max(0, x-1), min(x+2, grid.shape[0])):
            for j in range(max(0, y-1), min(y+2, grid.shape[1])):
                if grid[i,j] == 10:
                    flashes += 1
                    grid[i,j] = 0
                elif grid[i,j] == 9:
                    grid[i,j] +=1
                    queue.append((i,j))
                elif grid[i,j] > 0:
                    grid[i,j] += 1
    return grid, flashes

def part1(input, steps):
    cavern = input.copy()
    total_flashes = 0
    for n in range(steps):
        cavern, flashes = simulate_step(cavern)
        total_flashes += flashes
    print(f"After step {n+1}:\n", printmap(cavern))
    return total_flashes

def part2(input, maxsteps = 5000):
    cavern = input.copy()
    for n in range(maxsteps):
        simulate_step(cavern)
        if np.all(cavern == 0):
            print(f"After step {n+1}:\n", printmap(cavern))
            return n+1
    return None


input = np.array([[int(n) for n in list(line.strip())] for line in args.file.readlines()])
print("Before any steps:\n", printmap(input))
t = time.time()
print(f"Day 11 Part 1 solution: {part1(input, args.steps)}. Execution time: {time.time()-t:.6f} seconds")
t = time.time()
print(f"Day 11 Part 2 solution: {part2(input, args.maxiter)}. Execution time: {time.time()-t:.6f} seconds")
