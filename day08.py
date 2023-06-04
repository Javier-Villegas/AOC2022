from itertools import product
from timeit import default_timer as timer


def part_one(forest):
    visible_trees = [0 for j in range(len(forest)) for i in range(len(forest[0]))]
    right_left = [product(range(len(forest)),range(len(forest[0]))),
                  product(range(len(forest)),range(len(forest[0])-1,-1,-1))]
    top_bottom = [product(range(len(forest[0])),range(len(forest))),
                  product(range(len(forest[0])),range(len(forest)-1,-1,-1))]

    for x_dir in right_left:
        tallest = [-1 for _ in range(len(forest))]
        for i,j in x_dir:
            if tallest[i] < forest[i][j]:
                tallest[i] = forest[i][j]
                visible_trees[i+len(forest)*j] = 1

    for y_dir in top_bottom:
        tallest = [-1 for _ in range(len(forest[0]))]
        for j,i in y_dir:
            if tallest[j] < forest[i][j]:
                tallest[j] = forest[i][j]
                visible_trees[i+len(forest)*j] = 1

    return sum(visible_trees)


def part_two(forest):
    scenic_score = 0
    for i,j in product(range(len(forest)),range(len(forest[0]))):
        left_right = [range(j+1,len(forest[0])),range(j-1,-1,-1)]
        top_bottom = [range(i+1,len(forest)),range(i-1,-1,-1)]
        res = 1

        for x_dir in left_right:
            score = 0
            for x in x_dir:
                score += 1
                if forest[i][x] >= forest[i][j]:
                    break
            res *= score

        for y_dir in top_bottom:
            score = 0
            for y in y_dir:
                score += 1
                if forest[y][j] >= forest[i][j]:
                    break
            res *= score

        if res > scenic_score:
            scenic_score = res

    return scenic_score


with open('input/day08.txt') as f:
    forest = list(map(lambda x: list(map(lambda y: int(y),x[:-1])),f.readlines()))

t1 = timer()
print(f'Part 1: {part_one(forest)}')
print(f'Part 2: {part_two(forest)}')
print(f'Elapsed time: {timer()-t1}')
