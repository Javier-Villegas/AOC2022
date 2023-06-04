from timeit import default_timer as timer


operators = {'+' : lambda x,y: x + y,
             '-' : lambda x,y: x - y,
             '*' : lambda x,y: x * y,
             '/' : lambda x,y: x // y
             }


inverse_ops_0 = {'+' : lambda acc,x: acc - x,
                 '-' : lambda acc,x: acc + x,
                 '*' : lambda acc,x: acc // x,
                 '/' : lambda acc,x: acc * x}


inverse_ops_1 = {'+' : lambda acc,x: acc - x,
                 '-' : lambda acc,x: x - acc,
                 '*' : lambda acc,x: acc // x,
                 '/' : lambda acc,x: x // acc}


def operate_path(op, monkeys):
    if len(op) == 1:
        return int(op[0])
    
    return operators[op[1]](
                operate_path(monkeys[op[0]], monkeys),
                operate_path(monkeys[op[2]], monkeys)
            )

def find_path(op, monkeys, key):
    if len(op) == 1:
        return []
    elif op[0] == key or op[2] == key:
        return [key]
    else:
        branch_0 = find_path(monkeys[op[0]], monkeys, key)
        if branch_0:
            return [op[0]] + branch_0
        branch_1 = find_path(monkeys[op[2]], monkeys, key) 
        if branch_1: 
            return [op[2]] + branch_1
        
        return []


def equalize(op, monkeys, path, acc):
    if op[0] == path[-1]:
        return inverse_ops_0[op[1]](acc, operate_path(monkeys[op[2]], monkeys))
    elif op[2] == path[-1]:
        return inverse_ops_1[op[1]](acc, operate_path(monkeys[op[0]], monkeys))
    elif op[0] in path:
        acc = inverse_ops_0[op[1]](acc, operate_path(monkeys[op[2]], monkeys))
        return equalize(monkeys[op[0]], monkeys, path, acc)
    else:
        acc = inverse_ops_1[op[1]](acc, operate_path(monkeys[op[0]], monkeys))
        return equalize(monkeys[op[2]], monkeys, path, acc)


def solve_part_1(monkeys):
    return operate_path(monkeys['root'], monkeys)


def solve_part_2(monkeys):
    path = find_path(monkeys['root'], monkeys, 'humn')
    
    if monkeys['root'][0] in path:
        return equalize(monkeys[monkeys['root'][0]], monkeys, path, operate_path(monkeys[monkeys['root'][2]], monkeys))
    else:
        return equalize(monkeys[monkeys['root'][1]], monkeys, path, operate_path(monkeys[monkeys['root'][0]], monkeys))


with open('input/day21.txt') as f:
    monkeys = {k : v.split(' ') for k,v in list(map(lambda x: x[:-1].split(': '),f.readlines()))}

t1 = timer()
print(f'Part 1: {solve_part_1(monkeys)} ({timer()-t1} seconds)')
t2 = timer()
print(f'Part 2: {solve_part_2(monkeys)} ({timer()-t2} seconds)')
