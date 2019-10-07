from user import User
from board import Board
from scoreboard import Scoreboard
from ai import AI
import aiAlgorithms
import numpy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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
        self.manager.add_widget(self.nByN)
        self.manager.current='game'

class NByN(Screen):
    grid=ObjectProperty(None)
    def getw(self):
        return self.w
    def __init__(self,w,h,**kwargs):
        self.b=[]
        self.w=w
        self.ai=aiAlgorithms.MiniMax()
        self.board=Board(dimensions=[w,h])
        super(NByN,self).__init__(**kwargs)
        for y in range(h):
            self.b.append([])
            for x in range(w):
                self.b[-1].append(Tile(text="".format(x,y),xLoc=x,yLoc=y))
                self.b[-1][-1].bind(on_press=self.makeMove)
                self.grid.add_widget(self.b[-1][-1])
    def makeMove(self,instance):
        if self.board.cells[instance.xLoc][instance.yLoc]=="0.0":
            self.board.placeMove((instance.xLoc,instance.yLoc),self.board.players[self.board.currentPlayerNum].value)
            instance.text=str(self.board.players[self.board.currentPlayerNum].value)
            if self.board.checkWin(cells=self.board.cells,value=self.board.players[self.board.currentPlayerNum].value,nInARow=min(self.board.sizes)):
                popup = Popup(title='Winner!',
                content=Label(text="{} has won the game!".format(self.board.symbols[self.board.currentPlayerNum])),
                size_hint=(None, None), size=(400, 400))
                popup.open()
                return True
            self.board.currentPlayerNum=(self.board.currentPlayerNum+1)%len(self.board.players)
            move=self.ai.getMove(self.board,self.board.currentPlayerNum)
            print(move)
            location=move
            self.board.placeMove(location,self.board.players[self.board.currentPlayerNum].value)
            self.b[location[1]][location[0]].text=str(self.board.players[self.board.currentPlayerNum].value)
            self.board.currentPlayerNum=(self.board.currentPlayerNum+1)%len(self.board.players)

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
    MainApp().run()

def init():
    pass

if __name__=="__main__":
    main()
