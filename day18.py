from timeit import default_timer as timer

def compute_connections(cubes:dict) -> None:
    iterator = [(1,0,0),(0,1,0),(0,0,1)]
    for pos in cubes.keys():
        for it in iterator:
            new_pos = (pos[0] - it[0],
                       pos[1] - it[1],
                       pos[2] - it[2])
            if cubes.get(new_pos,-1) != -1:
                cubes[pos] -= 1
                cubes[new_pos] -= 1


def remove_outer_bubbles(cubes:dict,lims:tuple) -> None:
    iterator = [(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
    stack = [(0,0,0)]
    if cubes.get(stack[0]): del cubes[stack[0]]

    while stack:
        x,y,z = stack.pop(0)
        for delta_x,delta_y,delta_z in iterator:
            pos = (x + delta_x, y + delta_y, z + delta_z)
            if 0 <= pos[0] <= lims[0]+1 and 0 <= pos[1] <= lims[1]+1 and 0 <= pos[2] <= lims[2]+1:
                if cubes.get(pos):
                    del cubes[pos]
                    stack.append(pos)
    return


def solve_part1(droplets:dict) -> int:
    compute_connections(droplets)
    return sum([v for v in droplets.values()])


def solve_part2(droplets:dict, lims:tuple) -> int:
    air = {(x,y,z) : 6 for x in range(lims[0]+1) for y in range(lims[1]+1) for z in range(lims[2]+1) if droplets.get((x,y,z),-1) == -1}
    remove_outer_bubbles(air,lims)
    compute_connections(air)
    return sum([v for v in droplets.values()]) - sum([v for v in air.values()])


droplets = {}
max_x = max_y = max_z = 0
with open('input/day18.txt') as f:
    for l in f.readlines():
        x,y,z = list(map(lambda x: int(x),l[:-1].split(',')))
        max_x = x if x > max_x else max_x
        max_y = y if y > max_y else max_y
        max_z = z if z > max_z else max_z
        droplets[(x,y,z)] = 6

t = timer()
print(f'Part 1: {solve_part1(droplets)} ({timer()-t})')
t = timer()
print(f'Part 2: {solve_part2(droplets,(max_x,max_y,max_z))} ({timer()-t})')
