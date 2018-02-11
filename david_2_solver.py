"""
This is David's solution to the killer sudoku challenge

The set of possibilities for a square is represented as the 1 bits in an integer.
For example if a square is 7 that means the square is one of [1, 2, 3]

A possible combination of digits for a section is represented as the 1 bits in an integer.
For example a combo of 7 that means the section contains [1, 2, 3]

ToDo:]
    - make a data structure for the rule overlaps that is incrementally updated
    - use the data structure
    - exclude more values within a rule based on constraints from the combos and the current possibilities
    - when the board gets solved, notice earlier
    - experiment with "process rule" being a callable function,
        this would allow the use of the profiler
        this would allow calls inside add_value and remove_possibility
    - replace rule_memberships with "friends"
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
removed add_value
David 2 took a total of 5.210 seconds and 3506 bad guesses. Each bad guess took 1.486 milliseconds on average
added "to process" variable
David 2 took a total of 3.181 seconds and 3506 bad guesses. Each bad guess took 0.907 milliseconds on average
added checks on all subsets of all rules (this was then reverted)
David 2 took a total of 42.416 seconds and 1873 bad guesses. Each bad guess took 22.646 milliseconds on average
subtract a rule if it is a subset
David 2 took a total of 2.647 seconds and 1992 bad guesses. Each bad guess took 1.329 milliseconds on average
created remove_combos function
David 2 took a total of 2.568 seconds and 1992 bad guesses. Each bad guess took 1.289 milliseconds on average
remove_combos now removes possibilities from the board
David 2 took a total of 2.337 seconds and 2002 bad guesses. Each bad guess took 1.168 milliseconds on average
micro optimisation
David 2 took a total of 2.295 seconds and 2002 bad guesses. Each bad guess took 1.147 milliseconds on average
built machinery to calculate rule overlaps
David 2 took a total of 2.640 seconds and 1992 bad guesses. Each bad guess took 1.325 milliseconds on average
moved deductions 1-3 to their own functions and ditched progress_made
David 2 took a total of 2.630 seconds and 1992 bad guesses. Each bad guess took 1.320 milliseconds on average
enabled deduction 4
David 2 took a total of 2.485 seconds and 2029 bad guesses. Each bad guess took 1.225 milliseconds on average
moved deduction 5 and 6
David 2 took a total of 2.570 seconds and 2029 bad guesses. Each bad guess took 1.267 milliseconds on average
added deduction 5
David 2 took a total of 8.801 seconds and 1710 bad guesses. Each bad guess took 5.146 milliseconds on average
"""
import doctest
import itertools


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
    >>> remove_possibilities(board, rules, rule_memberships, 0, ~256)
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


def rule_overlaps_maker(rules):
    """This finds the overlaps between all of the rules"""
    # todo try to make this run faster by starting with rule_overlaps rather then rules O(n^2) -> O(n)
    rule_overlaps = []
    for i, rule1 in enumerate(rules):
        for rule2 in rules[:i]:
            intersection = rule1['locs'].intersection(rule2['locs'])
            if intersection:
                rule_overlaps.append((intersection, rule1, rule2))
    return rule_overlaps


def rule_overlaps_maker2(rule_memberships):
    """This finds the overlaps between all of the rules"""
    rule_overlaps = []
    return rule_overlaps


def consistency_check(rules, rule_memberships, rule_overlaps):
    # all the rules should be listed in rule_memberships
    for rule in rules:
        for loc in rule['locs']:
            assert rule in rule_memberships[loc]
    # all the rule_memberships should be listed in rules
    for loc in range(81):
        for rule in rule_memberships[loc]:
            assert loc in rule['locs']
    assert rule_overlaps == rule_overlaps_maker(rules)


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
    global bad_guesses
    bad_guesses = 0
    # convert the problem specific rules to my format
    rules = [{'locs': {x + y * 9 for x, y in section},
              'combos': combos_by_len_and_total[len(section)][total].copy(), 'to process': True}
             for total, section in problem]
    # convert the static rules to my format
    rules += [{'locs': locs.copy(), 'combos': {511}, 'to process': True}
              for locs in rows + cols + boxes]
    # I need to know which groups each square is a member of
    rule_memberships = [[rule for rule in rules if loc in rule['locs']] for loc in range(81)]
    # it makes some of the logic faster to pre compute the overlaps between the rules
    rule_overlaps = []
    for i, rule1 in enumerate(rules):
        for rule2 in rules[:i]:
            intersection = rule1['locs'].intersection(rule2['locs'])
            if intersection:
                rule_overlaps.append((intersection, rule1, rule2))
    assert len(rule_memberships[0]) == 4
    board = [511]*81
    for rule in rules:
        possible_values = union(rule['combos'])
        for loc in rule['locs']:
            board[loc] &= possible_values
    consistency_check(rules, rule_memberships, rule_overlaps)
    return board, rules, rule_memberships, rule_overlaps


def main(problem):
    """This is the entry point for my code. It takes a killer sudoku problem and returns the solution"""
    board, rules, rule_memberships, rule_overlaps = setup(problem)
    solved_board = solver(board, rules, rule_memberships, rule_overlaps)
    return [set_to_val[square] for square in solved_board], bad_guesses


def remove_possibilities(board, rules, rule_memberships, loc, possibilities):
    """This takes a board and removes a collection of possibilities from a single square."""
    if not possibilities & board[loc]:
        # if there is no overlap between the current possibilities and the possibilities to remove then return early
        return
    new_possibilities = (~possibilities) & board[loc]
    board[loc] = new_possibilities
    if new_possibilities in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
        # we now know that the value in the current square can't be found in any of the neighbors
        for rule in rule_memberships[loc]:
            # todo remove the location from the rule at this point, also if the rule becomes empty then remove the rule
            # rule['locs'].remove(loc)
            # rule['combos'] = [combo ^ new_possibilities for combo in rule['combos'] if combo & new_possibilities]
            for loc2 in rule['locs']:
                # only do the work to remove a value if the value is currently considered possible
                if loc2 != loc and new_possibilities & board[loc2]:
                    remove_possibilities(board, rules, rule_memberships, loc2, new_possibilities)
            # todo remove the rule if it gets too small
    if board[loc] == 0:
        raise Contradiction
    for rule in rule_memberships[loc]:
        rule['to process'] = True
        remove_combos(
            board, rules, rule_memberships, rule, [combo for combo in rule['combos'] if not (combo & board[loc])])


def remove_combos(board, rules, rule_memberships, rule, combos_to_remove):
    """This takes a rule, removes a combo from it and then does the appropriate other removals"""
    if not combos_to_remove:
        return
    for combo in combos_to_remove:
        rule['combos'].remove(combo)
    if not rule['combos']:
        raise Contradiction
    possibilities = union(rule['combos'])
    for loc in rule['locs']:
        remove_possibilities(board, rules, rule_memberships, loc, board[loc] & ~possibilities)


def deduction1(board, rules, rule_memberships, rule):
    """Remove combos if they need values that are not present"""
    banned_values = ~union(board[loc] for loc in rule['locs'])
    remove_combos(board, rules, rule_memberships, rule, [combo for combo in rule['combos'] if combo & banned_values])


def deduction2(board, rules, rule_memberships, rule):
    """Remove values from squares if they are not in any combo"""
    banned_values = ~union(rule['combos'])
    for loc in rule['locs']:
        if board[loc] & banned_values:
            remove_possibilities(board, rules, rule_memberships, loc, banned_values)


def deduction3(board, rules, rule_memberships, rule):
    """Set a value if it can only be in one location in the rule"""
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
                    remove_possibilities(board, rules, rule_memberships, loc, ~must_be_in_current_square)
                else:
                    # the current square must contain the value that must be present
                    raise Contradiction
            else:
                # if more then one value must be in the current square then something has gone wrong.
                raise Contradiction


def deduction4(board, rules, rule_memberships):
    """Remove known values from rules. This would ideally be done incrementally by the remove_possibilities function
    but doing so would change the size of locs while locs were being iterated over"""
    for loc in range(81):
        if rule_memberships[loc] and board[loc] in {1, 2, 4, 8, 16, 32, 64, 128, 256}:
            for rule in rule_memberships[loc]:
                rule['locs'].remove(loc)
                rule['combos'] = [combo & ~board[loc] for combo in rule['combos'] if combo & board[loc]]
                if len(rule['locs']) < 2:
                    if len(rule['locs']) == 1:
                        # assert pop_count[board[next(iter(rule2['locs']))]] == 1
                        rule_memberships[next(iter(rule['locs']))].remove(rule)
                    rules.remove(rule)
                else:
                    rule['to process'] = True
            rule_memberships[loc] = []


def deduction5(board, rules, rule_memberships, rule):
    """For every subset in the rule if the number of possibilities in the subset is the same size as the subset
    then remove the possibilities from all parts of the rule not in the subset
    this is a generalisation of the deduction "set a value if it can only be in one location in the rule" """
    locs = rule['locs']
    for subset_size in range(2, len(locs) - 1):
        for subset in itertools.combinations(locs, subset_size):
            possibilities = 0
            for loc in subset:
                possibilities |= board[loc]
            number_of_possibilities = pop_count[possibilities]
            if number_of_possibilities > len(subset):
                continue
            if number_of_possibilities == len(subset):
                # then I can exclude lots of possibilities from the others locations in the rule
                for loc in locs:
                    if loc not in subset:
                        remove_possibilities(board, rules, rule_memberships, loc, possibilities)
            else:
                raise Contradiction


def deduction6(rules, rule_memberships, rule):
    """Subtract rule 1 from rule 2 if rule 1 is a subset of rule 2 and rule 1 only has one combo"""
    if len(rule['combos']) == 1:
        # assert len(rule['locs']) != 1
        subset_combo = next(iter(rule['combos']))
        # todo try using rule_memberships to make this go faster. I should not check every rule.
        for rule2 in rules:
            if rule['locs'].issubset(rule2['locs']) and rule is not rule2:
                rule2['locs'] -= rule['locs']
                rule2['combos'] = [
                    superset_combo & ~subset_combo
                    for superset_combo in rule2['combos'] if not (subset_combo & ~superset_combo)]
                for loc in rule['locs']:
                    rule_memberships[loc].remove(rule2)
                # progress_made = True
                # If rule2 has 0 or 1 locations left it can be removed.
                if len(rule2['locs']) < 2:
                    if len(rule2['locs']) == 1:
                        # assert pop_count[board[next(iter(rule2['locs']))]] == 1
                        rule_memberships[next(iter(rule2['locs']))].remove(rule2)
                    rules.remove(rule2)
                else:
                    rule2['to process'] = True


def solver(board, rules, rule_memberships, rule_overlaps):
    """This solves an arbitrary board using deduction and when that fails, guessing solutions
    >>> board, rules, rule_memberships = setup(test_problem)
    >>> solver(board, rules, rule_memberships) # doctest: +ELLIPSIS
    [256, 64, 1, 4, 8, 32, 16, 128, ...
    """
    global bad_guesses
    # print_board(board)

    old_board = None
    while old_board != board:  # run the deductions until progress stops
        old_board = board.copy()
        deduction4(board, rules, rule_memberships)
        for rule in rules:
            if not rule['to process']:
                continue
            rule['to process'] = False
            deduction1(board, rules, rule_memberships, rule)
            deduction2(board, rules, rule_memberships, rule)
            deduction3(board, rules, rule_memberships, rule)
            deduction6(rules, rule_memberships, rule)
            assert len(rule['locs']) > 1

        '''
        # if rule A and rule B overlap and rule A must have a "5" somewhere in the overlap
        # then remove "5" from all locations in rule B not in the overlap
        rule_overlaps = rule_overlaps_maker(rules)  # todo remove this
        consistency_check(rules, rule_memberships, rule_overlaps)
        # for subset_size in range(2, len(locs)-1):
        for rule1, rule2, overlap in rule_overlaps:
            must_be_in_rule = 511
            for combo in rule1['combos']:
                must_be_in_rule &= combo
            locs = rule1['locs']
            for subset_size in range(3, len(locs)-2):
                for rule1_subset in itertools.combinations(locs, subset_size):
                    could_be_outside_subset = union(board[loc] for loc in locs if loc not in rule1_subset)
                    # print(must_be_in_rule & ~could_be_outside_subset)
        '''

        '''
        for every rule1_subset in rule:
            if there are numbers that must be in rule1_subset:
                for every rule2 that is a superset of rule1_subset:
                    remove the numbers from every square of rule2 not in rule1_subset

        '''
    # for rule in rules:
    #    deduction5(board, rules, rule_memberships, rule)

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
            rule['locs'] = rule['locs'].copy()
            possible_rules.append(rule)
            for loc in rule['locs']:
                possible_rule_memberships[loc].append(rule)
        # possible_rule_overlaps = rule_overlaps_maker(possible_rules)
        possible_rule_overlaps = rule_overlaps  # todo remove this
        try:
            remove_possibilities(possible_board, possible_rules, possible_rule_memberships, loc_to_guess, ~possibility)
            return solver(possible_board, possible_rules, possible_rule_memberships, possible_rule_overlaps)
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
set_to_total = [sum(set_to_list[i]) for i in range(512)]
bad_guesses = 0
rows = [{col+row*9 for col in range(9)} for row in range(9)]
cols = [{col+row*9 for row in range(9)} for col in range(9)]
boxes = [{col+row*9+box_col*3+box_row*3*9 for row in range(3) for col in range(3)}
         for box_row in range(3) for box_col in range(3)]
# combos contains every possible collection of the digits 1-9
# then group them by number of squares in the section and the sum of all the values in the section
# this looks like combo[length][total]
combos_by_len_and_total = [[[possible_section for possible_section in range(512)
                             if pop_count[possible_section] == length and set_to_total[possible_section] == total]
                            for total in range(46)] for length in range(9)]
assert combos_by_len_and_total[2][3] == [3]
# a rule that is 2 long and sums to 5 has 2 possibilities [1,4] and [2,3] these are represented as 9 and 6
assert combos_by_len_and_total[2][5] == [6, 9]
# a rule that is 3 long which sums to 20 should actually sum to 20
assert set_to_total[next(iter(combos_by_len_and_total[3][20]))] == 20

if __name__ == '__main__':
    import problems
    import time
    test_problem = problems.problems[-1][1]
    # doctest.testmod()
    test_board, test_rules, test_rule_memberships, test_rule_overlaps = setup(test_problem)
    test_solved_board = solver(test_board, test_rules, test_rule_memberships, test_rule_overlaps)
    print(bad_guesses, test_solved_board)

    start_time = time.perf_counter()
    for _ in range(1000):
        rule_overlaps_maker(test_rules)
    print(time.perf_counter() - start_time)


