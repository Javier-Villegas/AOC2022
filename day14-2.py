import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from timeit import default_timer as timer
from numba import jit,uintc

with open('input/day14.txt') as f:
    walls = list(map(lambda x: x[:-1].split(' -> '),f.readlines()))

sand_source = (500,0)
cave = np.zeros((1001,1001),dtype=np.uint32)

for w in walls:
    i = 0
    (a,b) = w[i].split(',')
    while i < len(w)-1:
        (na,nb) = w[i+1].split(',')
        minx = min(int(a),int(na))
        maxx = max(int(a),int(na))
        miny = min(int(b),int(nb))
        maxy = max(int(b),int(nb))
        if miny != maxy:
            cave[miny:maxy+1, minx] = 1
        else:
            cave[miny, minx:maxx+1] = 1
        a = na
        b = nb
        i += 1

floor = 0
for i in range(cave.shape[0]-1,-1,-1):
    if not (cave[i,:] < 1).all(): 
        floor = i
        break

def solve_part1_2(cave):
    j = 0
    part1 = True
    while True:
    #for j in range(94):
        y,x = (-1,500)
        if cave[0,500] == 2:
            return j
        while True:
            if y+1 > floor:
                if part1:
                    part1 = False
                    print(f'Part 1: {j}')               
                if y+1 > floor+1:
                    cave[y,x] = 2
                    break
            if cave[y+1,x] == 0: 
                y += 1
            elif cave[y+1,x] == 1 or cave[y+1,x] == 2:
                if cave[y+1,x-1] == 0:
                    x -= 1
                    y += 1
                elif cave[y+1,x+1] == 0:
                    x += 1
                    y += 1
                else:
                    cave[y,x] = 2
                    break

        j += 1

@jit(parallel=False,nopython=True)
def solve_part1(cave):
    i = 0
    while True:
        y,x = (-1,500)
        while True:
            if y+1 > floor:
                return i
            #if cave[y+1,x] = '.':
            #    y += 1
            if cave[y+1,x] != 0:
                if cave[y+1,x-1] == 0:
                    x -= 1
                elif cave[y+1,x+1] == 0:
                    x += 1
                else:
                    cave[y,x] = 2
                    break
            y += 1
        i += 1

@jit(parallel=False,nopython=True)
def solve_part2(cave):
    i = 0
    while True:
        y,x = (-1,500)
        if cave[0,500] == 2:
            return i
        while True:
            if y > floor:
                cave[y,x] = 2
                break
            if cave[y+1,x] != 0:
                if cave[y+1,x-1] == 0:
                    x -= 1
                elif cave[y+1,x+1] == 0:
                    x += 1
                else:
                    cave[y,x] = 2
                    break
            y += 1
        i += 1
cave[0,500] = 2
solve_part1(np.zeros((floor,floor)))
solve_part2(cave)
cave[0,500] = 0
t1 = timer()
p1 = solve_part1(cave)
print(f'Part 1: {p1}')
print(f'Part 2: {p1+solve_part2(cave)}')
print(f'Elapsed time: {timer()-t1}')
#print(f'Part 2: {solve_part1_2(cave)}')


#plt.figure()
#cave[cave == 0] = '0'
#cave[cave == '+'] = '5'
#cave[cave == '#'] = '2'
#cave[cave == 'o'] = '4'
#sns.heatmap(cave[:floor+2,325:675].astype(int))
#plt.show()
