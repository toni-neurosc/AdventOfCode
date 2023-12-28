#%%
import operator
from random import randint
from itertools import product
import numpy as np

class ALU:
    def __init__(self, program) -> None:
        self.memory = [0, 0, 0, 0]
        self.address = {'w':0, 'x':1, 'y':2, 'z':3}
        self.operators = {'inp': operator.setitem,
                          'add': operator.add,
                          'mul': operator.mul,
                          'div': operator.floordiv,
                          'mod': operator.mod,
                          'eql': operator.eq}
        self.program = program

    def test_number(self, digits):
        self.memory = [0, 0, 0, 0]
        zs = []
        for digit, step in zip(digits, program):
            step = [step[0] + (digit,)] + step[1:]
            for instruction in step:
                self.operation(*instruction)
                # print(f"Executing {step[0]} operation with inputs {step[1]} and {step[2]}. Memory: {self.memory}")
            zs.append(self.get_memory('z'))
        return(zs)
        # return self.memory

    def get_memory(self, address):
        return self.memory[self.address[address]]  

    def operation(self, operation, a, b):
        if isinstance(b, str):
            b = self.memory[self.address[b]]

        if operation == 'inp':
            self.operators[operation](self.memory, self.address[a], b)
        else:
            self.memory[self.address[a]] = int(self.operators[operation](self.memory[self.address[a]], b))

#%%
program = []
instructions = []
# for line in open(0).read().splitlines():
for line in open('d24_input.txt').read().splitlines():
    l = tuple([int(item) if not item.isalpha() else item for item in line.split()])
    if l[0] == 'inp':
        if instructions: program.append(instructions)
        instructions = [l]
    else:
        instructions.append(l)
program.append(instructions)

# params
a = np.array([step[4][2] for step in program])
b = np.array([step[5][2] for step in program])
c = np.array([step[15][2] for step in program])

print('a', a)
print('b', b)
print('c', c)
print('b+c', b+c)

# Generate all possible numbers of len L that don't contain 0's
def generate_numbers(L):
    return np.array(list(product(range(1,10), repeat=L)))

def part1():
    last_g0 = np.argwhere(b+c==0)[-1][0]
    numbers = generate_numbers(last_g0)
    print(f"Number list length: {numbers.shape[0]}")
    z = np.zeros([numbers.shape[0]])
    for i in range(last_g0):
        z = (z // a[i]) * 26 + numbers[:, i] + c[i]

    p = sum(a[last_g0:]==26)
    print(26**(p-1), 26**p)

    valid = np.where((z >= 26**(p-1)) & (z < 26**p))
    numbers = numbers[valid]
    z = z[valid]
    print(f"Number of valid numbers: {numbers.shape[0]}")

    # for i in range(last_g0, len(program)):
    #     numbers = np.hstack((numbers, ((z % 26) + b[i]).reshape([numbers.shape[0],1])))
    #     z = z // a[i]
    #     valid = np.where((numbers[:, -1] > 0) & (numbers[:, -1] < 10))
    #     numbers = numbers[valid]
    #     z = z[valid]
    #     print(numbers[-5:])
    
    
    print(z)
    return numbers, z

numbers, z = part1()

#%%
# Then, select viable numbers and calculate the rest of the digits by using (z % 26) + b == w

# Test my formula 
test_ALU = ALU(program)
def test_number_formula(number):
    zs = []
    z = 0
    for i, w in enumerate(number):
        g = not ((z % 26) + b[i] == w)
        z = ( ( z // a[i] ) * ( 25 * g + 1 ) ) + g * ( w + c[i] )
        zs.append(z)
    return(zs)

def test_formula():
    for n in range(100):
        number =[randint(1,9) for i in range(14)]
        aluZs = test_ALU.test_number(number)
        formulaZs = test_number_formula(number)
        if aluZs != formulaZs:
            print(f"Test failed for number {number}.")
    print(f"Test succesful.")

# test_formula()
# print(test_number_formula([5,3,6,8,2,4,5]))
# print(test_number_formula([9,9,9,9,9,9,9]))

#%%
test_ALU = ALU(program)
print(test_ALU.test_number([1,3,2,1,8,4,8]))
print(test_ALU.test_number([1,3,5,7,9,2,4,6,8,9,9,9,9,9]))




# %%
