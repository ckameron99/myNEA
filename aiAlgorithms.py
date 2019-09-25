import random
import functools
import operator
class MiniMax:
    def __init__(self):
        pass

class ABPMM(MiniMax):
    pass

class MCTS:
    def __init__(self):
        pass


class LookupTable:
    def __init__(self):
        pass


class MatchBox:
    def __init__(self):
        pass

class Random:
    def __init__(self):
        pass
    def getMove(self,board):
        while 1:
            move=random.randint(0,functools.reduce(operator.mul,board.sizes)-1)
            if board.cells[tuple([move%size for size in board.sizes])]=="0.0":
                return tuple([move%size for size in board.sizes])
