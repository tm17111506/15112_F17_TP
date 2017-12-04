import random
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

def legal_plays (fullPos, sList):
    currSet = set()
    for item in sList:
        currSet.add((item[0], item[1]))
    legalPlay = fullPos - currSet
    return legalPlay

def test():
    for i in range(2):
        color = "black"
        whiteTurn, blackTurn = 0,0
        b = Board(5)
        cpB = CPBoard(b)
        mc = MonteCarlo(cpB, time=15, max_moves=10)
        fullPos = []
        for i in range(5):
            for j in range(5):
                fullPos.append((i, j))
        fullPos = set(fullPos)
        while not b.checkEndGame():
            if color == "black":
                blackTurn +=1
                bList = list(legal_plays(fullPos, b.stoneL))
                bMove = choice(bList)
                b.add(bMove[0], bMove[1], color)
            else:
                whiteTurn += 1
                b.updateCPState(mc)
                wMove = mc.get_play()
                b.add(wMove[0], wMove[1], color)
            b.legalBoard()
            color = "white" if color == "black" else "black"
        print(blackTurn, whiteTurn, b.getBoard())

def main():
    test()
    
if __name__ == '__main__':
    main()