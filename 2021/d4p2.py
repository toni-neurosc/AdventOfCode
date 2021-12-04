import argparse, time

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

lines = [l.strip() for l in args.file.readlines()]

class board():
    def __init__(self, N):
        self.N = N # Assume square board
        self.numbers = []
        self.scores = ([0] * N, [0] * N) # (row scores, column scores)

    def __str__(self):
        r = ""
        for row in self.numbers:
            r += ' '.join([str(n) for n in row])
            r += '\n'
        return r

    def reset_scores(self):
        self.scores = ([0] * self.N, [0] * self.N) # (row scores, column scores)

    def is_winner(self):
        if (self.N in self.scores[0]) or (self.N in self.scores[1]):
            return True
        else:
            return False

    def draw_number(self, number):
        c = self.find_number(number)
        if c is None:
            return False
        self.scores[0][c[0]] += 1
        self.scores[1][c[1]] += 1
        return self.is_winner()

    def find_number(self, number):
        for i in range(self.N):
            for j in range(self.N):
                if self.numbers[i][j] == number:
                    return (i, j)


    def get_unmarked_sum(self, draws):
        flat = set([i for l in self.numbers for i in l])
        return sum(flat.difference(set(draws)))

    def add_row(self, row):
        self.numbers.append([int(n) for n in row.split()])


class bingo():
    def __init__(self, boards, draws):
        self.boards = boards
        self.draws = draws
        self.D = len(draws)

    def reset_scores(self):
        for b in self.boards:
            b.reset_scores()

    def play_game(self, mode):
        self.reset_scores()
        winner_boards = []
        winner_draws = []
        for i in range(self.D):
            for b in self.boards:
                w = b.draw_number(self.draws[i])
                if w:
                    # print(i, self.draws[i])
                    if mode == 'first': 
                        return b, self.draws[:i+1]
                    elif b not in winner_boards:
                        winner_boards.append(b)
                        winner_draws.append(self.draws[i])
        if mode == 'last':
            # print(winner_boards[-1], self.draws[:self.draws.index(winner_draws[-1]) + 1]
            return winner_boards[-1], self.draws[:self.draws.index(winner_draws[-1]) + 1]
            # time.sleep(1)

    def get_result(self, mode = 'first'):
        winner, drawn = self.play_game(mode)
        return winner.get_unmarked_sum(drawn) * drawn[-1]


L = len(lines)
boards = []
for i in range(L):
    if i == 0:
        draws = [int(n) for n in lines[i].split(',')]
        continue
    if not lines[i]:
        boards.append(board(5)) # In this game boards are 5x5
    else:
        boards[-1].add_row(lines[i])

# for b in boards:
#     print(b)

game = bingo(boards, draws)
print(f"Day 4 Part 1 solution: {game.get_result('first')}")
print(f"Day 4 Part 2 solution: {game.get_result('last')}")
