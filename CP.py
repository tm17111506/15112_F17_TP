from __future__ import division
import datetime
from random import choice
from math import log, sqrt
import os
from Board import*

'''
https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
'''

#Decide what is a state!! (single position, or full board, what happens when branching out)
class CPBoard(object):
    def __init__(self, board):
        self.board = board
        self.fullPos = []
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.fullPos.append((i, j))
        self.fullPos = set(self.fullPos)

    def start(self):
        # Returns a representation of the starting state of the game.
        pass
    
    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        r, c, color = state[-1]
        currPlayer = "black" if color == "white" else "white"
        return currPlayer

    def next_state(self, state, play, currPlayer):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        nState = state[:]
        if not isinstance(nState, list): nState = list(nState)
        nState.append((play[0], play[1], currPlayer))
        newState = self.checkCaptured(nState[:])
        return newState

    def legal_plays(self, state_history, prevMove = (-1,-1)):
        currSet = set()
        for item in state_history[-1]:
            currSet.add((item[0], item[1]))
        legalPlay = self.fullPos - currSet
        if prevMove in legalPlay: legalPlay.discard(prevMove)
        return legalPlay
        
    def winner(self, state_history):     
        #Create a new Board instance, add the elements in the latest state
        #Calls calcCPScore, and then determineScore at when all elements are added
        b = Board(self.board.size)
        state = state_history[-1]
        for step in state:
            b.calcCPScore(step)
        
        blackScore, whiteScore, winner = b.determineScore()
        return winner
    
    def removeFromState(self, capList, state):
        if capList == set():
            return state
        else:
            for elem in state:
                if (elem[0], elem[1]) in capList:
                    state.remove(elem)
            return state
    
    def checkCaptured(self, state):
        b = Board(self.board.size)
        capturedList = b.checkCapturedCP(state)
        return self.removeFromState(capturedList, state)
            
class MonteCarlo(object):
    def __init__(self, cpboard, **kwargs):
        self.C = 1.41
        self.cpboard = cpboard
        self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 10)
        
        #Stats
        self.wins={}
        self.plays={}
        self.readData()
        self.prevMove = (-1,-1)
        self.empBoard = self.emptyBoard()

    def readFile(self, path):
        with open(path, "rt") as f:
            return f.read()
    
    def writeFile(self, path, contents):
        with open(path, "wt") as f:
            f.write(contents)
        
    def readData(self):
        winsData = self.readFile("Winner_Dictionary.txt").splitlines()
        playsData = self.readFile("Player_Dictionary.txt").splitlines()
        if len(winsData) != 0:
            for i in range(0,len(winsData),2):
                self.wins[(winsData[i])] = int(winsData[i+1])
        if len(playsData) != 0:
            for j in range(0,len(playsData),2):
                self.plays[(playsData[j])] = int(playsData[j+1])
        
    def writesData(self):
        winsData, playsData = [], []
        for wKey in self.wins:
            winsData.append(str(wKey))
            winsData.append(str(self.wins[wKey]))
        for pKey in self.plays:
            playsData.append(str(pKey))
            playsData.append(str(self.plays[pKey]))
        
        winsData = "\n".join(winsData)
        playsData = "\n".join(playsData)
        
        self.writeFile("Winner_Dictionary.txt", winsData)
        self.writeFile("Player_Dictionary.txt", playsData)
        
        # os.close("Winner_Dictionary.txt")
        # os.close("Player_Dictionoary.txt")
        
    def update(self, state):
        self.states.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        print("Start CP")
        state = self.states[-1]

        player = self.cpboard.current_player(state)
        legal = self.cpboard.legal_plays(self.states[:], self.prevMove)
        
        if legal == []: return None
        if len(legal) == 1: return legal
        
        games = 0
        begin = datetime.datetime.utcnow()
        #self.run_simulation()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1
        
        self.writesData()
        
        moves_states = [(m, self.cpboard.next_state(state, m, player)) for m in legal]
        #p is the next state to move to, S is the state simulated / ran
        moveInPlay = self.formatMoveStates(moves_states[:])
        print(moveInPlay)
        percent_wins, move = max((self.wins.get((player, tuple(S)), 0) /self.plays.get((player, tuple(S)), 1),p)
            for p, S in moveInPlay)
        
        print("Done calc", percent_wins, move)
        self.prevMove = move
        return move
    
    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays = self.plays
        wins = self.wins
        
        states_copy = self.states[:]
        state = states_copy[-1]
        visited_states = set()
        player = self.cpboard.current_player(state)
        winner = self.cpboard.winner(states_copy)
        
        expand = True
        for move in range(self.max_moves):
            #Get all possible next moves
            legal = self.cpboard.legal_plays(states_copy)
            move_states = [self.cpboard.next_state(state, m, player) for m in legal]
            #CHANGE HERE
            isAllMoveInPlay, m_s = self.isMoveInPlay(move_states)
            if isAllMoveInPlay:
            # if all(plays.get((player, tuple(S))) for S in move_states):
                #If data is available for all plays in moves_state
                log_total = log(sum(plays[(player, S)] for S in m_s))
                value, state = max(
                        ((wins[(player, S)]/plays[(player, S)]) +
                        self.C*sqrt(log_total/plays[(player, S)]), S)
                        for S in m_s
                    )
                move = (state[0], state[1])
            else:
                formated_move_states = self.formatMoveStates(move_states)
                state = choice(formated_move_states)
                move = (state[-1][0], state[-1][1])
                                
            states_copy.append(state)
            
            #CHANGE HERE
            if expand and (player, self.setState(state[:])) not in plays:
            # if expand and (player, tuple(state)) not in plays:
                expand = False
                plays[(player, self.setState(state[:]))] = 0
                wins[(player, self.setState(state[:]))] = 0
            
            #CHANGE HERE
            visited_states.add((player, self.setState(state[:])))
            
            #Switches between black / white
            player = self.cpboard.current_player(state)
            winner = self.cpboard.winner(states_copy)
        
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1

            if player == winner: 
                self.wins[(player, state)] += 1
    
    def setState(self, state):
        return tuple(set(state))
    
    def emptyBoard(self):
        b = []
        for row in range(self.cpboard.board.size):
            l = []
            for col in range(self.cpboard.board.size):
                l.append(None)
            b.append(l)
        return b
    
    def stateToBoard(self, state):
        b = copy.deepcopy(self.empBoard)
        if not isinstance(state, list): state = [state[:]]
        for elem in state:
            b[elem[0]][elem[1]] = elem[2]
        return b
    
    def boardToState(self, boardList):
        stateList = []
        for board in boardList:
            s = []
            for row in range(len(board)):
                for col in range(len(board[0])):
                    if board[row][col] != None:
                        s.append((row, col, board[row][col]))
            if len(s) < 2: stateList.append(s[0])
            else:
                s = self.setState(s)
                stateList.append(s)
        return stateList
    
    def allRotation(self, state):
        numRotate = 3
        currBoard = self.stateToBoard(state)
        
        rotatedBoard = []
        rotatedBoard.append(currBoard)
        for i in range(numRotate):
            temp = []
            b = list(zip(*currBoard[::-1]))
            for item in b:
                temp.append(list(item))
            rotatedBoard.append(temp)
            currBoard = b
        
        stateList = self.boardToState(rotatedBoard)
        return stateList
    
    #Finds a list of moves that are in plays
    #If not in play, adds one of the rotates
    def formatMoveStates(self, m_s):
        move_rotated = []
        total_move_state = []
        curr_move = []
        for move in m_s:
            curr_move.append(move[0])
            move_rotated.append(self.allRotation(move[1]))
        for i in range(len(move_rotated)):
            moveSet = move_rotated[i]
            found = False
            for mr in moveSet:
                if mr in self.plays: 
                    found = True
                    total_move_state.append((curr_move[i],mr))
            if not found:
                total_move_state.append((curr_move[i], moveSet[0]))
        return total_move_state

    def isMoveInPlay(self, m_s):
        move_rotated = []
        total_move_state = []
        for move in m_s:
            move_rotated.append(self.allRotation(move))
        for moveSet in move_rotated:
            found = False
            for mr in moveSet:
                if mr in self.plays: 
                    found = True
                    total_move_state.append(mr)
                    break
            if not found: return False, None
        return True, total_move_state
                    
        