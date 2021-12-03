W = 3 # window size

with open("d1_input.txt") as f:
    l = f.readlines() # all lines

m = [int(line.strip())for line in l]
n = len(m) # number of measurements

print(n, n+1-W)
c=0
sc = ""
sp = ""
for i in range(n+1-W):
    sc = sum(m[i:i+3]) # current sum
    if sp:
        if sc > sp:
            c += 1
    sp = sc
print(c)