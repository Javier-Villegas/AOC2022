from timeit import default_timer as timer
def size(directory):
    s = 0
    for e in directory:
        if type(e) == File: 
            s += e.size
        else:
            s += size(e)
    directory.size = s
    return s


class Dir(list):
    def __init__(self,name):
        self.name = name
        self.size = 0

    def __str__(self):
        return self.name + ('\n'+'\t'*self.name.count('/'))+ ('\n'+'\t'*self.name.count('/')).join([str(e) for e in self])


class File():
    def __init__(self,name,size):
        self.name = name
        self.size = size
    
    def __str__(self):
        return f'File {self.name} (size={self.size})'


def cd(directory, command):
    if command == '/':
        return '/'
    elif command == '..':
        split = directory[::-1].split('/',2)
        return split[-1][::-1]+'/'
    else:
        return directory + command + '/'


with open('input/day07.txt') as f:
    terminal = f.readlines()

t1 = timer()
directory = ''
filesystem = {'/' : Dir('/')}

for cmd in terminal:
    if cmd[0] == '$':
        if cmd[2:4] == 'cd':
            directory = cd(directory,cmd[:-1].split(' ')[-1])
            current_dir = filesystem[directory]
    else:
        a,b = cmd[:-1].split(' ')
        if a == 'dir':
            filesystem[directory+b+'/'] = Dir(directory+b+'/')
            current_dir.append(filesystem[directory+b+'/'])
        else:
            current_dir.append(File(b,int(a)))

size(filesystem['/'])

need_free = filesystem['/'].size-(70000000-30000000)
print(f'Part 1: {sum([d.size for d in filesystem.values() if d.size <= 100000])}')
print(f'Part 2: {sorted([d.size for d in filesystem.values() if d.size >= need_free ])[0]}')
print(f'Elapsed time: {timer()-t1}')
#print(filesystem['/'])
