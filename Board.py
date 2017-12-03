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
    
    def add(self, row, col, color):
        self.stoneL.append((row, col))
        self.board[row][col] = color
        self.currPlayer = color
    
    def remove(self, row, col):
        self.board[row][col] = None
        self.stoneL.remove((row, col))
    
    def getBoard(self):
        return self.board
    
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
                    #c = "black" if self.board[i[0]][i[1]] == "white" else "white"
                    #self.score[c] += 1
                    self.remove(i[0], i[1])
                self.captured = set()
    
    def resetBoard(self):
        l = [None for i in range(self.size)]
        self.board = [copy.deepcopy(l) for j in range(self.size)]
        self.resetScore()
    
    def resetScore(self):
        self.score = {"black":0, "white":0}
        self.calcualted = False

    def isMoveLegal(self, x, y, c): #C is the flipped of the visual color
        if self.board[x][y] != None: return False
        if (x-1<0 or self.board[x-1][y] == c) and (x>=self.size or self.board[x+1][y]== c) \
            and (y-1<0 or self.board[x][y-1] == c) and (y>=self.size or self.board[x][y+1] == c):
                return False
        return True
    
    def determineScore(self):
        if not self.calcualted:
            bSet, wSet = set(), set()
            #Number of stones on the board
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] != None:
                        self.score[self.board[row][col]] += 1
                    else: #If == None
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
    
    def updateCPState(self, CP):
        state = [(i[0], i[1], self.board[i[0]][i[1]]) for i in self.stoneL]
        CP.update(state)
    
    def calcCPScore(self, step):
        row, col, color = step
        self.add(row, col, color)
        self.legalBoard()
        
    
    
        