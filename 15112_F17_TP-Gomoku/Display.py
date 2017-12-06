from tkinter import *

class Display(object):
    def __init__(self):
        self.boardSize = 8 #(9-1 since starts at 0)
        self.boardColor = "light goldenrod"
        self.bWidth, self.bHeight = 0,0
        self.stoneList = []
    
    def draw(self):
        self.run()
    
    def init(self, data):
        data.margin = 30
        data.preview = False
        data.mouseX, data.mouseY = 0,0
        data.previewX, data.previewY, data.previewR = 0,0, 15
        self.bWidth = (data.width-2*data.margin)/self.boardSize
        self.bHeight = (data.height-2*data.margin)/self.boardSize
        
        #Draw stones
        data.dropped = False
        data.color = "black"
        data.sr = 15
        
    def mousePressed(self, event, data):
        data.mouseX = event.x
        data.mouseY = event.y
        self.findRange(data)
        
    def keyPressed(self, event, data):
        pass
    
    def timerFired(self, data):
        pass        
    
    def findRange(self, data):
        mx, my = 0,0
        if (data.mouseX-data.margin)%self.bWidth <= self.bWidth/2:
            mx = (data.mouseX-data.margin)//self.bWidth
        else: 
            mx = ((data.mouseX-data.margin)//self.bWidth) + 1
        
        if (data.mouseY-data.margin)%self.bHeight <= self.bHeight/2:
            my = (data.mouseY-data.margin)//self.bHeight
        else: 
            my = ((data.mouseY-data.margin)//self.bHeight) + 1
        
        px = mx*self.bWidth + data.margin
        py = my*self.bHeight + data.margin
        
        if data.previewX == px and data.previewY == py:
            data.dropped=True
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
        for stone in self.stoneList:
            canvas.create_oval(stone[0]-data.sr, stone[1]-data.sr,
                                stone[0]+data.sr, stone[1]+data.sr,
                                fill = stone[2])
    
    def drawBoard(self, canvas, data):
        dy = self.bHeight
        dx = self.bWidth
        for i in range(self.boardSize+1):
            canvas.create_line(data.margin, data.margin+i*dy, 
                                data.width-data.margin, data.margin+i*dy)
            canvas.create_line(data.margin+i*dx, data.margin, 
                                data.margin+i*dx, data.height-data.margin)
    
    def redrawAll(self, canvas, data):
        self.drawBoard(canvas, data)
        self.drawStone(canvas, data)
        if data.dropped:
            self.stoneList.append((data.previewX, data.previewY, data.color))
        else: self.drawPreview(canvas, data)
       
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

d = Display()
d.draw()