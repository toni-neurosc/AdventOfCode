import numpy as np
import time

def solve(seafloor):
    # This is very slow, takes 10 seconds for the input
    # Not sure where the slow happens, I loop through the whole array twice per step. 
    # Maybe it's the data copying? Or the comparisons?
    # Idea for faster implementation: instead of loops, use -1, 0 and 1 for values, sum the array with the same array rolled by one, ...
    done = False
    step = 0

    while not done:
        done = True
        seafloor_temp = seafloor.copy()
        for i in range(seafloor.shape[0]):
            for j in range(seafloor.shape[1]):
                if seafloor[i, j] == 1 and seafloor[i, (j + 1)  % seafloor.shape[1]] == 0:
                    # print(f"Moving '>' in position [{i}][{j}] right")
                    seafloor_temp[i, j] = 0
                    seafloor_temp[i, (j + 1)  % seafloor.shape[1]] = 1
                    done = False

        seafloor = seafloor_temp.copy()

        for i in range(seafloor.shape[0]):
            for j in range(seafloor.shape[1]):
                if seafloor[i, j] == 10 and seafloor[(i + 1)  % seafloor.shape[0], j] == 0:
                    # print(f"Moving 'v' in position [{i}][{j}] down")
                    seafloor_temp[i, j] = 0
                    seafloor_temp[(i + 1)  % seafloor.shape[0], j] = 10
                    done = False

        seafloor = seafloor_temp.copy()

        step += 1

    return step

def solve_fast(seafloor):
    done = False
    step = 0
    while not done:
        # Horizontal movements
        h_moves = (seafloor - np.roll(seafloor, -1, 1)) == 1
        seafloor -= h_moves
        seafloor += np.roll(h_moves, 1, 1)

        # Vertical movements
        v_moves = (seafloor - np.roll(seafloor, -1, 0)) == 10
        seafloor -= 10*v_moves
        seafloor += 10*np.roll(v_moves, 1, 0)

        if not (h_moves | v_moves).any():
            done=True

        step += 1

    return step

t = time.perf_counter()    
to_integer = {'.': 0, '>': 1, 'v': 10}
seafloor = np.array([[to_integer[c] for c in row] for row in open(0).read().splitlines()])
print(f"Day 25 Part 1 solution: {solve_fast(seafloor)}. Execution time: {time.perf_counter() - t:.6f} seconds.")


