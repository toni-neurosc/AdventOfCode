import sys, time
import numpy as np

input = np.array([int(n) for n in sys.stdin.readline().strip().split(',')])
# input = np.array([16,1,2,0,4,2,7,1,2,14]) # Test input

def min_hdist(input, incremental = False):
    if incremental:
        min_cost = float('inf')
        for i in range(max(input)):
            d = abs(i-input)
            c = np.sum(d*(d+1)//2)
            if c < min_cost: 
                min_cost = c
                target = i
        # min_dest = np.round(np.mean(input))
        # d = abs(input - min_dest)
        # print(np.size(d))
        # min_dist = sum(np.array(list(map(lambda x: x*(x+1)//2, d))))
    else:
        target = round(np.median(input))
        min_cost = np.sum(np.abs(input-target))
    return min_cost, target

t = time.time()
print(f"Day 7 Part 1 solution: {min_hdist(input, incremental=False)}. Execution time: {time.time()-t:.6f} seconds")

t = time.time()
print(f"Day 7 Part 2 solution: {min_hdist(input, incremental=True)}. Execution time: {time.time()-t:.6f} seconds")