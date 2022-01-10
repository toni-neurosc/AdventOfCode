from itertools import product
from collections import Counter, defaultdict

def part1(position):
    player = 0
    die = list(range(1,101))
    scores = [0,0]
    turn = 0
    while scores[0] < 1000 and scores[1] < 1000:
        turn += 1
        position[player] = position[player] + sum(die[:3])
        while position[player] > 10: 
            position[player] -= 10
        scores[player] += position[player]
        # print(f"Turn {turn}: Player {player+1} rolls {die[0]}+{die[1]}+{die[2]} and moves to space {position[player]} for a total score of {scores[player]}")
        die = die[3:] + die[:3]
        player = abs(player-1)
    print(f"Day 21 Part 1 solution: {scores[player]*turn*3}")

def part2(position):
    outcomes = Counter([sum(p) for p in product([1,2,3],repeat=3)])
    states = {((0,position[0]),(0,position[1])): 1} # {((player1score, player1pos), (player2score, player2pos)) : universeCount}
    player = 0
    done = False
    while not done:
        new_states = defaultdict(int)
        done = True
        for state, universes in list(states.items()):
            if state[0][0] < 21 and state[1][0] < 21:
                done = False
                for result, count in outcomes.items():
                    pos = state[player][1] + result
                    while pos > 10: 
                        pos -= 10
                    new_state = (state[0], (state[1][0]+pos, pos)) if player else ((state[0][0]+pos, pos), state[1])
                    new_states[new_state] += count * universes
            else:
                new_states[state] += universes
        states = new_states        
        player = abs(player-1)
    winned = [0,0]
    for state, universes in states.items():
        if state[0][0] > state[1][0]:
            winned[0] += universes
        else:
            winned[1] += universes
    print(f"Day 21 Part 2 solution: {max(winned)}")

position = [int(line.split(': ')[1]) for line in open(0).read().splitlines()]
print(f"Player 1 starting position: {position[0]}")
print(f"Player 2 starting position: {position[1]}")

part1(position[:])
part2(position[:])