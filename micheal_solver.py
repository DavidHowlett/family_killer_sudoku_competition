# this is designed to solve kiler suduko
# square is a 1x1 grid and box is a 3x3 grid

# 123
# 456  #the number for each box
# 789
import copy
import datetime

counter = 0


def solve(supo, sums, sum2,bi,ci,ri):
    # supo=suduko posibillities
    # sums=list of lists which contain a list of loactions and what they add up to
    # sum2[x][y] = numbers that can be used to sum to x in y spaces
    # bi = box impossibilities = all the known numbers in a box
    # ci = coloumn impossibilities
    # ri = row impossibilities
    global counter
    d = 1
    while d == 1:  # for as long as the last attempt solved somthing, search again
        d = 0
        for row in range(9):
            for col in range(9):  # col for column
                #bn = int((row - (row % 3)) + (col - (col % 3)) / 3)  # box number. bi[bn]=all the numbers that square can't be because of the box its in.
                sq = supo[row][col]  # sq is the square we want to deal with
                if type(sq) is list:
                    a = 0
                    sq = sq.copy()
                    si = []
                    for s in range(len(sums)):
                        if [row, col] in sums[s][0]:
                            si = sum2[len(sums[s][0])][sums[s][1]]  # sum impossiblities
                            break
                    for i in range(len(sq)):  # for each possibility in square
                        # print(sq[i],bi[int((row-(row%3))+(col-(col%3))/3)],row,col,int((row-(row%3))+(col-(col%3))/3),bi)
                        if (sq[i] in bi[int((row - (row % 3)) + (col - (col % 3)) / 3)]) or (sq[i] in ci[col]) or (
                                sq[i] in ri[row]) or (
                                sq[i] in si):  # if a possibility is in the row, col, box or cant be in section
                            supo[row][col].pop(i - a)
                            a += 1
                    if len(supo[row][col]) == 0:  # if there are no soloutions
                        return 'error'
                    if len(supo[row][col]) == 1:  # if square is now solved
                        d = 1
                        supo[row][col] = supo[row][col][0]
                        ci[col].append(supo[row][col])
                        ri[row].append(supo[row][col])
                        bi[int((row - (row % 3)) + (col - (col % 3)) / 3)].append(supo[row][col])
                        sums[s][1] = sums[s][1] - supo[row][col]  # s is the index for where in sums sq is
                        for i in range(len(sums[s][0])):  # remove sq from the sum it's in
                            if sums[s][0][i] == [row, col]:
                                sums[s][0].pop(i)
                                if (sums[s] == [[], 0]) and (s != len(sums) - 1):  # last bit provides robustness
                                    sums.pop(s)
                                break
    allsolved = 'true'
    for row in range(9):
        for col in range(9):
            if type(supo[row][col]) == list:  # this section checks if it's all solved, if so it returns the answer
                allsolved = 'false'
                break
    if allsolved == 'true':
        return supo
    for np in range(2, 10):  # finds location of square with least uncertainty np=number of possibillities
        for row in range(9):
            for col in range(9):
                if type(supo[row][col]) == list:  # if unknown
                    if len(supo[row][col]) == np:  # if least unknowns
                        for i in range(np):  # for each possibility
                            for s in range(len(sums)):
                                if [row, col] in sums[s][0]:
                                    for m in range(len(sums[s][0])):  # removes square from sums2
                                        if [row, col] == sums[s][0][m]:
                                            sums2 = copy.deepcopy(sums)
                                            sums2[s][0].pop(m)
                                            testsupo = copy.deepcopy(supo)
                                            sums2[s][1] -= supo[row][col][i]
                                            testsupo[row][col] = testsupo[row][col][i]
                                            bi2 = copy.deepcopy(bi)
                                            ci2 = copy.deepcopy(ci)
                                            ri2 = copy.deepcopy(ri)
                                            bi2[int((row - (row % 3)) + (col - (col % 3)) / 3)].append(supo[row][col][i])
                                            ci2[col].append(supo[row][col][i])
                                            ri2[row].append(supo[row][col][i])
                                            test = solve(testsupo, sums2, sum2,bi2,ci2,ri2)  # test if it is a soloution
                                            if test == 'error':
                                                counter += 1
                                                break
                                            else:
                                                return test
                        return 'error'
    return 'error'


def sum1(a):  # finds every way to sum a:9
    if a == 9:
        return [[[], 0], [[9], 9]]
    b = sum1(a + 1)  # finds every way to sum a+1:9
    for i in range(len(b)):
        c = b[i]
        c = c.copy()
        d = c[0]
        d = d.copy()
        d = [a] + d  # add another number
        c[1] += a  # increase total
        b.append([d, c[1]])  # add an extra way of summing which includes a
    return b


def sum2():
    a = sum1(1)
    length = len(a)
    sumto = []
    for total in range(46):
        b = []
        for i in range(length):
            if a[i][1] == total:
                b.append(a[i])
        sumto.append(b)
    # sumto[x] gives all ways to sum to x
    # print(sumto)
    sum2 = []
    for length in range(10):
        b = []
        for total in range(46):
            c = []
            for i in range(len(sumto[total])):
                if len(sumto[total][i][0]) == length:
                    c = c + sumto[total][i][0]
            d = []
            for i in range(1, 10):
                if i not in c:
                    d.append(i)
            b.append(d)
        sum2.append(b)
    # sum2[x][y] gives all numbers you cant be used to sum to y if you have x elements
    return sum2


sum2 = sum2()  # sum2[x][y] = all the numbers that cant sum to y in x numbers
supo = []
for row in range(9):
    d = []
    for col in range(9):
        d.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
    supo.append(d)  # gets supo to have every number 1:9 as options in every square
# supo=[[9,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
# supo=[[1, 2, 3, 4, 5, 6, 7, 8, [8, 9]], [[4, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, 9], [1, 2, 3, 7, 8, 9], [1, 2, 3, 7, 8, 9], [1, 2, 3, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9]], [[4, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, 9], [1, 2, 3, 7, 8, 9], [1, 2, 3, 7, 8, 9], [1, 2, 3, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9]], [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 7, 8, 9], [1, 2, 4, 5, 6, 7, 8, 9], [1, 2, 3, 5, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 7, 8, 9], [1, 2, 4, 5, 6, 7, 8, 9], [1, 2, 3, 5, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 7, 8, 9], [1, 2, 4, 5, 6, 7, 8, 9], [1, 2, 3, 5, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 7, 8, 9], [1, 2, 4, 5, 6, 7, 8, 9], [1, 2, 3, 5, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 7, 8, 9], [1, 2, 4, 5, 6, 7, 8, 9], [1, 2, 3, 5, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 7, 8, 9], [1, 2, 4, 5, 6, 7, 8, 9], [1, 2, 3, 5, 6, 7, 8, 9], [1, 2, 3, 4, 6, 7, 8, 9], [1, 2, 3, 4, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]]
#supo = [[9, 2, 6, 5, 8, 3, 4, 7, 1], [7, 3, 8, 4, 1, 6, 2, 5, 9], [1, 4, 5, 2, 7, 9, 3, 6, 8],
#        [3, 5, 9, 7, 6, 2, 1, 8, 4], [4, 8, 7, 1, 9, 5, 6, 2, 3], [6, 1, 2, 8, 3, 4, 7, 9, 5],
#        [5, 7, 3, 6, 4, 8, 9, 1, 2], [8, 6, 4, 9, 2, 1, 5, 3, 7], [2, 9, 1, 3, 5, 7, 8, 4, 6]]
'''
sums = [[[[0, 0], [1, 0]], 16], [[[0, 1], [1, 1]], 5], [[[0, 2], [0, 3]], 11], [[[0, 4], [1, 4]], 9],
        [[[0, 5], [0, 6]], 7], [[[0, 7], [0, 8], [1, 7]], 13], [[[1, 2], [2, 2]], 13], [[[1, 3], [2, 3]], 6],
        [[[1, 5], [1, 6]], 8], [[[1, 8], [2, 8]], 17], [[[2, 0], [3, 0]], 4], [[[2, 1], [3, 1], [3, 2]], 18],
        [[[2, 4], [2, 5]], 16], [[[2, 6], [3, 6]], 4], [[[2, 7], [3, 7]], 14],
        [[[3, 3], [4, 3], [4, 4], [4, 5], [5, 5]], 26], [[[3, 4], [3, 5]], 8], [[[3, 8], [4, 8]], 7],
        [[[4, 0], [5, 0]], 10], [[[4, 1], [4, 2]], 15], [[[4, 6], [4, 7]], 8], [[[5, 1], [6, 1]], 8],
        [[[5, 2], [6, 2]], 5], [[[5, 3], [5, 4]], 11], [[[5, 6], [5, 7], [6, 7]], 17], [[[5, 8], [6, 8]], 7],
        [[[6, 0], [7, 0]], 13], [[[6, 3], [6, 4]], 10], [[[6, 5], [7, 5]], 9], [[[6, 6], [7, 6]], 14],
        [[[7, 1], [8, 1], [8, 0]], 17], [[[7, 2], [7, 3]], 13], [[[7, 4], [8, 4]], 7], [[[7, 7], [8, 7]], 7],
        [[[7, 8], [8, 8]], 13], [[[8, 2], [8, 3]], 4], [[[8, 5], [8, 6]], 15]]
'''
sums = [
    [13, [[0, 0], [0, 1]]],
    [5, [[1, 0], [1, 1]]],
    [24, [[2, 0], [3, 0], [4, 0], [5, 0]]],
    [6, [[6, 0], [6, 1]]],
    [11, [[7, 0], [7, 1]]],
    [28, [[8, 0], [8, 1], [8, 2], [7, 2], [6, 2]]],
    [16, [[2, 1], [3, 1], [4, 1]]],
    [5, [[5, 1], [5, 2]]],
    [14, [[0, 2], [1, 2], [2, 2]]],
    [17, [[3, 2], [4, 2], [4, 3]]],
    [41, [[0, 3], [1, 3], [2, 3], [2, 4], [2, 5], [1, 5], [0, 5]]],
    [8, [[3, 3], [3, 4], [3, 5]]],
    [10, [[5, 3], [6, 3]]],
    [7, [[7, 3], [8, 3]]],
    [4, [[0, 4], [1, 4]]],
    [32, [[4, 4], [5, 4], [6, 4], [7, 4], [8, 4]]],
    [13, [[4, 5], [4, 6], [3, 6]]],
    [9, [[5, 5], [6, 5]]],
    [12, [[7, 5], [8, 5]]],
    [17, [[0, 6], [1, 6], [2, 6]]],
    [13, [[5, 6], [5, 7]]],
    [25, [[6, 6], [7, 6], [8, 6], [8, 7], [8, 8]]],
    [7, [[0, 7], [0, 8]]],
    [12, [[1, 7], [1, 8]]],
    [13, [[2, 7], [3, 7], [4, 7]]],
    [17, [[6, 7], [6, 8]]],
    [3, [[7, 7], [7, 8]]],
    [23, [[2, 8], [3, 8], [4, 8], [5, 8]]]
]


def main(problem):
    # problem = [[b, a] for a, b in problem]
    for i in problem:
        i[0], i[1] = i[1], i[0]

    return solve(supo, problem, sum2, [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []],
          [[], [], [], [], [], [], [], [], []])  # solve it


if __name__ == '__main__':
    a = datetime.datetime.now()
    c = main(sums)
    b = datetime.datetime.now()
    print('it took:', b - a)
    print(counter)
    for i in range(9):
        print(c[i])