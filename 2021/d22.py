
def get_volume(cuboid):
    x,y,z = cuboid[1:]
    return (x[1]-x[0]+1)*(y[1]-y[0]+1)*(z[1]-z[0]+1)

def get_intersection(cuboidA, cuboidB):
    # To do
    overlaps = []
    for dim in range(1, 4):
        endpoints = cuboidA[dim]+cuboidB[dim]
        endpoints = list(zip(endpoints, ['A', 'A', 'B', 'B']))
        endpoints.sort()
        if endpoints[0][1] == endpoints[1][1]:
            overlaps.append((endpoints[1][0], endpoints[2][0]))
        else:
            return None
    return overlaps

    print(overlaps)

    return overlaps[0]*overlaps[1]*overlaps[2]

def reboot_reactor(steps, part = 1):
    pass

cuboids = []
for line in open(0).read().splitlines():
    instruction, coordinates = line.split()
    coordinates = [tuple(dim[2:].split('..')) for dim in coordinates.split(',')]
    x,y,z = [(int(p[0]), int(p[1])) for p in coordinates]
    cuboids.append( (instruction, x, y ,z) )

print(get_intersection(cuboids[0], cuboids[1]))
# print(f"Day 22 Part 1 solution: {reboot_reactor(steps)}")
# print(f"Day 22 Part 1 solution: {reboot_reactor(steps, part = 2)}")