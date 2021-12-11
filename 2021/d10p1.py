import sys, time
import re

input = [line.strip() for line in sys.stdin.readlines()]


def check_line(s):
    d = {'(':')', '[':']','{':'}','<':'>'}
    scores = {')':3, ']':57, '}':1197, '>':25137}

    line = s # Make a copy of input to work on it
    while line: # Loop for as long as there are characters in the string
        # Find innermost chunks, if there are none the line is incomplete
        matches = tuple(re.finditer('([\(\[\{<][\)\]}>])', line)) 
        # print(len(matches))
        if not matches: #
            print(f"{s} - Line incomplete")
            return 0
        delete = []
        # For each innesmost chunk, check if it's a correct pair, if not return score
        for match in matches:
            chars = match.groups()[0]
            if chars[1] == d[chars[0]]:
                delete += [match.start(), match.end()-1]
            else:
                print(f"{s} - Expected {d[chars[0]]}, but found {chars[1]} instead.")
                return scores[chars[1]]
        line = ''.join([line[i] for i in range(len(line)) if i not in delete])
        # print(line)

score = 0
for line in input:
    score += check_line(line)

print(f"Day 10 Part 1 solution: {score}")