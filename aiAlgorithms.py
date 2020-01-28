#! /usr/bin/python3
#TODO: Inherit as much as possible
#random is a library to generate pseudo-random numbers that I use to generate random moves
import random
import functools
#operator is a module that provides pythonic operators as methods
import operator
#numpy is a module that I used for multi-dimensional array data structure and multi-dimensional enumeration
import numpy
#math provides inf which is a numerical data type which is larger than any int or float
from math import inf

class NoneAI: #used when the game is in two player mode
    def __init__(self,board):
        pass
    def getMove(self,playerIndex):
        return False

class NaiveMiniMax: #standard minimax algorithm
    def __init__(self,board):
        self.playerIndex=None
        self.board=board
    def getMove(self,playerIndex):
        #calculate the maximum number of moves that will be played
        maxDepth=-1
        for index, value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                maxDepth+=1
        self.maxDepth=maxDepth
        self.playerIndex=playerIndex
        #as the ai is trying to maximise the reward, the current predicted reward is set to -infinity so that any move is better than that
        bestMoveValue,bestMoveLocation=-inf,None
        for index,value in numpy.ndenumerate(self.board.cells):
            if value=="0.0":
                playerValue=self.board.players[self.playerIndex].value
                self.board.cells[index]=playerValue #try a particular move
                nextPlayerNum=self.playerIndex+1
                nextPlayerNum%=len(self.board.players)
                val=self.minimax(maxDepth,nextPlayerNum) #check the expected reward of the move
                self.board.cells[index]="0.0" #return the board to the previous state before that move
                if val>=bestMoveValue: #if the move has a better reward than the previous best move, then reassign the best move
                    bestMoveValue=val
                    bestMoveLocation=index
        return bestMoveLocation


    def minimax(self,depth,playerIndex):
        #start by checking if the board state gives an immediate reward
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
        #recurse another move to find the expected reward from the non-terminal board state
        nextPlayerNum=playerIndex+1
        nextPlayerNum%=len(self.board.players)
        playerValue=self.board.players[playerIndex].value
        if playerIndex==self.playerIndex: #maximising, as this is the AI's turn to make a move
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=playerValue
                    val=self.minimax(depth-1,nextPlayerNum)
                    self.board.cells[index]="0.0"
                    bestMoveValue=max(val,bestMoveValue)
        else: #minimising reward, simulating a perfect opponent
            bestMoveValue=inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=playerValue
                    val=self.minimax(depth-1,nextPlayerNum)
                    self.board.cells[index]="0.0"
                    bestMoveValue=min(val,bestMoveValue)
        return bestMoveValue

class MiniMax(NaiveMiniMax):
    # identical to naive minimax, but preferes to win quickly and lose or draw over a longer time, in order to give maximum time for sub-optimal opponent to make a mistake that improves the AI's outcome
    def getMove(self,playerIndex):
        self.winMoveDepth=maxDepth #the AI tries to minimise this
        self.loseMoveDepth=0 #the AI tries to maximise this, and it also doubles as a drawing move depth
        maxDepth=-1
        for index, value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                maxDepth+=1
        self.maxDepth=maxDepth
        self.playerIndex=playerIndex
        bestMoveValue,bestMoveLocation=-inf,None
        playerValue=self.board.players[self.playerIndex].value
        nextPlayerNum==self.playerIndex+1
        nextPlayerNum%=len(self.board.players)
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=playerValue
                val,moveDepth=self.minimax(maxDepth,nextPlayerNum) #also retrieve the amount of moves that will be played to achieve the reward following the move
                self.board.cells[index]="0.0"
                if val>=bestMoveValue:
                    if val==-1 or val == 0: #if the AI can't currently win, then maximise the move depth
                        if moveDepth>=self.loseMoveDepth:
                            bestMoveValue=val
                            bestMoveLocation=index
                            self.loseMoveDepth=moveDepth
                    elif val==1: #if the AI is going to win, then minimise the number of moves
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
        nextPlayerNum=playerIndex+1
        nextPlayerNum%=len(self.board.players)
        playerValue=self.board.players[playerIndex].value
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=playerValue
                    val,moveDepth=self.minimax(depth-1,nextPlayerNum)
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
                    self.board.cells[index]=playerValue
                    val,moveDepth=self.minimax(depth-1,nextPlayerNum)
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
        playerValue=self.board.players[self.playerIndex].value
        nextPlayerNum=self.playerIndex+1
        nextPlayerNum%=len(self.board.players)
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=playerValue
                val=self.abpmm(maxDepth,nextPlayerNum,-inf,inf)
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
        nextPlayerNum=playerIndex+1
        nextPlayerNum%=len(self.board.players)
        playerValue=self.board.players[playerIndex].value
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=playerValue
                    val=self.abpmm(depth-1,nextPlayerNum,alpha,beta)
                    self.board.cells[index]="0.0"
                    bestMoveValue=max(val,bestMoveValue)
                    alpha=max(alpha,bestMoveValue)
                    if alpha>=beta:
                        break
        else:
            bestMoveValue=inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    self.board.cells[index]=playerValue
                    val=self.abpmm(depth-1,nextPlayerNum,alpha,beta)
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
        nextPlayerNum=playerIndex+1
        nextPlayerNum%=len(self.board.players)
        playerValue=self.board.players[playerIndex].value
        for index,value in numpy.ndenumerate(self.board.cells):
            if self.board.cells[index]=="0.0":
                self.board.cells[index]=playerValue
                val,moveDepth=self.abpmm(maxDepth,nextPlayerNum,-inf,inf)
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
        emptyCells=0
        for index,value in numpy.ndenumerate(self.board.cells):
            if value=="0.0":
                emptyCells+=1
        if emptyCells==0:
            return 0,0
        nextPlayerNum=playerIndex+1
        nextPlayerNum%=len(self.board.players)
        playerValue=self.board.players[playerIndex].value
        if playerIndex==self.playerIndex:
            bestMoveValue=-inf
            for index,value in numpy.ndenumerate(self.board.cells):
                if self.board.cells[index]=="0.0":
                    val,moveDepth=None,None
                    self.board.cells[index]=playerValue
                    if self.board.checkWin(value=playerValue):
                        val,moveDepth= 1,0
                    if val is None:
                        val,moveDepth=self.abpmm(depth-1,nextPlayerNum,alpha,beta)
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
                    val,moveDepth=None,None
                    self.board.cells[index]=playerValue
                    if self.board.checkWin(value=playerValue):
                        val,moveDepth= -1,0
                    if val is None:
                        val,moveDepth=self.abpmm(depth-1,nextPlayerNum,alpha,beta)
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


class Random:
    def __init__(self,board):
        pass
    def getMove(self):
        while 1:
            numCells=functools.reduce(operator.mul,self.board.sizes)
            move=random.randint(0,numCells-1)
            move=tuple([move%size for size in self.board.sizes])
            if self.board.cells[move]=="0.0":
                return tuple([move%size for size in self.board.sizes])
