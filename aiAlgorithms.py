import random
import functools
import operator
from math import infinity as inf
class MiniMax:
    def __init__(self):
        self.HUMAN=-1
        self.COMPUTER=1
    def getMove(self,board,playerIndex):
        depth=sum([1 for index, value in np.ndenumerate(board.cells)])
        self.miniMax(board,board.cells,)
    def miniMax(self,board,boardCells,depth,player,boardPlayer):
        if player==self.COMPUTER:
            best=[None]*board.dimensions+[-infinity]
        elif player==self.HUMAN:
            best=[None]*board.dimensions+[+infinity]

        if depth==0 or (any([board.checkWin(value=user.value,cells=boardCells) for user in board.players]) or "0.0" not in boardCells):
            winners=[user for user in board.players in board.checkWin(value=user.value,cells=boardCells)]
            if len(winners)==0:
                return [None]*board.dimensions+[0]
            elif winners[0]==boardPlayer:
                return [None]*board.dimensions+[1]
            else:
                return [None]*board.dimensions+[-1]

            for index, value in np.ndenumerate(boardCells):
                boardCells[index]=player
                score=self.miniMax(board,boardCells.copy(),depth-1,-player)
                boardCells[index]="0.0"
                for i in range(index):
                    score[i]=index[i]

            if player==self.COMPUTER and score[-1]>best[-1]:
                best=scoreu
            elif player==self.HUMAN and score[-1]<best[-1]:
                best=score
        return best

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
