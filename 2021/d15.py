import heapq
from collections import defaultdict
import time 

grid = [[int(n) for n in line] for line in open(0).read().splitlines()]

def shortest_path(grid, origin, end=None):
    # Find shortest paths from a node to all the others using Dijkstra's algorithm
    # with a min heap implementation
    nrows = len(grid)
    ncols = len(grid[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    heap = [(0, origin)]
    distances = defaultdict(lambda: float('inf'), {origin:0})
    parents = {origin:None}
    while heap:
        current = heapq.heappop(heap)[1]
        visited.add(current)
        # Generate coordinates for non-diagonal neighbors
        neighbors = [(current[0]+i, current[1]+j) for i,j in moves]
        for neighbor in neighbors:
            if neighbor not in visited and 0 <= neighbor[0] < nrows and 0 <= neighbor[1] < ncols:
                new_distance = distances[current] + grid[neighbor[0]][neighbor[1]]
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current # Keep track of shortest route to a given node
                    heapq.heappush(heap, (new_distance, neighbor))
                if neighbor == end:
                    return distances, parents
            
    return distances, parents

def extend_grid(grid, N):
    # Function to extend the grid N times in both axes
    new_grid = [l[:] for l in grid]
    for n in range(1,N):
        for i in range(len(grid)):
            new_grid[i] += [item+n if item+n<10 else item+n-9 for item in grid[i]]
    for n in range(1,N):
        for i in range(len(grid)):
            new_grid.append([item+n if item+n<10 else item+n-9 for item in new_grid[i]])
    return new_grid

def get_path(parents, origin, end):
    # Get the sequence of nodes that make the shortest path from origin to end
    # provided that end was visited during the graph walk
    found = False
    path = [end]
    while not found:
        path.append(parents[path[-1]])
        if path[-1] == origin:
            found = True
    return path[::-1]

def print_path(grid, path):
    # Print grid to console with shortest path in bold
    for i, row in enumerate(grid):
        line = ''
        for j, number in enumerate(row):
            if (i,j) in path:
                line += "\033[1m" + str(number) + "\033[0m"
            else:
                line += str(number)
        print(line)
    return None

t = time.time()
distances, parents = shortest_path(grid, (0,0))
print(f"Day 15 Part 1 solution: {distances[(len(grid)-1, len(grid[0])-1)]}. Execution time: {time.time()-t:.6f} seconds")
path = get_path(parents, (0,0), (len(grid)-1, len(grid[0])-1))
print_path(grid, path)
t = time.time()
grid = extend_grid(grid, 5)
distances, parents = shortest_path(grid, (0,0), (len(grid)-1, len(grid[0])-1))
print(f"Day 15 Part 2 solution: {distances[(len(grid)-1, len(grid[0])-1)]}. Execution time: {time.time()-t:.6f} seconds")
# path = get_path(parents, (0,0), (len(grid)-1, len(grid[0])-1))
# print_path(grid, path)