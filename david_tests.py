import timeit
import problems
import davids_solver as ds


sections = ds.setup(problems.problem1)
board = ds.init_board(sections)
for loc in range(81):
    assert len(ds.group_memberships[loc]) == 4


'''The solution to problem 1 is:
9 7 1 3 4 6 5 8 2 
2 3 4 5 8 1 7 6 9 
6 8 5 9 7 2 3 4 1 
5 4 2 7 1 8 6 9 3 
8 1 7 6 9 3 4 2 5 
3 6 9 2 5 4 8 1 7 
4 2 3 1 6 7 9 5 8 
7 5 6 8 2 9 1 3 4 
1 9 8 4 3 5 2 7 6 '''
ds.print_board(board)
print(board)
board = ds.add_value(board, sections, 0, 9)
print(board)


def dad_func(x):
    if x < 1:
        return False
    while x | 1 == 0:
        x = x >> 1
    return x == 1


def is_solved(x):
    return x in {1, 2, 4, 8, 16, 32, 64, 128, 256}


print(timeit.timeit("a.union(b)", setup='a={1,2,3};b={4}', number=1_000_000))
print(timeit.timeit("a|b", setup='a,b=7,8', number=1_000_000))

print(timeit.timeit("a.intersection(b)", setup='a={1,2,3};b={4}', number=1_000_000))
print(timeit.timeit("a&b", setup='a,b=7,8', number=1_000_000))

print(timeit.timeit("a.difference(b)", setup='a={1,2,3};b={4}', number=1_000_000))
print(timeit.timeit("a^b", setup='a,b=7,8', number=1_000_000))

print(timeit.timeit("len(a)", setup='a={1,2,3};b={4}', number=1_000_000))
print(timeit.timeit("bin(a).count('1')", setup='a,b=7,8', number=1_000_000)) # this can go faster with gmpy
# print(timeit.timeit("gmpy.popcount(a)", setup='a,b=7,8', number=1_000_000))

print('it all works!')

