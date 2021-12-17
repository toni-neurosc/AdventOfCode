import math
operations =  (sum, math.prod, min, max, None,
               lambda x: 1 if x[0] > x[1] else 0,
               lambda x: 1 if x[0] < x[1] else 0, 
               lambda x: 1 if x[0] == x[1] else 0)

sumversions = 0
def parse_packet(packet):
    global sumversions # Initially I returned this through recursive calls
    sumversions += int(packet[:3],2)
    typeid = int(packet[3:6],2)
    if typeid == 4: # Base case
        content = packet[6:]
        groups = []
        for i in range(len(content)//5):
            groups.append(content[(i*5)+1:(i+1)*5])
            if content[i*5] == '0': break
        return int(''.join(groups), 2), packet[len(groups*5)+6:] 
    else:
        values = []
        lengthid = 15 if packet[6] == '0' else 11
        countdown = int(packet[7:7+lengthid],2)
        content = packet[7+lengthid:]
        counter = 0
        while counter < countdown:
            sub_value, content = parse_packet(content)
            values.append(sub_value)
            counter = len(packet)-7-lengthid-len(content) if lengthid == 15 else counter+1
        value = operations[typeid](values)
        return value, content
        
hexa = open(0).readline().strip()
binary = bin(int(hexa, 16))[2:].zfill(4*len(hexa))

result = parse_packet(binary)[0]
print(f"Day 16 Part 1 solution: {sumversions}")
print(f"Day 16 Part 2 solution: {result}")