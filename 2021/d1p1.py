with open("d1_input.txt") as f:
    rp = "" # previous read
    rc = "" # current read
    c = 0 # count
    for line in f:
        if not line:
            continue
        rc = int(line.strip())
        if rp:
            if rc > rp:
                c += 1
        rp = rc

print(c)