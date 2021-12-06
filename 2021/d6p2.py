import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('days', type=int) # How many generations to calculate
parser.add_argument('rate', type=int) # How often do the fish reproduce (i.e. every "rate" days)
parser.add_argument('file', type=argparse.FileType('r')) # Input file
args = parser.parse_args()

def grow_lanterfish(fish_count, days):
    # print(days)
    # print(fish_count)
    if days > 0:
        new_fish = fish_count[0]
        for i in range(rate+1):
            fish_count[i] = fish_count[i+1]
        fish_count[rate-1] += new_fish
        fish_count[-1] = new_fish
        return grow_lanterfish(fish_count, days-1)
    else:
        return fish_count

fish = [int(n) for n in args.file.readline().strip().split(',')]
days = args.days
rate = args.rate

fish_count = [fish.count(i) for i in range(rate+2)]

t = time.time()
a = grow_lanterfish(fish_count, days)
print(f"Day 6 Part 2 solution: {sum(a)}")
print(f"Execution time: {time.time() - t:.6f} seconds")
