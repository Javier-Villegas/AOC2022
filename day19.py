from dataclasses import dataclass
from functools import lru_cache
import re

class Material:

    def __init__(self,clay,ore,obsidian,geode):
        self.clay = clay
        self.ore = ore
        self.obsidian = obsidian
        self.geode = geode
        return 

    def __str__(self):
        return f'Clay: {self.clay} Ore: {self.ore} Obsidian: {self.obsidian} Geode: {self.geode}'

    def __le__(self, other):
        return (self.clay <= other.clay and self.ore <= other.ore and self.obsidian <= other.obsidian)

    def __add__(self, other):
        return Material(self.clay+other.clay,self.ore+other.ore,self.obsidian+other.obsidian,self.geode+other.geode)

    def __sub__(self, other):
        return Material(self.clay-other.clay,self.ore-other.ore,self.obsidian-other.obsidian,self.geode-other.geode)


    def copy(self):
        return Material(self.clay,self.ore,self.obsidian,self.geode)


class Blueprint:
    id: int
    cost: dict[str,Material]
    time: int = 1
    storage: Material = Material(clay=0,ore=1,obsidian=0,geode=0)
    production: Material = Material(clay=0,ore=1,obsidian=0,geode=0)

    def __init__(self,bp:str='') -> None:
        if bp:
            mat = re.findall(r'[0-9]+',bp)
            print(mat)
            self.id = int(mat[0])
            self.cost = {}
            self.cost['ore'] = Material(clay=0,ore=int(mat[1]),obsidian=0,geode=0)
            self.cost['clay'] = Material(clay=0,ore=int(mat[2]),obsidian=0,geode=0)
            self.cost['obsidian'] = Material(clay=int(mat[4]),ore=int(mat[3]),obsidian=0,geode=0)
            self.cost['geode'] = Material(clay=0,ore=int(mat[5]),obsidian=int(mat[6]),geode=0)

        return

    def __str__(self):
        return 'Blueprint ' +str(self.id)+'\nStorage: '+str(self.storage)+'\nProduction: '+str(self.production)+'\nRobot cost:\n\t'+"\n\t".join([r+": "+str(m) for r,m in self.cost.items()])


    def __repr__(self):
        return '\n'+self.__str__()

    def copy(self):
        new_blueprint = Blueprint()
        new_blueprint.id = self.id
        new_blueprint.time = self.time
        new_blueprint.cost = self.cost.copy()
        new_blueprint.storage = self.storage.copy()
        new_blueprint.production = self.production.copy()
        return new_blueprint
    
    def update_time(self):
        self.storage = self.storage + self.production
        self.time += 1

def next(blueprint:Blueprint,visited):
    stack = [blueprint] 
    #while stack:
    while blueprint.time < 24:
        #blueprint = stack.pop(0)
        blueprint.update_time()
        #if blueprint in visited:
            #continue
        if blueprint.cost['geode'] <= blueprint.storage:
            new_bp = blueprint.copy()
            new_bp.storage -= new_bp.cost['geode']
            print(f'Time: {new_bp.time} + 1 geode/min')
            new_bp.production.geode += 1
            #visited.append(new_bp)
            blueprint = new_bp
            continue

        if not blueprint.production.obsidian or blueprint.cost['geode'].obsidian/blueprint.production.obsidian > blueprint.cost['geode'].ore/blueprint.production.ore:
            if blueprint.cost['obsidian'] <= blueprint.storage:
                blueprint.storage -= blueprint.cost['obsidian']
                blueprint.production.obsidian += 1
                print(f'Time: {blueprint.time} + 1 obsidian/min')
            
        if not blueprint.production.clay or blueprint.cost['obsidian'].clay/blueprint.production.clay > blueprint.cost['obsidian'].ore/blueprint.production.ore:
            if blueprint.cost['clay'] <= blueprint.storage:
                blueprint.storage -= blueprint.cost['clay']
                blueprint.production.clay += 1
                print(f'Time: {blueprint.time} + 1 clay/min')
        if blueprint.cost['ore'] <= blueprint.storage:
            blueprint.storage -= blueprint.cost['ore']
            blueprint.production.ore += 1
            print(f'Time: {blueprint.time} + 1 ore/min')
    return blueprint


    

with open('input/test19') as f:
    blueprints = [Blueprint(x) for x in f.readlines()]
    #print(blueprints)


for bp in blueprints:
    print(next(bp,[]))
