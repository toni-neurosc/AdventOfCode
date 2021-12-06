import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument('days', type=int)
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

fish = [int(n) for n in args.file.readline().strip().split(',')]
days = args.days

def grow_lanterfish(fish_list, days):
    if days > 0:
        fish = fish_list[-1]
        fish_list.append([n-1 if n > 0 else 6 for n in fish] + [8] * fish.count(0))
        return grow_lanterfish(fish_list, days-1)
    else:
        return fish_list

def print_lanternfish(fish_list):
    for i, fish in enumerate(fish_list):
        if i == 0:
            print(f"Initial state: {','.join([str(i) for i in fish])}")
        elif i == 1:
            print(f"After  {i} day:  {','.join([str(i) for i in fish])}")
        elif i > 9:
            print(f"After {i} days: {','.join([str(i) for i in fish])}")
        else:
            print(f"After  {i} days: {','.join([str(i) for i in fish])}")

# print_lanternfish(grow_lanterfish([fish], days))

fish_list = grow_lanterfish([fish], days)
print(f"Part 1 solution: {len(fish_list[-1])}")