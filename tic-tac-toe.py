# Python Tic-Tac-Toe
# By Atlinx
#
# Made on 1/11/2021 for MLH Local Hack Day

import os

piecesInLineToWin = 3
quitGame = False
spacesLeft = 0

class Error(Exception):
    pass

class InputInvalidError(Error):
    pass

class InvalidPiecePlacement(Error):
    pass

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def isPositionInBoard(position):
    return 0 <= position[0] < w and 0 <= position[1] < h

def tryPlace(position, team):
    if (not isPositionInBoard(position)) or board[position[0]][position[1]] != ' ':
        return False
    board[position[0]][position[1]] = team
    global spacesLeft
    spacesLeft -= 1
    return True

def checkForWin(position, team):
    for x in range(-1, 2):
        for y in range (-1, 2):
            if x == y == 0:
                continue
            if checkDirection(position, team, [x, y], piecesInLineToWin):
                return True
    return False

def checkDirection(position, team, xyIncrements, numberOfChecks):
    position = position[:] # Pass by value
    while numberOfChecks > 0:
        if (not isPositionInBoard(position)) or board[position[0]][position[1]] != team:
            return False
        position[0] += xyIncrements[0]
        position[1] += xyIncrements[1]
        numberOfChecks -= 1
    return True

# Prints board in ascii art in the console
def printBoard():
    widthDigits = len(str(w))

    # Generate array of padded text
    paddedLabels = [""] * w
    for x in range(w):
        paddedLabels[x] = ("{:>" + str(widthDigits) + "}").format(str(x))
    
    string = ""

    # Print padded text as vertical
    for row in range(widthDigits):
        string = " "
        for label in paddedLabels:
            string += " " + label[row]
        print(string)
    
    print()

    heightDigits = len(str(h))
    for y in range(h):
        if y > 0:
            string = " " * (heightDigits + 1)
            for x in range(w):
                string += "-" + ("+" if x < w - 1 else "")
            print(string)
        string = ("{:>" + str(heightDigits) + "}").format(str(y)) + " "
        for x in range(w):
            string += board[x][y] + ("|" if x < w - 1 else "")
        print(string)
    print()

# Application Loop
while not quitGame:
    cls()

    board = None
    inputValue = None
    w = h = 3
    currentTeam = 'O'
    winner = None

    print("Python Tic-Tac-Toe - Atlinx - MLH LHD 1/11/2021\n")

    while True:
        try:
            inputValue = input("What is the board size?\n\nFormat your response as \"width height\". Both 'width' and 'height' must each be >= 3.\nEnter nothing for a default 3x3 board.\n").split()
            if inputValue:
                w = int(inputValue[0]) 
                h = int(inputValue[1])
                if w < 3 or h < 3:
                    raise InputInvalidError
            else:
                w = h = 3
            
            board = [[' ' for x in range(h)] for y in range(w)]
            spacesLeft = h * w
            break
        except (ValueError, IndexError, InputInvalidError):
            cls()
            print("Not a valid input. Please try again.\n")
        
    cls()
    while True:
        try:
            inputValue = input("Who goes first, O or X?\n\nType either 'O' or 'X'.\nEnter nothing for O to go first\n")
            
            if not inputValue:
                currentTeam = 'O'
                break
                
            if not "OX".__contains__(inputValue[0]):
                raise InputInvalidError
            
            currentTeam = inputValue[0]
            
            break
        except (IndexError, InputInvalidError):
            cls()
            print("Not a valid input. Please try again.\n")

    cls()
    # Game Loop
    while winner == None:
        while True:
            printBoard()
            try:
                inputValue = input(currentTeam + ", enter a coordinate to place piece.\n\nFormat your response as \"row column\", where the 'row' and 'column' are based on the row and column labels on the top and left respectively\n").split()
                x = int(inputValue[0]) 
                y = int(inputValue[1])
                if not tryPlace([x, y], currentTeam):
                    raise InvalidPiecePlacement
                if spacesLeft == 0:
                    winner = 'T'
                if checkForWin([x, y], currentTeam):
                    winner = currentTeam
                break
            except (ValueError, IndexError):
                cls()
                print("Not a valid input. Please try again.\n")
            except InvalidPiecePlacement:
                cls()
                print (str(x) + ", " + str(y) + " is not a valid place for a piece. Please try again.\n")
        currentTeam = 'O' if currentTeam == 'X' else 'X'
        cls()

    printBoard()
    if winner == 'T':
        print("Uh oh, looks like there's a tie!\n")
    else:
        print("Congradulations! " + winner + " is the winner!\n")

    while True:
        try:
            inputValue = input("Play again?\n\nRespond with 'Y' for yes and 'N' for no.\n")[0].upper()
            if inputValue == 'Y':
                break
            elif inputValue == 'N':
                quitGame = True
                cls()
                break
            else:
                raise InputInvalidError
            break
        except (IndexError, InputInvalidError):
            cls()
            print("Not a valid input. Please try again.\n")
