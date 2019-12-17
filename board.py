import numpy, itertools
class Board:
    def __init__(self,dimensions=[3,3],numPlayers=2):
        self.cells=numpy.zeros(dimensions)
        self.cells=self.cells.astype("U")
        self.dimensions=len(dimensions)
        self.sizes=dimensions
        self.players=[]
        self.symbols=["X","O","V","P"]
        for i in range(numPlayers):
            self.players.append(Player(self,self.symbols[i]))
        self.currentPlayerNum=0
        self.winnerIndex=-1

    def __repr__(self):
        return self.cells.__repr__()

    def getWinner(self):
        return self.winnerIndex

    def placeMove(self,coordinates,value):
        if self.winnerIndex==-1:
            self.cells.itemset(coordinates,value) # coordinates has to be passed as a tuple
            return True
        return False

    def checkWin(self, nInARow=3, value=1,cells=None):
        if cells is None:
            cells=self.cells
        def checkWinAdj(nInARow,coordinates,value,adjCoord):
            direction=numpy.array(adjCoord)-numpy.array(coordinates)
            if min(numpy.array(coordinates)+(nInARow-1)*direction)>=0 and all(numpy.array(coordinates)+(nInARow-1)*direction<self.sizes):
                return all([cells[tuple(numpy.array(coordinates)+dist*numpy.array(direction))]==value for dist in range(nInARow)])

        def checkWinCell(nInARow,coordinates,value):
            pos=[[max(0,d-1),d,min(d+1,self.sizes[dimension]-1)] for dimension,d in enumerate(coordinates)]
            indexes=itertools.product("".join([chr(ord("0")+i) for i in range(3)]),repeat=len(coordinates))
            surroundingCoordinates=[[pos[i][int(index[i])] for i in range(len(index))] for index in indexes]
            surroundingCoordinates=[list(coord) for coord in set(tuple(i) for i in surroundingCoordinates)]
            surroundingCoordinates.remove(list(coordinates))
            return any([checkWinAdj(nInARow,coordinates,value,adjCoord) for adjCoord in surroundingCoordinates])

        iterable=numpy.nditer(cells,flags=['multi_index'])
        if any(checkWinCell(nInARow,iterable.multi_index,value) for cell in iterable if cell==value):
            self.winnerIndex=self.symbols.index(value)
            return True
        return False

class Player:
    def __init__(self,board,value):
        self.board=board
        self.value=value
