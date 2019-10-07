import random
import functools
import operator
import numpy
from math import inf
import time
'''class MiniMax:
    def __init__(self):
        self.HUMAN=-1
        self.COMPUTER=1
    def getMove(self,board,playerIndex):
        depth=sum([1 for index, value in numpy.ndenumerate(board.cells)])
        move=self.miniMax(board,board.cells.copy(),depth,self.COMPUTER,board.players[playerIndex])
        return move
    def miniMax(self,board,boardCells,depth,player,boardPlayer):
        if player==self.COMPUTER:
            best=[None]*board.dimensions+[-inf]
        elif player==self.HUMAN:
            best=[None]*board.dimensions+[+inf]
        #if depth==0 or (any([board.checkWin(value=user.value,cells=boardCells) for user in board.players]) or "0.0" not in boardCells):
        if any([board.checkWin(value=user.value,cells=boardCells) for user in board.players]) or depth==0:
            winners=[user for user in board.players if board.checkWin(value=user.value,cells=boardCells)]
            if len(winners)==0:
                return [None]*board.dimensions+[0]
            elif winners[0]==boardPlayer:
                return [None]*board.dimensions+[1]
            else:
                return [None]*board.dimensions+[-1]

        for index, value in numpy.ndenumerate(boardCells):
            if boardCells[index]=="0.0":
                boardCells[index]=boardPlayer.value
                score=self.miniMax(board,boardCells,depth-1,-player,boardPlayer)
                boardCells[index]="0.0"
                if player==self.COMPUTER and score[-1]>best[-1]:
                    best=score
                    for dim,indx in enumerate(index):
                        best[dim]=indx
                elif player==self.HUMAN and score[-1]<best[-1]:
                    best=score
                    for dim,indx in enumerate(index):
                        best[dim]=indx

        return best
'''
class MiniMax:
    def getMove(self,board,playerIndex):
        maxDepth=9
        bestMoveValue=-inf
        bestMove=None
        boardCells=board.cells.copy()
        for index, value in numpy.ndenumerate(boardCells):
            if boardCells[index]=="0.0":
                boardCells[index]="O"
                value=self.minimax(board,boardCells,maxDepth,True)
                print(index,value)
                boardCells[index]="0.0"
                if value>bestMoveValue:
                    bestMove=index
                    bestMoveValue=value
        return bestMove
    def minimax(self,board,boardCells,depth,isPlayerMaximised):
        #print(boardCells,depth)
        for player in board.players:
            #print(player.value,boardCells,depth)
            '''if input("contine?")!="" and f:
                while True:
                    exec(input())'''
            if board.checkWin(cells=boardCells,value=player.value):
                if player.value=="X":
                    return -1
                else:
                    return 1
            #return 0
        if isPlayerMaximised:
            bestValue=-inf
            for index, value in numpy.ndenumerate(boardCells):
                if boardCells[index]=="0.0":
                    boardCells[index]="X"
                    value=self.minimax(board,boardCells,depth-1,False)
                    boardCells[index]="0.0"
                    bestValue=max(value,bestValue)
            return bestValue

        else:
            bestValue=inf
            for index, value in numpy.ndenumerate(boardCells):
                if boardCells[index]=="0.0":
                    boardCells[index]="O"
                    value=self.minimax(board,boardCells,depth-1,True)
                    boardCells[index]="0.0"
                    bestValue=min(value,bestValue)
            return bestValue


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
