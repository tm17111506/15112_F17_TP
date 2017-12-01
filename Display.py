from tkinter import *
from Board import *

class Display(object):
    def __init__(self):
        self.boardSize = 8
        self.boardColor = "light goldenrod"
        self.bWidth, self.bHeight = 0,0
        self.gmBoard = None
        self.inGame = False
        self.endGame = False
        self.winState = None
        self.CP = None
    
    def getCP(self, CP):
        self.CP = CP
    
    def draw(self):
        self.run()
    
    def init(self, data):
        data.margin = 30
        data.preview = False
        data.mouseX, data.mouseY = 0,0
        #Coordinates for preview rect
        data.previewX, data.previewY, data.previewR = 0,0, 15
        #Width and height of each board boxes
        self.bWidth = (data.width-2*data.margin)/self.boardSize
        self.bHeight = (data.height-2*data.margin)/self.boardSize
        
        #Draw stones
        data.dropped = False
        data.color = "white"
        data.sr = 15
    
    def restartGame(self, data):
        self.init(data)
        self.gmBoard.resetBoard()
        self.inGame = False
        self.endGame = False
    
    def mousePressed(self, event, data):
        data.mouseX = event.x
        data.mouseY = event.y
        self.findRange(data)
        self.gmBoard.legalBoard()
        if data.dropped == True:
            self.gmBoard.updateCPState(self.CP)
            if data.color == "white": self.CP.get_play()
            
        
    def keyPressed(self, event, data):
        if not self.endGame and event.keysym == 's':
            self.inGame = True
            self.endGame = False
        if event.keysym == 'r':
            self.restartGame(data)
        if event.keysym == 'Return':
            self.winState = self.gmBoard.determineScore()
            self.endGame = True
            self.inGame = False
    
    def timerFired(self, data):
        pass        
    
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
        # if data.previewX == px and data.previewY == py and \
        #         self.gmBoard.isMoveLegal(mx, my, data.color):
            data.dropped=True
            #Flips the color after isMoveLegal is checked
            data.color = "white" if data.color == "black" else "black"
            self.gmBoard.add(mx, my, data.color)
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
    
    def drawStartScreen(self, canvas, data):
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
    
    def drawEndScreen(self, canvas, data):
        blackScore, whiteScore, win = self.winState
        margin = 50
        canvas.create_text(data.width/2, data.height/2-margin*2, text = "Game Over!",
                            font="Helvetica 26 bold")
        canvas.create_text(data.width/2, data.height/2-margin, text = "%s wins!"%win,
                            font="Helvetica 20 bold")
        canvas.create_text(data.width/2, data.height/2, text = "Black Score: %d"%blackScore,
                            font="Helvetica 10 bold")
        canvas.create_text(data.width/2, data.height/2+margin/2, text = "White Score: %d"%whiteScore,
                            font="Helvetica 10 bold")
    
    def redrawAll(self, canvas, data):
        if not self.inGame:
            if self.endGame: self.drawEndScreen(canvas, data)
            else: self.drawStartScreen(canvas, data)
        elif self.endGame:
            self.drawEndScreen(canvas, data)
        else:
            self.drawBoard(canvas, data)
            self.drawStone(canvas, data)
            if not data.dropped: self.drawPreview(canvas, data)
       
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