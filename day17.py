from timeit import default_timer as timer
from typing import Union

class Rock(dict):
    def __init__(self,kind,bottom):
        if kind == '+':
            self.left = 2
            self.right = self.left+2
            self.bottom = bottom
            self.top = bottom+2
            self[0] = (self.left,self.bottom+1)
            self[1] = (self.left+1,self.bottom)
            self[2] = (self.right,self.bottom+1)
            self[3] = (self.left+1,self.bottom+2)
        if kind == '-':
            self.left = 2
            self.bottom = bottom
            self.right = self.left+3
            self.top = bottom
            self[0] = (self.left,self.bottom)
            self[1] = (self.left+1,self.bottom)
            self[2] = (self.left+2,self.bottom)
            self[3] = (self.left+3,self.bottom)

        if kind == '|':
            self.bottom = bottom
            self.top = bottom+3
            self.left = 2
            self.right = self.left
            self[0] = (self.left,self.bottom)
            self[1] = (self.left,self.bottom+1)
            self[2] = (self.left,self.bottom+2)
            self[3] = (self.left,self.bottom+3)

        if kind == 'L':
            self.left = 2
            self.bottom = bottom
            self.top = bottom+2
            self.right = self.left+2
            self[0] = (self.left+2,self.bottom+2)
            self[1] = (self.left+2,self.bottom+1)
            self[2] = (self.left+2,self.bottom)
            self[3] = (self.left+1,self.bottom)
            self[4] = (self.left,self.bottom)


        if kind == 'o':
            self.left = 2
            self.bottom = bottom
            self.top = bottom+1
            self.right = self.left+1
            self[0] = (self.left,self.bottom+1)
            self[1] = (self.left,self.bottom)
            self[2] = (self.right,self.bottom)
            self[3] = (self.right,self.bottom+1)

    def __move_right(self,cave):
        if self.right < 6 and not [1 for piece in self.values() if cave.get((piece[0]+1,piece[1]))]:
            self.right += 1
            self.left += 1
            for key in self.keys():
                pos = self[key]
                self[key] = (pos[0]+1,pos[1])
            return True
        else:
            return False


    def __move_left(self,cave):
        if self.left > 0 and not [1 for piece in self.values() if cave.get((piece[0]-1,piece[1]))]:
            self.right -= 1
            self.left -= 1
            for key in self.keys():
                pos = self[key]
                self[key] = (pos[0]-1,pos[1])
            return True
        else:
            return False

    def move_horizontal(self,cave,direction):
        if direction == '<':
            self.__move_left(cave)
        elif direction == '>':
            self.__move_right(cave)
        

    def move_down(self,cave):
        if self.bottom > 0 and not [1 for piece in self.values() if cave.get((piece[0],piece[1]-1))]:
            self.bottom -= 1
            self.top -= 1
            for key in self.keys():
                pos = self[key]
                self[key] = (pos[0],pos[1]-1)
            return True
        else:
            return False




def simulation(jets,n,part2=False) -> Union[int,list]:
    top = jet_iter = last_left = last_right = i = 0
    rock_kinds= ['-','+','L','|','o']
    cave = {}
    periodic_height = {}

    while i < n or part2:
        rock = Rock(kind=rock_kinds[i%5],bottom=top+3)
        falling = True

        if part2 and i % 5 == 0 and last_left != 0 and last_right != 6:
            if periodic_height.get(jet_iter):
                periodic_height[jet_iter].append((i,top))
                break
            else:
                periodic_height[jet_iter] = [(i,top)]

        while falling:
            rock.move_horizontal(cave,jets[jet_iter])

            jet_iter = jet_iter+1 if jet_iter+1 < len(jets) else 0
            #jet_iter = (jet_iter+1)%len(jets)
            falling = rock.move_down(cave)

        last_left = rock.left
        last_right = rock.right
        top = top if rock.top < top else rock.top+1
        for pieces in rock.values():
            cave[pieces] = 1

        i += 1
    

    if part2:
        return periodic_height[jet_iter]
    else:
        return top


def solve_part1(jets) -> int:
    result = simulation(jets,2022)
    assert isinstance(result, int)
    return result


def solve_part2(jets) -> int:
    base = simulation(jets,n=0,part2=True)
    assert isinstance(base,list)
    delta_rocks = base[1][0]-base[0][0]
    delta_height = base[1][1]-base[0][1]
    iters = 1_000_000_000_000
    return ((iters-base[0][0])//delta_rocks-1)*delta_height+simulation(jets,delta_rocks+iters%delta_rocks)


with open('input/day17.txt') as f:
    jets = f.read()[:-1]

t1 = timer()
print(f'Part 1: {solve_part1(jets)} ({timer()-t1} seconds)')
t2 = timer()
print(f'part 2: {solve_part2(jets)} ({timer()-t2} seconds)')
