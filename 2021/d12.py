import argparse, time
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

def print_matrix(mat):
    for row in mat:
        print(row)
    print()
    return None

def make_mapping(pairs):
    # Get unique IDs for the caves and map them to indexes with a dict:
    cave_names = list(set([item for pair in pairs for item in pair]))
    cave_ids = dict(zip(cave_names, range(len(cave_names))))
    reverse_cave_ids = dict(zip(range(len(cave_names)), cave_names))
    return cave_ids, reverse_cave_ids

def make_adj_mat(pairs, cave_ids):
    # Build adjacency matrix:
    adj_mat = [[0] * len(cave_ids) for count in range(len(cave_ids))]
    # Diagonals are kept 0s because we never want to stay in the same cave
    for pair in pairs:
        adj_mat[cave_ids[pair[0]]][cave_ids[pair[1]]] = 1
        adj_mat[cave_ids[pair[1]]][cave_ids[pair[0]]] = 1
    # Remove connections to start
    for row in adj_mat:
        row[cave_ids['start']] = 0
    return adj_mat

def find_neighbors(node, adjacency_matrix):
    connections = adjacency_matrix[node]
    return [i for i in range(len(connections)) if connections[i] == 1]

def find_paths(pairs, part2 = False):
    cave_ids, reverse_cave_ids = make_mapping(pairs)
    adj_mat = make_adj_mat(pairs, cave_ids)
    neighbors = {cave:find_neighbors(cave, adj_mat) for cave in cave_ids.values()}

    numpaths = 0
    paths = []
    stack = [[cave_ids['start']]]
    twice_stack = [0]

    while stack:
        current_path = stack.pop()
        twice = twice_stack.pop()      
        for node in neighbors[current_path[-1]]:
            node_name = reverse_cave_ids[node]
            if node_name == 'end':
                # paths.append(current_path + [node])
                numpaths += 1
            elif node_name.isupper() or node not in current_path or (part2 and not twice):
                stack.append(current_path + [node])
                twice_stack.append(1 if (node in current_path and node_name.islower()) else twice)
    return numpaths

def find_paths_recursive(pairs, part2 = False):
    cave_ids, reverse_cave_ids = make_mapping(pairs)
    adj_mat = make_adj_mat(pairs, cave_ids)
    neighbors = {cave:find_neighbors(cave, adj_mat) for cave in cave_ids.values()}

    def flatten_list(l):
        return [item for sublist in l for item in sublist]

    def paths_to_end(path, twice, neighbors, reverse_cave_ids):
        if reverse_cave_ids[path[-1]] == 'end':
            return [path]
        else:
            return flatten_list([paths_to_end(path+[n], 1 if n in path and reverse_cave_ids[n].islower() else twice, neighbors, reverse_cave_ids) \
                for n in neighbors[path[-1]] if (reverse_cave_ids[n].isupper() or n not in path or (part2 and not twice))])

    paths = paths_to_end([cave_ids['start']], 0, neighbors, reverse_cave_ids)
    return paths

def translate_paths(pairs, paths):
    reverse_cave_ids = make_mapping(pairs)[1]
    return [[reverse_cave_ids[id] for id in path] for path in paths]
    
pairs = [line.strip().split('-') for line in args.file.readlines()]
# pairs = [line.strip().split('-') for line in open('inputs/d12_input.txt').readlines()]

t = time.time()
paths1 = find_paths(pairs, part2=False)
print(f"Day 12 Part 1 solution: {(paths1)}. Execution time: {time.time()-t:.6f} seconds")
t = time.time()
paths2 = find_paths(pairs, part2=True)
print(f"Day 12 Part 2 solution: {(paths2)}. Execution time: {time.time()-t:.6f} seconds")

t = time.time()
paths3 = find_paths_recursive(pairs, part2=False)
print(f"Day 12 Part 1 solution (recursive): {len(paths3)}. Execution time: {time.time()-t:.6f} seconds")

t = time.time()
paths4 = find_paths_recursive(pairs, part2 = True)
print(f"Day 12 Part 2 solution (recursive): {len(paths4)}. Execution time: {time.time()-t:.6f} seconds")

# print(paths3)
# import profile
# profile.run('find_paths(pairs, part2=True)')