from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty,NumericProperty
import time
import numpy
import itertools
Builder.load_file("mg.kv")
class MenuScreen(Screen):
    def __init__(self,**kwargs):
        self.xDim=3
        self.yDim=3
        super(MenuScreen,self).__init__(**kwargs)
    def update(self,x,y):
        if x!=None:
            self.xDim=int(x)
        if y!=None:
            self.yDim=int(y)
    def start(self):
        self.settingsScreen=SettingsScreen(name='game',w=self.yDim,h=self.xDim)
        self.manager.add_widget(self.settingsScreen)
        self.manager.current='game'



class SettingsScreen(Screen):
    grid=ObjectProperty(None)
    def getw(self):
        return self.w
    def __init__(self,w,h,**kwargs):
        self.b=[]
        self.w=w
        self.board=Board(dimensions=[w,h])
        super(SettingsScreen,self).__init__(**kwargs)
        for y in range(h):
            self.b.append([])
            for x in range(w):
                self.b[-1].append(Tile(text="".format(x,y),xLoc=x,yLoc=y))
                self.b[-1][-1].bind(on_press=self.makeMove)
                self.grid.add_widget(self.b[-1][-1])
    def makeMove(self,instance):
        self.board.placeMove((instance.xLoc,instance.yLoc),1)
        self.board.checkWin()

# Create the screen manager
class Tile(Button):
    xLoc=NumericProperty(1)
    yLoc=NumericProperty(1)

class TestApp(App):
    def __init__(self,**kwargs):
        super().__init__()
    def build(self):
        sm = ScreenManager()
        b=MenuScreen(name="menu")
        sm.add_widget(b)
        sm.current='menu'
        return sm


class Board:
    def __init__(self,dimensions=[3,3],numPlayers=2):
        self.cells=numpy.zeros(dimensions)
        self.dimensions=len(dimensions)
        self.sizes=dimensions
        self.players=[]

    def __repr__(self):
        return self.cells.__repr__()

    def placeMove(self,coordinates,value):
        self.cells.itemset(coordinates,value) # coordinates has to be passed as a tuple
        print(self.checkWin())

    def checkWin(self, nInARow=3, value=1):
        def checkWinAdj(nInARow,coordinates,value,adjCoord):
            direction=numpy.array(adjCoord)-numpy.array(coordinates)
            if min(numpy.array(coordinates)+(nInARow-1)*direction)>=0 and all(numpy.array(coordinates)+(nInARow-1)*direction<self.sizes):
                return all([self.cells[tuple(numpy.array(coordinates)+dist*numpy.array(direction))]==value for dist in range(nInARow)])

        def checkWinCell(nInARow,coordinates,value):
            pos=[[max(0,d-1),d,min(d+1,self.sizes[dimension]-1)] for dimension,d in enumerate(coordinates)]
            indexes=itertools.product("".join([chr(ord("0")+i) for i in range(3)]),repeat=len(coordinates))
            surroundingCoordinates=[[pos[i][int(index[i])] for i in range(len(index))] for index in indexes]
            surroundingCoordinates=[list(coord) for coord in set(tuple(i) for i in surroundingCoordinates)]
            surroundingCoordinates.remove(list(coordinates))
            return any([checkWinAdj(nInARow,coordinates,value,adjCoord) for adjCoord in surroundingCoordinates])

        iterable=numpy.nditer(self.cells,flags=['multi_index'])
        return any(checkWinCell(nInARow,iterable.multi_index,value) for cell in iterable if cell==value)

if __name__ == '__main__':
    TestApp().run()
