from timeit import default_timer as timer
import numpy as np
with open('input/input_flash_9') as f:
    series = list(map(lambda x: x[:-1].split(' '),f.readlines()))
t1 = timer()
head = (0,0)
tail = (0,0)
move_head = {
        'R' : lambda x,y: (x[0] + y, x[1]),
        'L' : lambda x,y: (x[0] - y, x[1]),
        'U' : lambda x,y: (x[0], x[1] + y),
        'D' : lambda x,y: (x[0], x[1] - y)
        }

visited = {(0,0) : 1}

for move in series:
    for step in range(int(move[1])):
        head = move_head[move[0]](head,1)
        if abs(tail[0]-head[0])+abs(tail[1]-head[1]) > 1:
            if move[0] == 'R' or move[0] == 'L':
                if head[0]-tail[0] > 1:
                    tail = (head[0]-1,head[1])
                elif tail[0]-head[0] > 1:
                    tail = (head[0]+1,head[1])
            else:
                if head[1]-tail[1] > 1:
                    tail = (head[0],head[1]-1)
                elif tail[1]-head[1] > 1:
                    tail = (head[0],head[1]+1)
        visited[tail] = 1

print(f'Part 2: {sum([v for v in visited.values()])}')

visited = {(0,0):1}
rope = [(0,0) for _ in range(10)]
min_x = min_y = max_x = max_y = 0
for move in series:
    for step in range(int(move[1])):
        rope[0] = move_head[move[0]](rope[0],1)
        for i in range(len(rope)-1):
            if rope[i][0] - rope[i+1][0] > 1:
                if rope[i][1] - rope[i+1][1] > 1:
                    rope[i+1] = (rope[i][0]-1,rope[i][1]-1)
                elif rope[i+1][1] - rope[i][1] > 1:
                    rope[i+1] = (rope[i][0]-1,rope[i][1]+1)
                else:
                    rope[i+1] = (rope[i][0]-1,rope[i][1])
            
            elif rope[i+1][0] - rope[i][0] > 1:
                if rope[i][1] - rope[i+1][1] > 1:
                    rope[i+1] = (rope[i][0]+1,rope[i][1]-1)
                elif rope[i+1][1] - rope[i][1] > 1:
                    rope[i+1] = (rope[i][0]+1,rope[i][1]+1)
                else:
                    rope[i+1] = (rope[i][0]+1,rope[i][1])

            elif rope[i][1] - rope[i+1][1] > 1:
                if rope[i][0] - rope[i+1][0] > 1:
                    rope[i+1] = (rope[i][0]-1,rope[i][1]-1)
                elif rope[i+1][0] - rope[i][0] > 1:
                    rope[i+1] = (rope[i][0]+1,rope[i][1]-1)
                else:
                    rope[i+1] = (rope[i][0],rope[i][1]-1)
            
            elif rope[i+1][1] - rope[i][1] > 1:
                if rope[i][0] - rope[i+1][0] > 1:
                    rope[i+1] = (rope[i][0]-1,rope[i][1]+1)
                elif rope[i+1][0] - rope[i][0] > 1:
                    rope[i+1] = (rope[i][0]+1,rope[i][1]+1)
                else:
                    rope[i+1] = (rope[i][0],rope[i][1]+1)

        # Debug
        #if rope[0][0] < min_x:
        #    min_x = rope[0][0]
        #if rope[0][0] > max_x:
        #    max_x = rope[0][0]
        #if rope[0][1] < min_y:
        #    min_y = rope[0][1]
        #if rope[0][1] > max_y:
        #    max_y = rope[0][1]
        #board = np.ones((max_x-min_x+1,max_y-min_y+1),dtype=str)
        #board[:] = '.'
        #print(f'Move: {move} - step {step}')
        #for r in range(len(rope)):
        #    board[rope[r][0]-min_x,rope[r][1]-min_y] = str(r)
        #for b in board:
        #    print(''.join(b))
        #print('---------------')
        visited[rope[-1]] = 1

print(f'Part 2: {sum([v for v in visited.values()])}')
print(f'Elapsed time: {timer()-t1}')

#print(visited)



