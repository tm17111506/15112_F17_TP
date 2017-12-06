board=[ [  "white",  None,  None,  None,  None,  None,  None,  None,  None,  None,  None ],
        [  None,  "white",  None,  None,  None,  None,  None,  None,  None,  None,  None ],
        [  None,  None,  "white",  None,  None,  None,  None,  None,  None,  None,  None ],
        [  None,  None,  None,  "white",  None,  None,  None,  None,  None,  None,  None ],
        [  None,  None,  None,  None,  "white",  None,  None,  None,  None,  None,  None ],
        [  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None ],
        [  None,  None,  None,  None,  "white",  None,  None,  None,  None,  None,  None ],
        [  None,  None,  None,  "white",  None,  None,  None,  None,  None,  None,  None ],
        [  None,  None,  "white",  None,  None,  None,  None,  None,  None,  None,  None ],
        [  None,  "white",  None,  None,  None,  None,  None,  None,  None,  None,  None ],
        [  "white",  None,  None,  None,  None,  None,  None,  None,  None,  None,  None ]]

winner = 0
gomokuWinLength = 5
size = 11
boardSize = 11
def checkNegXScore():
    startPos1 = (0,6)
    startPos2 = (6,0)
    midPos1, midPos2 = (4,4), (6,6)
    for i in range(size//2+1):
        pos1 = (startPos1[0], startPos1[1]-i)
        pos2 = (startPos2[0]-i, startPos2[1])
        for j in range(i+1):
            l_2=[]
            l_1=[]
            for n in range(gomokuWinLength):
                l_1.append(board[pos1[0]+n+j][pos1[1]+n+j])
                l_2.append(board[pos2[0]+n+j][pos2[1]+n+j])
            if None not in l_1:
                if "black" not in l_1:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l_1:
                    winner = "black"
                    print(winner)
                    return True
            if None not in l_2:
                if "black" not in l_2:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l_2:
                    winner = "black"
                    print(winner)
                    return True
                    
    if board[midPos1[0]][midPos1[1]] != None or board[midPos2[0]][midPos2[1]] != None:
        for i in range(boardSize//2+1):
            pos = (i, i)
            l = [board[pos[0]+n][pos[1]+n] for n in range(gomokuWinLength)]
            if None not in l:
                if "black" not in l:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l:
                    winner = "black"
                    print(winner)
                    return True
    return False

def checkVertScore():
    midPos = (4,6)
    for col in range(len(board[0])):
        if board[midPos[0]][col] == None or \
            board[midPos[1]][col] == None:
                continue
        for i in range(len(board)-gomokuWinLength+1):
            l = []
            l=[board[i+j][col] for j in range(gomokuWinLength)]
            if None not in l:
                if "black" not in l:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l:
                    winner = "black"
                    print(winner)
                    return True
    return False
    
def checkHorzScore():
    midPos = (4,6)
    for row in range(len(board)):
        if board[row][midPos[0]] == None or \
            board[row][midPos[1]] == None:
                continue
        for i in range(len(board)-gomokuWinLength+1):
            if None not in board[row][i:i+gomokuWinLength]:
                if "black" not in board[row][i:i+gomokuWinLength]:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in board[row][i:i+gomokuWinLength]:
                    winner = "black"
                    print(winner)
                    return True
    return False

def checkPosXScore():
    startPos1 = (0,4)
    startPos2 = (6,10)
    midPos1, midPos2 = (4,6), (6,4)
    for i in range(size//2+1):
        pos1 = (startPos1[0], startPos1[1]+i)
        pos2 = (startPos2[0]-i, startPos2[1])
        for j in range(i+1):
            l_1 = [board[pos1[0]+n+j][pos1[1]-n-j] for n in range(gomokuWinLength)]
            l_2 = [board[pos2[0]+n+j][pos2[1]-n-j] for n in range(gomokuWinLength)]
            if None not in l_1:
                if "black" not in l_1:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l_1:
                    winner = "black"
                    print(winner)
                    return True
            if None not in l_2:
                if "black" not in l_2:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l_2:
                    winner = "black"
                    print(winner)
                    return True
                    
    if board[midPos1[0]][midPos2[1]] != None or board[midPos2[0]][midPos2[1]] != None:
        for i in range(boardSize//2+1):
            pos = (boardSize-1-i, i)
            print(pos)
            l=[]
            for n in range(gomokuWinLength):
                l.append(board[pos[0]-n][pos[1]+n])
            print(l)
            if None not in l:
                if "black" not in l:
                    winner = "white"
                    print(winner)
                    return True
                if "white" not in l:
                    winner = "black"
                    print(winner)
                    return True
    return False

def determineGomokuScore():
    checkPosXScore()
    checkNegXScore()
    checkVertScore()
    checkHorzScore()
    return winner

print(determineGomokuScore())