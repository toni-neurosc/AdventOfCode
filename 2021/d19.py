import numpy as np
import time

def merge_maps(a1,a2):
    # Return relative position (x,y,z) of scanner with a2 
    for p1 in a1:    # Loop through points in both arrays
        s1 = set([frozenset([abs(n) for n in p]) for p in a1 - p1]) # Center a1 around p1 and make set of frozensets (hashable)
        for p2 in a2:
            s2 = set([frozenset([abs(n) for n in p]) for p in a2 - p2])  # Center a2 around p2 and maket set
            overlap = (s1 & s2)
            if  len(overlap) > 11:
                order, sign = find_orientation(a1 - p1, a2 - p2, overlap)
                d = p1 - p2[order]*sign
                if d is not None:
                    return np.unique(np.vstack([a1, (a2[:,order]*sign)+d]), axis=0), d
    return None, None

def find_orientation(a1, a2, overlap):
    # Find an the coordinates of an overlapping point
    overlap = set([item for item in overlap if 0 not in item])  
    o = overlap.pop()
    i1 = [ i for i,p in enumerate(a1) if len(set(map(abs,p)) & o ) == 3 ][0]
    i2 = [ i for i,p in enumerate(a2) if len(set(map(abs,p)) & o ) == 3 ][0]
    p1, p2 = a1[i1], a2[i2]
    order = [0] * 3
    sign = [0] * 3
    for i in range(3):
        order[i] = np.where(abs(p2) == abs(p1[i]))[0][0]
        sign[i] = p1[i] // p2[order[i]]
    return order, sign

def beacon_map(scanners):
    beacons = scanners[0]
    queue = scanners[1:]
    scanner_positions = []
    while queue:
        new_scan = queue.pop(0)
        new_beacons, position = merge_maps(beacons, new_scan)
        if new_beacons is not None:
            beacons = new_beacons
            scanner_positions.append(position)
        else:
            queue.append(new_scan)
    return new_beacons, scanner_positions

report = []
scan = []
for line in open(0).read().splitlines():
    if line.startswith('---'):
        if scan:
            report.append(np.array(scan))
        scan = []
    elif line:
        scan.append([int(n) for n in line.split(',')])
report.append(np.array(scan))

t = time.time()
beacon_positions, scanner_positions = beacon_map(report)
print(f"Day 19 Part 1 solution: {len(beacon_positions)}. Execution time: {time.time()-t:.6f} seconds.")

t = time.time()
max_distance = 0
for i in range(len(scanner_positions)):
    for j in range(len(scanner_positions)):
        if i != j:
            s = sum(abs(scanner_positions[i]-scanner_positions[j]))
            if s > max_distance: max_distance = s

print(f"Day 19 Part 2 solution: {max_distance}. Execution time: {time.time()-t:.6f} seconds.")


