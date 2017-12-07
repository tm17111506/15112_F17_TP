#########################
# AI Class for Gomoku Game
# This class uses AlphaBeta Pruning to pick out the highest scoring state and
# its cooresponding move
# 
# Optimization is applied at legal_move choice to speed up the search time
# An end-game state check is also used in order to avoid unnecessary branch outs
# 
# Structure of the AlphaBeta Pruning: 
# https://tonypoer.io/2016/10/28/implementing-minimax-and-alpha-beta-pruning-using-python/
#
#########################
import copy

#########################
class AlphaBeta:

    def __init__(self, size, startColor):
        self.boardSize = size
        self.endDepth = 3 #Search depth of the AI
        self.startPlayer = startColor #Starting player for CP
        self.starting = True

        self.scoreKey = {"OOOOO": 50000, "+OOOO+": 4320,
                         "+OOO++": 720, "++OOO+": 720,
                         "+OO+O+": 720, "+O+OO+": 720,
                         "OOOO+": 720, "+OOOO": 720,
                         "OO+OO": 720, "O+OOO": 720,
                         "OOO+O": 720, "++OO++": 120,
                         "++O+O+": 120, "+O+O++": 120,
                         "+++O++": 20, "++O+++": 20}
        sc = -3 #Scalar of reward points for the opponent
        self.oppScoreKey = {"AAAAA": 50000*sc, "+AAAA+": 4320*sc,
                            "+AAA++": 720*sc, "++AAA+": 720*sc,
                            "+AA+A+": 720*sc, "+A+AA+": 720*sc,
                            "AAAA+": 3720*sc, "+AAAA": 3720*sc,
                            "AA+AA": 720*sc, "A+AAA": 720*sc,
                            "AAA+A": 720*sc, "++AA++": 120*sc,
                            "++A+A+": 120*sc, "+A+A++": 120*sc,
                            "+++A++": 20*sc, "++A+++": 20*sc}
        self.prevMove = (-1,-1)
        self.emptyBoard = [[None for i in range(self.boardSize)] for j in range(self.boardSize)]

    #Main algorithm for Alpha-Beta Pruning search
    #Takes in currentState of the board and a previous move (for optimization)
    def alpha_beta_search(self, node, prevMove):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        player = self.startPlayer
        self.prevMove = prevMove
        
        #If AI is the starting player
        if node == self.emptyBoard:
            node[int(self.boardSize/2)][int(self.boardSize/2)] = player
            return node
        
        #Finds all the legal next board states
        successors = self.getSuccessors(node, player)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta, player)

            if value > best_val:
                best_val = value
                best_state = state

        return best_state

    def max_value(self, node, alpha, beta, player, depth=0):
        player = "black" if player == "white" else "white"
        if self.isTerminal(depth):
            return self.getUtility(node, player)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node, player)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta, player, depth+1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta, player, depth=0):
        player = "black" if player == "white" else "white"
        if self.isTerminal(depth):
            return self.getUtility(node, player)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node, player)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta, player, depth+1))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    

    # Find the legal moves based on the position within 1 unit away
    # from current board state and its plays
    def getPosSurrounding(self, position, state):
        legalPos=set()
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    if state[position[0]+i][position[1]+j] == None:
                        legalPos.add((position[0]+i, position[1]+j))
                except:
                    continue
        return legalPos
        
    def getStateLegalPos(self, state, player):
        legalPosition = set()
        sortedL = []
        #Finds a set of legalPosition given the currenet board state
        for row in range(len(state)):
            for col in range(len(state[0])):
                if state[row][col] != None:
                    if (row, col) not in legalPosition:
                        posSet = self.getPosSurrounding((row, col), state)
                        legalPosition.update(posSet)
        
        legalPosition = list(legalPosition)
        sortLegalPos = []
        for elem in legalPosition:
            sortLegalPos.append((elem, self.getPossibleScore(elem, state, player)))
            #Optimizes the choice of move based on calculated value
        reverseSort=None
        
        # Sorts the value-legal-position based on Player
        # Self = maximize, opponent = minimize
        if player == self.startPlayer: reverseSort = True
        else: reverseSort = False
        sortLegalPos.sort(key=lambda tup: tup[1], reverse=reverseSort)

        for pos in sortLegalPos:
            sortedL.append(pos[0])
        if len(sortedL) > 10:
            sortedL = sortedL[:10]
        return sortedL
    
    def getSuccessors(self, node, player):
        assert node is not None
        allLegalPos = self.getStateLegalPos(node, player)
        children = []
        for pos in allLegalPos:
            b = copy.deepcopy(node)
            b[pos[0]][pos[1]] = player
            children.append(b)
        return children

    def isTerminal(self, depth):
        return depth == self.endDepth

#############################################
#Score calculation and optimization methods

#############################################
    
# Helper functions to finding the score at a position
# The score at the position is based off of 4 directions:
#   Positive Diagonal, Negative Diagonal, Vertical, Horizontal
# In each direction, the value is found by stretching 4 units away from the
# central position, and then matced to the scoreKey
# +: Blank space, A: Opponent, O: Self
    
    def getVertScore(self, pos, state, player):
        score = 0
        code = ''
        sk = {}
        if state[pos[0]][pos[1]] == player: sk = self.scoreKey
        else: sk = self.oppScoreKey
        for i in range(-4, 5):
            key = pos[1] + i
            if key >=0 and key < self.boardSize:
                if state[pos[0]][key] == None: code = code + '+'
                elif state[pos[0]][key] == player: code = code + 'O'
                else: code = code + 'A'
        
        for pattern in sk:
            if pattern in code: 
                score += sk[pattern]
        return score
    
    def getHorScore(self, pos, state, player):
        score = 0
        code = ''
        sk = {}
        if state[pos[0]][pos[1]] == player: sk = self.scoreKey
        else: sk = self.oppScoreKey
        for i in range(-4, 5):
            key = pos[0] + i
            if key >=0 and key < self.boardSize:
                if state[key][pos[1]] == None: code = code + '+'
                elif state[key][pos[1]] == player: code = code + 'O'
                else: code = code + 'A'
                
        for pattern in sk:
            if pattern in code: score += sk[pattern]
        return score
        
    def getPosXScore(self, pos, state, player):
        score = 0
        code = ''
        sk = {}
        if state[pos[0]][pos[1]] == player: sk = self.scoreKey
        else: sk = self.oppScoreKey
        for i in range(-4, 5):
            r = pos[0] - i
            c = pos[1] + i
            if r >=0 and c < self.boardSize and r >=0 and r < self.boardSize:
                if state[r][c] == None: code = code + '+'
                elif state[r][c] == player: code = code + 'O'
                else: code = code + 'A'
                
        for pattern in sk:
            if pattern in code: score += sk[pattern]
        return score
        
    def getNegXScore(self, pos, state, player):
        score = 0
        sk = {}
        if state[pos[0]][pos[1]] == player: sk = self.scoreKey
        else: sk = self.oppScoreKey
        code = ''
        for i in range(-4, 5):
            r = pos[0] + i
            c = pos[1] + i
            if r >=0 and c < self.boardSize and r >=0 and r < self.boardSize:
                if state[r][c] == None: code = code + '+'
                elif state[r][c] == player: code = code + 'O'
                else: code = code + 'A'
        
        for pattern in sk:
            if pattern in code: score += sk[pattern]
        return score
    
    def getPossibleScore(self, pos, state, player):
        s = copy.deepcopy(state)
        if s[pos[0]][pos[1]] == None:
            s[pos[0]][pos[1]] = player
        score = self.getPosScore(pos, s, player) + self.getPosScore(self.prevMove, s, player)
        #print(player, score)
        return score
    
    def getPosScore(self, pos, state, player):
        vs = self.getVertScore(pos, state, player)
        hs = self.getHorScore(pos, state, player)
        px = self.getPosXScore(pos, state, player)
        nx = self.getNegXScore(pos, state, player)

        #End Game evalulation
        if player == "white":
            if vs == 50000*-0.9 or hs == 50000*-0.9 or \
                px == 50000*-0.9 or nx == 50000*-0.9:
                    return -float('inf')
        if player == "black":
            if vs == 50000 or hs == 50000 or \
                px == 50000 or nx == 50000:
                    return float('inf') 
        
        score = vs + hs + px + nx
        return score
    
    # The total score of a board state given
    # by the sum of all plays on the board
    def getUtility(self, node, player):
        assert node is not None
        sumScore = 0
        for row in range(len(node)):
            for col in range(len(node[0])):
                if node[row][col] != None:
                    sumScore += self.getPosScore((row,col), node, player)
        return sumScore