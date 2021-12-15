import collections
from os import killpg
import time

lines = open(0).read().splitlines()
chain = lines[0]
rules = {pair[0]:pair[1] for pair in [tuple(line.split(' -> ')) for line in lines[2:]]}

def polymerize_naive(chain, rules, steps):
    # This is an almost one-liner that runs a simulation of the polymerization process
    # Very memory intenstive
    for i in range(steps):
        chain = ''.join([chain[i]+rules[chain[i:i+2]] if chain[i:i+2] in rules.keys() else chain[i:i+2] for i in range(len(chain)-1) ]) + chain[-1]
    return [chain.count(c) for c in set(chain)]

def polymerize_recursive(chain, rules, steps):
    # This is a recursive approach using memoization, because I wanted to practice that
    # However, it's overly complex for the task at hand, since iteration with a simple 
    # update rule is sufficient for this problem. 

    # Get list of all possible characters
    chars = sorted(list( set(chain) | set(rules.values()) | set(''.join(rules.keys())) ))
    
    cache = {} # Initialize empty dictionary for memoization
    def recurse(pair, depth):
        # Base case
        if depth == 0:
            if (pair, 0) not in cache:
                cache[(pair, 0)] = {char:pair.count(char) for char in chars}
            return cache[(pair, 0)]

        # Generate new pairs    
        new_pairs =  [pair[0]+rules[pair], rules[pair]+pair[1]]
        counter = collections.Counter()
        for new_pair in new_pairs:
            if (new_pair, depth-1) in cache:
                counter.update(cache[(new_pair, depth-1)]) # If result in cache, recursion not needed 
            else:
                counter.update(recurse(new_pair, depth-1)) # Recursive call
        counter[rules[pair]] -= 1 # The inserted character is in both pairs, so it was counted twice
        cache[(pair, depth)] = counter # Add result to cache
        return counter
    
    # Call recursive function for each pair in original string
    pairs = [chain[i:i+2] for i in range(len(chain)-1)] 
    result = collections.Counter()
    for pair in pairs:
        result.update(recurse(pair, steps))
    # Remove overlaps
    result.update({char:-chain[1:-1].count(char) for char in chars})
    return result


def polymerize_iterative(chain, rules, steps):
    # This implementation uses a Counter (a special form of dictionary) to 
    # keep track of the number of occurrences of each pair, and for each iteration
    # updates the counts according to a simple rule: if a pair P1 with count C
    # transforms into P2 and P3, then count for P1 is decreased by C, and count
    # for P2 and P3 is increased by C 

    pairs = [chain[i:i+2] for i in range(len(chain)-1)]
    # Make a dictionary that maps a pair to the resulting pairs after insertion
    transform = {k:[k[0]+v, v+k[1]] for k,v in rules.items()}

    counter = collections.Counter(pairs)
    for i in range(steps):
        delta = collections.Counter()
        # Add up all the changes in a single step
        for pair, count in counter.items():
            delta[transform[pair][0]] += count
            delta[transform[pair][1]] += count
            delta[pair] -= count
        # Update the count with the changes
        counter.update(delta)

    # Count all the characters in the pairs, taking into account that all appear twice
    # (all pairs overlap) except the 2 characters at the ends of the chain 
    result = collections.Counter()
    for pair,count in counter.items():
        result.update({k:(v*count) for k,v in collections.Counter(pair).items()})
    result[chain[0]] += 1
    result[chain[-1]] += 1
    return {k:v//2 for k,v in result.items()}
 


t = time.time()
counts = polymerize_recursive(chain, rules, 10)
print(f"Day 14 Part 1 solution: {max(counts.values()) - min(counts.values())}. Execution time: {time.time()-t:.6f} seconds")
t = time.time()
counts = polymerize_recursive(chain, rules, 40)
print(f"Day 14 Part 2 solution: {max(counts.values()) - min(counts.values())}. Execution time: {time.time()-t:.6f} seconds")


t = time.time()
counts = polymerize_iterative(chain, rules, 10)
print(f"Day 14 Part 1 solution: {max(counts.values()) - min(counts.values())}. Execution time: {time.time()-t:.6f} seconds")
t = time.time()
counts = polymerize_iterative(chain, rules, 40)
print(f"Day 14 Part 2 solution: {max(counts.values()) - min(counts.values())}. Execution time: {time.time()-t:.6f} seconds")
