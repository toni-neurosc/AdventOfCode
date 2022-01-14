from collections import defaultdict
from time import perf_counter

COSTS = {'A':1, 'B':10, 'C':100, 'D':1000}
ROOMCOLS = {3:'A', 5:'B', 7:'C', 9:'D'}

def manhattan(a, b):
    # Cityblock distance between 2 points
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def print_board(state):
    # Print board for debugging
    board = [list("#############"), 
             list("#...........#"),
             list("###.#.#.#.###"),
             list("  #.#.#.#.#  "),
             list("  #########  ")]
    for room, char in state:
        board[room[0]][room[1]] = char
    for row in board:
        print(''.join(row))
        
def solve(diagram, part2 = False):
    # Takes the diagram as input and returns minimum cost to organize the amphipods 

    def clear_path(start, end, occupied):
        # Check if hallway is free between the 2 column coordinates
        colrange = range(min(start[1], end[1])+1, max(start[1], end[1]))
        for room in occupied:
            if room != start and room in hallway and room[1] in colrange:
                return False
        # if start or destination is a room check that room space above is free:
        for tile in (start, end):
            if tile not in hallway:
                for j in range(tile[0]-1, 0, -1):
                    if (j, tile[1]) in occupied:
                        return False
        return True

    def is_solved(state):
        return all([room in rooms[char] for room, char in state])
        
    if part2:
        diagram = (diagram[:3] +
                   ["  #D#C#B#A#"] +
                   ["  #D#B#A#C#"] +
                   diagram[3:])
        
    hallway = set()
    rooms = defaultdict(set)
    initial_state = ()

    for i, row in enumerate(diagram):
        for j, char in enumerate(row):
            if char in 'ABCD':
                initial_state += (((i,j), char),)
            if char in '.ABCD':
                if diagram[i-1][j] == diagram[i+1][j] == '#':
                    hallway.add((i,j))
                elif diagram[i][j-1] ==  diagram[i][j+1] == '#':
                    rooms[ROOMCOLS[j]].add((i,j))

    queue = [(0, initial_state)]
    cost_dict = defaultdict(lambda: float('inf'))
    min_cost = float('inf')

    while queue:
        cost, state = queue.pop()
        state_dict = {item[0]:item[1] for item in state}
        occupied = set(state_dict.keys())

        for start, char in state: # Iterate through amphipods
            
            # If already in final position skip the move
            if start in rooms[char]: # in proper room
                if (start[0]+1, start[1]) not in state_dict: # has nothing below
                    continue # skip move
                elif state_dict[(start[0]+1, start[1])] == char: # has something below and it's the same
                    continue # skip move
            
            if start not in hallway: # If in wrong room may move to hallway
                dest = (hallway - occupied)
            # Note: i don't allow room to room movements to be able to compute costs using Manhattan distance
            else: # If in hallway can go to the proper room
                for room in sorted(rooms[char], reverse=True): # Check positions in row starting inside
                    if room not in state_dict: # if position is empty move there
                        dest = {room}
                        break
                    elif state_dict[room] != char: # if there's an incorrect pod there not move yet
                        dest = set()
                        break

            # Filter out obstructed paths 
            dest = [end for end in dest if clear_path(start, end, occupied)]      

            # For each legal movement, generate new states and costs and add to queue
            for end in dest:
                new_state_dict = state_dict.copy()
                del new_state_dict[start]
                new_state_dict[end] = char
                
                # Transform the new state into a sorted tuple to add to the cost dictionary
                new_state = tuple(sorted([((k[0],k[1]),v) for k,v in new_state_dict.items()], key = lambda x: (x[0][0],x[0][1])))
                new_cost = cost + (manhattan(start, end) * COSTS[char])

                if is_solved(new_state):
                    if new_cost < min_cost:
                        min_cost = new_cost # Update minimal cost if smaller than currently registered
                elif new_cost < cost_dict[new_state]:
                    # Only add the new state and cost if a cheaper way to reach it was found
                    cost_dict[new_state] = new_cost
                    queue.append((new_cost, new_state))

    return(min_cost)

diagram = open(0).read().splitlines()
t = perf_counter()
print(f"Day 23 Part 1 solution: {solve(diagram)}. Execution time: {perf_counter() - t:.6f} seconds.")

t = perf_counter()
print(f"Day 23 Part 2 solution: {solve(diagram, True)}. Execution time: {perf_counter() - t:.6f} seconds.")

# Comments on performance: currently takes about 10 seconds to find the solution
# Profiling shows that most of the time is taken by the clear_path function
# followed by sorting and the lambda function from the dictionary to tuple conversion
# A more efficient way to convert the state to hashable would help, as well as