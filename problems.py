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
    7 3 9 8 5 2 1 4 6
    6 2 4 9 3 1 5 7 8
    1 5 8 6 7 4 3 9 2
    8 9 2 5 4 3 7 6 1
    3 1 7 2 9 6 4 8 5
    4 6 5 1 8 7 2 3 9
    9 7 1 3 2 8 6 5 4
    2 8 3 4 6 5 9 1 7
    5 4 6 7 1 9 8 2 3
"""
problems = {
    'problem 1': [
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
        [15, [[8, 5], [8, 6]]]],
    'problem 2': [  # from https://krazydad.com/killersudoku/sfiles/KD_Killer_IN12_8_v50.pdf
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
        [23, [[2, 8], [3, 8], [4, 8], [5, 8]]]
    ],
    'grandad slow problem': [
        [15, [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3]]],
        [19, [[2, 0], [3, 0], [4, 0], [3, 1], [4, 1]]],
        [38, [[5, 0], [5, 1], [6, 1], [6, 2], [6, 3], [7, 3]]],
        [23, [[6, 0], [7, 0], [7, 1]]],
        [3,  [[8, 0], [8, 1]]],
        [23, [[0, 1], [0, 2], [0, 3]]],
        [16, [[2, 1], [2, 2]]],
        [11, [[3, 2], [3, 3], [4, 2]]],
        [16, [[5, 2], [5, 3], [4, 3], [4, 4]]],
        [25, [[7, 2], [8, 2], [8, 3], [8, 4]]],
        [13, [[2, 3], [2, 4], [3, 4]]],
        [10, [[0, 4], [1, 4]]],
        [18, [[5, 4], [6, 4], [5, 5]]],
        [11, [[7, 4], [7, 5], [6, 5], [6, 6]]],
        [30, [[0, 5], [1, 5], [2, 5], [0, 6], [1, 6]]],
        [22, [[3, 5], [4, 5], [4, 6], [4, 7]]],
        [34, [[8, 5], [7, 6], [8, 6], [7, 7], [8, 7]]],
        [22, [[2, 6], [3, 6], [2, 7], [3, 7]]],
        [6,  [[5, 6], [5, 7], [5, 8]]],
        [18, [[0, 7], [1, 7], [0, 8], [1, 8]]],
        [10, [[6, 7], [6, 8], [7, 8], [8, 8]]],
        [22, [[2, 8], [3, 8], [4, 8]]],

    ]
}

# I now want to confirm that each co-ordinate is found in one square and one square only
all_squares = [[x, y] for x in range(9) for y in range(9)]
assert len(all_squares) == 9*9
for problem in problems.values():
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

# the odd code below ensures that problems with the same origin stay grouped together in the dict
grouped_problems = dict()
for original_name, original_problem in problems.copy().items():
    to_duplicate = {original_name: original_problem}

    # expand problem set with rotational invariance
    for name, problem in to_duplicate.copy().items():
        to_duplicate[name + ' rotated'] = [[_total, [[y, 8-x] for x, y in rule]] for _total, rule in problem]

    # expand problem set with inversion invariance
    for name, problem in to_duplicate.copy().items():
        to_duplicate[name + ' inverted'] = [[_total, [[8-x, 8-y] for x, y in rule]] for _total, rule in problem]

    # expand problem set with reflection invariance
    for name, problem in to_duplicate.copy().items():
        to_duplicate[name + ' reflected'] = [[_total, [[8-x, y] for x, y in rule]] for _total, rule in problem]

    # expand problem set with numerical flipping (1->9 and 7->3)
    for name, problem in to_duplicate.copy().items():
        to_duplicate[name + ' flipped'] = [[
            len(rule)*10-_total, [[x, y] for x, y in rule]] for _total, rule in problem]
    grouped_problems.update(to_duplicate)
problems = grouped_problems
