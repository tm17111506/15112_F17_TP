from __future__ import division
import datetime
from random import choice
from math import log, sqrt
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
        nState.append((play[0], play[1], currPlayer))
        newState = self.checkCaptured(nState[:])
        return newState

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        currSet = set()
        for item in state_history[-1]:
            currSet.add((item[0], item[1]))
        legalPlay = self.fullPos - currSet
        return legalPlay
        
    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        
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
            #Low efficiency!!
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
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.C = 1.41
        self.cpboard = cpboard
        self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 10)
        
        #Stats
        self.wins={}
        self.plays={}

    def update(self, state):
        # Takes a game state, and appends it to the history.
        # Here we input the state of the board, from class board
        self.states.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.states[-1]

        player = self.cpboard.current_player(state)
        legal = self.cpboard.legal_plays(self.states[:])
        
        if legal == []: return None
        if len(legal) == 1: return legal
        
        games = 0
        begin = datetime.datetime.utcnow()
        #self.run_simulation()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(s, self.cpboard.next_state(state, s, player)) for s in legal]
        #p is the next state to move to, S is the state simulated / ran
        percent_wins, move = max((self.wins.get((player, tuple(S)), 0) /self.plays.get((player, tuple(S)), 1),p)
            for p, S in moves_states)
        
        print(percent_wins, move)
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
            
            if all(plays.get((player, tuple(S))) for S in move_states):
                #If data is available for all plays in moves_state
                log_total = log(sum(plays[(player, tuple(S))] for S in move_states))
                value, state = max(
                        ((wins[(player, tuple(S))]/plays[(player, tuple(S))]) +
                        self.C*sqrt(log_total/plays[(player, tuple(S))]), S)
                        for S in move_states
                    )
                move = (state[0], state[1])
            else:
                state = choice(move_states)
                move = (state[-1][0], state[-1][1])
                                
            #Chooses a random play
            #play = choice(legal)
            #state = self.board.next_state(state, play) #Updates the board
            states_copy.append(state)
            
            # winner = self.board.winner(states_copy)
            # if winner: break
            
            if expand and (player, tuple(state)) not in plays:
                expand = False
                #Adds if it is unseen node
                plays[(player, tuple(state))] = 0
                wins[(player, tuple(state))] = 0
                # if t > self.max_depth: #Keeps tracks of deepest level within max_moves
                #     self.max_depth = t
            
            visited_states.add((player, tuple(state)))
            
            #Switches between black / white
            player = self.cpboard.current_player(state)
            winner = self.cpboard.winner(states_copy)
            # if winner: break
        
        for player, state in visited_states:
            if (player, tuple(state)) not in self.plays:
                continue
                #Not a tracked node
            self.plays[(player, tuple(state))] += 1
            #But winner is inside the for loop tho
            if player == winner: 
                self.wins[(player, tuple(state))] += 1