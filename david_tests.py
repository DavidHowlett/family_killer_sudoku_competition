import timeit


if __name__ == '__main__':
    # print(timeit.timeit("a.union(b)", setup='a={1,2,3};b={4}', number=1_000_000))
    # print(timeit.timeit("a|b", setup='a,b=7,8', number=1_000_000))

    # print(timeit.timeit("a.intersection(b)", setup='a={1,2,3};b={4}', number=1_000_000))
    # print(timeit.timeit("a&b", setup='a,b=7,8', number=1_000_000))

    # print(timeit.timeit("a.difference(b)", setup='a={1,2,3};b={4}', number=1_000_000))
    # print(timeit.timeit("a^b", setup='a,b=7,8', number=1_000_000))

    print(timeit.timeit("len(a)", setup='a={1,2,3};b={4}', number=1_000_000))
    print(timeit.timeit("bin(a).count('1')", setup='a,b=7,8', number=1_000_000)) # this can go faster with gmpy
    # print(timeit.timeit("gmpy.popcount(a)", setup='a,b=7,8', number=1_000_000))
    print(timeit.timeit(
        "7 in {1,2,4,8,16,32,64,128,256}", number=1_000_000))
    print(timeit.timeit(
        "solved(7)", setup='def solved(x):return (x in {1,2,4,8,16,32,64,128,256})', number=1_000_000))
    setup = 'import davids_solver as ds;import problems;import copy;sections = ds.setup(problems.problem1)'
    print(timeit.timeit("[s.copy() for s in sections]", setup=setup, number=10_000))
    print(timeit.timeit("copy.deepcopy(sections)", setup=setup, number=10_000))

    print('it all works!')
