"""This file contains example killer sudoku problems that have been checked.
The first problem was typed by Michael. The solution is:
    9 7 1 3 4 6 5 8 2
    2 3 4 5 8 1 7 6 9
    6 8 5 9 7 2 3 4 1
    5 4 2 7 1 8 6 9 3
    8 1 7 6 9 3 4 2 5
    3 6 9 2 5 4 8 1 7
    4 2 3 1 6 7 9 5 8
    7 5 6 8 2 9 1 3 4
    1 9 8 4 3 5 2 7 6
The second problem was typed by David. The solution is:
    ???
"""
problem1 = [
    [16, [[0, 0], [1, 0]]],
    [5,  [[0, 1], [1, 1]]],
    [11, [[0, 2], [0, 3]]],
    [9,  [[0, 4], [1, 4]]],
    [7,  [[0, 5], [0, 6]]],
    [13, [[0, 7], [0, 8], [1, 7]]],
    [13, [[1, 2], [2, 2]]],
    [6,  [[1, 3], [2, 3]]],
    [8,  [[1, 5], [1, 6]]],
    [17, [[1, 8], [2, 8]]],
    [4,  [[2, 0], [3, 0]]],
    [18, [[2, 1], [3, 1], [3, 2]]],
    [16, [[2, 4], [2, 5]]],
    [4,  [[2, 6], [3, 6]]],
    [14, [[2, 7], [3, 7]]],
    [26, [[3, 3], [4, 3], [4, 4], [4, 5], [5, 5]]],
    [8,  [[3, 4], [3, 5]]],
    [7,  [[3, 8], [4, 8]]],
    [10, [[4, 0], [5, 0]]],
    [15, [[4, 1], [4, 2]]],
    [8,  [[4, 6], [4, 7]]],
    [8,  [[5, 1], [6, 1]]],
    [5,  [[5, 2], [6, 2]]],
    [11, [[5, 3], [5, 4]]],
    [17, [[5, 6], [5, 7], [6, 7]]],
    [7,  [[5, 8], [6, 8]]],
    [13, [[6, 0], [7, 0]]],
    [10, [[6, 3], [6, 4]]],
    [9,  [[6, 5], [7, 5]]],
    [14, [[6, 6], [7, 6]]],
    [17, [[7, 1], [8, 1], [8, 0]]],
    [13, [[7, 2], [7, 3]]],
    [7,  [[7, 4], [8, 4]]],
    [7,  [[7, 7], [8, 7]]],
    [13, [[7, 8], [8, 8]]],
    [4,  [[8, 2], [8, 3]]],
    [15, [[8, 5], [8, 6]]],
]

problem2 = [  # from https://krazydad.com/killersudoku/sfiles/KD_Killer_IN12_8_v50.pdf
    [13, [[0, 0], [0, 1]]],
    [5,  [[1, 0], [1, 1]]],
    [24, [[2, 0], [3, 0], [4, 0], [5, 0]]],
    [6,  [[6, 0], [6, 1]]],
    [11, [[7, 0], [7, 1]]],
    [28, [[8, 0], [8, 1], [8, 2], [7, 2], [6, 2]]],
    [16, [[2, 1], [3, 1], [4, 1]]],
    [5,  [[5, 1], [5, 2]]],
    [14, [[0, 2], [1, 2], [2, 2]]],
    [17, [[3, 2], [4, 2], [4, 3]]],
    [41, [[0, 3], [1, 3], [2, 3], [2, 4], [2, 5], [1, 5], [0, 5]]],
    [8,  [[3, 3], [3, 4], [3, 5]]],
    [10, [[5, 3], [6, 3]]],
    [7,  [[7, 3], [8, 3]]],
    [4,  [[0, 4], [1, 4]]],
    [32, [[4, 4], [5, 4], [6, 4], [7, 4], [8, 4]]],
    [13, [[4, 5], [4, 6], [3, 6]]],
    [9,  [[5, 5], [6, 5]]],
    [12, [[7, 5], [8, 5]]],
    [17, [[0, 6], [1, 6], [2, 6]]],
    [13, [[5, 6], [5, 7]]],
    [25, [[6, 6], [7, 6], [8, 6], [8, 7], [8, 8]]],
    [7,  [[0, 7], [0, 8]]],
    [12, [[1, 7], [1, 8]]],
    [13, [[2, 7], [3, 7], [4, 7]]],
    [17, [[6, 7], [6, 8]]],
    [3,  [[7, 7], [7, 8]]],
    [23, [[2, 8], [3, 8], [4, 8], [5, 8]]],
]

problems = [problem1, problem2]

# I now want to confirm that each co-ordinate is found in one square and one square only
all_squares = [[x, y] for x in range(9) for y in range(9)]
assert len(all_squares) == 9*9
for problem in problems:
    all_present_squares = []
    total = 0
    for value, squares in problem:
        total += value
        for square in squares:
            if square not in all_squares:
                print('invalid square:', square)
            if square in all_present_squares:
                print('the square:', square, 'is present more then once')
            all_present_squares.append(square)
    for square in all_squares:
        if square not in all_present_squares:
            print('the square', square, 'is missing')
    if total != 5*9*9:
        print('the total value of the squares is', total, 'which is wrong. It should be', 5*9*9)

# Michael wanted the problems flipped to be the same as in his code
michael_style_problems = [(b, a) for a, b in problem1]
# print(michael_style_problems)
