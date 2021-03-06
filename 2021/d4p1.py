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

    def is_winner(self):
        if self.N in self.scores[0] + self.scores[1]:
            return 1
        else:
            return 0

    def draw_number(self, number):
        c = self.find_number(number)
        if c is None:
            return 0
        self.scores[0][c[0]] += 1
        self.scores[1][c[1]] += 1
        print(self.is_winner())
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

    def play_game(self):
        for i in range(self.D):
            for b in self.boards:
                w = b.draw_number(self.draws[i])
                print(b.scores)
                if w: 
                    return b, self.draws[:i+1]
            # time.sleep(1)

    def get_result(self):
        winner, drawn = self.play_game()
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
result = game.get_result()

print(result)