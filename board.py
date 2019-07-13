import numpy
class Board:
    def __init__(self,dimensions=[3,3]):
        self.cells=numpy.empty(dimensions)

    def placeMove(self,coordinates,value):
        self.cells.itemset(coordinates,value) # coordinates has to be passed as a tuple

    def checkWon(self,nInARow=3):
        pass
