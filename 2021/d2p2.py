with open("d2_input.txt") as f:
    h = 0 # horizontal position
    d = 0 # depth
    a = 0 # aim
    for line in f:
        if not line:
            continue
        c = line.strip().split(' ') # command
        c1 = c[0] # type of command
        c2 = int(c[1]) # magnitude of command
        if c1 == 'forward':
            h += c2
            d += a*c2
        elif c1 == 'up':
            a -= c2
        elif c1 == 'down':
            a += c2
print(h*d)