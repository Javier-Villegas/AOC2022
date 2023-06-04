import re
import bisect
from numba import jit

class Valve(list):
    def __init__(self,name,flow):
        self.name = name
        self.flow = flow
        self.costs = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def next(valve,time,pressure,closed,visited):
    if time == 0:
        return {}

    ret = [{'valve':valve,'time':time,'pressure':pressure,'closed':closed,'visited':visited}]

    if valve.flow == 0 and valve.name not in closed:
        next_closed = closed+[valve.name]
        next_valve = []
    elif valve.name in closed:
        next_valve = []
    else:
        next_valve = [valve]


    next_valve = next_valve+[v for v in valve]

    next_valve = sorted(next_valve,key=lambda x: 0 if x.name in closed else x.flow*(time-1) if x.name != valve.name else x.flow*(time),reverse=True)
    time -= 1
    for nv in next_valve:
        next_closed = closed if nv.name != valve.name else closed+[valve.name]
        next_pressure = pressure if nv.name != valve.name else pressure + valve.flow*time

        #if (valve.name,nv.name,next_pressure,next_closed) not in visited:
        if not list(filter(lambda x: x[0] == valve.name and 
                                 x[1] == nv.name and
                                 x[2] <= next_pressure and
                                 x[3] == next_closed,
                       visited)):

            visited.append((valve.name,nv.name,next_pressure,next_closed))
            ret.append({'valve':nv,
                        'time':time,
                        'pressure': next_pressure,
                        'closed': next_closed,
                        'visited':visited})
            return ret
    ret[0]['time'] = time
    return ret

def search(valve,key,depth,visited):
    if valve.name == key:
        return 0

    if valve.name in visited:
        return -1

    if list(filter(lambda x: x.name == key,valve)):
        return depth+1
    else:
        ret = []
        for v in valve:
            ret.append(search(v,key,depth+1,visited+[valve.name]))
        ret =  list(filter(lambda x: x >= 0,ret))
        if ret:
            return sorted(ret)[0]
    return -1
    
def find_weigths(rooms, state,visited_states):
    valve = state['valve']
    time = state['time']
    pressure = state['pressure']
    open_valves = state['open_valves']


    weigths = []
    for v in open_valves:
        w = valve.costs[rooms[v].name]#search(valve,rooms[v].name,0,[])
        weigths.append((rooms[v].name,rooms[v].flow*(time-w-1),w))

    for w in sorted(list(filter(lambda x: x[1] > 0, weigths)),key=lambda x: x[1],reverse=True):
        next_open_valves = open_valves.copy()
        next_open_valves.remove(rooms[w[0]].name)

        if not list(filter(lambda x: 
                           x['valve'].name == w[0] and
                           x['pressure'] >= pressure+w[1]  and
                           x['open_valves'] == next_open_valves and 
                           x['time'] == time-w[2]-1,visited_states)):
            return w[1] 
    return 0


def next_best(rooms,state,visited_states):
    valve = state['valve']
    time = state['time']
    pressure = state['pressure']
    open_valves = state['open_valves']


    #weigths = []
    #for v in open_valves:
    #    w = valve.costs[rooms[v].name]#search(valve,rooms[v].name,0,[])
    #    weigths.append((rooms[v].name,rooms[v].flow*(time-w-1),w))

    weigths = list(map(lambda x: (rooms[x].name,rooms[x].flow*(time-valve.costs[rooms[x].name]-1),valve.costs[rooms[x].name]),open_valves))
    for w in sorted(list(filter(lambda x: x[1] > 0, weigths)),key=lambda x: x[1],reverse=True):
        next_open_valves = open_valves.copy()
        next_open_valves.remove(rooms[w[0]].name)

        if not list(filter(lambda x: 
                           x['valve'].name == w[0] and
                           x['pressure'] >= pressure+w[1]  and
                           x['open_valves'] == next_open_valves and 
                           x['time'] >= time-w[2]-1,visited_states)):
            new_state ={'valve':rooms[w[0]],'time':time-w[2]-1,'pressure':pressure+w[1],'open_valves':next_open_valves}
            visited_states.append(new_state)
            return [state,new_state]
    return []
    
def part1(rooms):
    open_valves = [v.name for v in rooms.values() if v.flow > 0]

    status = [{'valve':rooms['AA'],'time':30,'pressure':0,'open_valves':open_valves}]
    known_states = []
    maximum = 0
    while status:
        state = status.pop(-1)
        #print(len(known_states))
        ret_states = next_best(rooms,state,known_states)
        if ret_states:
            #if not ret_states[-1]['open_valves']:
            #    print(ret_states[-1]['pressure'])
            #    exit()
            if ret_states[-1]['pressure'] > maximum:
                maximum = ret_states[-1]['pressure']
                maximum_ret = ret_states[-1]
    
            if ret_states[0]['pressure'] > ret_states[1]['pressure']:
                print('What the fuck? Why?')
                status.append(ret_states[1])
                status.append(ret_states[0])
            else:
                status.append(ret_states[0])
                status.append(ret_states[1])
                #bisect.insort(status,ret_states[0],key=lambda x: x['pressure']+find_weigths(rooms,x,known_states))
                #bisect.insort(status,ret_states[1],key=lambda x: x['pressure']+find_weigths(rooms,x,known_states))
    print(maximum)
    return maximum



from timeit import default_timer as timer
with open('input/day16.txt') as f:
    valves = list(map(lambda x: re.findall(r'([A-Z]{2}|[\d]+)',x),f.readlines()))

rooms = {}
for valve in valves:
    rooms[valve[0]] = Valve(valve[0],int(valve[1]))

for valve in valves:
    rooms[valve[0]].extend([rooms[v] for v in valve[2:]])

for valve in rooms.values():
    print('A mi me estan grabando')
    valve.costs = {v.name : search(valve,v.name,0,[]) for v in rooms.values()}
    print(valve.costs)
    #valve.costs = sorted(valve.costs,key=valve.costs.get)
    #print(valve.costs)


import networkx as nx
import matplotlib.pyplot as plt
graph = nx.DiGraph()
for v1 in rooms.values():
        for v2 in rooms.values():
            if v1.costs[v2.name] == 1 or (v1.costs[v2.name] == 0 and v1.flow > 0):
                graph.add_edge(v1.name,v2.name,weigth=v1.costs[v2.name])

plt.figure()
nx.draw(graph)
plt.show()


#open_valves = [v.name for v in rooms.values() if v.flow > 0]
#
#status = [{'valve':rooms['AA'],'time':30,'pressure':0,'open_valves':open_valves}]
#known_states = []
#
#maximum = 0
#t1 = timer()
#while status:
#    state = status.pop(-1)
#
#    ret_states = next_best(rooms,state,known_states)
#    if ret_states:
#        #if not ret_states[-1]['open_valves']:
#        #    print(ret_states[-1]['pressure'])
#        #    exit()
#        if ret_states[-1]['pressure'] > maximum:
#            maximum = ret_states[-1]['pressure']
#            maximum_ret = ret_states[-1]
#
#        if ret_states[0]['pressure'] > ret_states[1]['pressure']:
#            print('What the fuck? Why?')
#            status.append(ret_states[1])
#            status.append(ret_states[0])
#        else:
#            status.append(ret_states[0])
#            status.append(ret_states[1])
    
    #for s in ret_states:
    #   status.append(s) 

    #input()
t1 = timer()
#part1(rooms)
#print(maximum)
#print(maximum_ret)

print(f'{timer()-t1}')

#print(sorted(list(filter(lambda x: x['valve'].name == 'DD' and x['open_valves']==['BB','CC','EE','HH','JJ'],known_states)),key=lambda x: x['pressure'])[-1])
#print(sorted(list(filter(lambda x: x['valve'].name == 'BB' and x['open_valves']==['CC','EE','HH','JJ'],known_states)),key=lambda x: x['pressure'])[-1])
#print(sorted(list(filter(lambda x: x['valve'].name == 'JJ' and x['open_valves']==['CC','EE','HH'],known_states)),key=lambda x: x['pressure'])[-1])
#print(sorted(list(filter(lambda x: x['valve'].name == 'HH' and x['open_valves']==['CC','EE'],known_states)),key=lambda x: x['pressure'])[-1])
#print(sorted(list(filter(lambda x: x['valve'].name == 'EE' and x['open_valves']==['CC'],known_states)),key=lambda x: x['pressure'])[-1])
#print(sorted(list(filter(lambda x: x['valve'].name == 'CC' and x['open_valves']==[],known_states)),key=lambda x: x['pressure'])[-1])



def possible_paths(node):
    queue = collections.deque([0,node])
    result = {}
    while deque:
        distance, node = queue.popleft()
        for node2 in node:
            if node2 not in results:
                results[node2] = distance+2
                queue.append((distance+1,node2))
