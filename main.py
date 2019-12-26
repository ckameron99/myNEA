from user import User
from board import Board
from scoreboard import Scoreboard
from ai import AI
import aiAlgorithms
import functools
import numpy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
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
        self.nByN=QuantumTicTacToe(name='game',w=self.yDim,h=self.xDim)
        self.manager.add_widget(self.nByN)
        self.manager.current='game'

class NByN(Screen):
    grid=ObjectProperty(None)
    def getw(self):
        return self.w
    def __init__(self,w,h,**kwargs):
        self.b=[]
        self.w=w
        self.winner=None
        self.board=Board(dimensions=[w,h])
        self.ai=aiAlgorithms.ABPMM(self.board)
        super(NByN,self).__init__(**kwargs)
        for y in range(h):
            self.b.append([])
            for x in range(w):
                self.b[-1].append(Tile(text="",xLoc=x,yLoc=y))
                self.b[-1][-1].bind(on_press=self.makeMove)
                self.grid.add_widget(self.b[-1][-1])
    def makeMove(self,instance):
        if self.board.cells[instance.xLoc][instance.yLoc]=="0.0":
            self.board.placeMove((instance.xLoc,instance.yLoc),self.board.players[self.board.currentPlayerNum].value)
            instance.text=str(self.board.players[self.board.currentPlayerNum].value)
            if self.board.checkWin(cells=self.board.cells,value=self.board.players[self.board.currentPlayerNum].value,nInARow=min(self.board.sizes)):
                self.winner=self.board.currentPlayerNum
                popup = Popup(title='Winner!',
                content=Label(text="{} has won the game!".format(self.board.symbols[self.board.currentPlayerNum])),
                size_hint=(None, None), size=(400, 400))
                popup.open()
                return True
            self.board.currentPlayerNum=(self.board.currentPlayerNum+1)%len(self.board.players)
            move=self.ai.getMove(self.board.currentPlayerNum)
            print(move)
            location=move
            self.board.placeMove(location,self.board.players[self.board.currentPlayerNum].value)
            self.b[location[1]][location[0]].text=str(self.board.players[self.board.currentPlayerNum].value)
            self.board.currentPlayerNum=(self.board.currentPlayerNum+1)%len(self.board.players)


class UltimateTicTacToe(NByN):
    grid=ObjectProperty(None)
    def __init__(self,w=3,h=3,**kwargs):
        self.w=9
        self.mainBoard=Board(dimensions=[w,h])
        self.subBoards=numpy.ndarray((3,3),dtype=numpy.dtype(Board))
        for index,x in numpy.ndenumerate(self.subBoards):
            self.subBoards[index]=Board(dimensions=[3,3])
        #self.ai=aiAlgorithms.MCTS(self.board)
        super(NByN,self).__init__(**kwargs)
        for cellNum in range(81):
            mainBoardY=cellNum//27
            subBoardY=(cellNum%27)//9
            mainBoardX=(cellNum%9)//3
            subBoardX=cellNum%3
            tile=UltimateTile(text="",mainBoardX=mainBoardX,mainBoardY=mainBoardY,subBoardX=subBoardX,subBoardY=subBoardY)
            tile.bind(on_press=self.makeMove)
            self.grid.add_widget(tile)

    def makeMove(self,instance):
        if self.subBoards[instance.mainBoardX][instance.mainBoardY].cells[instance.subBoardX][instance.subBoardY]=="0.0" and self.subBoards[instance.mainBoardX][instance.mainBoardY].winnerIndex==-1:
            instance.text=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)
            self.subBoards[instance.mainBoardX][instance.mainBoardY].placeMove((instance.subBoardX,instance.subBoardY),str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value))
            if self.subBoards[instance.mainBoardX][instance.mainBoardY].checkWin(value=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)):
                self.mainBoard.placeMove((instance.mainBoardX,instance.mainBoardY),str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value))
                if self.mainBoard.checkWin(value=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)):
                    print("Winner!")
            self.mainBoard.currentPlayerNum=(self.mainBoard.currentPlayerNum+1)%len(self.mainBoard.players)

class QuantumTicTacToe(NByN):
    grid=ObjectProperty(None)

    def seq(self):
        id=0
        while 1:
            yield id
            id+=1

    def __init__(self,w=3,h=3,**kwargs):
        self.w=w
        self.moveNumber=1
        self.firstMove=True
        self.collapsedBoard=Board(dimensions=[3,3])
        self.superPositionBoard=numpy.ndarray((3,3),dtype=numpy.dtype(self.QuantumTile))
        gen=self.seq()
        for index,x in numpy.ndenumerate(self.superPositionBoard):
            self.superPositionBoard[index]=self.QuantumTile(next(gen),self)
        super(NByN,self).__init__(**kwargs)
        for y in range(3):
            for x in range(3):
                tile=Tile(text="",xLoc=x,yLoc=y)
                tile.bind(on_press=self.makeMove)
                self.grid.add_widget(tile)
                self.superPositionBoard[x][y].guiTile=tile


    class DragLabel(DragBehavior,Label):
        pass


    def makeMove(self,instance):
        if self.collapsedBoard.cells[instance.xLoc][instance.yLoc]=="0.0":
            if self.firstMove:
                self.firstMove^=1
                self.firstMoveX=instance.xLoc
                self.firstMoveY=instance.yLoc
                instance.text+="{}{} ".format(self.collapsedBoard.symbols[self.collapsedBoard.currentPlayerNum],self.moveNumRepr(self.moveNumber))
            else:
                self.firstMove^=1
                instance.text+="{}{} ".format(self.collapsedBoard.symbols[self.collapsedBoard.currentPlayerNum],self.moveNumRepr(self.moveNumber))
                if self.superPositionBoard[instance.xLoc][instance.yLoc].id!=self.superPositionBoard[self.firstMoveX][self.firstMoveY].id:
                    self.superPositionBoard[instance.xLoc][instance.yLoc].updateTileId(self.superPositionBoard[self.firstMoveX][self.firstMoveY].id)
                    self.superPositionBoard[instance.xLoc][instance.yLoc].quantumStates[self.moveNumber]=self.superPositionBoard[self.firstMoveX][self.firstMoveY]
                    self.superPositionBoard[self.firstMoveX][self.firstMoveY].quantumStates[self.moveNumber]=self.superPositionBoard[instance.xLoc][instance.yLoc]
                else:
                    self.getFirstMovePrecidenceAndCollapse(self.firstMoveX,self.firstMoveY,instance.xLoc,instance.yLoc,self.moveNumber)
                self.moveNumber+=1
                self.collapsedBoard.currentPlayerNum=(self.collapsedBoard.currentPlayerNum+1)%len(self.collapsedBoard.players)

    def moveNumRepr(self,num):
        return (num+1)//len(self.collapsedBoard.players) #converts the move number into the move number of the player

    def getFirstMovePrecidenceAndCollapse(self,firstMoveX,firstMoveY,secondMoveX,secondMoveY,moveNumber):
        def firstMoveCollapse(instance):
            self.superPositionBoard[firstMoveX][firstMoveY].collapse(moveNumber)
            self.popup.dismiss()
        def secondMoveCollapse(instance):
            self.superPositionBoard[secondMoveX][secondMoveY].collapse(moveNumber)
            self.popup.dismiss()

        firstMove=Button(text="First move")
        notFirstMove=Button(text="Second move")
        #dragBox=DragLabel()
        box=BoxLayout()
        box.add_widget(firstMove)
        box.add_widget(notFirstMove)
        #box.add_widget(dragBox)
        self.popup=Popup(title="Collapsing menu",content=box,auto_dismiss=False,size_hint=(None,None),size=(300,100),pos_hint={'top':1})
        firstMove.bind(on_press=firstMoveCollapse)
        notFirstMove.bind(on_press=secondMoveCollapse)
        self.popup.open()


    class QuantumTile:
        def __init__(self,id,game):
            self.id=id
            self.quantumStates={}
            self.collapsed=False
            self.guiTile=None
            self.game=game

        def updateTileId(self,id):
            self.id=id
            for moveNumber, tile in self.quantumStates.items():
                if tile.id!=id:
                    tile.updateTileId(id)

        def collapse(self,collapsingMoveNumber):
            print(self.guiTile.xLoc,self.guiTile.yLoc,collapsingMoveNumber)
            self.collapsed=True
            self.guiTile.text="{}{}".format(self.game.collapsedBoard.symbols[(collapsingMoveNumber-1)%len(self.game.collapsedBoard.players)],self.game.moveNumRepr(collapsingMoveNumber))
            for moveNumber,tile in self.quantumStates.items():
                if moveNumber!=collapsingMoveNumber:
                    if not tile.collapsed:
                        tile.collapse(moveNumber)




class Tile(Button):
    xLoc=NumericProperty(1)
    yLoc=NumericProperty(1)

class UltimateTile(Button):
    mainBoardX=NumericProperty(1)
    mainBoardY=NumericProperty(1)
    subBoardX=NumericProperty(1)
    subBoardY=NumericProperty(1)

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
    MainApp().run()

if __name__=="__main__":
    main()
