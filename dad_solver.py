#Killer Sudoku Solver

#Nomenclature:
#Rows, Columns are obvious.
#Box is a 3x3 grid.
#Cage is a set of numbers with a border and total.

#Design decision: Internally, we work in binary representations, using 9 bit:
#000000001 represents '1'
#000000010 represents '2'
#000000100 represents '3'
#100000000 represents '9'
#000000011 represents '1' and/or '2'

#Step 1 is to generate basic data on possible numbers
#Step 2 is to load the puzzle data in, and apply the possible numbers
#Step 3 is to solve. There are 5 sets of constraints:
#Constraint 1: No row may contain a duplicate number
#Constraint 2: No column may contain a duplicate number
#Constraint 3: No box may contain a duplicate number
#Constraint 4: No cage may contain a duplicate number
#Constraint 5: A cage must total to the total given for that section

import time
#import problems

#***********************************************************************************************************************
def print_board(board):
# Function to display the board as-is, where LHS is only definite values, rhs is possible values
#For example:
#1 . . . . . . 2 .          1  987654321  987654321  987654321  987654321  987654321     6 4321         2   987654321
#. . . . . 3 . . .  987654321   8     2   987654321  987654321  987654321        3      7 5  2   987654321  987654321
#. . . 4 . . . . .  98765  2   987654321  9 7 5           4     987654321  987654321  987654321  987654321  987654321
#. 5 . . . 6 . . .  987 54321      5      987654321  987654321  9 7     1     6       987654321  987654321  987654321
#. . . . . . . . .  987654321  987654321  987654321       43    987654321  987654321  9  6 4321  987654321  987654321
#. . . . 7 . . 8 9  987654321  987654321  987654321  987654321    7        987654321  987654321   8         9
#. . . . . . . . 2  987654321  987654321  987654321  987654321  987654321  98  54 21  987654321  987654321         2
#. 3 . . . . . . .  987654321        3    987654321  987654321  98   4  1  987654321  987654321  987654321  987654321
#. . . . . . . . 1  987654321  987654321  987654321  987654321   87 54321  987654321  987654321  987654321          1
#***********************************************************************************************************************
    for row in range(9):
        rowbase=row*9
        #Left hand show of known cells
        for col in range(9):
            cellno=rowbase+col;
            if popcount[board[cellno]]<=1:
                print(binarytodecimal[board[cellno]],end=' ')
            else:
                print('. ',end='')
        #right hand view of possible values
        for col in range(9):
            cellno=rowbase+col;
            print(binarytodisplay[board[cellno]],end=' ')

        print()




starttime=time.perf_counter()

#Step 1: Find every possible combination of 9 digits. Get their totals.
#Result should be 46 rows with totals from 0 to 45 showing every combination that can give that total, eg:
#0
#1 (1)
#2 (2)
#3 (1,2)
#4 (1,3)
#5 (1,4), (2,3)
#6 (1,5), (2,4), (1,2,3)
#however, we would do this in binary because everything is binary:
#0
#1 (0b1)
#2 (0b10)
#3 (0b1,0b10)
#4 (0b1,0b100)
#5 (0b1,0b1000), (0b10,0b100)
#6 (0b1,0b10000), (0b10,0b1000), (0b1,0b10,0b100)
#
#Then we need to store these in a 2D array- total and number of digits we need.
#What we really want to know is that if the total is 12 and uses 2 digits, they could be 3+9, 4+8, 5+7, ie any of 3,4,5,6,7,8,9
#Then we can stuff 3-9 into the section as possibles, and exclude 1 & 2.

binarytodecimal=[] #Given a set of binary digits, what is the decimal equivalent?
decimaltobinary=[] #given a digit count and decimal number, what bits _might_ be used to make that total?
popcount       =[] #How many bits in a given binary number
binarytodisplay=[] #What should this be shown as on screen?

for i in range(10):         #For up to 9 required digits
    decimaltobinary.append([])
    for j in range(46):        #Pre-fill the array with empty elements
        decimaltobinary[i].append(0)

bit = [None for i in range(10)]
dec = [None for i in range(10)]
for i in range(512):
    total=0
    bitcount=0
    displayas=''
    for bitno in range(10):
        bit[bitno]=i & (1<<bitno)
        dec[bitno]=bit[bitno]*(bitno+1)>>bitno
        if bit[bitno]:
            total=total+bitno+1
            bitcount+=1
            displayas=str(bitno+1)+displayas
        else:
            displayas=' '         +displayas

    binarytodecimal.append(total)
    decimaltobinary[bitcount][total]=decimaltobinary[bitcount][total] | i
    popcount.append(bitcount)
    binarytodisplay.append(displayas)

#    print(total, bitcount, bit[::-1])
#    print(total, bitcount, dec[::-1])


#So, we can convert from a binary pattern to the decimal value, and from a decimal value to all the possible bits that could make it up.

endtime=time.perf_counter() #1 mS, 4mS with print statements
print('Setup elapsed time= ',1000*(endtime-starttime),'mS')
starttime=time.perf_counter();

#Prepare the 9x9 grid as 81 linear elements
board=[511]*81  #given a digit count and decimal number, what bits _might_ be used to make that total?

#Test data to prove print_board(board)

#board[0]=1<<0; board[7]=1<<1; board[14]=1<<2; board[21]=1<<3; board[28]=1<<4; board[32]=1<<5; board[49]=1<<6; board[52]=1<<7; board[53]=1<<8; board[62]=1<<1; board[64]=1<<2; board[80]=1<<0
#print_board(board)


def main(problem):
    # Load the cage data into the linear board
    for cage in problem:
        print("Cage total= ", cage[0], end='')
        binary = decimaltobinary[cage[0]]      # This is the list of possible binary bits
        for cells in cage[1]:                # For each cell in the cage
            x = cells[0]
            y = cells[1]
            board[x+y*9] = binary              # Restrict the bits according to the pattern outlined above.
            print(', x=', x, ', y=', y, end='')
        print("")
    print_board(board)                       # Show the board after setup. This should be much simpler than before
    bad_guess_count=987654321  # An appropriate number of glitches!
    return board, bad_guess_count

#The cage data is loaded from problems.py above, as an import. Now process it...
#for problemno in problems.problems[0]
#  print(problems.problems[problemno])
#for cage in problems[problemno]:
#  print(problems[problemno][cage])


if __name__ == '__main__':
    import problems
    test_problem = problems.problems[0][1]
    print(main(test_problem))
