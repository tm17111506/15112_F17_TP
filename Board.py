import copy

class Board(object):
    def __init__(self, boardSize):
        self.size = boardSize
        l = [None for i in range(self.size)]
        self.board = [copy.deepcopy(l) for j in range(self.size)]
        self.captured = set()
        self.score = {"black":0, "white":0}
        self.calcualted=False
    
    def add(self, row, col, color):
        self.board[row][col] = color
    
    def remove(self, row, col):
        self.board[row][col] = None
    
    def getBoard(self):
        return self.board
    
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
    
    def legalBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                self.checkCaptured(row, col, self.board[row][col])
                if self.captured != set():
                    for i in self.captured:
                        self.score[self.board[i[0]][i[1]]] += 1
                        self.board[i[0]][i[1]] = None
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
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] != None:
                        self.score[self.board[row][col]] += 1
            self.calcualted=True
            
        win = None
        if self.score["black"] > self.score["white"]: win = "Black"
        elif self.score["black"] < self.score["white"]: win = "White"
        else: win = None
        
        return (self.score["black"], self.score["white"], win)
    
    
        