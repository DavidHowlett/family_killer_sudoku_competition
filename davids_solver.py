from time import perf_counter as now
import copy
import random
import problems


class Contradiction(Exception):
    """Raised when the board is in an inconsistent state"""


rows = [{col+row*9 for col in range(9)} for row in range(9)]
cols = [{col+row*9 for row in range(9)} for col in range(9)]
boxes = [{col+row*9+box_col*3+box_row*3*9 for row in range(3) for col in range(3)}
         for box_row in range(3) for box_col in range(3)]
section_totals = [(total, {x+(8-y)*9 for x, y in section}) for total, section in problems.problem2]
section_totals = [section_totals[-2]]
sections = [section for total, section in section_totals]
# print(boxes)
# print(sections)
groups = rows+cols+boxes+sections
# I need to know which groups each square is a member of
group_memberships = [[group for group in groups if loc in group] for loc in range(81)]
# friends of a location are the locations that share a row, column or box
friends = [set().union(*[group for group in group_memberships[loc]]).difference({loc})
           for loc in range(81)]

'''
total   squares lists
3       2       [[1,2]]
4       2       [[1,3]]
5       2       [[1,4], [2,3]]
6       2       [[1,5], [2,4]]
7       2       [[1,5], [2,5], [3,4]]
8       2       [[1,6], [2,6], [3,5]]

6       3       [[1,2,3]]
7       3       [[1,2,4]]
8       3       [[1,2,5], [1,3,4]]
9       3       [[1,2,6], [1,3,5], [2,3,4]]

'''
'''
possible_sections = [
    None,
    None,
    {
        3: [{1, 2}],
        4: [{1, 3}],
        5: [{1, 4}, {2, 3}],
        6: [{1, 5}, {2, 4}],
        7: [{1, 6}, {2, 5}, {3, 5}],
    }
]

possible_sections = [
    {(section_length+section_length**2)//2: [set(range(1, section_length+1))]} for section_length in range(4)]
for worm_length in range(2, 4):
    for worm in possible_sections[worm_length]:
        print(worm)

    print(current_worms)

print(possible_worms)
'''


def print_board(board):
    for row in range(9):
        for col in range(9):
            square = board[col + row * 9]
            if len(square) == 0:
                print('!', end=' ')
            elif len(square) == 1:
                print(*square, end=' ')
            else:
                print('.', end=' ')
        print('')
    print('')


def slow_consistency_check(board):
    """This does a bunch of sanity checks"""
    for group in groups:
        if len(set().union(*[board[loc] for loc in group])) < len(group):
            raise Contradiction
    for total, section in section_totals:
        if all(len(board[loc]) == 1 for loc in section) and \
                sum(board[loc].__iter__().__next__() for loc in section) != total:
            raise Contradiction


def add_value(board, loc, val):
    """Given a board and a location set the value at the location and remove all numbers that are now impossible.
    This function does not change the board given.
    It will either return a board or raise a Contradiction."""
    assert 0 <= loc < 81
    assert 0 < val < 10
    board = copy.deepcopy(board)
    # set the current square
    board[loc] = [val]
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
                add_value(board, loc2, *friend2)
            # todo here you should check if this leaves a group where a number can only be in one location
    slow_consistency_check(board)
    return board


def solver(board):
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
    progress_possible = False
    # for possibility in random.sample(board[loc_to_guess], k=len(board[loc_to_guess])):
    for possibility in board[loc_to_guess]:
        try:
            return solver(add_value(board, loc_to_guess, possibility))
        except Contradiction:
            # then that particular guess is wrong
            pass
    if not progress_possible:
        # if there is a square on the current board which has no possible values
        # then there is a contradiction somewhere
        print('Backtrack')
        raise Contradiction


def main(problem):
    return solver([list(range(1, 10)) for _ in range(81)])


if __name__ == '__main__':
    # board is the current state of the solution
    global_board = [list(range(1, 10)) for _ in range(81)]
    # this bit generates a legal sudoku board
    for col in range(6):
        for row in range(7):
            add_value(global_board, col + row * 9, 1+(col + row * 12 - row//3) % 9)

    '''
    # this almost always generates bad boards
    for loc in range(81):
        try:
            global_board = add_value(global_board, loc, random.randint(1, 9))
        except Contradiction:
            pass
    '''
    # add_value(global_board, 80, 1)
    # add_value(global_board, 7, 3)
    # print_board(global_board)
    '''
    start_time = now()
    print_board(main(global_board))
    print('Section totals:', section_totals)
    print(f'the run took: {now()-start_time} seconds')
    '''


