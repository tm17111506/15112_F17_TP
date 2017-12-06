from tkinter import *
from AlphaBeta import *
from Board import *

class Display(object):
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.boardColor = "light goldenrod"
        self.bWidth, self.bHeight = 0,0
        self.gmBoard = None
        self.inGame = False
        self.endGame = False
        self.winState = None
        self.chooseNumPlayer = False
        self.numPlayer = 0
        self.gameChoice = None #(1 = Go, 2 = GoMoku)
        self.alphaBeta = AlphaBeta(boardSize, "white")
    
    def draw(self):
        self.run()
    
    def init(self, data):
        data.margin = 30
        data.preview = False
        data.mouseX, data.mouseY = 0,0
        #Coordinates for preview rect
        data.previewX, data.previewY, data.previewR = 0,0, 10
        #Width and height of each board boxes
        self.bWidth = (data.width-2*data.margin)/self.boardSize
        self.bHeight = (data.height-2*data.margin)/self.boardSize
        
        #Draw stones
        data.dropped = False
        data.color = "black"
        data.sr = 10
    
    def restartGame(self, data):
        self.init(data)
        self.gmBoard.resetBoard()
        self.inGame = False
        self.endGame = False
        self.chooseNumPlayer = False
        self.gameChoice = None
        #Define new AlphaBeta
    
    def mousePressed(self, event, data):
        data.mouseX = event.x
        data.mouseY = event.y
        self.findRange(data)
        if self.gameChoice == 1:
            self.gmBoard.legalBoard()
        
    def keyPressed(self, event, data):
        if not self.chooseNumPlayer and event.keysym == '1':
            self.chooseNumPlayer = True
            self.numPlayer = 1
        elif not self.chooseNumPlayer and event.keysym == '2':
            self.chooseNumPlayer = True
            self.numPlayer = 2
        if self.chooseNumPlayer:
            if self.numPlayer == 1:
                self.gameChoice = 2
            elif self.numPlayer == 2:
                if event.keysym == 'g':
                    self.gameChoice = 1
                if event.keysym == 'm':
                    self.gameChoice = 2
            
            if not self.endGame:
                if self.numPlayer == 1:
                    if event.keysym == 's':
                        self.inGame = True
                        self.endGame = False
                elif self.numPlayer == 2:
                    if self.gameChoice == 1: 
                        if event.keysym == 's':
                            self.inGame = True
                            self.endGame = False
                    elif self.gameChoice == 2:
                        if event.keysym == 's':
                            self.inGame = True
                            self.endGame = False
            
            if self.numPlayer == 2 and self.gameChoice == 1 and self.inGame:
                if event.keysym == 'Return':
                    self.inGame = False
                    self.endGame = True

            if event.keysym == 'r':
                self.restartGame(data)
    
    def timerFired(self, data):
        if self.gmBoard.checkEndGameGomoku():
            self.endGame = True
            self.inGame = False
            
    
    def determineWin(self, data):
        if self.gameChoice == 1 and self.endGame:
            self.winState = self.gmBoard.determineGoScore()
        elif self.gameChoice == 2 and self.endGame:
            self.winState = self.gmBoard.determineGomokuScore()
    
    def findRange(self, data):
        mx, my = 0,0
        if (data.mouseX-data.margin)%self.bWidth <= self.bWidth/2:
            mx = int((data.mouseX-data.margin)//self.bWidth)
        else: 
            mx = int(((data.mouseX-data.margin)//self.bWidth) + 1)
        
        if (data.mouseY-data.margin)%self.bHeight <= self.bHeight/2:
            my = int((data.mouseY-data.margin)//self.bHeight)
        else: 
            my = int(((data.mouseY-data.margin)//self.bHeight) + 1)
        
        px = mx*self.bWidth + data.margin
        py = my*self.bHeight + data.margin
        
        if data.previewX == px and data.previewY == py and \
            self.gmBoard.getBoard()[mx][my] == None:
            data.dropped=True
            if self.numPlayer == 1:
                if data.color == "black":
                    self.gmBoard.add(mx, my, data.color)
                    print("Starting CP")
                    newState = self.alphaBeta.alpha_beta_search(self.gmBoard.getBoard())
                    self.gmBoard.setBoard(newState)
                    print("Done")
                    #Play AlphaBeta Move of Gomoku
            else:
                self.gmBoard.add(mx, my, data.color)
                data.color = "white" if data.color == "black" else "black"
        else:
            data.dropped=False
        
        data.previewX, data.previewY = px, py
    
    def drawPreview(self, canvas, data):
        buffer=10
        r = data.previewR
        px, py = data.previewX, data.previewY
        if px > data.margin-buffer and \
            px < data.width-data.margin+buffer and \
            py > data.margin-buffer and \
            py < data.height-data.margin+buffer:
                #X-Lines
                canvas.create_line(px-r, py-r, px-r+r/2, py-r, 
                                    fill = "white", width=2)
                canvas.create_line(px+r/2, py-r, px+r, py-r,
                                    fill = "white", width=2)
                canvas.create_line(px-r, py+r, px-r+r/2, py+r,
                                    fill = "white", width=2)
                canvas.create_line(px+r/2, py+r, px+r, py+r,
                                    fill = "white", width=2)
                #Y-lines
                canvas.create_line(px-r, py+r/2, px-r, py+r,
                                    fill = "white", width=2)
                canvas.create_line(px-r, py-r, px-r, py-r/2,
                                    fill = "white", width=2)
                canvas.create_line(px+r, py+r/2, px+r, py+r,
                                    fill = "white", width=2)
                canvas.create_line(px+r, py-r, px+r, py-r/2,
                                    fill = "white", width=2)
    
    def drawStone(self, canvas, data):
        self.gmBoard.legalBoard()
        board = self.gmBoard.getBoard()
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] != None:
                    x = row*self.bWidth + data.margin
                    y = col*self.bHeight + data.margin
                    canvas.create_oval(x-data.sr, y-data.sr, x+data.sr, y+data.sr,
                                        fill = board[row][col])
        
    def drawBoard(self, canvas, data):
        dy = self.bHeight
        dx = self.bWidth
        for i in range(self.boardSize+1):
            canvas.create_line(data.margin, data.margin+i*dy, 
                                data.width-data.margin, data.margin+i*dy)
            canvas.create_line(data.margin+i*dx, data.margin, 
                                data.margin+i*dx, data.height-data.margin)
    
    def drawGoStartScreen(self, canvas, data):
        start=70
        margin = 50
        canvas.create_text(data.width/2, margin+start, text = "GO Game!",
                            font="Times 26 bold")
        canvas.create_text(data.width/2, margin*2+start, text = "Press 's' to start",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*3+start, text = "Press 'r' to restart",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*4+start, text = "Press 'Enter' to End",
                            font="Times 16")
    
    def drawGomokuStartScreen(self, canvas, data):
        start=70
        margin = 50
        canvas.create_text(data.width/2, margin+start, text = "Gomoku!",
                            font="Times 26 bold")
        canvas.create_text(data.width/2, margin*2+start, text = "Press 's' to start",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*3+start, text = "Press 'r' to restart",
                            font="Times 16")
    
    def drawUserScreen(self, canvas, data):
        start=70
        margin = 50
        canvas.create_text(data.width/2, margin+start, text = "Go...Moku Game!",
                            font="Times 26 bold")
        canvas.create_text(data.width/2, margin*2+start, text = "Choose Number of PLayers",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*3+start, text = "Press '1' for 1 player",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*4+start, text = "Press '2' for 2 player",
                            font="Times 16")
    
    def drawGoEndScreen(self, canvas, data):
        self.determineWin(data)
        blackScore, whiteScore, win = self.winState
        margin = 50
        canvas.create_text(data.width/2, data.height/2-margin*2, text = "Go Game Over!",
                            font="Helvetica 26 bold")
        canvas.create_text(data.width/2, data.height/2-margin, text = "%s wins!"%win,
                            font="Helvetica 20 bold")
        canvas.create_text(data.width/2, data.height/2, text = "Black Score: %d"%blackScore,
                            font="Helvetica 10 bold")
        canvas.create_text(data.width/2, data.height/2+margin/2, text = "White Score: %d"%whiteScore,
                            font="Helvetica 10 bold")
    
    def drawGomokuEndScreen(self, canvas, data):
        self.determineWin(data)
        win = self.winState
        margin = 50
        canvas.create_text(data.width/2, data.height/2-margin*2, text = "Gomoku Game Over!",
                            font="Helvetica 26 bold")
        canvas.create_text(data.width/2, data.height/2-margin, text = "%s wins!"%win,
                            font="Helvetica 20 bold")
    
    def drawChooseGame(self, canvas, data):
        start=70
        margin = 50
        canvas.create_text(data.width/2, margin+start, text = "Go...Moku Game!",
                            font="Times 26 bold")
        canvas.create_text(data.width/2, margin*2+start, text = "Choose which game to play",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*3+start, text = "Press 'g' for Go",
                            font="Times 16")
        canvas.create_text(data.width/2, margin*4+start, text = "Press 'm' for Gomoku",
                            font="Times 16")
    
    def redrawAll(self, canvas, data):
        if not self.chooseNumPlayer:
            self.drawUserScreen(canvas, data)
        else:
            if not self.inGame:
                if self.endGame:
                    if self.gameChoice == 1:
                        self.drawGoEndScreen(canvas, data)
                    elif self.gameChoice == 2:
                        self.drawGomokuEndScreen(canvas, data)
                else:
                    if self.numPlayer == 1:
                        self.drawGomokuStartScreen(canvas, data)
                    else:
                        if self.gameChoice == None:
                            self.drawChooseGame(canvas, data)
                        else:
                            if self.gameChoice == 1:
                                self.drawGoStartScreen(canvas, data)
                            elif self.gameChoice == 2:
                                self.drawGomokuStartScreen(canvas, data)
            else:
                self.drawBoard(canvas, data)
                self.drawStone(canvas, data)
                if not data.dropped: self.drawPreview(canvas, data)

            # if not self.inGame:
            #     if self.endGame: self.drawEndScreen(canvas, data)
            #     else: self.drawStartScreen(canvas, data)
            # elif self.endGame:
            #     self.drawEndScreen(canvas, data)
       
    def run(self, width=400, height=400):
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill=self.boardColor, width=0)
            self.redrawAll(canvas, data)
            canvas.update()    
    
        def mousePressedWrapper(event, canvas, data):
            self.mousePressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def keyPressedWrapper(event, canvas, data):
            self.keyPressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def timerFiredWrapper(canvas, data):
            self.timerFired(data)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        # Set up data and call init
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 100 # milliseconds
        self.init(data)
        # create the root and the canvas
        root = Tk()
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")