"""
possible constraints to implement:
✓ if {5} becomes the value of a square remove 5 from all friends
x initialise squares within a section 3 long with a total of 10 to only allow numbers found in combos[3][10]
x on each change in a section
    x work out which of combos[3][10] is still possible and only allow square possibilities in that

x if 5 is only allowed in one square in a group (of size 9) set that square to 5

todo list:
- figure out why the solver still recurses when problem is nearly solved (that should be handled with add_value)
- add doc

"""


import copy


class Contradiction(Exception):
    """Raised when the board is in an inconsistent state"""


rows = [{col+row*9 for col in range(9)} for row in range(9)]
cols = [{col+row*9 for row in range(9)} for col in range(9)]
boxes = [{col+row*9+box_col*3+box_row*3*9 for row in range(3) for col in range(3)}
         for box_row in range(3) for box_col in range(3)]
static_groups = rows + cols + boxes
# combos contains every possible collection of the digits 1-9
combos = [frozenset(i + 1 for i in range(9) if j & 1 << i) for j in range(512)]
# then group them by length and total
combos = [[
    frozenset(c for c in combos if len(c) == length and sum(c) == total) for total in range(46)] for length in range(9)]


def setup(problem):
    global friends
    global groups
    global group_memberships
    sections = [{
            'total': total,
            'locs': {x + y * 9 for x, y in section},
            'combos': combos[len(section)][total]}
        for total, section in problem]
    groups = rows + cols + boxes + [section['locs'] for section in sections]
    # I need to know which groups each square is a member of
    group_memberships = [[group for group in groups if loc in group] for loc in range(81)]
    # friends of a location are the locations that share a row, column or box
    friends = [set.union(*group_memberships[loc]).difference({loc})for loc in range(81)]
    return sections


def init_board(sections):
    # initialise the board based on the known possible combos
    board = [list(range(1, 10)) for _ in range(81)]
    for section in sections:
        possible_values = set(frozenset.union(*section['combos']))
        for loc in section['locs']:
            board[loc] = copy.copy(possible_values)
    return board


def print_board(board):
    to_print = ''
    for row in range(9):
        for col in range(9):
            square = board[col + row * 9]
            if len(square) == 0:
                to_print += '! '
            elif len(square) == 1:
                to_print += str(square)[1] + ' '
            else:
                to_print += '. '
        to_print += '\n'
    to_print += '\n'
    print(to_print)


def slow_consistency_check(board, sections):
    """This does a bunch of sanity checks"""
    for group in groups:
        if len(set().union(*[board[loc] for loc in group])) < len(group):
            raise Contradiction
    for section in sections:
        if all(len(board[loc]) == 1 for loc in section['locs']) and \
                sum(board[loc].__iter__().__next__() for loc in section['locs']) != section['total']:
            raise Contradiction


def add_value(board, sections, loc, val):
    """Given a board and a location set the value at the location and remove all numbers that are now impossible.
    This function does not change the board given.
    It will either return a board or raise a Contradiction."""
    assert 0 <= loc < 81
    assert 0 < val < 10
    board = copy.deepcopy(board)
    # set the current square
    board[loc] = {val}
    # we now know that the value in the current square can't be found in any of the neighbors
    for loc2 in friends[loc]:
        friend2 = board[loc2]
        if val in friend2:
            friend2.remove(val)
            if not friend2:
                raise Contradiction
            # if the other square becomes solved as a result of the removal then
            # extra processing is required
            if len(friend2) == 1:
                board = add_value(board, sections, loc2, *friend2)
            # todo here you should check if this leaves a group where a number can only be in one location
    slow_consistency_check(board, sections)
    return board


def solver(board, sections):
    """This solves an arbitrary board by guessing solutions"""
    print_board(board)
    loc_to_guess = None
    min_len = 999
    # find the uncertain square with the least possible values
    for loc in range(81):
        len_square = len(board[loc])
        if 1 < len_square < min_len:
            min_len = len_square
            loc_to_guess = loc
            if min_len == 2:
                # 2 is the best possible so looking further is pointless
                break
    if loc_to_guess is None:
        # then the board is solved :-)
        return board
    for possibility in board[loc_to_guess]:
        try:
            if sum(len(square) for square in board) < 86:
                print('close now')
            possible_board = add_value(board, sections, loc_to_guess, possibility)
            return solver(possible_board, sections)
        except Contradiction:
            # then that particular guess is wrong
            pass
    # if there is a square on the current board which has no possible values
    # then there is a contradiction somewhere
    # print('Backtrack')
    raise Contradiction


def main(problem):
    # problem = problem[-1:]
    sections = setup(problem)
    board = init_board(sections)
    slow_consistency_check(board, sections)  # todo remove
    return solver(board, sections)


'''
solve time history:
initial solver time
1.856   problem1
fixed a bug
1.027   problem1

'''