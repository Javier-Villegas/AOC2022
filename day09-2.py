from timeit import default_timer as timer

def simulate(moves,n):
    dx_dy = {'R':(1,0),'L':(-1,0),'U':(0,1),'D':(0,-1)}
    rope = [[0,0] for _ in range(n)]
    visited = {(0,0):1}

    for direction,steps in list(map(lambda x: x[:-1].split(' '),moves)):
        dx,dy = dx_dy[direction]
        for step in range(int(steps)):
            rope[0][0] += dx
            rope[0][1] += dy
            
            for i in range(n-1):
                Ax = rope[i][0] - rope[i+1][0] 
                Ay = rope[i][1] - rope[i+1][1]
                if abs(Ax) > 1 or abs(Ay) > 1:
                    rope[i+1][0] += 1 if Ax > 0 else -1 if Ax < 0 else 0
                    rope[i+1][1] += 1 if Ay > 0 else -1 if Ay < 0 else 0
            visited[tuple(rope[-1])] = 1
    return sum([v for v in visited.values()])

with open('input/day09.txt') as f:
    moves = f.readlines()

t1 = timer()
print(f'Part 1: {simulate(moves,2)}')
print(f'Part 2: {simulate(moves,10)}')
print(f'Elapsed time: {timer()-t1}')
