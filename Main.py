from CP import*
from Display import*
from Board import*

'''
File organization:
- Display takes all canvas actions 
- Board is the main class that runs the calculations of score / position of the Go Board
- CP means computer player, now it contains the structure of the Monte Carlo Search Tree
    - Will be filled in with current player and next state determinations
'''

b = Board(5)
d = Display()
d.gmBoard = b
cpB = CPBoard(b)
mc = MonteCarlo(cpB, time=15, max_moves=20)
d.getCP(mc)

def main():
    d.draw()
    
#Not sure how the main works
if __name__ == '__main__':
    main()