from timeit import default_timer as timer
import heapq

def find(arr:list,key:str):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == key:
                return (i,j)
    return (0,0)

def bfs(area:list):
    row_max = len(area)
    col_max = len(area[0])
    visited = [[False for _ in range(len(area[0]))] for _ in range(len(area))]
    i,j = find(area,'S')
    print((i,j))
    res = [(0,(i,j))]
    visited[i][j] = True
    area[i][j] = 'a'
    while True:
        cost,pos = heapq.heappop(res)
        iter_pos = [(pos[0]-1,pos[1]),
                    (pos[0]+1,pos[1]),
                    (pos[0],pos[1]-1),
                    (pos[0],pos[1]+1)]
        for p in iter_pos:
            if 0 <= p[0] < row_max and 0 <= p[1] < col_max and not visited[p[0]][p[1]]:
                if area[p[0]][p[1]] == 'E' and area[pos[0]][pos[1]] >= 'y':
                    return cost+1
                elif area[p[0]][p[1]] != 'E' and ord(area[pos[0]][pos[1]])+1 >= ord(area[p[0]][p[1]]):
                    heapq.heappush(res,(cost+1,p))
                    visited[p[0]][p[1]] = True


def reverse_bfs(area):
    row_max = len(area)
    col_max = len(area[0])
    visited = [[False for _ in range(len(area[0]))] for _ in range(len(area))]
    i,j = find(area,'E')
    res = [(0,(i,j))]
    visited[i][j] = True
    area[i][j] = 'z'
    while True:
        cost,pos = heapq.heappop(res)
        iter_pos = [(pos[0]-1,pos[1]),
                    (pos[0]+1,pos[1]),
                    (pos[0],pos[1]-1),
                    (pos[0],pos[1]+1)]
        for p in iter_pos:
            if 0 <= p[0] < row_max and 0 <= p[1] < col_max and not visited[p[0]][p[1]]:
                if area[p[0]][p[1]] == 'a' and area[pos[0]][pos[1]] == 'b':
                    return cost+1
                elif area[p[0]][p[1]] != 'a' and ord(area[pos[0]][pos[1]]) <= ord(area[p[0]][p[1]])+1:
                    heapq.heappush(res,(cost+1,p))
                    visited[p[0]][p[1]] = True


with open('input/day12.txt') as f:
    area = list(map(lambda x: list(x[:-1]),f.readlines()))


t1 = timer()
min = bfs(area)
print(f'Part 1: {min}')
t2 = timer()
print(f'Elapsed time: {t2-t1}')

print(f'Part 2: {reverse_bfs(area)}')
print(f'Elapsed time: {timer()-t2}')
