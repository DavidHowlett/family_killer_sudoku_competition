"""
This is David's solution to the killer sudoku challenge

The set of possibilities for a square is represented as the 1 bits in an integer.
For example if a square is 7 that means the square is one of [1, 2, 3]

A possible combination of digits for a section is represented as the 1 bits in an integer.
For example a combo of 7 that means the section contains [1, 2, 3]

ToDo:
    - the solutions of each of the solvers should be checked against each other
    - understand robert's code
    - unify on a single representation of the rules

    - simplify the unit tests (it is okay to have shared imports and setup)
    - cover the solver and main with unit tests
    - simplify my code (this should be allowed to make it slower)
    - add better deductive logic


David 2 took a total of 32.328 seconds and 146381 bad guesses. Each bad guess took 0.221 milliseconds on average
moved the location of the search for the missing digit
David 2 took a total of 27.883 seconds and 88999 bad guesses. Each bad guess took 0.313 milliseconds on average
"""
import doctest


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
    If this is a bottleneck it should be replaced this with gmpy.popcount(a)
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
    assert single_possibility in {1, 2, 4, 8, 16, 32, 64, 128, 256}
    assert single_possibility != board[loc]
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


def solver(board, sections):
    global bad_guesses
    """This solves an arbitrary board using deduction and when that fails, guessing solutions"""
    # check if this leaves a group of 9 where a number can only be in one location
    # this is computationally expensive because I need to find a large number of unions
    # print_board(board)
    progress_made = True
    while progress_made:
        progress_made = False
        for group in static_groups:
            for loc in group:
                # don't bother looking at squares that already known
                if board[loc] not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                    found_digits = 0
                    for loc2 in group:
                        if loc2 != loc:
                            found_digits = found_digits | board[loc2]
                    digits_unaccounted_for = 511 ^ found_digits
                    if digits_unaccounted_for:
                        if digits_unaccounted_for not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                            raise Contradiction
                        if not digits_unaccounted_for & board[loc]:
                            raise Contradiction
                        add_value(board, sections, loc, digits_unaccounted_for)
                        progress_made = True
        """
        for rule in rules:
            if rule[2]:
                for subset in rule:
                    possibilities = union(subset)
                    number_of_possibilities = popcount(possibilities)
                    if number_of_possibilities < len(subset):
                        raise Contradiction
                    elif number_of_possibilities == len(subset):
                        # then I can exclude lots of possibilities from the others locations in the rule
                    
                    
        """
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
            return solver(possible_board, possible_sections)
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
    sections = setup(problem)
    board = init_board(sections)
    solved_board = solver(board, sections)
    return [set_to_val[square] for square in solved_board], bad_guesses


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
static_groups = boxes+rows+cols
# combos contains every possible collection of the digits 1-9
combos = list(range(512))
# then group them by number of squares in the section and the sum of all the values in the section
# this looks like combo[length][total]
combos = [[[possible_section for possible_section in combos
            if pop_count(possible_section) == length and section_sum(possible_section) == total]
           for total in range(46)] for length in range(9)]
assert combos[2][3] == [3]
# a section that is 2 long and sums to 5 has 2 possibilities [1,4] and [2,3] these are represented as 9 and 6
assert combos[2][5] == [6, 9]

if __name__ == '__main__':
    doctest.testmod()
    import problems
    print(main(problems.problems['problem 2']))
