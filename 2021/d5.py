import argparse
import time
import numpy as np

t = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

class Segment():
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def getX(self):
        return [self.start[0], self.end[0]]

    def getY(self):
        return [self.start[1], self.end[1]]

    def is_vert(self):
        if self.start[0] == self.end[0]:
            return True
        else:
            return False

    def is_horz(self):
        if self.start[1] == self.end[1]:
            return True
        else:
            return False

def find_overlaps(segments, board, diagonal=False):
    for s in segments:
        # print(f"Segment is {'Vertical' if s.is_vert() else ('Horizontal' if s.is_horz() else 'Diagonal')}")
        if s.is_vert():
            x = s.getX()[0]
            ymin = min(s.getY())
            ymax = max(s.getY())
            board[ymin:ymax+1, x] += 1
        elif s.is_horz():
            y = s.getY()[0]
            xmin = min(s.getX())
            xmax = max(s.getX())
            board[y, xmin:xmax+1] += 1
        elif diagonal:
            y1 = s.getY()[0]
            y2 = s.getY()[1]
            x1 = s.getX()[0]
            x2 = s.getX()[1]
            yspan = abs(y2-y1)+1
            xspan = abs(x2-x1)+1
            yrange = np.linspace(y1, y2, yspan, dtype=int)
            xrange = np.linspace(x1, x2, xspan, dtype=int)
            for x, y in zip(xrange, yrange):
                board[y, x] += 1
    return np.sum(board > 1)

segments = []
x = []
y = []
for l in args.file.readlines():
    pair = l.strip().split(' -> ')
    start = [int(n) for n in pair[0].split(',')]
    end = [int(n) for n in pair[1].split(',')]
    s = Segment(start, end)
    segments.append(s)
    x += s.getX()
    y += s.getY()
xdim = max(x)+1
ydim = max(y)+1
board = np.zeros([ydim, xdim])
print(f"Part 1 solution: {find_overlaps(segments, board, diagonal = False)}")
board = np.zeros([ydim, xdim])
print(f"Part 2 solution: {find_overlaps(segments, board, diagonal = True)}")

print(f"Execution time: {time.time() - t}")