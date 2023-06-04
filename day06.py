from timeit import default_timer as timer
with open('input/day06.txt') as f:
    signal = f.read()

t = timer()
part_one = False
for i in range(len(signal)):
    if not part_one and len(set(signal[i:i+4])) == 4:
        print(f'Part 1: {i+4}')
        part_one = True
    elif part_one and len(set(signal[i:i+14])) == 14:
        print(f'Part 2: {i+14}')
        break
print(f'Elapsed time: {timer()-t}')
