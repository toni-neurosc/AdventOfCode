# %%
import sys, time

input = [line.strip().split(' | ') for line in sys.stdin.readlines()]
# input = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'.split(' | ')
# input = 'abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | cdfeb fcadb cdfeb cdbaf'.split(' | ')
# input = 'abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | ac fcadb acd cdbaf'.split(' | ')

# %%

def decode(patterns):
    S = [set(s) for s in patterns]

    D_numbers = dict()
    D_segments = dict()

    D_numbers[1] = [s for s in S if len(s) == 2][0]
    D_numbers[4] = [s for s in S if len(s) == 4][0]
    D_numbers[7] = [s for s in S if len(s) == 3][0]
    D_numbers[8] = [s for s in S if len(s) == 7][0]

    set_five = [s for s in S if len(s) == 5]
    set_six = [s for s in S if len(s) == 6]

    D_segments['a'] = D_numbers[7].difference(D_numbers[1])
    bd = D_numbers[4].difference(D_numbers[1])
    eg = D_numbers[8].difference(set.union(D_numbers[7], D_numbers[4]))
    abfg = set.intersection(*set_six)
    adg = set.intersection(*set_five)
    cde = D_numbers[8].difference(abfg)
    D_segments['d'] = set.intersection(adg, cde)
    D_segments['b'] = bd.difference(D_segments['d'])
    D_segments['f'] = abfg.difference(adg).difference(D_segments['b'])
    D_segments['g'] = abfg.difference(set.union(D_segments['a'], D_segments['b'], D_segments['f']))
    D_segments['c'] = cde.difference(set.union(bd,eg))
    D_segments['e'] = eg.difference(D_segments['g'])

    return {j.pop():i for i,j in D_segments.items()}


def part1(outputs):
    # print(outputs)
    # n = 0
    # for output in outputs:
    #     for number in output.split():
    #         print(number)
    #         if len(number) in [2,3,4,7]:
    #             n += 1
    # return n
    return len([number for output in outputs for number in output.split() if len(number) in [2,3,4,7]])

def part2(input):
    reverse_code = {'abcefg':'0',
                    'cf':'1',
                    'acdeg':'2',
                    'acdfg':'3',
                    'bcdf':'4', 
                    'abdfg':'5',
                    'abdefg':'6',
                    'acf':'7',
                    'abcdefg':'8',
                    'abcdfg':'9'}
    total = 0
    for data in input:
        code = decode(data[0].split())
        print(code)
        number = ''
        for word in data[1].split():
            translated = ''.join(sorted([code[letter] for letter in word]))
            number += reverse_code[translated]
        total += int(number)
    return total



outputs = [i[1] for i in input]
print(f"Day 8 Part 1 solution: {part1(outputs)}")
print(f"Day 8 Part 2 solution: {part2(input)}")
