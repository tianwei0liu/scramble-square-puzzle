import sys

tileList = []

def valueof(a_square):
    """return the value of a square"""
    return a_square[0]

def tilesof(a_square):
    """return the tiles of a square"""
    return a_square[1]

def rotate(a_square):
    """rotate the input square for 90 degrees counter-clockwise and return it"""
    copy = a_square
    tiles = copy[1]
    tiles = tiles[1:] + [tiles[0]]
    copy[1] = tiles
    return copy

def tile_match(tileA,tileB):
    """return true if the two tiles matches; false otherwise"""
    if tileA[0] == tileB[0] and (1 - (ord(tileA[1]) - 48)) == ord(tileB[1]) - 48:
        return True
    else:
        return False

def square_match(temp, a_square):
    """return true if we can add the square; false otherwise"""
    if len(temp) == 0:
        return True
    else:
        if len(temp) == 1 or len(temp) == 2:
            squareA = temp[-1]
            tilesA = tilesof(squareA)
            tilesB = tilesof(a_square)
            if tile_match(tilesA[1], tilesB[3]):
                return True
            else:
                return False
        elif len(temp) == 3 or len(temp) == 6:
            squareA = temp[-3]
            tilesA = tilesof(squareA)
            tilesB = tilesof(a_square)
            if tile_match(tilesA[2],tilesB[0]):
                return True
            else:
                return False
        elif len(temp) == 4 or len(temp) == 5 or len(temp) == 7 or len(temp) == 8:
            squareUp = temp[-3]
            squareLeft = temp[-1]
            tilesUp = tilesof(squareUp)
            tilesLeft = tilesof(squareLeft)
            tilesB = tilesof(a_square)
            if tile_match(tilesUp[2],tilesB[0]) and tile_match(tilesLeft[1],tilesB[3]):
                return True
            else:
                return False
        return False

def stack_find(stack, elem, stack_order):
    """return the index of the elem in the stack(list) if found;
    if not return -1."""
    i = len(stack_order) - 1
    if len(stack_order) != len(stack):
        print("NotOK")
    while i >= 0 and stack_order[i] == 0:
        if stack[i] == elem:
            return i
            break
        i -= 1
    return -1

def stack_delete(stack, i):
    """delete the elem at positon i in the stack, and return the stack afterward"""
    if i >= 0:
        return stack[:i] + stack[i+1:]
    else:
        return stack

def create_rotation(squares):
    """create all the rotations of a squares"""
    result = []
    rotation = []
    for i in range(0,9):
        rotation = squares[i]
        for j in range(0,4):
            result = result + [rotation[::]]
            rotation = rotate(rotation)
    return result

def val_min(sq1, sq2, sq3, sq4):
    """return the min value of the four input squares"""
    i = min(valueof(sq1), valueof(sq2), valueof(sq3), valueof(sq4))
    return i

def DF_search(squares):
    """implement DFS to find all the unique solutions to the puzzle."""
    number = 0
    stack = [] 
    stack_order = []

    temp = [] 
    result = []
    rotations = create_rotation(squares)
    used = [False] * 9
    for l in range(0,9):
        for r in range(0,4):
            stack = [rotations[4*l+r]] + stack
            stack_order = [len(temp)] + stack_order
    while stack != [] and stack_order != []:
        if len(temp) <= stack_order[0]:
            a_square = stack[0]
            stack = stack[1:]
            stack_order = stack_order[1:]                
            used[valueof(a_square) - 1] = True
            temp = temp + [a_square]
            if len(temp) == 9:
                min_val = val_min(temp[0],temp[2],temp[6],temp[8])
                if min_val == valueof(temp[0]):
                    result = [temp] + result
                    i_2 = stack_find(stack, rotate(temp[2]), stack_order)
                    stack = stack_delete(stack, i_2)
                    stack_order = stack_delete(stack_order, i_2)
                    i_3 = stack_find(stack, rotate(rotate(rotate(temp[6]))), stack_order)
                    stack = stack_delete(stack, i_3)
                    stack_order = stack_delete(stack_order, i_3)
                    i_4 = stack_find(stack, rotate(rotate(temp[8])), stack_order)
                    stack = stack_delete(stack, i_4)
                    stack_order = stack_delete(stack_order, i_4)
            for x in range(0,9):
                if used[x] == False:
                    for y in range(0,4):
                        if square_match(temp, rotations[4 * x + y]):
                            stack = [rotations[4 * x + y]] + stack
                            stack_order = [len(temp)] + stack_order
        else:
            used[valueof(temp[-1]) - 1] = False
            temp = temp[:-1]
    return result
	
def printPuzzle(arrayOfTiles):
   """takes in a list of 9 tiles and prints them in ASCII output"""
   x = 0
   while (x < 9):
      print('+--------+--------+--------+')
      print('|' + str(arrayOfTiles[x][0]) + '  ' + str(arrayOfTiles[x][1][0]) + '   |' \
                + str(arrayOfTiles[x+1][0]) + '  ' + str(arrayOfTiles[x+1][1][0]) + '   |' \
                + str(arrayOfTiles[x+2][0]) + '  ' + str(arrayOfTiles[x+2][1][0]) + '   |')
      print('|' + str(arrayOfTiles[x][1][3]) + '    ' + str(arrayOfTiles[x][1][1]) + '|' \
                + str(arrayOfTiles[x+1][1][3]) + '    ' + str(arrayOfTiles[x+1][1][1]) + '|' \
                + str(arrayOfTiles[x+2][1][3]) + '    ' + str(arrayOfTiles[x+2][1][1]) + '|')
      print('|' + '   ' + str(arrayOfTiles[x][1][2]) + '   |   ' \
                        + str(arrayOfTiles[x+1][1][2]) + '   |   ' \
                        + str(arrayOfTiles[x+2][1][2]) + '   |')
      x = x + 3
   print('+--------+--------+--------+')
	
def main():
   """reads from a file given as a command-line arg and parses the tiles,
   making a list of 9 tiles, calls the DFS function, and then prints the result"""
   filename = str(sys.argv[1])
   filestring = open(filename,'r')
   print("Input tiles:")
   for line in filestring:
     line = line.strip('\n')
     line = line.strip('\r')
     tileList.append(line.split(','))
   id = 1
   for i in tileList:
     print(str(id) + '. <' + str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + ', ' + str(i[3]) + '>')
     tempList = i
     tileList[id-1] = []
     tileList[id-1] = [id, tempList]
     id = id + 1
   result = DF_search(tileList)
   if len(result) == 1:
     print("\n" + str(len(result)) + " unique solution found:")
   elif len(result) == 0:
     print("\n" + "No solution found.")
   else:
     print("\n" + str(len(result)) + " unique solutions found:")
   j = 0
   while (j < len(result)):
     printPuzzle(result[j])
     print("")
     j = j + 1

if __name__ == "__main__":
   main()
