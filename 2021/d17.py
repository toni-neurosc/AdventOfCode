import re
import time
def part2(target_x, target_y):
    # First, find all the possible initial vertical speeds y0 that will land on the target (between Y0 and Y1)
    # For this, we are looking for any amount of consecutive numbers between D-1 and D, where D is the distance
    # between the origin and the bottom (minimum Y coordinate) of the target
    # This is because when we give a Vy initial upwards velocity to the probe, it comes back to Y=0 with 
    # -(Vy+1) downwards speed. If Vy + 1 > D we will miss target, as well as if we shot downwards with Yv0 < D
    y0=[]
    min_y = min(target_y) # Bottom coordinate of target
    max_y = max(target_y) # Top coordinate of target
    for Vy in range(-min_y-1, min_y-1, -1): # Iterate over possible initial vertical speeds
        if min_y <= Vy <= max_y: 
            y0.append((Vy, 1)) # If you hit the target in 1 step record this Vy
        for Vyy in range(Vy-1, min_y-1, -1): # If not, start adding consecutive numbers
            if min_y <= sum(range(Vy, Vyy-1, -1)) <= max_y:
                y0.append((Vy, abs(Vyy-Vy)+1)) # If hit, record Vy
            elif sum(range(Vy,Vyy-1, -1)) < target_y[0]: 
                break # If go past target, change to next Vy

    # Once we know which initical vertical speeds can hit target in Y axis, we check which ones
    # will land in the right X coordinates by looking for sequences of decreasing consecutive numbers
    # starting at Vx and of length equal to the number of steps needed to hit in the Y axis.
    results = set()
    for Vy, steps in y0: # Iterate over possible Vy
        for Vx in range(max(target_x)+1): # Maximum Vx is the farthest end of the target in X
            # Sum decreasing values of Vx (with a minimal value of 0)
            if target_x[0] <= sum([Vx-i if i<=Vx else 0 for i in range(steps)]) <= target_x[1]:
                results.add((Vx,Vy)) # If within target, record pair of speeds (Vx, Vy)
    return len(results)

input = open(0).readline().strip()
print(input)
target_x, target_y = [[int(n) for n in match.split('..')] for match in re.findall("(-*\d+..-*\d+)", input)]

print(f"Day 17 Part 1 solution: {target_y[0]*(target_y[0]+1)//2}")
t = time.time()
print(f"Day 17 Part 2 solution: {part2(target_x, target_y)}. Execution time: {time.time()-t:.6f} seconds")