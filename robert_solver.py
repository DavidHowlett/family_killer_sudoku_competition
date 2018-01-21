import time
import copy
import problems

# Middle of problem state:
# List of cells
#   containing set of possible values
# List of remaining rules
#   List/set of cells applying to
#   set of possible solutions
#       Either combinations or permutations

# Deductive component
#   We apply a rule (a collection of possible solutions) to it's collection of cells
#   Many possible deductions
#       A value is not in possible solutions, so value can be removed from all cells
#       Some values in cells have been fixed, so we can simplify the rule, make it apply to fewer cells
#       A value is not available in some cells, so some rule solutions are no longer valid
#       A rule is not possible to achieve with the given cells, so raise an error
#       A rule's subjects have been completely defined, so no need to keep the rule around.

# Are there deductions to make that require considering multiple rules?

# Branching component
# Deductive is fast, but probably won't be good enough to solve alone.
# Therefore choose a cell, and examine every possibility.
#

ITERCOUNT = 0


class RuleViolationError(RuntimeError):
    pass


def init_problem(problem):

    problem = copy.deepcopy(problem)  # to avoid trouble for David and Micheal
    # Add basic sudoku rules (implied)
    # This can be moved to import time
    # Rows contain unique 1-9
    problem += [(45, [(row, col) for col in range(9)]) for row in range(9)]
    # Cols contain unique 1-9
    problem += [(45, [(row, col) for row in range(9)]) for col in range(9)]
    # big squares contain unique 1-9
    for big_row in range(3):
        for big_col in range(3):
            problem += [(45, [(row+3*big_row, col+3*big_col) for row in range(3) for col in range(3)])]

    # Convert from dual index to single index
    for index, rule in enumerate(problem):
        problem[index] = (rule[0], {row*9+col for col, row in rule[1]})

    return problem


def copy_custom(cells, rules):
    """Slightly faster version of deepcopy

    Deepcopy also copies immutable things like ints, so this is much faster"""
    return [cell.copy() for cell in cells], \
           [([p.copy() for p in possibles], targets.copy()) for possibles, targets in rules]


def main(problem):
    global bad_guesses
    """Solve the problem given in target"""
    # there have been no bad guesses at this point
    bad_guesses = 0

    # Create a dictionary of all possible combinations
    # This can be moved to import time
    combinations = {n: [] for n in range(46)}
    for i in range(2 ** 9):
        filt = "{0:0>9b}".format(i)
        nums = {val + 1 for val, flag in enumerate(filt) if int(flag)}

        combinations[sum(nums)] += [nums]

    # Load problem
    rules = init_problem(problem)

    # Replace target values with combinations
    rules = [([combo.copy() for combo in combinations[val] if len(combo) == len(subjects)], subjects)
             for val, subjects in rules]

    # Generate initial set of cells
    cells = [{i+1 for i in range(9)} for _ in range(9 ** 2)]

    return [next(iter(square)) for square in core(cells, rules)], bad_guesses


def core(cells, rules):
    """Solve the problem given"""

    global ITERCOUNT
    global bad_guesses

    # print(ITERCOUNT)
    # Do some deductive phase here
    deduction_made = True  # Controls whether we go around the loop again
    while deduction_made:
        ITERCOUNT += 1
        deduction_made = False
        # Do rule vs cell comparison
        for possibles, targets in rules:
            # Some values in cells have been fixed, so we can simplify the rule, make it apply to fewer cells
            for target in list(targets):
                if len(cells[target]) == 1:
                    fixed_value = next(iter(cells[target]))  # Grab the value of the cell
                    for possible in possibles[:]:
                        try:
                            possible.remove(fixed_value)
                        except KeyError:
                            # Bad possibility!
                            possibles.remove(possible)
                    targets.remove(target)

            # A value is not available in some cells, so some rule solutions are no longer valid
            # Use a dumb test for now
            target_possibles = set().union(*[cells[target] for target in targets])
            for poss_index, possible in reversed(list(enumerate(possibles))):
                # Reverse to avoid issue where deleting elements from the list makes it shorter
                if possible - target_possibles:
                    # Some number is in "possible" which isn't in any cell
                    del possibles[poss_index]

            # A rule might not possible to achieve with the given cells, so raise an error
            if all([len(possible) != len(targets) for possible in possibles]):
                # This can occur if two cells in the same rule have been fixed to the same value.
                raise RuleViolationError

            # A value is not in possible solutions, so value can be removed from all cells
            rule_possibles = set().union(*possibles)
            for target in targets:
                removables = cells[target] - rule_possibles
                if removables:
                    deduction_made = True
                    cells[target] -= removables
                    if not cells[target]:
                        raise RuleViolationError

        # Check for rules that are subsets of each other
        for possibles1, targets1 in rules:
            if len(possibles1) != 1:
                # Current algorithm a little dumb, only handles case with single combination in inner
                continue
            possible1 = possibles1[0]
            if len(possible1) == 0:
                # Current set is empty, matches with every set but uselessly
                continue
            for possibles2, targets2 in rules:
                if targets1.issubset(targets2) and targets1 is not targets2:
                    # We can subtract rule1 from rule2!
                    for t in targets1:
                        targets2.remove(t)

                    # Kill off possibles2 that don't contain possible1
                    for possible in list(possibles2):
                        if not possible1.issubset(possible):
                            possibles2.remove(possible)

                    # Reduce possibles2 by possible1
                    for p in possibles2:
                        for e in possibles1[0]:
                            p.remove(e)

                    deduction_made = True
        rules = list(filter(lambda x: x[1], rules))  # Filter out empty rules

    if any([not possibles and targets for targets, possibles in rules]):
        pass  # raise RuleViolationError

    # Do some branching phase
    best_cell = None
    best_qual = 9999

    for cell, possibles in enumerate(cells):
        if 1 < len(possibles) < best_qual:
            best_cell = cell
            best_qual = len(possibles)

    if best_cell is None:
        # Could not branch at all, so must have found optimal solution
        return cells
    else:
        for possible in list(cells[best_cell]):
            cells[best_cell] = {possible, }
            try:
                return core(*copy_custom(cells, rules))
            except RuleViolationError:
                bad_guesses += 1
        else:
            # Euhh, no possible value of best_cell is valid, must violate a rule
            raise RuleViolationError


if __name__ == '__main__':
    ct = time.time()
    main(problems.problems["problem 2"])
    print(time.time()-ct)
