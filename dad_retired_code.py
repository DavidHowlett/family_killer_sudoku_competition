"""
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

    for boxy in range(0,3):
        for boxx in range(0, 3):
            for y in range(0, 3):
                for x in range(0,3):
                    boxtoboard.append((boxx*3)+(boxy*27)+x+y*9)
    print(boxtoboard)


print("binarytodecimal=",binarytodecimal)
print("decimaltobinary=",decimaltobinary)
print("popcount=",popcount)
print("binarytodisplay=",binarytodisplay)

------------------------------------------------------------------------------------------------------------------------
#Buildsets
for n in range(0,9): #Rows
    sets.append([])
    for i in range(0,9):
        sets[n].append(n*9+i)
for n in range(0,9): #Cols
    sets.append([])
    for i in range(0,9):
        sets[n+9].append(n+i*9)
for boxy in range(0, 3):
    for boxx in range(0, 3):
        sets.append([])
        for y in range(0, 3):
            for x in range(0, 3):
                sets[boxy*3+boxx+18].append((boxx * 3) + (boxy * 27) + x + y * 9)
print(sets)

def ruleof1nonet(n): #Eliminate possibles from other cells where one cell on that nonet is definitely known.
    #print("ruleof1nonet(",n,")")

    singles=0  #We know no values for sure
    for n1 in range(0,9): #Look at every cell for single values
        if popcount[board[nonettoboard[n*9+n1]]]==1:
            singles=singles or board[nonettoboard[n*9+n1]]         #Just in case we have an error with 2 cells having the same value. Avoid the error getting more complicated!
    notsingles=511-singles    #Find every unknown value
    for n1 in range(0,9): #Look at every cell for single values
        if popcount[board[nonettoboard[n*9+n1]]]!=1:
            board[nonettoboard[n*9+n1]]=board[nonettoboard[n*9+n1]] & notsingles  #Wipe out the values we clearly know

def ruleof2nonet(n): #Eliminate possibles where a cellpair in that nonet are definitely known.
    #for example:         3 1  987654321  987654321
    #               987654321        3 1  987654321
    #               987654321  987654321  987654321
    #should result in 3 & 1 being removed from the rest of the nonet:
    #for example:         3 1  987654 2   987654 2
    #               987654 2         3 1  987654 2
    #               987654 2   987654 2   987654 2
    #    print("ruleof2nonet(",n,")")
    for n1 in range(0,8):                         #Compare every cell on the row
        cellvalue = board[nonettoboard[n * 9 + n1]]  # What is in this cell?
        if popcount[cellvalue] == 2:  # and if only 2 digits are set then...
            for n2 in range(n1+1,9):                  #with every other cell on the row
#               print("n1=",n1,", n2=",n2)           #display where we are
                if cellvalue==board[nonettoboard[n*9+n2]]:  #If the values are the same
#                   print("Match")
                    notthis=511-cellvalue;        #The inverse of this value
                    for nn in range(0,9):         #Look through every cell on the nonet
                        if (nn!=n1) and (nn!=n2): #If the cell is not one that we are pointing at right now:
                            board[nonettoboard[n*9+nn]]=board[nonettoboard[n*9+nn]] & notthis #Strip these digits

def ruleof3nonet(n): #Eliminate possibles where a celltriple in that nonet are definitely known.
    #for example:      6  3 1  987654321  987654321
    #               987654321     6  3 1  987654321
    #                  6  3 1  987654321  987654321
    #should result in 3 & 1 being removed from the rest of the nonet:
    #for example:      6  3 1  987 54 2   987 54 2
    #               987 54 2      6  3 1  987 54 2
    #                  6  3 1  987 54 2   987 54 2
    #    print("onlyhererow(",y,")")
    for n1 in range(0,7):                         #Compare every cell on the row
        cellvalue = board[nonettoboard[n * 9 + n1]]  # What is in this cell?
        if popcount[cellvalue] == 3:  # and if only 3 digits are set then...
            for n2 in range(n1+1,8):                  #with every other cell on the row
                for n3 in range(n2 + 1, 9):           # with every other cell on the row
    #                print("n1=",n1,", n2=",n2,", n3=",n3)  #display where we are
                    if (cellvalue==board[nonettoboard[n*9+n2]]) and (cellvalue==board[nonettoboard[n*9+n3]]):  #If the values are the same
#                       print("Match")
                        notthis=511-cellvalue;        #The inverse of this value
                        for nn in range(0,9):          #Look through every cell on the nonet
                            if (nn!=n1) and (nn!=n2) and (nn!=n3): #If the cell is not one that we are pointing at right now:
                                board[nonettoboard[n*9+nn]]=board[nonettoboard[n*9+nn]] & notthis #Strip these digits



def testruleof1nonet(): #Test the "Rule of 1" for a nonet.
    #Try each nonet in the puzzle.
    for nonet in range(0,9):
        resetboard(511)  # set every cell to every possible value
        board[nonettoboard[nonet*9+5]]=16   #Middle cell in this nonet is now "5"
        ruleof1nonet(nonet)       #Remove "5" from every cell in that nonet
        # test that "5" has been removed from the nonet, but nowhere else
        for testnonet in range(0,9):
            for n in range(0,9):
                if (testnonet==nonet):     #If this is the nonet we want
                    if (n==5):
                        assert board[nonettoboard[testnonet*9+n]]==16 #This is the cell we pre-set
                    else:
                        assert board[nonettoboard[testnonet*9+n]]==511-16 #This is the nonet, but not the cell
                else:
                    assert board[nonettoboard[testnonet*9+n]]==511 #If this is not the nonet we are testing

def testruleof2nonet(): #Test the "Rule of 2" for a nonet. If 2 cells contain the same 2 digits, eliminate that from the rest of the cells
    #Try each nonet in the puzzle.
    for nonet in range(0,9):
        resetboard(511)  # set every cell to every possible value
        board[nonettoboard[nonet*9+ 0]]=5   #Top left cell in this nonet is now "3" or "1"
        board[nonettoboard[nonet*9+ 4]]=5   #Middle cell in this nonet is now "3" or "1"
        ruleof2nonet(nonet)                 #Remove "3" and "1" from 7 cells in that nonet
        #print_board()
        # test that "3" & "1" have been removed from the nonet, but nowhere else
        # print_board()
        for testnonet in range(0,9):
            for n in range(0,9):
               if testnonet==nonet:     #If this is the nonet we want
                    if (n==0) or (n==4):
                        assert board[nonettoboard[testnonet*9+n]]==5 #This is the cell we pre-set
                    else:
                        assert board[nonettoboard[testnonet*9+n]]==511-5 #This is the nonet, but not the cell
               else:
                    assert board[nonettoboard[testnonet*9+n]]==511 #If this is not the nonet we are testing


def testruleof3nonet():  # Test the "Rule of 3" for a nonet. If 3 cells contain the same 3 digits, eliminate that from the rest of the cells
    # Try each nonet in the puzzle.
        for nonet in range(0, 9):
            resetboard(511)  # set every cell to every possible value
            board[nonettoboard[nonet * 9 + 0]] = 13  # Top left cell in this nonet is now "4", "3" or "1"
            board[nonettoboard[nonet * 9 + 5]] = 13  # Middle cell in this nonet is now "4", "3" or "1"
            board[nonettoboard[nonet * 9 + 7]] = 13  # bottom centre cell in this nonet is now "4", "3" or "1"
            ruleof3nonet(nonet)  # Remove "4", "3" and "1" from 7 cells in that nonet
            #print_board()
            # test that "4", "3" & "1" have been removed from the nonet, but nowhere else
            # print_board()
            for testnonet in range(0, 9):
                for n in range(0, 9):
                    if testnonet == nonet:  # If this is the nonet we want
                        if (n == 0) or (n == 5) or (n==7):
                            assert board[nonettoboard[testnonet * 9 + n]]== 13  # This is the cell we pre-set
                        else:
                            assert board[nonettoboard[testnonet * 9 + n]]== 511 - 13  # This is the nonet, but not the cell
                    else:
                        assert board[nonettoboard[testnonet * 9 + n]]== 511  # If this is not the nonet we are testing

nonettoboard = [0, 1, 2, 9, 10, 11, 18, 19, 20, 3, 4, 5, 12, 13, 14, 21, 22, 23, 6, 7, 8, 15, 16, 17, 24, 25, 26, 27, 28,
              29, 36, 37, 38, 45, 46, 47, 30, 31, 32, 39, 40, 41, 48, 49, 50, 33, 34, 35, 42, 43, 44, 51, 52, 53, 54,
              55, 56, 63, 64, 65, 72, 73, 74, 57, 58, 59, 66, 67, 68, 75, 76, 77, 60, 61, 62, 69, 70, 71, 78, 79, 80]


"""

#for i in range(10):         #For up to 9 required digits
#    decimaltobinary.append([])
#    for j in range(46):        #Pre-fill the array with empty elements
#        decimaltobinary[i].append(0)
