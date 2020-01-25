#! /usr/bin/python3
import numpy
import itertools


class Board:
    def __init__(self, dimensions=[3, 3], numPlayers=2,user1=None,user2=None):
        self.cells = numpy.zeros(dimensions)
        self.cells = self.cells.astype("U")
        self.dimensions = len(dimensions)
        self.sizes = dimensions
        self.players = []
        users=[user1,user2]
        self.symbols = ["X", "O", "V", "P"]
        for i in range(numPlayers):
            if users[i] is None:
                self.players.append(Player(self, self.symbols[i]))
            else:
                self.players.append(Player(self, users[i].symbol, users[i]))
        self.currentPlayerNum = 0
        self.winnerIndex = -1

    def __repr__(self):
        return self.cells.__repr__()

    def getWinner(self):
        return self.winnerIndex

    def setWinner(self, value): #only needs to be used with ultimate tic tac toe
        self.winnerIndex = self.symbols.index(value)

    def placeMove(self, coordinates, value):
        if self.winnerIndex == -1:
            self.cells.itemset(coordinates, value) # coordinates has to be passed as a tuple
            return True
        return False

    def checkWin(self,  nInARow = 3,  value = 1, cells = None): #check if the board has been won by a particular value
        if cells is None:
            cells = self.cells
        def checkWinAdj(nInARow, coordinates, value, adjCoord):
            direction = numpy.array(adjCoord)-numpy.array(coordinates) #calculate the direction from the main cell to the
            farCoords = numpy.array(coordinates)+(nInARow-1)*direction
            if min(farCoords)>= 0 and all(farCoords<self.sizes):
                for dist in range(nInARow):
                    pos = numpy.array(coordinates)+dist*numpy.array(direction)
                    pos = tuple(pos)
                    if cells[pos]!= value:
                        return False
                return True

        def checkWinCell(nInARow, coordinates, value):
            #generate the corners of the group of cells that are adjacent to the move
            pos = []
            for dimension, d in enumerate(coordinates):
                pos.append([max(0, d-1), d, min(d+1, self.sizes[dimension]-1)])
            #creates a list of all indexes within the board
            tmp = [chr(ord("0")+i) for i in range(3)]
            indexes = itertools.product("".join(tmp), repeat = len(coordinates))
            #create a list of all indexes adjacent to the cell,  but with duplicates
            surroundingCoordinates = []
            for index in indexes:
                tmp = []
                for i in range(len(index)):
                    tmp.append(pos[i][int(index[i])])
                surroundingCoordinates.append(tmp)
            #remove duplicates
            tupleCoords = set(tuple(i) for i in surroundingCoordinates)
            surroundingCoordinates = [list(coord) for coord in tupleCoords]
            #remove the original index
            surroundingCoordinates.remove(list(coordinates))
            #for each adjacent cell to the main cell,  check if there is a row starting in the main cell in the direction of the adjacent cell
            for adjCoord in surroundingCoordinates:
                if checkWinAdj(nInARow, coordinates, value, adjCoord):
                    return True
            return False

        iterable = numpy.nditer(cells, flags = ['multi_index'])
        #for each cell,  check if a row of three starts at that cell
        for cell in iterable:
            if cell == value:
                if checkWinCell(nInARow, iterable.multi_index, value):
                    return True
        return False

class Player:
    def __init__(self, board, value,user=None):
        self.board = board
        self.value = value
        self.user=user
        if user is not None:
            self.name=user.forename
        else:
            self.name=self.value
