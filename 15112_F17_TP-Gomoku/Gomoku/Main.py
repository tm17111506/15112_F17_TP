###########################################################################
# 15112 F17 Term Project
# Go...Moku Game!
# Tiffany Ma
# Section M

# This is a program that includes 2 games: Go and Gomoku
# Go and Gomoku uses a similar form of board play
# In this program, you will be able to choose whether you want a 1 player
# or 2 player game. 
# Go is available in 1 player, Gomoku is available in both 1 and 2 player
# Ctrl+Shift+E to Run Game
###########################################################################

from Display import*
from Board import*

# Board size is set to optimize possible play and calculation speed of Gomoku AI
boardSize = 11
b = Board(boardSize)
d = Display(boardSize-1)
d.gmBoard = b

def main():
    d.draw()
    
if __name__ == '__main__':
    main()