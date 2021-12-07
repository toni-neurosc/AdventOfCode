import sys, time

input = [int(n) for n in sys.stdin.readline().strip().split(',')]
# input = [16,1,2,0,4,2,7,1,2,14] # Test input
    
def min_hdist(input, incremental = False):
    # Calculates the minimum horizontal distance the crabs have to move by iterating 
    # all possible final positions, and over all initial positions.
    # Complexity is O(m*n), where m is number of positions and n is number of crabs
    min_cost = float('inf')
    for i in range(max(input)):
        s = 0
        for n in input:
            if incremental:
                # s += sum(range(abs(n - i) + 1)) # Brute force method
                d = abs(n - i)
                s += d * (d + 1) // 2 # Triangular number formula
            else: 
                s += abs(n - i)
            if s > min_cost: break # If we exceed current minimum, skip to next position
            # print(f"Move from {n} to {i}: {abs(n - i)} fuel")
        if s < min_cost: min_cost = s
    return min_cost

t = time.time()
print(f"Day 7 Part 1 solution: {min_hdist(input, incremental=False)}. Execution time: {time.time()-t:.6f} seconds")

t = time.time()
print(f"Day 7 Part 2 solution: {min_hdist(input, incremental=True)}. Execution time: {time.time()-t:.6f} seconds")
