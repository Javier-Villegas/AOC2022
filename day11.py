from timeit import default_timer as timer

    
class Monkey:
    def __init__(self,m):
        self.items,self.operation,self.mod,self.test,self.next = process_monkey(m)





def process_monkey(m):
    m = m.split('\n')
    items = list(map(lambda x: int(x),m[1].split(': ')[1].split(', ')))
    op = m[2].split(' = ')[1].split(' ')
    op1 = (lambda x,y: x+y) if op[1]=='+' else (lambda x,y: x*y)
    op2 = (lambda z: op1((z if op[0] == 'old' else int(op[0])), (z if op[2] == 'old' else int(op[2]))))
    test = (lambda t: t % int(m[3].split(' ')[-1]) == 0)
    test_res = { True : int(m[4][-1]), False : int(m[5][-1])}
    return (items,op2,int(m[3].split(' ')[-1]),test,test_res)

with open('input/day11.txt') as f:
    monkey_chunk = f.read().split('\n\n')

t1 = timer()


monkeys = list(map(lambda x: Monkey(x),monkey_chunk))
activity = [0 for _ in range(len(monkeys))]
for _ in range(20):
    for i in range(len(monkeys)):
        activity[i] += len(monkeys[i].items)
        for val in monkeys[i].items:
            next_value = monkeys[i].operation(val)//3
            next_monkey = monkeys[i].next[monkeys[i].test(next_value)]
            monkeys[next_monkey].items.append(next_value)
        monkeys[i].items.clear()

print(f'Part 1: {(lambda x,y: x*y)(*sorted(activity,reverse=True)[:2])}')


from functools import reduce
monkeys = list(map(lambda x: Monkey(x),monkey_chunk))
mod = reduce(lambda x,y: x*y,[monkey.mod for monkey in monkeys])
activity = [0 for _ in range(len(monkeys))]
for _ in range(10000):
    for i in range(len(monkeys)):
        activity[i] += len(monkeys[i].items)
        for val in monkeys[i].items:
            next_value = monkeys[i].operation(val)%mod
            next_monkey = monkeys[i].next[monkeys[i].test(next_value)]

            monkeys[next_monkey].items.append(next_value)
        monkeys[i].items.clear()

print(f'Part 2: {(lambda x,y: x*y)(*sorted(activity,reverse=True)[:2])}')
print(f'Elapsed time: {timer()-t1}')
