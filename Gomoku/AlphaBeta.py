'''
https://tonypoer.io/2016/10/28/implementing-minimax-and-alpha-beta-pruning-using-python/
'''
import copy

class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, size, startColor):
        # self.game_tree = game_tree  # GameTree
        # self.root = game_tree.root  # GameNode
        self.boardSize = size
        self.endDepth = 3
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
        sc = -0.8 #scale for opp color
        self.oppScoreKey = {"AAAAA": 50000*sc, "+AAAA+": 4320*sc,
                            "+AAA++": 720*sc, "++AAA+": 720*sc,
                            "+AA+A+": 720*sc, "+A+AA+": 720*sc,
                            "AAAA+": 720*sc, "+AAAA": 720*sc,
                            "AA+AA": 720*sc, "A+AAA": 720*sc,
                            "AAA+A": 720*sc, "++AA++": 120*sc,
                            "++A+A+": 120*sc, "+A+A++": 120*sc,
                            "+++A++": 20*sc, "++A+++": 20*sc}
                            
        self.emptyBoard = [[None for i in range(self.boardSize)] for j in range(self.boardSize)]

    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        player = self.startPlayer
        
        if node == self.emptyBoard:
            node[int(self.boardSize/2)][int(self.boardSize/2)] = player
            return node

        successors = self.getSuccessors(node, player)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta, player)
            if value > best_val:
                best_val = value
                best_state = state
        # print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
        # print "AlphaBeta:  Best State is: " + best_state.Name
        return best_state

    def max_value(self, node, alpha, beta, player, depth=0):
        # print "AlphaBeta-->MAX: Visited Node :: " + node.Name
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
        # print "AlphaBeta-->MIN: Visited Node :: " + node.Name
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
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
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
        for row in range(len(state)):
            for col in range(len(state[0])):
                if state[row][col] != None:
                    if (row, col) not in legalPosition:
                        posSet = self.getPosSurrounding((row, col), state)
                        legalPosition.update(posSet)
        
        legalPosition = list(legalPosition)
        sortLegalPos = []
        for elem in legalPosition:
            sortLegalPos.append((elem, self.getPosScore(elem, state, player)))
        reverseSort=None
        if player == self.startPlayer: reverseSort = True
        else: reverseSort = False
        sortLegalPos.sort(key=lambda tup: tup[1], reverse=reverseSort)
        for pos in sortLegalPos:
            sortedL.append(pos[0])
        # if len(sortedL) > 10:
        #     sortedL = sortedL[:10]
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

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, depth):
        return depth == self.endDepth
    
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
            r = pos[1] - i
            c = pos[0] + i
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
            r = pos[1] + i
            c = pos[0] + i
            if r >=0 and c < self.boardSize and r >=0 and r < self.boardSize:
                if state[r][c] == None: code = code + '+'
                elif state[r][c] == player: code = code + 'O'
                else: code = code + 'A'
        
        for pattern in sk:
            if pattern in code: score += sk[pattern]
        return score
    
    def getPosScore(self, pos, state, player):
        score=0
        score = self.getVertScore(pos, state, player) + \
                self.getHorScore(pos, state, player) + \
                self.getPosXScore(pos, state, player) + \
                self.getNegXScore(pos, state, player)
        return score
    
    def getUtility(self, node, player):
        assert node is not None
        sumScore = 0
        for row in range(len(node)):
            for col in range(len(node[0])):
                if node[row][col] != None:
                    sumScore += self.getPosScore((row,col), node, player)
                # if node[row][col] == player:
                #     sumScore += self.getPosScore((row,col), node, player)
        return sumScore