import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('days', type=int) # How many generations to calculate
parser.add_argument('rate', type=int) # How often do the fish reproduce (i.e. every "rate" days)
parser.add_argument('file', type=argparse.FileType('r')) # Input file
args = parser.parse_args()

def grow_lanterfish(fish_count, days):
    # Takes a list of length equal to rate, where each position contains an integer representing
    # the number of fish that have a number of days until replication equal to the position index
    # Then simulated a number of replication cycles equal to the "days" parameter in a recursive fashion

    # print(days)
    # print(fish_count)
    if days > 0:
        new_fish = fish_count[0] # Store the number of fish due for replication
        for i in range(rate+1): 
            fish_count[i] = fish_count[i+1] # Move all the fish that have more than 0 days until reproduction one position down
        fish_count[rate-1] += new_fish # Reset the replication stage of the fish that have just replicated and add them to the proper stage
        fish_count[-1] = new_fish # Add the corresponding newly spawned fish
        return grow_lanterfish(fish_count, days-1)
    else:
        return fish_count

fish = [int(n) for n in args.file.readline().strip().split(',')] # Count fish for each stage of the reproduction cycle
days = args.days
rate = args.rate

fish_count = [fish.count(i) for i in range(rate+2)]

t = time.time()
a = grow_lanterfish(fish_count, days)
print(f"Day 6 Part 2 solution: {sum(a)}")
print(f"Execution time: {time.time() - t:.6f} seconds")
