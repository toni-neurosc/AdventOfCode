import sys, time
import re
from statistics import median

input = [line.strip() for line in sys.stdin.readlines()]

def check_line(s):
    d = {'(':')', '[':']','{':'}','<':'>'}

    line = s # Make a copy of input to work on it
    while line: # Loop for as long as there are characters in the string
        # Find innermost chunks, if there are none the line is incomplete
        matches = tuple(re.finditer('([\(\[\{<][\)\]}>])', line)) 
        # print(len(matches))
        if not matches: #
            print(f"{s} - Line incomplete")
            return 0, line
        delete = []
        # For each innesmost chunk, check if it's a correct pair
        for match in matches:
            chars = match.groups()[0]
            if chars[1] == d[chars[0]]:
                delete += [match.start(), match.end()-1]
            else:
                print(f"{s} - Expected {d[chars[0]]}, but found {chars[1]} instead.")
                return 1, chars[1]
        line = ''.join([line[i] for i in range(len(line)) if i not in delete])
        # print(line)

def complete_line(line):
    d = {'(':')', '[':']','{':'}','<':'>'}

    return [d[c] for c in line[::-1]]

def calculate_score(line):
    points = {')':1, ']':2, '}':3, '>':4}
    score = 0
    for i in range(len(line)):
        score += points[line[i]]*5**(len(line)-i-1)
    return score


scores = []
for line in input:
    is_corrupt, incomplete_line = check_line(line)
    if not is_corrupt:
        scores.append(calculate_score(complete_line(incomplete_line)))

print(f"Day 10 Part 2 solution: {median(scores)}")