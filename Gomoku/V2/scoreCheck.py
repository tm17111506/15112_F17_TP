b = [[None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, 'white', None, None, None, None, None, None], [None, None, None, None, None, 'black', None, None, None, None, None], [None, None, None, None, None, None, 'white', None, None, None, None], [None, None, None, None, None, None, None, 'black', None, None, None], [None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None]]

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")


scoreKey = {"OOOOO": 50000, "+OOOO+": 4320,
                    "+OOO++": 720, "++OOO+": 720,
                    "+OO+O+": 720, "+O+OO+": 720,
                    "OOOO+": 720, "+OOOO": 720,
                    "OO+OO": 720, "O+OOO": 720,
                    "OOO+O": 720, "++OO++": 120,
                    "++O+O+": 120, "+O+O++": 120,
                    "+++O++": 20, "++O+++": 20}
sc = -0.9 #scale for opp color
oppScoreKey = {"AAAAA": 50000*sc, "+AAAA+": 4320*sc,
                    "+AAA++": 720*sc, "++AAA+": 720*sc,
                    "+AA+A+": 720*sc, "+A+AA+": 720*sc,
                    "AAAA+": 720*sc, "+AAAA": 720*sc,
                    "AA+AA": 720*sc, "A+AAA": 720*sc,
                    "AAA+A": 720*sc, "++AA++": 120*sc,
                    "++A+A+": 120*sc, "+A+A++": 120*sc,
                    "+++A++": 20*sc, "++A+++": 20*sc}

startPlayer = "black"
boardSize = 11

def getVertScore(pos, state, player):
    score = 0
    code = ''
    sk = {}
    if state[pos[0]][pos[1]] == player: sk = scoreKey
    else: sk = oppScoreKey
    for i in range(-4, 5):
        key = pos[1] + i
        if key >=0 and key < boardSize:
            if state[pos[0]][key] == None: code = code + '+'
            elif state[pos[0]][key] == player: code = code + 'O'
            else: code = code + 'A'
    
    print("Vert Code", code)
    for pattern in sk:
        if pattern in code: 
            score += sk[pattern]
    print("vert", score)
    return score

def getHorScore(pos, state, player):
    score = 0
    code = ''
    sk = {}
    if state[pos[0]][pos[1]] == player: sk = scoreKey
    else: sk = oppScoreKey
    for i in range(-4, 5):
        key = pos[0] + i
        if key >=0 and key < boardSize:
            if state[key][pos[1]] == None: code = code + '+'
            elif state[key][pos[1]] == player: code = code + 'O'
            else: code = code + 'A'
            
    print("Hoz code", code)
    for pattern in sk:
        if pattern in code: score += sk[pattern]
    print("Hoz", score)
    return score
    
def getPosXScore(pos, state, player):
    score = 0
    code = ''
    sk = {}
    if state[pos[0]][pos[1]] == player: sk = scoreKey
    else: sk = oppScoreKey
    for i in range(-4, 5):
        r = pos[1] - i
        c = pos[0] + i
        if r >=0 and c < boardSize and r >=0 and r < boardSize:
            if state[r][c] == None: code = code + '+'
            elif state[r][c] == player: code = code + 'O'
            else: code = code + 'A'
    
    print("Px code", code)
    for pattern in sk:
        if pattern in code: score += sk[pattern]
    print("Px", score)
    return score
    
def getNegXScore(pos, state, player):
    score = 0
    sk = {}
    if state[pos[0]][pos[1]] == player: sk = scoreKey
    else: sk = oppScoreKey
    code = ''
    for i in range(-4, 5):
        r = pos[1] + i
        c = pos[0] + i
        if r >=0 and c < boardSize and r >=0 and r < boardSize:
            if state[r][c] == None: code = code + '+'
            elif state[r][c] == player: code = code + 'O'
            else: code = code + 'A'
    
    print("Neg X code", code)
    for pattern in sk:
        if pattern in code: score += sk[pattern]
    print("Nx", score)
    return score

def getPosScore(pos, state, player):
    score=0
    score = getVertScore(pos, state, player) + \
            getHorScore(pos, state, player) + \
            getPosXScore(pos, state, player) + \
            getNegXScore(pos, state, player)
    return score

def getUtility(node, player):
    assert node is not None
    sumScore = 0
    for row in range(len(node)):
        for col in range(len(node[0])):
            if node[row][col] != None:
                print(row, col, sumScore, player)
                sumScore += getPosScore((row,col), node, player)
            # if node[row][col] == player:
            #     sumScore += self.getPosScore((row,col), node, player)
    return sumScore

print2dList(b)
print(getUtility(b, "black"))