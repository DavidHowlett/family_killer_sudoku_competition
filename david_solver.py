"""
This is David's solution to the killer sudoku challenge

The set of possibilities for a square is represented as the 1 bits in an integer.
For example if a square is 7 that means the square is one of [1, 2, 3]

A possible combination of digits for a section is represented as the 1 bits in an integer.
For example a combo of 7 that means the section contains [1, 2, 3]


solve time history:

initial solver time
1.856   problem1

fixed a bug
1.027   problem1

switched to bitwise sets
0.131 problem1

removed slow_consistency_checker from critical path
0.0137 problem1

prune some invalid combos
0.0059 seconds to run
152 add_value_calls
23.2418 seconds to run
289498 add_value_calls

prune more invalid combos
0.0054 seconds to run problem 1
117 add_value_calls
4 bad_guesses
8.4603 seconds to run problem 2
231125 add_value_calls
76425 bad_guesses

reset counters on problem start
0.0051 seconds to run problem 1
117 add_value_calls
4 bad_guesses
8.4074 seconds to run problem 2
231008 add_value_calls
76421 bad_guesses

added extra constraint
0.0196 seconds to run problem 1
87 add_value_calls
1 bad_guesses
7.1403 seconds to run problem 2
33377 add_value_calls
6631 bad_guesses

removed asserts
0.0209 seconds to run problem 1
87 add_value_calls
1 bad_guesses
6.6137 seconds to run problem 2
31171 add_value_calls
6631 bad_guesses

removed call to union
0.0145 seconds to run problem 1
87 add_value_calls
1 bad_guesses
4.4375 seconds to run problem 2
34710 add_value_calls
6631 bad_guesses

made ex union code execute less often
0.0051 seconds to run problem 1
102 add_value_calls
2 bad_guesses
2.1823 seconds to run problem 2
53716 add_value_calls
11169 bad_guesses

changed search order
0.0058 seconds to run problem 1
106 add_value_calls
2 bad_guesses
0.4858 seconds to run problem 2
11168 add_value_calls
2536 bad_guesses
"""
# import doctest


class Contradiction(Exception):
    """Raised when the board is in an inconsistent state"""


def union(xs):
    """This takes an iterable and returns the union of every element
    >>> union([1, 2, 3])
    3
    >>> union([2, 5])
    7
    """
    y = 0
    for x in xs:
        y = y | x
    return y


def pop_count(x):
    """This finds the number of 1's in the binary representation of a number
    Todo replace this with gmpy.popcount(a)
    >>> pop_count(0)
    0
    >>> pop_count(1)
    1
    >>> pop_count(5)
    2
    """
    return bin(x).count('1')


def square_possibilities(square):
    """This prints the possibilities of a square as a list
    >>> square_possibilities(0)
    []
    >>> square_possibilities(1+4+16)
    [1, 3, 5]
    >>> for square in range(512):assert len(square_possibilities(square)) == pop_count(square)
    """
    return [i+1 for i in range(9) if square & 1 << i]


def section_sum(x):
    """This returns the sum of every possibility in a square or combo
    >>> section_sum(0)
    0
    >>> section_sum(5)
    4
    >>> section_sum(7)
    6
    """
    return sum(square_possibilities(x))


def setup(problem):
    """This defines all the globals needed and returns a formatted list of sections
    >>> import problems
    >>> sections = setup(problems.problems['problem 1'])
    >>> sections[4]
    {'total': 10, 'locs': {4, 5}, 'combos': [40, 68, 130, 257]}
    """
    global friends
    global groups
    global group_memberships
    initial_sections = [{
            'total': total,
            'locs': {x + y * 9 for x, y in section},
            'combos': combos[len(section)][total]}
        for total, section in problem]
    sections = [None for _ in range(81)]
    for section in initial_sections:
        for loc in section['locs']:
            sections[loc] = section
    groups = rows + cols + boxes + [section['locs'] for section in initial_sections]
    # I need to know which groups each square is a member of
    group_memberships = [[group for group in groups if loc in group] for loc in range(81)]
    # friends of a location are the locations that share a row, column or box
    friends = [set.union(*group_memberships[loc]).difference({loc})for loc in range(81)]
    return sections


def init_board(sections):
    """Create a board from a list of sections
    >>> import problems
    >>> sections = setup(problems.problems['problem 1'])
    >>> board = init_board(sections)
    >>> len(board)
    81
    >>> board[:4]  # The board now contains the possible values at each position
    [320, 320, 5, 5]
    """
    board = [0b111_111_111 for _ in range(81)]
    for section in sections:
        possible_values = union(section['combos'])
        for loc in section['locs']:
            board[loc] = possible_values
    # todo more values can be excluded in particular straight sections exclude values from their row
    return board


def print_board(board):
    """ This prints a board in a human readable form
    >>> import problems
    >>> sections = setup(problems.problems['problem 1'])
    >>> board = init_board(sections)
    >>> add_value(board, sections, 0, 256)
    >>> print_board(board)
    9 7 . . . . . . .  |  256  64   5   5 175 175 184 184 191
    . . . . . . . . .  |   15  15 191 511 480 119 119 511 511
    . . . . . . . . .  |  190 184 184 511 480  15  15 504   5
    . . . . . . . . .  |  254  27  27 511 511 510 495 504   5
    . . . . . . . . .  |  255 191 320 119 511 510 495  63  63
    . . . . . . . . .  |   63  55 320 119 511 511 255 255 480
    . . . . . . . . .  |   63  55   5   5 119 511 432 432 480
    . . . . . . . . .  |  255 447 432 432 119 511 511  63  63
    . . . . . . . . .  |  255 384 384  63  63  63  63 504 504
    <BLANKLINE>
    <BLANKLINE>
    """
    to_print = ''
    for row in range(9):
        for col in range(9):
            square = board[col + row * 9]
            if square == 0:
                to_print += '! '
            elif square in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                to_print += str(set_to_val[square]) + ' '
            else:
                to_print += '. '
        to_print += ' | '
        for col in range(9):
            square = board[col + row * 9]
            to_print += f' {square:>3}'
        to_print += '\n'
    to_print += '\n'
    print(to_print)


def slow_consistency_check(board, sections):
    """This does a bunch of sanity checks, this should not be left in the final solver"""
    for square in board:
        assert square
    for group in groups:
        assert section_sum(union(board[loc] for loc in group)) >= len(group)
    for section in sections:
        # if all the squares in a section are solved check that the section has the right total
        if all(board[loc] in {1, 2, 4, 8, 16, 32, 64, 128, 256} for loc in section['locs']):
            assert section_sum(union(board[loc] for loc in section['locs'])) == section['total']


def add_value(board, sections, loc, single_possibility):
    global add_value_calls
    """Given a board and a location set the value at the location and remove all numbers that are now impossible.
    This function will change the given board and sections. It may raise a Contradiction. 
    Only call add_value on squares that don't have a value already.
    >>> import problems
    >>> sections = setup(problems.problems['problem 1'])
    >>> board = init_board(sections)
    >>> add_value(board, sections, 0, 256)
    >>> board[0]
    256
    >>> board[1]
    64
    >>> board[9] & 256
    0
    """
    assert 0 <= loc < 81
    # assert single_possibility in {1, 2, 4, 8, 16, 32, 64, 128, 256}
    # assert single_possibility != board[loc]
    add_value_calls += 1
    # set the current square
    remove_possibilities(board, sections, loc, ~single_possibility, False)

    # if all the squares in a section are solved check that the section has the right total
    section = sections[loc]
    if all(board[loc] in {1, 2, 4, 8, 16, 32, 64, 128, 256} for loc in section['locs']):  # Todo this is inefficient
        if not (section_sum(union(board[loc] for loc in section['locs'])) == section['total']):
            # assert False
            raise Contradiction
        # assert section_sum(union(board[loc] for loc in section['locs'])) == section['total']

    # we now know that the value in the current square can't be found in any of the neighbors
    for loc2 in friends[loc]:
        # only do the work to remove a value if the value is currently considered possible
        if single_possibility & board[loc2]:
            remove_possibilities(board, sections, loc2, single_possibility, True)


def remove_possibilities(board, sections, loc, possibilities, recurse, ):
    """This takes a board and removes a collection of possibilities from a single square
    >>> import problems
    >>> sections = setup(problems.problems['problem 1'])
    >>> board = init_board(sections)
    >>> remove_possibilities(board, sections, 0, 64, True)
    >>> board[0]
    256
    >>> board[1]
    64
    """
    if not possibilities & board[loc]:
        # if there is no overlap between the current possibilities and the possibilities to remove then return early
        return
    new_possibilities = (~possibilities) & board[loc]
    if new_possibilities in {1, 2, 4, 8, 16, 32, 64, 128, 256} and recurse:
        add_value(board, sections, loc, new_possibilities)
    else:
        board[loc] = new_possibilities
    if board[loc] == 0:
        raise Contradiction

    # exclude combo possibilities that become impossible
    section = sections[loc]
    new_combos = [combo for combo in section['combos'] if board[loc] & combo]
    if new_combos != section['combos']:
        # use the new combos to reduce the possibilities in a section
        section['combos'] = new_combos
        for loc2 in section['locs']:
            remove_possibilities(board, sections, loc2, ~union(section['combos']), True)
    
    if not recurse:
        # check if this leaves a group of 9 where a number can only be in one location
        for group in static_groups[loc]:
            for loc2 in group:
                # don't bother looking at squares that already known
                if board[loc2] not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                    found_digits = 0
                    for loc3 in group:
                        if loc3 != loc2:
                            found_digits = found_digits | board[loc3]
                    digits_unaccounted_for = 511 ^ found_digits
                    if digits_unaccounted_for:
                        # if digits_unaccounted_for not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                        #    raise Contradiction
                        add_value(board, sections, loc2, digits_unaccounted_for)


def extra_checks(board, sections, loc):
    # check if this leaves a group of 9 where a number can only be in one location
    for group in static_groups[loc]:
        for loc2 in group:
            # don't bother looking at squares that already known
            if board[loc2] not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                found_digits = 0
                for loc3 in group:
                    if loc3 != loc2:
                        found_digits = found_digits | board[loc3]
                digits_unaccounted_for = 511 ^ found_digits
                if digits_unaccounted_for:
                    # if digits_unaccounted_for not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                    #    raise Contradiction
                    add_value(board, sections, loc2, digits_unaccounted_for)


def extra_checks2(board, sections):
    # check if this leaves a group of 9 where a number can only be in one location
    for group in rows + cols + boxes:
        for loc2 in group:
            # don't bother looking at squares that already known
            if board[loc2] not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                found_digits = 0
                for loc3 in group:
                    if loc3 != loc2:
                        found_digits = found_digits | board[loc3]
                digits_unaccounted_for = 511 ^ found_digits
                if digits_unaccounted_for:
                    # if digits_unaccounted_for not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                    #    raise Contradiction
                    add_value(board, sections, loc2, digits_unaccounted_for)


def solver(board, sections):
    global bad_guesses
    """This solves an arbitrary board by guessing solutions"""
    # print_board(board)
    loc_to_guess = None
    min_possibility_count = 999
    # find the uncertain square with the least possible values
    for loc in range(81):
        possibility_count = pop_count(board[loc])
        if 1 < possibility_count < min_possibility_count:
            min_possibility_count = possibility_count
            loc_to_guess = loc
            if min_possibility_count == 2:
                # 2 is the best possible so looking further is pointless
                break
    if loc_to_guess is None:
        # then the board is solved :-)
        return board
    for possibility in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
        if not possibility & board[loc_to_guess]:
            continue
        possible_board = board[:]
        possible_sections = [s.copy() for s in sections]
        try:
            add_value(possible_board, possible_sections, loc_to_guess, possibility)
            solver(possible_board, possible_sections)
            return possible_board
        except Contradiction:
            # then that particular guess is wrong
            bad_guesses += 1
            pass
    # if there is a square on the current board which has no possible values
    # then there is a contradiction somewhere
    # print('Backtrack')
    raise Contradiction


def main(problem):
    global add_value_calls
    global bad_guesses
    add_value_calls = 0
    bad_guesses = 0
    # problem = problem[-1:]
    sections = setup(problem)
    board = init_board(sections)
    solved_board = solver(board, sections)
    # print_board(solved_board)
    return solved_board


set_to_val = {1 << i: i+1 for i in range(9)}
assert 0 not in set_to_val
assert set_to_val[1] == 1
assert set_to_val[2] == 2
assert set_to_val[4] == 3
assert set_to_val[8] == 4

val_to_set = {i+1: 1 << i for i in range(9)}  # this could be an array
assert 0 not in val_to_set
assert val_to_set[1] == 1
assert val_to_set[2] == 2
assert val_to_set[3] == 4
assert val_to_set[4] == 8

add_value_calls = 0
bad_guesses = 0
rows = [{col+row*9 for col in range(9)} for row in range(9)]
cols = [{col+row*9 for row in range(9)} for col in range(9)]
boxes = [{col+row*9+box_col*3+box_row*3*9 for row in range(3) for col in range(3)}
         for box_row in range(3) for box_col in range(3)]
# static_groups = [[group for group in rows + cols + boxes if loc in group] for loc in range(81)]
static_groups = [[{0, 1, 2, 3, 4, 5, 6, 7, 8}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{0, 1, 2, 3, 4, 5, 6, 7, 8}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{9, 10, 11, 12, 13, 14, 15, 16, 17}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {0, 1, 2, 9, 10, 11, 18, 19, 20}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {3, 4, 5, 12, 13, 14, 21, 22, 23}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{18, 19, 20, 21, 22, 23, 24, 25, 26}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {6, 7, 8, 15, 16, 17, 24, 25, 26}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{32, 33, 34, 35, 27, 28, 29, 30, 31}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{36, 37, 38, 39, 40, 41, 42, 43, 44}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {36, 37, 38, 45, 46, 47, 27, 28, 29}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {32, 39, 40, 41, 48, 49, 50, 30, 31}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{45, 46, 47, 48, 49, 50, 51, 52, 53}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {33, 34, 35, 42, 43, 44, 51, 52, 53}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{54, 55, 56, 57, 58, 59, 60, 61, 62}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{64, 65, 66, 67, 68, 69, 70, 71, 63}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {0, 36, 72, 9, 45, 18, 54, 27, 63}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {64, 1, 37, 73, 10, 46, 19, 55, 28}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {65, 2, 38, 74, 11, 47, 20, 56, 29}, {64, 65, 72, 73, 74, 54, 55, 56, 63}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {66, 3, 39, 75, 12, 48, 21, 57, 30}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {67, 4, 40, 76, 13, 49, 22, 58, 31}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {32, 68, 5, 41, 77, 14, 50, 23, 59}, {66, 67, 68, 75, 76, 77, 57, 58, 59}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {33, 69, 6, 42, 78, 15, 51, 24, 60}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {34, 70, 7, 43, 79, 16, 52, 25, 61}, {69, 70, 71, 78, 79, 80, 60, 61, 62}], [{72, 73, 74, 75, 76, 77, 78, 79, 80}, {35, 71, 8, 44, 80, 17, 53, 26, 62}, {69, 70, 71, 78, 79, 80, 60, 61, 62}]]
# combos contains every possible collection of the digits 1-9
# combos = list(range(512))
# then group them by number of squares in the section and the sum of all the values in the section
# this looks like combo[length][total]
# combos = [[[possible_section for possible_section in combos
#            if pop_count(possible_section) == length and section_sum(possible_section) == total]
#           for total in range(46)] for length in range(9)]
combos = [[[0], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [1], [2], [4], [8], [16], [32], [64], [128], [256], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [3], [5], [6, 9], [10, 17], [12, 18, 33], [20, 34, 65], [24, 36, 66, 129], [40, 68, 130, 257], [48, 72, 132, 258], [80, 136, 260], [96, 144, 264], [160, 272], [192, 288], [320], [384], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [7], [11], [13, 19], [14, 21, 35], [22, 25, 37, 67], [26, 38, 41, 69, 131], [28, 42, 49, 70, 73, 133, 259], [44, 50, 74, 81, 134, 137, 261], [52, 76, 82, 97, 138, 145, 262, 265], [56, 84, 98, 140, 146, 161, 266, 273], [88, 100, 148, 162, 193, 268, 274, 289], [104, 152, 164, 194, 276, 290, 321], [112, 168, 196, 280, 292, 322, 385], [176, 200, 296, 324, 386], [208, 304, 328, 388], [224, 336, 392], [352, 400], [416], [448], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [15], [23], [27, 39], [29, 43, 71], [30, 45, 51, 75, 135], [46, 53, 77, 83, 139, 263], [54, 57, 78, 85, 99, 141, 147, 267], [58, 86, 89, 101, 142, 149, 163, 269, 275], [60, 90, 102, 105, 150, 153, 165, 195, 270, 277, 291], [92, 106, 113, 154, 166, 169, 197, 278, 281, 293, 323], [108, 114, 156, 170, 177, 198, 201, 282, 294, 297, 325, 387], [116, 172, 178, 202, 209, 284, 298, 305, 326, 329, 389], [120, 180, 204, 210, 225, 300, 306, 330, 337, 390, 393], [184, 212, 226, 308, 332, 338, 353, 394, 401], [216, 228, 312, 340, 354, 396, 402, 417], [232, 344, 356, 404, 418, 449], [240, 360, 408, 420, 450], [368, 424, 452], [432, 456], [464], [480], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [31], [47], [55, 79], [59, 87, 143], [61, 91, 103, 151, 271], [62, 93, 107, 155, 167, 279], [94, 109, 115, 157, 171, 199, 283, 295], [110, 117, 158, 173, 179, 203, 285, 299, 327], [118, 121, 174, 181, 205, 211, 286, 301, 307, 331, 391], [122, 182, 185, 206, 213, 227, 302, 309, 333, 339, 395], [124, 186, 214, 217, 229, 310, 313, 334, 341, 355, 397, 403], [188, 218, 230, 233, 314, 342, 345, 357, 398, 405, 419], [220, 234, 241, 316, 346, 358, 361, 406, 409, 421, 451], [236, 242, 348, 362, 369, 410, 422, 425, 453], [244, 364, 370, 412, 426, 433, 454, 457], [248, 372, 428, 434, 458, 465], [376, 436, 460, 466, 481], [440, 468, 482], [472, 484], [488], [496], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [63], [95], [111, 159], [119, 175, 287], [123, 183, 207, 303], [125, 187, 215, 311, 335], [126, 189, 219, 231, 315, 343, 399], [190, 221, 235, 317, 347, 359, 407], [222, 237, 243, 318, 349, 363, 411, 423], [238, 245, 350, 365, 371, 413, 427, 455], [246, 249, 366, 373, 414, 429, 435, 459], [250, 374, 377, 430, 437, 461, 467], [252, 378, 438, 441, 462, 469, 483], [380, 442, 470, 473, 485], [444, 474, 486, 489], [476, 490, 497], [492, 498], [500], [504], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [127], [191], [223, 319], [239, 351], [247, 367, 415], [251, 375, 431], [253, 379, 439, 463], [254, 381, 443, 471], [382, 445, 475, 487], [446, 477, 491], [478, 493, 499], [494, 501], [502, 505], [506], [508], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [255], [383], [447], [479], [495], [503], [507], [509], [510], []]]
# assert combos[2][3] == [3]
# a section that is 2 long and sums to 5 has 2 possibilities [1,4] and [2,3] these are represented as 9 and 6
# assert combos[2][5] == [6, 9]
# doctest.testmod()
