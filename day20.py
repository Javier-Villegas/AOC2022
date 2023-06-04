from uuid import uuid1

class Node:
    def __init__(self, number):
        self.number = number
        self.id = uuid1()

with open('input/day20.txt') as f:
    files = list(map(lambda x: Node(int(x)),f.readlines()))

file_size = len(files)
for n in files.copy():
    pos = files.index(n)
    files.pop(pos)

    if i == 0:
        files.insert(pos, i)
    elif i > 0:
        new_pos = (pos + i) % (file_size - 1)
        if new_pos == 0:
            files.append(i)
        else:
            files.insert(new_pos, i)
    elif i < 0:
        new_pos = pos + i
        if new_pos < 0:
            new_pos = (new_pos % (file_size - 1))
        if new_pos == 0:
            files.append(i)
        else:
            files.insert(new_pos, i)


pos_zero = files.index(0)
print(files[(1000+pos_zero)%file_size])
print(files[(2000+pos_zero)%file_size])
print(files[(3000+pos_zero)%file_size])
print(sum([files[(1000+pos_zero)%file_size],files[(2000+pos_zero)%file_size],files[(3000+pos_zero)%file_size]]))
