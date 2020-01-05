import random
import functools
import operator
import numpy
from math import inf
import time

class NoneAI:
    def __init__(self,board):
        pass
    def getMove(self,playerIndex):
        return False

class NaiveMiniMax:
    def __init__(self,board):
        self.playerIndex=None
        self.board=board
    def getMove(self,playerIndex):
        maxDepth=-1
        for index, value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                maxDepth+=1
        self.maxDepth=maxDepth
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=self.board.players[self.playerIndex].value
                val=self.minimax(maxDepth,(self.playerIndex+1)%len(self.board.players))
                self.board.cells[index]="0.0"
                if val>=bestMoveValue:
                    bestMoveValue=val
                    bestMoveLocation=index
        return bestMoveLocation


    def minimax(self,depth,playerIndex):
        for player in self.board.players:
            if self.board.checkWin(value=player.value):
                if playerIndex!=self.playerIndex:
                    return 1
                else:
                    return -1
        emptyCells=0
        for index,value in numpy.ndenumerate(self.board.cells):
            if value=="0.0":
                emptyCells+=1
        if emptyCells==0:
            return 0
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val=self.minimax(depth-1,(playerIndex+1)%len(self.board.players))
                    self.board.cells[index]="0.0"
                    bestMoveValue=max(val,bestMoveValue)
        else:
            bestMoveValue=inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val=self.minimax(depth-1,(playerIndex+1)%len(self.board.players))
                    self.board.cells[index]="0.0"
                    bestMoveValue=min(val,bestMoveValue)
        return bestMoveValue

class MiniMax:
    def __init__(self,board):
        self.playerIndex=None
        self.board=board
    def getMove(self,playerIndex):
        maxDepth=-1
        for index, value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                maxDepth+=1
        self.maxDepth=maxDepth
        self.winMoveDepth=maxDepth
        self.loseMoveDepth=0
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=self.board.players[self.playerIndex].value
                val,moveDepth=self.minimax(maxDepth,(self.playerIndex+1)%len(self.board.players))
                self.board.cells[index]="0.0"
                if val>=bestMoveValue:
                    if val==-1 or val == 0:
                        if moveDepth>=self.loseMoveDepth:
                            bestMoveValue=val
                            bestMoveLocation=index
                            self.loseMoveDepth=moveDepth
                    elif val==1:
                        if moveDepth<self.winMoveDepth:
                            bestMoveValue=val
                            bestMoveLocation=index
                            self.winMoveDepth=moveDepth
        return bestMoveLocation


    def minimax(self,depth,playerIndex):
        winMoveDepth=self.maxDepth
        loseMoveDepth=0
        for player in self.board.players:
            if self.board.checkWin(value=player.value):
                if playerIndex!=self.playerIndex:
                    return 1,0
                else:
                    return -1,0
        emptyCells=0
        for index,value in numpy.ndenumerate(self.board.cells):
            if value=="0.0":
                emptyCells+=1
        if emptyCells==0:
            return 0,0
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val,moveDepth=self.minimax(depth-1,(playerIndex+1)%len(self.board.players))
                    self.board.cells[index]="0.0"
                    if val>=bestMoveValue:
                        if val==-1 or val == 0:
                            if moveDepth>=loseMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                loseMoveDepth=moveDepth
                                bestMoveDepth=loseMoveDepth
                        elif val==1:
                            if moveDepth<=winMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                winMoveDepth=moveDepth
                                bestMoveDepth=winMoveDepth
        else:
            bestMoveValue=inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val,moveDepth=self.minimax(depth-1,(playerIndex+1)%len(self.board.players))
                    self.board.cells[index]="0.0"
                    if val<=bestMoveValue:
                        if val==1 or val == 0:
                            if moveDepth>=loseMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                loseMoveDepth=moveDepth
                                bestMoveDepth=loseMoveDepth
                        elif val==-1:
                            if moveDepth<=winMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                winMoveDepth=moveDepth
                                bestMoveDepth=winMoveDepth
        return bestMoveValue,bestMoveDepth+1

class NABPMM:
    def __init__(self,board):
        self.playerIndex=None
        self.board=board
    def getMove(self,playerIndex):
        maxDepth=-1
        for index, value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                maxDepth+=1
        self.maxDepth=maxDepth
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=self.board.players[self.playerIndex].value
                val=self.abpmm(maxDepth,(self.playerIndex+1)%len(self.board.players),-inf,inf)
                self.board.cells[index]="0.0"
                if val>=bestMoveValue:
                    bestMoveValue=val
                    bestMoveLocation=index
        return bestMoveLocation


    def abpmm(self,depth,playerIndex,alpha,beta):
        for player in self.board.players:
            if self.board.checkWin(value=player.value):
                if playerIndex!=self.playerIndex:
                    return 1
                else:
                    return -1
        emptyCells=0
        for index,value in numpy.ndenumerate(self.board.cells):
            if value=="0.0":
                emptyCells+=1
        if emptyCells==0:
            return 0
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val=self.abpmm(depth-1,(playerIndex+1)%len(self.board.players),alpha,beta)
                    self.board.cells[index]="0.0"
                    bestMoveValue=max(val,bestMoveValue)
                    alpha=max(alpha,bestMoveValue)
                    if alpha>=beta:
                        break
        else:
            bestMoveValue=inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val=self.abpmm(depth-1,(playerIndex+1)%len(self.board.players),alpha,beta)
                    self.board.cells[index]="0.0"
                    bestMoveValue=min(val,bestMoveValue)
                    beta=min(beta,bestMoveValue)
                    if alpha>=beta:
                        break
        return bestMoveValue

class ABPMM:
    def __init__(self,board):
        self.playerIndex=None
        self.board=board
    def getMove(self,playerIndex):
        maxDepth=-1
        for index, value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                maxDepth+=1
        self.maxDepth=maxDepth
        self.winMoveDepth=maxDepth
        self.loseMoveDepth=0
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=self.board.players[self.playerIndex].value
                val,moveDepth=self.abpmm(maxDepth,(self.playerIndex+1)%len(self.board.players),-inf,inf)
                self.board.cells[index]="0.0"
                if val>=bestMoveValue:
                    if val==-1 or val == 0:
                        if moveDepth>=self.loseMoveDepth:
                            bestMoveValue=val
                            bestMoveLocation=index
                            self.loseMoveDepth=moveDepth
                    elif val==1:
                        if moveDepth<self.winMoveDepth:
                            bestMoveValue=val
                            bestMoveLocation=index
                            self.winMoveDepth=moveDepth
        return bestMoveLocation


    def abpmm(self,depth,playerIndex,alpha,beta):
        winMoveDepth=self.maxDepth
        loseMoveDepth=0
        for player in self.board.players:
            if self.board.checkWin(value=player.value):
                if playerIndex!=self.playerIndex:
                    return 1,0
                else:
                    return -1,0
        emptyCells=0
        for index,value in numpy.ndenumerate(self.board.cells):
            if value=="0.0":
                emptyCells+=1
        if emptyCells==0:
            return 0,0
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val,moveDepth=self.abpmm(depth-1,(playerIndex+1)%len(self.board.players),alpha,beta)
                    self.board.cells[index]="0.0"
                    if val>=bestMoveValue:
                        if val==-1 or val == 0:
                            if moveDepth>=loseMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                loseMoveDepth=moveDepth
                                bestMoveDepth=loseMoveDepth
                        elif val==1:
                            if moveDepth<=winMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                winMoveDepth=moveDepth
                                bestMoveDepth=winMoveDepth
                    alpha=max(alpha,bestMoveValue)
                    if alpha>=beta:
                        break
        else:
            bestMoveValue=inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=self.board.players[playerIndex].value
                    val,moveDepth=self.abpmm(depth-1,(playerIndex+1)%len(self.board.players),alpha,beta)
                    self.board.cells[index]="0.0"
                    if val<=bestMoveValue:
                        if val==1 or val == 0:
                            if moveDepth>=loseMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                loseMoveDepth=moveDepth
                                bestMoveDepth=loseMoveDepth
                        elif val==-1:
                            if moveDepth<=winMoveDepth:
                                bestMoveValue=val
                                bestMoveLocation=index
                                winMoveDepth=moveDepth
                                bestMoveDepth=winMoveDepth
                    beta=min(beta,bestMoveValue)
                    if alpha>=beta:
                        break
        return bestMoveValue,bestMoveDepth+1



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
    def __init__(self,board):
        pass
    def getMove(self):
        while 1:
            move=random.randint(0,functools.reduce(operator.mul,self.board.sizes)-1)
            if self.board.cells[tuple([move%size for size in self.board.sizes])]=="0.0":
                return tuple([move%size for size in self.board.sizes])
