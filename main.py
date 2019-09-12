from user import User
from board import Board
from scoreboard import Scoreboard
from ai import AI
import aiAlgorithms

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty,NumericProperty

Builder.load_file("main.kv")

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
    def startNByN(self):
        self.nByN=NByN(name='game',w=self.yDim,h=self.xDim)
        sm.add_widget(self.nByN)
        self.manager.current='game'

class NByN(Screen):
    grid=ObjectProperty(None)
    def getw(self):
        return self.w
    def __init__(self,w,h,**kwargs):
        self.b=[]
        self.w=w
        self.board=Board(dimensions=[w,h])
        super(NByN,self).__init__(**kwargs)
        for y in range(h):
            self.b.append([])
            for x in range(w):
                self.b[-1].append(Tile(text="".format(x,y),xLoc=x,yLoc=y))
                self.b[-1][-1].bind(on_press=self.makeMove)
                self.grid.add_widget(self.b[-1][-1])
    def makeMove(self,instance):
        self.board.placeMove((instance.xLoc,instance.yLoc),1)
        self.board.checkWin()

class Tile(Button):
    xLoc=NumericProperty(1)
    yLoc=NumericProperty(1)

class MainApp(App):
    def __init__(self):
        super().__init__()
    def build(self):
        sm = ScreenManager()
        b=MenuScreen(name="menu")
        sm.add_widget(b)
        sm.current='menu'
        return sm

def main():
    init()
    MainApp.run()

def init():
    pass

if __name__=="__main__":
    main()
