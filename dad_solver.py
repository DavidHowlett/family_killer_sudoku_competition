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

#binarytodecimal=[] #Given a set of binary digits, what is the decimal equivalent?
#decimaltobinary=[] #given a digit count and decimal number, what bits _might_ be used to make that total?
#popcount       =[] #How many bits in a given binary number
#binarytodisplay=[] #What should this be shown as on screen?
#boxtoboard     =[] #Linearise the boxes to board positions.

import time
import dad_tests

#import problems


starttime=time.perf_counter()




bit = [None for i in range(10)]
dec = [None for i in range(10)]


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



###############################################################################
def loadproblem(problem):
#This finds the possible digits for a cage from the cage totals and cell count
#and then sets these values into each cell. It ignores anything higher as
#these higher functions require the application of the initial cage data
###############################################################################
    # Load the cage data into the linear board
    print("loadproblem(problem)")
    for cage in problem:
#        print("Cage total= ", cage[0], end='')
        cellcount=0
        for cells in cage[1]:                 # How many cells do we have?
            cellcount=cellcount+1
#        print(", Cellcount=", cellcount, end='')
        binary = decimaltobinary[cellcount][cage[0]]      # This is the list of possible binary bits
#        print(", Binary=",binarytodisplay[binary], end='')
        for cells in cage[1]:                # For each cell in the cage
            x = cells[0]
            y = cells[1]
            board[x+(y*9)] = binary              # Restrict the bits according to the pattern outlined above.
#            print(', x=', x, ', y=', y, end='')
#        print("")

###############################################################################
def initialremovecages(problem):
#Now that the initial cage data has been applied, giving the very widest
#possible set of binary digits to make the code work, a bit more processing
#with the cages is possible. For example if a cage has 2 cells and a total of
#3 or 4, there are 2 digits (either 1 & 2 or 1 & 3) that cannot exist
#elsewhere on a row or column and maybe nonet. So, this code is to do this
#initial compute to simplify the problem, cage by cage.
###############################################################################
    print("initialremovecages(problem)")
    cageno=0          #Loop counter for debugging
    for cage in problem:
        cageno=cageno+1


#        if cage[0]>4:      ########Ignore anything but this column of interest
#            print(", but continue to simplify debugging")
#            continue

        cellcount=0
        for cells in cage[1]:                 # How many cells do we have?
            cellcount=cellcount+1

#        print("cageno=",cageno,", Cage total= ", cage[0],", cellcount=", cellcount, ", bitpattern=",binarytodisplay[decimaltobinary[cellcount][cage[0]]])

        if cageno==199:
            continue

#        print(", Cellcount=", cellcount, end='')
        binary = decimaltobinary[cellcount][cage[0]]      # This is the list of possible binary bits
#        print(", Binary=",binarytodisplay[binary], end='')
        #Find the x & y bounds of this cage:
        minx=9; maxx=0; miny=9; maxy=0;      #
        for cells in cage[1]:                # For each cell in the cage
            x = cells[0]
            y = cells[1]
            minx=min(minx, x)
            maxx=max(maxx, x)
            miny=min(miny, y)
            maxy=max(maxy, y)

#        print()
#        print("minx=",minx,", maxx=",maxx,", miny= ",miny,", maxy=",maxy)
        bitpattern=decimaltobinary[cellcount][cage[0]]  #What bit pattern do we have?
        notbitpattern=511-bitpattern          #2's complement of this pattern

        #Now we know the bounds of this cage, we can see if we can do any elimination...
        if (popcount[bitpattern] == cellcount):  # If we have exactly the right number of digits
#            print("bitpattern=", bitpattern, "popcount[bitpattern]=", popcount[bitpattern])
            if (minx==maxx):  #If this is a single-column cage...
                for y in range(0,miny):
                    board[x + (y * 9)]=board[x+(y*9)] & notbitpattern
#                    print("column pre  (", x, ",", y, ")")
                for y in range(maxy+1,9):
                    board[x + (y * 9)]=board[x+(y*9)] & notbitpattern
#                    print("column post (", x, ",", y, ")")
            if (miny==maxy):  #If this is a single-row cage...
                for x in range(0,minx):
                    board[x + (y * 9)]=board[x+(y*9)] & notbitpattern
#                    print("row   pre  (",x,",",y,")")
                for x in range(maxx+1,9):
                    board[x + (y * 9)]=board[x+(y*9)] & notbitpattern
#                    print("row   post (", x, ",", y, ")")

            #Now do the same process for a nonet:
            ## If the number of digits is the number of cells, and all within one nonet, they can be removed from the nonet
            nminx=minx//3; nmaxx=maxx//3; nminy=miny//3; nmaxy=maxy//3;  #Get the nonet-equivalents
            if (nminx==nmaxx) and (nminy==nmaxy): #if all within one nonet
                for x in range(3 * nminx, 3 * nminx + 3):
                    for y in range(3 * nminy, 3 * nminy + 3):
                        #I must exclude the nonet from the cells being addressed here or it will trash stuff!!!!
                        #Remove cage cells from those affected here.
                        #Bodge: For now, I am only going to process cells outside the square containing the rectanble
                        if (x<minx) or (x>maxx) or (y<miny) or (y>maxy):
                            board[x + (y * 9)] = board[x + (y * 9)] & notbitpattern
#                            print("cageno=",cageno,", nonet(",x,",",y,")")

def ruleof1row   (y, board): #Eliminate possibles where a cell on that row is definitely known.
    #print("ruleof1row(",y,")")
    singles=0  #We know no values for sure
    for x in range(0,9): #Look at every cell for single values
        if popcount[board[x+y*9]]==1:
          singles=singles+board[x+y*9]
    notsingles=511-singles    #Find every unknown value
    for x in range(0, 9):  # Look at every cell for single values
        if popcount[board[x+y*9]]!=1:
            board[x + y * 9]=board[x + y * 9] & notsingles  #Wipe out the values we clearly know


def ruleof1col   (x, board):  #Eliminate possibles where a cell on that col is definitely known.
    #print("ruleof1col(",x,")")
    singles=0  #We know no values for sure
    for y in range(0,9): #Look at every cell for single values
        if popcount[board[x+y*9]]==1:
          singles=singles+board[x+y*9]
    notsingles=511-singles    #Find every unknown value
    for y in range(0, 9):  # Look at every cell for single values
        if popcount[board[x+y*9]]!=1:
            board[x + y * 9]=board[x + y * 9] & notsingles  #Wipe out the values we clearly know


def ruleof2row   (y, board): #Eliminate possibles where a cellpair on that row are definitely known.
    #for example:          21         21  987654321  987654321  987654321  987654321  987654321  987654321  987654321
    #should result in 2 & 1 being removed from the rest of the row
#    print("onlyhererow(",y,")")
    for x1 in range(0,8):                         #Compare every cell on the row
        for x2 in range(x1+1,9):                    #with every other cell on the row
#            print("x1=",x1,", x2=",x2)            #display where we are
            if board[x1+y*9]==board[x2+y*9]:      #If the values are the same
#                print("Match")
                cellvalue=board[x1+y*9]           #What is in this cell?
                if popcount[cellvalue]==2:        #and if only 2 digits are set then...
                    notthis=511-cellvalue;        #The inverse of this value
                    for x3 in range(0,9):         #Look through every cell on the row
                        if (x3!=x1) and (x3!=x2): #If the cell is not one that we are pointing at right now:
                            board[x3 + y * 9]=board[x3 + y * 9] & notthis #Strip these digits

def ruleof2col   (x, board): #Eliminate possibles where a cellpair on that col are definitely known.
    #for example:          21         21  987654321  987654321  987654321  987654321  987654321  987654321  987654321
    #should result in 2 & 1 being removed from the rest of the col
#    print("onlyherecol(",x,")")
    for y1 in range(0,8):                         #Compare every cell on the col
        for y2 in range(y1+1,9):                    #with every other cell on the col
#            print("y1=",y1,", y2=",y2)            #display where we are
            if board[x+y1*9]==board[x+y2*9]:      #If the values are the same
#                print("Match")
                cellvalue=board[x+y1*9]           #What is in this cell?
                if popcount[cellvalue]==2:        #and if only 2 digits are set then...
                    notthis=511-cellvalue;        #The inverse of this value
                    for y3 in range(0,9):         #Look through every cell on the col
                        if (y3!=y1) and (y3!=y2): #If the cell is not one that we are pointing at right now:
                            board[x + y3 * 9]=board[x + y3 * 9] & notthis #Strip these digits

#def ruleof2box   (n, board): #Eliminate possibles where a cellpair on that box are definitely known.

#def ruleof3row(y, board): continue
#def ruleof3col(x, board): continue
#def ruleof3box(n, board): continue

#def ruleof4row(y, board): continue
#def ruleof4col(x, board): continue
#def ruleof4box(n, board): continue

#def ruleof5row(y, board): continue
#def ruleof5col(x, board): continue
#def ruleof5box(n, board): continue

#def ruleof6row(y, board): continue
#def ruleof6col(x, board): continue
#def ruleof6box(n, board): continue

#def ruleof7row(y, board): continue
#def ruleof7col(x, board): continue
#def ruleof7box(n, board): continue

#def ruleof8row(y, board): continue
#def ruleof8col(x, board): continue
#def ruleof8box(n, board): continue


def onlyplacerow(y, board):           #Find if a digit is in only one row
    for bit in range(0,9):            #Look for this bit number
        val=1<<bit                    #This is the value we want to find
        count=0                       #How many have we found?
        for x in range(0,9):          #Look in every cell
            if board[x+y*9] & val>0:  #If this bit is present
                count=count+1
        if count==1:                  #If this digit is only once on this row, then it must be there!
            for x in range(0, 9):     # Look in every cell
                if board[x + y * 9] & val > 0:  # If this bit is present
                    board[x + y * 9] = val      #Scrap the other possibilities

def onlyplacecol(x, board):           #Find if a digit is in only one row
    for bit in range(0,9):            #Look for this bit number
        val=1<<bit                    #This is the value we want to find
        count=0                       #How many have we found?
        for y in range(0,9):          #Look in every cell
            if board[x+y*9] & val>0:  #If this bit is present
                count=count+1
        if count==1:                  #If this digit is only once on this row, then it must be there!
            for y in range(0, 9):     # Look in every cell
                if board[x + y * 9] & val > 0:  # If this bit is present
                    board[x + y * 9] = val      #Scrap the other possibilities

def testruleof1box(): #Test the "Rule of 1" for a box.
    resetboard(511)   #Convert everything to every possible


def main(problem):
    n=0


    print("main(problem)")     ; #print_board(board);     #initial state

    loadproblem(problem)       ; print_board(board);     #import the problem data and show it

    #Tests for each function
    testruleof1box()
#    testruleof2box()
#    testruleof3box()
#    testruleof4box()
#    testruleof5box()
#    testruleof6box()
#    testruleof7box()
#    testruleof8box()
#    testonlyplacebox()
#    testruleof1col()
#    testruleof2col()
#    testruleof3col()
#    testruleof4col()
#    testruleof5col()
#    testruleof6col()
#    testruleof7col()
#    testruleof8col()
#    testonlyplacecol()
#    testruleof1row()
#    testruleof2row()
#    testruleof3row()
#    testruleof4row()
#    testruleof5row()
#    testruleof6row()
#    testruleof7row()
#    testruleof8row()
#    testonlyplacerow()

    if 2<1:
        #resetboard(511);
        initialremovecages(problem); print_board(board);     #Remove the cage data from other rows and columns

    while len(todo)>9990:  #Whilst there are still items to process.
                         #Items are of the form Xn where X is (B)ox, (C)olumn, or (R)ow, and n is the Box, Row or Column number
        item=todo.pop()
        SetType=item[0]  #Is this a Box, Column or Row? (B, C, R)
        n      =item[1]  #Box, Column or Row number (0-8)

        print("To do ",SetType, n)

        if   SetType=='b':
            ruleof1box(n, board)
            ruleof2box(n, board)
            #ruleof3box(n, board)
            #ruleof4box(n, board)
            #ruleof5box(n, board)
            #ruleof6box(n, board)
            #ruleof7box(n, board)
            #ruleof8box(n, board)
            onlyplacebox(i,board);  # print_board(board);      #If a value can only be in one place on the row, kill it from the rest of the row.
        elif SetType=='c':
            ruleof1col(n, board);  # print_board(board);      #Eliminate possibles where a cell on that col is definitely known.
            ruleof2col(n, board);  # print_board(board);
            #ruleof3col(n, board);  # print_board(board);
            #ruleof4col(n, board);  # print_board(board);
            #ruleof5col(n, board);  # print_board(board);
            #ruleof6col(n, board);  # print_board(board);
            #ruleof7col(n, board);  # print_board(board);
            #ruleof8col(n, board);  # print_board(board);
            onlyplacecol(i,board);  # print_board(board);      #If a value can only be in one place on the row, kill it from the rest of the row.
        elif SetType=='r':
            ruleof1row(n, board);  # print_board(board);      #Eliminate possibles where a cell on that row is definitely known.
            ruleof2row(n, board);  # print_board(board);
            #ruleof3row(n, board);  # print_board(board);
            #ruleof4row(n, board);  # print_board(board);
            #ruleof5row(n, board);  # print_board(board);
            #ruleof6row(n, board);  # print_board(board);
            #ruleof7row(n, board);  # print_board(board);
            #ruleof8row(n, board);  # print_board(board);
            onlyplacerow(i,board);  # print_board(board);      #If a value can only be in one place on the row, kill it from the rest of the row.

#resetboard(511); board[30]=8; board[40]=1; board[50]=256; print_board(board)  #Test onlyhererow
        #print("ruleof1row & ruleof1col")
        #print_board(board)

        #if 2>11:
            #resetboard(511); board[0]=9; board[6]=9; board[12]=384; board[21]=384;
         #   print("ruleof2row & ruleof2col")
         #   for i in range(0,9):
         #       ruleof2col   (i, board); #print_board(board);
                #findpairsbox   (i, board)
         #   print_board(board)

#        if 2>11:
#            #resetboard(510); board[0]=511; board[9]=511; board[10]=511; board[20]=511;  #Should be able to prove that "1" only occurs in top left, forcing col and row.
#            print("onlyplacerow & fonlyplacecol")
#            for i in range(0,9):
#                onlyplacerow   (i, board); #print_board(board);      #If a value can only be in one place on the row, kill it from the rest of the row.
#                onlyplacecol   (i, board); #print_board(board);      #If a value can only be in one place on the col, kill it from the rest of the col
#                #onlyplacebox   (i, board);
#            print_board(board);


    #cleannonet (0      ); print_board(board);     #Eliminate duplicates


    bad_guess_count=0  # An appropriate number of glitches!
    #print_board(board);
    #print("BoardPopcount(board)= ",boardpopcount(board))
    print("Elapsed=", time.perf_counter()-starttime)
    if (boardpopcount(board)==81):
        print("SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS SUCCESS ")
    return board, bad_guess_count


if __name__ == '__main__':
    import problems
    test_problem = problems.problems[0][1]
    main(test_problem)
