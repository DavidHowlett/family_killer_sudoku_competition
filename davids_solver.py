from time import perf_counter as now
import problems


class Contradiction(Exception):
    """Raised when the board is in an inconsistent state"""


# board is the current state of the solution
board = [list(range(1, 10)) for _ in range(81)]
rows = [{col+row*9 for col in range(9)} for row in range(9)]
cols = [{col+row*9 for row in range(9)} for col in range(9)]
boxes = [{col+row*9+box_col*3+box_row*3*9 for row in range(3) for col in range(3)}
         for box_row in range(3) for box_col in range(3)]
groups = rows+cols+boxes
# friends of a location are the locations that share a row, column or box
friends = [set().union(*[group.difference({loc}) for group in groups if loc in group]) for loc in range(81)]


def add_value(_board, loc, val):
    """Given a board and a location set the value at the location and remove all numbers that are now impossible"""
    assert 0 <= loc < 81
    assert 0 < val < 10
    # set the current square
    _board[loc] = [val]
    # we now know that the value in the current square can't be found in any of the neighbors
    for loc2 in friends[loc]:
        friend2 = _board[loc2]
        if val in friend2:
            friend2.remove(val)
            # if the other square becomes solved as a result of the removal then
            # extra processing is required
            if len(friend2) == 1:
                add_value(_board, loc2, *friend2)


for i in range(8):
    add_value(board, i, i+1)


def print_board(_board):
    for row in range(9):
        for col in range(9):
            square = _board[col + row * 9]
            print(square[0] if len(square) == 1 else '.', end=' ')
        print('')


print_board(board)

"""
I plan to use the numbers 0-80 to represent the board locations, left to right top down

each board location will be 

"""

