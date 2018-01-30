"""
This is David's solution to the killer sudoku challenge

The set of possibilities for a square is represented as the 1 bits in an integer.
For example if a square is 7 that means the square is one of [1, 2, 3]

A possible combination of digits for a section is represented as the 1 bits in an integer.
For example a combo of 7 that means the section contains [1, 2, 3]

ToDo:
    - start using the 'to process' variable
    - simplify the setup code using the 'to process' variable instead of smart initialisation
    - generalise the "# set a value if it can only be in one location in the rule" to work with all subsets of a rule
    - subtract rule 1 from rule 2 if rule 1 is a subset of rule 2
    - try removing add_value and replacing it with a smarter remove_possibilities
    - experiment with "process rule" being a callable function,
        this would allow the use of the profiler
        this would allow calls inside add_value and remove_possibility
    - understand robert's code


David 2 took a total of 32.328 seconds and 146381 bad guesses. Each bad guess took 0.221 milliseconds on average
moved the location of the search for the missing digit
David 2 took a total of 27.883 seconds and 88999 bad guesses. Each bad guess took 0.313 milliseconds on average
major rework of the data structures to have a unified set of rules.
David 2 took 0.1815 seconds and 350 bad guesses to run grandad slow problem
replaced functions with lookups
David 2 took 0.0897 seconds and 350 bad guesses to run grandad slow problem
added deductions using combos
David 2 took 0.0311 seconds and 54 bad guesses to run grandad slow problem
David 2 took a total of 7.388 seconds and 13877 bad guesses. Each bad guess took 0.532 milliseconds on average
if a rule must have a value and it can only be in one place then add the value
David 2 took a total of 5.418 seconds and 3506 bad guesses. Each bad guess took 1.545 milliseconds on average
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


def print_board(board):
    """This prints a board in a human readable form with the solved squares and the possible values both shown.
    >>> board, rules, rule_memberships = setup(test_problem)
    >>> add_value(board, rules, rule_memberships, 0, 256)
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


def setup(problem):
    """
    >>> board, rules, rule_memberships = setup(test_problem)
    >>> print_board(board)
    . . . . . . . . .  |  320 320   5   5 495 495 504 504 511
    . . . . . . . . .  |   15  15 511 511 480 119 119 511 511
    . . . . . . . . .  |  510 504 504 511 480  15  15 504   5
    . . . . . . . . .  |  510  27  27 511 511 510 495 504   5
    . . . . . . . . .  |  255 255 320 119 511 510 495  63  63
    . . . . . . . . .  |   63 119 320 119 511 511 255 255 480
    . . . . . . . . .  |   63 119   5   5 119 511 432 432 480
    . . . . . . . . .  |  511 511 432 432 119 511 511  63  63
    . . . . . . . . .  |  511 384 384  63  63  63  63 504 504
    <BLANKLINE>
    <BLANKLINE>
    """
    global add_value_calls
    global bad_guesses
    add_value_calls = 0
    bad_guesses = 0
    # convert the problem specific rules to my format
    rules = [{'locs': {x + y * 9 for x, y in section}, 'combos': combos[len(section)][total], 'to process': True}
             for total, section in problem]
    # convert the static rules to my format
    rules += [{'locs': locs, 'combos': {511}, 'to process': True}
              for locs in rows + cols + boxes]
    # I need to know which groups each square is a member of
    rule_memberships = [[rule for rule in rules if loc in rule['locs']] for loc in range(81)]
    assert len(rule_memberships[0]) == 4
    board = [511]*81
    for rule in rules:
        possible_values = union(rule['combos'])
        for loc in rule['locs']:
            board[loc] &= possible_values
    return board, rules, rule_memberships


def main(problem):
    """This is the entry point for my code. It takes a killer sudoku problem and returns the solution"""
    board, rules, rule_memberships = setup(problem)
    solved_board = solver(board, rules, rule_memberships)
    return [set_to_val[square] for square in solved_board], bad_guesses


def add_value(board, rules, rule_memberships, loc, single_possibility):
    """Given a board and a location set the value at the location and remove all numbers that are now impossible.
    This function will change the given board and rules. It may raise a Contradiction.
    Only call add_value on squares that don't have a value already.
    >>> board, rules, rule_memberships = setup(test_problem)
    >>> print_board(board)
    . . . . . . . . .  |  320 320   5   5 495 495 504 504 511
    . . . . . . . . .  |   15  15 511 511 480 119 119 511 511
    . . . . . . . . .  |  510 504 504 511 480  15  15 504   5
    . . . . . . . . .  |  510  27  27 511 511 510 495 504   5
    . . . . . . . . .  |  255 255 320 119 511 510 495  63  63
    . . . . . . . . .  |   63 119 320 119 511 511 255 255 480
    . . . . . . . . .  |   63 119   5   5 119 511 432 432 480
    . . . . . . . . .  |  511 511 432 432 119 511 511  63  63
    . . . . . . . . .  |  511 384 384  63  63  63  63 504 504
    <BLANKLINE>
    <BLANKLINE>
    >>> add_value(board, rules, rule_memberships, 0, 256)
    >>> board[0]
    256
    >>> board[1]
    64
    >>> board[9] & 256
    0
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
    global add_value_calls
    assert 0 <= loc < 81
    assert single_possibility in {1, 2, 4, 8, 16, 32, 64, 128, 256}
    assert single_possibility != board[loc]
    add_value_calls += 1
    # set the current square
    remove_possibilities(board, rules, rule_memberships, loc, ~single_possibility, False)
    # we now know that the value in the current square can't be found in any of the neighbors
    for rule in rule_memberships[loc]:
        for loc2 in rule['locs']:
            # only do the work to remove a value if the value is currently considered possible
            if loc2 != loc and single_possibility & board[loc2]:
                remove_possibilities(board, rules, rule_memberships, loc2, single_possibility, True)
        # todo remove the location from the rule at this point, also if the rule becomes empty then remove the rule


def remove_possibilities(board, rules, rule_memberships, loc, possibilities, recurse):
    """This takes a board and removes a collection of possibilities from a single square."""
    if not possibilities & board[loc]:
        # if there is no overlap between the current possibilities and the possibilities to remove then return early
        return
    new_possibilities = (~possibilities) & board[loc]
    if new_possibilities in {1, 2, 4, 8, 16, 32, 64, 128, 256} and recurse:
        add_value(board, rules, rule_memberships, loc, new_possibilities)
    else:
        board[loc] = new_possibilities
    if board[loc] == 0:
        raise Contradiction
    for rule in rule_memberships[loc]:
        new_combos = [combo for combo in rule['combos'] if combo & board[loc]]
        if not new_combos:
            raise Contradiction
        rule['combos'] = new_combos


def solver(board, rules, rule_memberships):
    """This solves an arbitrary board using deduction and when that fails, guessing solutions
    >>> board, rules, rule_memberships = setup(test_problem)
    >>> solver(board, rules, rule_memberships) # doctest: +ELLIPSIS
    [256, 64, 1, 4, 8, 32, 16, 128, ...
    """
    global bad_guesses
    # print_board(board)
    # check if this leaves a group of 9 where a number can only be in one location
    # this is computationally expensive because I need to find a large number of unions
    # print_board(board)
    progress_made = True
    while progress_made:
        progress_made = False
        for rule in rules:
            # remove combos if they need values that are not present
            banned_values = ~union(board[loc] for loc in rule['locs'])
            new_combos = [combo for combo in rule['combos'] if not (combo & banned_values)]
            if not new_combos:
                raise Contradiction
            if new_combos != rule['combos']:
                progress_made = True
                rule['combos'] = new_combos

            # remove values from squares if they are not in any combo
            banned_values = ~union(rule['combos'])
            for loc in rule['locs']:
                if board[loc] & banned_values:
                    remove_possibilities(board, rules, rule_memberships, loc, banned_values, True)

            # set a value if it can only be in one location in the rule
            for loc in rule['locs']:
                # don't bother looking at squares that are already known
                if board[loc] not in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
                    required_digits = 511
                    for combo in rule['combos']:
                        required_digits &= combo
                    found_digits = 0
                    for loc2 in rule['locs']:
                        if loc2 != loc:
                            found_digits |= board[loc2]
                    must_be_in_current_square = required_digits & ~ found_digits
                    if not must_be_in_current_square:
                        # most of the time this constraint yields nothing of use
                        pass
                    elif must_be_in_current_square in {0, 1, 2, 4, 8, 16, 32, 64, 128, 256}:
                        if must_be_in_current_square & board[loc]:
                            add_value(board, rules, rule_memberships, loc, must_be_in_current_square)
                            progress_made = True
                        else:
                            # the current square must contain the value that must be present
                            raise Contradiction
                    else:
                        # if more then one value must be in the current square then something has gone wrong.
                        raise Contradiction

            '''
            # If a subset of a rule contains as many possibilities as the size of the subset
            # then all the possibilities in the subset can be removed from every part of the
            # rule not in the subset
            # this is a generalisation of the deduction "set a value if it can only be in one location in the rule"
            if rule[2]:
                for subset in rule:
                    possibilities = union(subset)
                    number_of_possibilities = popcount(possibilities)
                    if number_of_possibilities < len(subset):
                        raise Contradiction
                    elif number_of_possibilities == len(subset):
                        # then I can exclude lots of possibilities from the others locations in the rule  
            '''

    loc_to_guess = None
    min_possibility_count = 999
    # find the uncertain square with the least possible values
    for loc in range(81):
        possibility_count = pop_count[board[loc]]
        if 1 < possibility_count < min_possibility_count:
            min_possibility_count = possibility_count
            loc_to_guess = loc
            if min_possibility_count == 2:
                # 2 is the best possible so looking further is pointless
                break
    if loc_to_guess is None:
        # then the board is solved :-)
        return board
    for possibility in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
        if not possibility & board[loc_to_guess]:
            continue
        possible_board = board[:]
        possible_rules = []
        possible_rule_memberships = [[] for _ in range(81)]
        for rule in rules:
            rule = rule.copy()
            rule['combos'] = rule['combos'].copy()
            possible_rules.append(rule)
            for loc in rule['locs']:
                possible_rule_memberships[loc].append(rule)
        try:
            add_value(possible_board, possible_rules, possible_rule_memberships, loc_to_guess, possibility)
            return solver(possible_board, possible_rules, possible_rule_memberships)
        except Contradiction:
            # then that particular guess is wrong
            bad_guesses += 1
    # if there is a square on the current board which has no possible values
    # then there is a contradiction somewhere
    # print('Backtrack')
    raise Contradiction


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

pop_count = [bin(x).count('1') for x in range(512)]
set_to_list = [[i+1 for i in range(9) if j & 1 << i] for j in range(512)]
add_value_calls = 0
bad_guesses = 0
rows = [{col+row*9 for col in range(9)} for row in range(9)]
cols = [{col+row*9 for row in range(9)} for col in range(9)]
boxes = [{col+row*9+box_col*3+box_row*3*9 for row in range(3) for col in range(3)}
         for box_row in range(3) for box_col in range(3)]
# combos contains every possible collection of the digits 1-9
# then group them by number of squares in the section and the sum of all the values in the section
# this looks like combo[length][total]
combos = [[[possible_section for possible_section in range(512)
            if pop_count[possible_section] == length and sum(set_to_list[possible_section]) == total]
           for total in range(46)] for length in range(9)]
assert combos[2][3] == [3]
# a section that is 2 long and sums to 5 has 2 possibilities [1,4] and [2,3] these are represented as 9 and 6
assert combos[2][5] == [6, 9]

if __name__ == '__main__':
    import problems
    test_problem = problems.problems[0][1]
    doctest.testmod()
    test_board, test_rules, test_rule_memberships = setup(test_problem)
    test_solved_board = solver(test_board, test_rules, test_rule_memberships)
    print(bad_guesses, test_solved_board)
