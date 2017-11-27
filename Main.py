from Display import*
from Board import*

b = Board(9)
d = Display()
d.gmBoard = b

def main():
    d.draw()
    
#Not sure how the main works
if __name__ == '__main__':
    main()