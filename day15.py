import re
from timeit import default_timer as timer
import numpy as np


def contains(x,y,s,b):
    d = abs(s[0]-b[0])+abs(s[1]-b[1])
    dxy = abs(s[0]-x)+abs(s[1]-y)
    return dxy <= d


with open('input/day15.txt') as f:
    pairs = f.readlines()


pairs = list(map(lambda y: list(map(lambda x: int(x),re.findall(r'([-]*\d+).*?([-]*\d+).*?([-]*\d+).*?([-]*\d+)',y)[0])),pairs))
pairs = list(map(lambda x: [(x[0],x[1]),(x[2],x[3])],pairs))

res = set()
y = 2000000
t1 = timer()
for s,b in pairs:
    d = abs(s[0]-b[0])+abs(s[1]-b[1])
    if s[1] < y:
        if s[1] + d >= y:
            n = s[1]+d-y+1
            for i in range(0,n):
                res.add(s[0]+i)
                res.add(s[0]-i)
    else:
        if s[1]-d <= y:
            n = y-(s[1]-d)+1
            for i in range(0,n):
                res.add(s[0]+i)
                res.add(s[0]-i)
for s,b in pairs:
    if s[1] == y and s[0] in res:
        res.remove(s[0])
    if b[1] == y and b[0] in res:
        res.remove(b[0])

maximum = 4000000
def solve_part2(pairs):
    for i,(s,b) in enumerate(pairs):
        d = abs(s[0]-b[0])+abs(s[1]-b[1])+1
        
        for x,y in zip(range(s[0]-d,s[0]+1),range(s[1],s[1]+d+1)):
            
            if not (0 <= x <= maximum) or not (0 <= y <= maximum):
                continue

            if not any([contains(x,y,sref,bref) for j,(sref,bref) in enumerate(pairs) if j != i]):
                return (x,y)

        for x,y in zip(range(s[0]-d,s[0]+1),range(s[1],s[1]-d,-1)):
            if not (0 <= x <= maximum) or not (0 <= y <= maximum):
                continue
            found = False
            for j,(sref,bref) in enumerate(pairs):
                if i == j:
                    continue
                found = contains(x,y,sref,bref)
                if found:
                    break
            if not found:
                return (x,y)
    
    
        for x,y in zip(range(s[0],s[0]+d+1),range(s[1]+d,s[1]-1,-1)):
            if not (0 <= x <= maximum) or not (0 <= y <= maximum):
                continue
            found = False
            for j,(sref,bref) in enumerate(pairs):
                if i == j:
                    continue
                found = contains(x,y,sref,bref)
                if found:
                    break
            if not found:
                return (x,y)
    
        for x,y in zip(range(s[0],s[0]+d+1),range(s[1]-d,s[1]+1)):
            if not (0 <= x <= maximum) or not (0 <= y <= maximum):
                continue
            found = False
            for j,(sref,bref) in enumerate(pairs):
                if i == j:
                    continue
                found = contains(x,y,sref,bref)
                if found:
                    break
            if not found:
                return (x,y)

def solver_part22(pairs):
    outer = []
    for s,b in pairs:
        ranges = set()
        ranges.update(set([(x,y) for x,y in zip(range(s[0]-d,s[0]+1)),range(s[1]+d,s[1]+1)]),
                      set([(x,y) for x,y in zip(range(s[0]-d,s[0]+1)),range(s[1]-d,s[1]-d,-1)]))
import matplotlib.pyplot as plt
import seaborn as sns

x,y = solve_part2(pairs)
print(f'Part 1: {len(res)}')
print(f'Part 2: {x*4000000+y}')
print(f'Elapsed time: {timer()-t1}')
