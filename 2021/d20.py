import time 

def zeropad(image, n, char):
    padded = [char * n + row + char * n for row in image]
    for i in range(n):
        padded.append(char * len(padded[0]))
        padded.insert(0, padded[-1])
    return padded

def enhance(image, code, pad):
    padded = zeropad(image, 2, pad)
    new_image = []
    for i in range(1,len(padded)-1):
        row = ''
        for j in range(1,len(padded[0])-1):
            row += code[int(padded[i-1][j-1:j+2] + padded[i][j-1:j+2] + padded[i+1][j-1:j+2],2)]
        # print(row)
        new_image.append(row)
    return new_image

def print_image(image):
    for row in image:
        print(''.join(['#' if c == '1' else '.' for c in row]))
    print('\n')

def solve(image, code, n):
    for i in range(n):
        image = enhance(image, code, '0' if i%2==0 else '1')
    return ''.join(image).count('1')


input = [''.join(['1' if c == '#' else '0' for c in line]) for line in open(0).read().splitlines()]
code = input[0]
image = input[2:]

t = time.time()
print(f"Day 20 Part 1 solution: {solve(image,code,2)}. Execution time: {time.time()-t:.6f} seconds")

t = time.time()
print(f"Day 20 Part 1 solution: {solve(image,code,50)}. Execution time: {time.time()-t:.6f} seconds")
