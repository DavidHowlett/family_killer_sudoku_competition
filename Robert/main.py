import os

# Load problem

# Precalculate sums for 1-45 for 1-9 numbers

# Consider converting to 0-8 instead of 1-9

# Middle of problem state:
# List of cells
#   containing set of possible values
# List of remaining rules
#   List/set of cells applying to
#   set of possible solutions
#       Either combinations or permuations

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


def main(target):
    """Solve the problem given in target"""

    # Create a dictionary of all possible combinations
    combinations = {n: [] for n in range(46)}
    for i in range(2 ** 9):
        filt = "{0:0>9b}".format(i)
        nums = {val + 1 for val, flag in enumerate(filt) if int(flag)}

        combinations[sum(nums)] += [nums]



def core(cells, rules):
    """Solve the problem given"""
    # Do some deductive phase here

    # Do some branching phase


if __name__ == '__main__':
    main("test.txt")
