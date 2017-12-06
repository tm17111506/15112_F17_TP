from Display import*
from Board import*

boardSize = 11
b = Board(boardSize)
d = Display(boardSize-1)
d.gmBoard = b

def main():
    d.draw()
    
#Not sure how the main works
if __name__ == '__main__':
    main()