from timeit import default_timer as timer
with open('input/day10.txt') as f:
    instructions = f.readlines()

t1 = timer()
res = 0
X = clock = 1
screen = [['.' for _ in range(40)] for _ in range(6)]
instruction_set_cycles = {'addx':2,'noop':1}

for i,inst in enumerate(instructions):
    inst = inst[:-1].split(' ')
    cycles = instruction_set_cycles[inst[0]]
    Y = int(inst[1]) if cycles == 2 else 0

    for _ in range(cycles):
        if (clock-1)%40 >= X-1 and (clock-1)%40 < (X+2):
            screen[(clock-1)//40][(clock-1)%40] = '#'
        if (clock + 20) % 40 == 0 :
            res += clock*X
        clock += 1
    
    X += Y

print(f'Part 1: {res}')
print(f'Part 2:')
for row in screen:
    print(''.join(row))
print(f'Elapsed time: {timer()-t1}')
        
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
a = np.zeros((8,42))
a[1:-1,1:-1] = (np.array(screen) == '#')

plt.figure()
sns.heatmap(a)
plt.show()

