import random
import functools
import operator
import numpy
from math import inf
import time

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
        print(maxDepth)
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=self.board.players[self.playerIndex].value
                val=self.minimax(maxDepth,(self.playerIndex+1)%len(self.board.players))
                self.board.cells[index]="0.0"
                print(val)
                if val>=bestMoveValue:
                    bestMoveValue=val
                    bestMoveLocation=index
        return bestMoveLocation


    def minimax(self,depth,playerIndex):
        for player in self.board.players:
            if self.board.checkWin(value=self.board.players[playerIndex].value):
                if playerIndex==self.playerIndex:
                    return 1
                else:
                    return -1
                    print(board.cells)
                    input()
        if depth==0:
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
        #print(depth,val,self.board.cells,"\n")
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
                val=self.minimax(maxDepth,(self.playerIndex+1)%len(self.board.players))
                self.board.cells[index]="0.0"
                print(val)
                if val>=bestMoveValue:
                    bestMoveValue=val
                    bestMoveLocation=index
        return bestMoveLocation


    def minimax(self,depth,playerIndex):
        for player in self.board.players:
            if self.board.checkWin(value=self.board.players[playerIndex].value):
                if playerIndex==self.playerIndex:
                    return 1
                else:
                    return -1
                    print(board.cells)
                    input()
        if depth==0:
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
        #print(depth,val,self.board.cells,"\n")
        return bestMoveValue

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
        print(maxDepth)
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=self.board.players[self.playerIndex].value
                val=self.abpmm(maxDepth,(self.playerIndex+1)%len(self.board.players),-inf,inf)
                self.board.cells[index]="0.0"
                print(val)
                if val>=bestMoveValue:
                    bestMoveValue=val
                    bestMoveLocation=index
        return bestMoveLocation


    def abpmm(self,depth,playerIndex,alpha,beta):
        for player in self.board.players:
            if self.board.checkWin(value=self.board.players[playerIndex].value):
                if playerIndex==self.playerIndex:
                    return 1
                else:
                    return -1
                    print(board.cells)
                    input()
        if depth==0:
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
        #print(depth,val,self.board.cells,"\n")
        return bestMoveValue

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
