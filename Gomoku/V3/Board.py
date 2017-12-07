import copy
 
class Board(object):
    def __init__(self, boardSize):
        self.size = boardSize
        l = [None for i in range(self.size)]
        self.board = [copy.deepcopy(l) for j in range(self.size)]
        self.captured = set()
        self.surrounded = {"black":set(), "white":set()}
        self.score = {"black":0, "white":0}
        self.calcualted=False
        self.stoneL = []
        self.currPlayer = "black"
        self.gomokuWinLength = 5
        self.winner=None
    
    def add(self, row, col, color):
        self.stoneL.append((row, col))
        self.board[row][col] = color
        self.currPlayer = color
    
    def remove(self, row, col):
        self.board[row][col] = None
        self.stoneL.remove((row, col))
    
    def getBoard(self):
        return self.board
    
    def setBoard(self, b):
        self.board = b
    
    def checkSurrounded(self, x, y, color, l=None):
        if l == None: 
            l = set()
        if x<0 or x >= self.size or y < 0 or y >= self.size:
            return True
        if self.board[x][y] == color: return True
        if (x,y) in l:
            return True
        if self.board[x][y] != color and self.board[x][y] != None:
            return False
        else:
            l.add((x,y))
            solution = self.checkSurrounded(x, y-1, color, l) and \
                        self.checkSurrounded(x, y+1, color, l) and \
                        self.checkSurrounded(x-1, y, color, l) and \
                        self.checkSurrounded(x+1, y, color, l)
            if solution:
                self.surrounded[color] = l
                return True
            self.surrounded[color] = set()
            return False
    
    #x, y coordinate
    def checkCaptured(self, x, y, color, l=None):
        if l == None: l = set()
        if x<0 or x >= self.size or y < 0 or y >= self.size:
            return True
        if self.board[x][y] == None:
            return False
        if self.board[x][y] != color:
            return True
        if (x,y) in l:
            return True
        else:
            l.add((x,y))
            solution = self.checkCaptured(x, y-1, color, l) and \
                        self.checkCaptured(x, y+1, color, l) and \
                        self.checkCaptured(x-1, y, color, l) and \
                        self.checkCaptured(x+1, y, color, l)
            if solution: 
                self.captured = l
                return True
            else:
                self.captured = set()
                return False
    
    def checkCapturedCP(self, stateL):
        capturedL = set()
        for state in stateL:
            row, col, color = state
            self.add(row, col, color)
            self.checkCaptured(row, col, color)
            if self.captured != set():
                capturedL.update(self.captured)
                self.captured = set()
        return capturedL
    
    def legalBoard(self):
        for stone in self.stoneL:
            row, col = stone[0], stone[1]
            self.checkCaptured(row, col, self.board[row][col])
            if self.captured != set():
                for i in self.captured:
                    c = "black" if self.board[i[0]][i[1]] == "white" else "white"
                    self.score[c] += 1
                    self.remove(i[0], i[1])
                self.captured = set()
    
    def resetBoard(self):
        l = [None for i in range(self.size)]
        self.board = [copy.deepcopy(l) for j in range(self.size)]
        self.resetScore()
    
    def resetScore(self):
        self.score = {"black":0, "white":0}
        self.calcualted = False
        self.winner = None
    
    def checkPosXScore(self):
        startPos1 = (0,4)
        startPos2 = (6,10)
        midPos1, midPos2 = (4,6), (6,4)
        for i in range(self.size//2+1):
            pos1 = (startPos1[0], startPos1[1]+i)
            pos2 = (startPos2[0]-i, startPos2[1])
            for j in range(i+1):
                l_1 = [self.board[pos1[0]+n+j][pos1[1]-n-j] for n in range(self.gomokuWinLength)]
                l_2 = [self.board[pos2[0]+n+j][pos2[1]-n-j] for n in range(self.gomokuWinLength)]
                if None not in l_1:
                    if "black" not in l_1:
                        self.winner = "white"
                        return True
                    if "white" not in l_1:
                        self.winner = "black"
                        return True
                if None not in l_2:
                    if "black" not in l_2:
                        self.winner = "white"
                        return True
                    if "white" not in l_2:
                        self.winner = "black"
                        return True
        if self.board[midPos1[0]][midPos1[1]] != None or self.board[midPos2[0]][midPos2[1]] != None:
            for k in range(self.size//2+1):
                pos=(self.size-1-k, k)
                l=[self.board[pos[0]-n][pos[1]+n] for n in range(self.gomokuWinLength)]
                if None not in l:
                    if "black" not in l:
                        self.winner = "white"
                        return True
                    if "white" not in l:
                        self.winner = "black"
                        return True
        return False
                
    def checkNegXScore(self):
        startPos1 = (0,6)
        startPos2 = (6,0)
        midPos1, midPos2 = (4,4), (6,6)
        for i in range(self.size//2+1):
            pos1 = (startPos1[0], startPos1[1]-i)
            pos2 = (startPos2[0]-i, startPos2[1])
            for j in range(i+1):
                l_1 = [self.board[pos1[0]+n+j][pos1[1]+n+j] for n in range(self.gomokuWinLength)]
                l_2 = [self.board[pos2[0]+n+j][pos2[1]+n+j] for n in range(self.gomokuWinLength)]
                if None not in l_1:
                    if "black" not in l_1:
                        self.winner = "white"
                        return True
                    if "white" not in l_1:
                        self.winner = "black"
                        return True
                if None not in l_2:
                    if "black" not in l_2:
                        self.winner = "white"
                        return True
                    if "white" not in l_2:
                        self.winner = "black"
                        return True
        return False
    
    def checkVertScore(self):
        midPos = (4,6)
        for col in range(len(self.board[0])):
            if self.board[midPos[0]][col] == None or \
                self.board[midPos[1]][col] == None:
                    continue
            for i in range(len(self.board)-self.gomokuWinLength+1):
                l = []
                l=[self.board[i+j][col] for j in range(self.gomokuWinLength)]
                if None not in l:
                    if "black" not in l:
                        self.winner = "white"
                        return True
                    if "white" not in l:
                        self.winner = "black"
                        return True
        return False
        
    def checkHorzScore(self):
        midPos = (4,6)
        for row in range(len(self.board)):
            if self.board[row][midPos[0]] == None or \
                self.board[row][midPos[1]] == None:
                    continue
            for i in range(len(self.board)-self.gomokuWinLength+1):
                if None not in self.board[row][i:i+self.gomokuWinLength]:
                    if "black" not in self.board[row][i:i+self.gomokuWinLength]:
                        self.winner = "white"
                        return True
                    if "white" not in self.board[row][i:i+self.gomokuWinLength]:
                        self.winner = "black"
                        return True
        return False
    
    def determineGomokuScore(self):
        self.checkPosXScore()
        self.checkNegXScore()
        self.checkVertScore()
        self.checkHorzScore()
        return self.winner
    
    def determineGoScore(self):
        if not self.calcualted:
            bSet, wSet = set(), set()
            #Number of stones on the board
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] != None:
                        self.score[self.board[row][col]] += 1
                    elif self.countNone() < 120: #If == None
                        self.checkSurrounded(row, col, "black")
                        b = self.surrounded["black"]
                        self.checkSurrounded(row, col, "white")
                        w = self.surrounded["white"]
                        if b != set(): bSet = bSet.union(b)
                        if w != set(): wSet = wSet.union(w)
            self.score["black"] += len(bSet)
            self.score["white"] += len(wSet)
            self.calcualted=True
            
        win = None
        if self.score["black"] > self.score["white"]: win = "black"
        elif self.score["black"] < self.score["white"]: win = "white"
        else: win = None
        return (self.score["black"], self.score["white"], win)
    
    def checkEndGameGo(self):
        numNone = self.countNone()
        if numNone <= self.size**2 * 0.15:
            return True
        return False
    
    def checkEndGameGomoku(self):
        if self.determineGomokuScore() != None:
            return True
        return False
    
    def countNone(self):
        num = 0
        for l in self.board:
            for elem in l:
                if elem == None: num += 1
        return num