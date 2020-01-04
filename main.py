from user import User
from board import Board
from scoreboard import Scoreboard
from ai import AI
import aiAlgorithms
import functools
import numpy
import os
import pickle
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty,NumericProperty


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
        self.manager.transition.direction='left'
        self.manager.current='game'

    def startUltimate(self):
        self.ultimate=UltimateTicTacToe(name='game',w=self.yDim,h=self.xDim)
        self.manager.add_widget(self.ultimate)
        self.manager.transition.direction='left'
        self.manager.current='game'

    def startQuantum(self):
        self.quantum=QuantumTicTacToe(name='game',w=self.yDim,h=self.xDim)
        self.manager.add_widget(self.quantum)
        self.manager.transition.direction='left'
        self.manager.current='game'

    def loadFileGUI(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def loadFile(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            #TODO: load game from pickled file
            pass
        self.dismissPopup()

    def dismissPopup(self):
        self.popup.dismiss()


class NByN(Screen):
    grid=ObjectProperty(None)
    def __init__(self,w,h,**kwargs):
        self.b=[]
        self.w=w
        self.h=h
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
            emptyCells=0
            for index,value in numpy.ndenumerate(self.board.cells):
                if value=="0.0":
                    emptyCells+=1
            if emptyCells==0:
                popup = Popup(title='Draw!',
                content=Label(text="Neither player has won the game!"),
                size_hint=(None, None), size=(400, 400))
                popup.open()
                return True
            self.board.currentPlayerNum=(self.board.currentPlayerNum+1)%len(self.board.players)
            move=self.ai.getMove(self.board.currentPlayerNum)
            self.board.placeMove(move,self.board.players[self.board.currentPlayerNum].value)
            self.b[move[1]][move[0]].text=str(self.board.players[self.board.currentPlayerNum].value)
            if self.board.checkWin(cells=self.board.cells,value=self.board.players[self.board.currentPlayerNum].value,nInARow=min(self.board.sizes)):
                self.winner=self.board.currentPlayerNum
                popup = Popup(title='Winner!',
                content=Label(text="{} has won the game!".format(self.board.symbols[self.board.currentPlayerNum])),
                size_hint=(None, None), size=(400, 400))
                popup.open()
                return True
            self.board.currentPlayerNum=(self.board.currentPlayerNum+1)%len(self.board.players)

    def loadFileGUI(self):
        content = LoadDialog(load=self.loadFile, cancel=self.dismissPopup)
        self.popup = Popup(title="Load game", content=content,
                            size_hint=(0.75, 0.75))
        self.popup.open()

    def loadFile(self, path, filename):
        with open(os.path.join(path, filename[0]).replace("/savedGames/savedGames/","/savedGames/") ,"rb") as f:
            self.board=pickle.load(f)
            self.boardToGUI()
        self.dismissPopup()

    def saveFileGUI(self):
        content = SaveDialog(save=self.saveFile, cancel=self.dismissPopup)
        self.popup = Popup(title="Save game", content=content,
                            size_hint=(0.75, 0.75))
        self.popup.open()

    def saveFile(self, path, filename):
        with open(os.path.join(path, filename), 'wb') as f:
            pickle.dump(self.board,f)
        self.dismissPopup()

    def dismissPopup(self):
        self.popup.dismiss()

    def boardToGUI(self):
        self.ai=aiAlgorithms.ABPMM(self.board)
        self.grid.clear_widgets()
        self.b=[]
        for y in range(self.h):
            self.b.append([])
            for x in range(self.w):
                if self.board.cells[x][y]=="0.0":
                    boardText=''
                else:
                    boardText=self.board.cells[x][y]
                self.b[-1].append(Tile(text=boardText,xLoc=x,yLoc=y))
                self.b[-1][-1].bind(on_press=self.makeMove)
                self.grid.add_widget(self.b[-1][-1])


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


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
                self.subBoards[instance.mainBoardX][instance.mainBoardY].setWinner(str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value))
                self.mainBoard.placeMove((instance.mainBoardX,instance.mainBoardY),str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value))
                if self.mainBoard.checkWin(value=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)):
                    print("Winner!")
            self.mainBoard.currentPlayerNum=(self.mainBoard.currentPlayerNum+1)%len(self.mainBoard.players)

    def loadFile(self, path, filename):
        with open(os.path.join(path, filename[0]).replace("/savedGames/savedGames/","/savedGames/") ,"rb") as f:
            self.subBoards=pickle.load(f)
            self.boardToGUI()
        self.dismissPopup()

    def saveFile(self, path, filename):
        with open(os.path.join(path, filename), 'wb') as f:
            pickle.dump(self.subBoards,f)
        self.dismissPopup()

    def boardToGUI(self):
        #set up the sub boards and the GUI
        self.grid.clear_widgets()
        numMoves=0
        for cellNum in range(81):
            mainBoardY=cellNum//27
            subBoardY=(cellNum%27)//9
            mainBoardX=(cellNum%9)//3
            subBoardX=cellNum%3
            if self.subBoards[mainBoardX][mainBoardY].cells[subBoardX][subBoardY]=="0.0":
                boardText=''
            else:
                boardText=self.subBoards[mainBoardX][mainBoardY].cells[subBoardX][subBoardY]
                numMoves+=1
            tile=UltimateTile(text=boardText,mainBoardX=mainBoardX,mainBoardY=mainBoardY,subBoardX=subBoardX,subBoardY=subBoardY)
            tile.bind(on_press=self.makeMove)
            self.grid.add_widget(tile)
        #set the current player to the player when the game was saved
        self.mainBoard.currentPlayerNum=numMoves%len(self.mainBoard.players)
        #construct the main board from the subboards
        for index,subBoard in numpy.ndenumerate(self.subBoards):
            for player in self.mainBoard.players:
                if subBoard.checkWin(value=player.value):
                    self.mainBoard.placeMove(index,player.value)


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
            xPos=index[1]
            yPos=index[0]
            self.superPositionBoard[index]=self.QuantumTile(next(gen),self,xPos,yPos)
        super(NByN,self).__init__(**kwargs)
        for y in range(3):
            for x in range(3):
                tile=Tile(text="",xLoc=x,yLoc=y)
                tile.bind(on_press=self.makeMove)
                self.grid.add_widget(tile)
                self.superPositionBoard[x][y].guiTile=tile


    def makeMove(self,instance):
        if not self.superPositionBoard[instance.xLoc][instance.yLoc].collapsed:
            if self.firstMove:
                self.firstMove^=1
                self.firstMoveX=instance.xLoc
                self.firstMoveY=instance.yLoc
                instance.text+="{}{} ".format(self.collapsedBoard.symbols[self.collapsedBoard.currentPlayerNum],self.moveNumRepr(self.moveNumber))
            else:
                if not (instance.xLoc==self.firstMoveX and instance.yLoc==self.firstMoveY):
                    self.firstMove^=1
                    instance.text+="{}{} ".format(self.collapsedBoard.symbols[self.collapsedBoard.currentPlayerNum],self.moveNumRepr(self.moveNumber))
                    if instance.text.count(" ")%3==0:
                        instance.text+="\n"
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
            checkWins()

        def secondMoveCollapse(instance):
            self.superPositionBoard[secondMoveX][secondMoveY].collapse(moveNumber)
            self.popup.dismiss()
            checkWins()

        def checkWins():
            winners=[]
            for symbol in self.collapsedBoard.symbols[:len(self.collapsedBoard.players)]:
                if self.collapsedBoard.checkWin(value=symbol):
                    winners.append(symbol)
            if len(winners)==1:
                popup = Popup(title='Winner!',
                content=Label(text="{} has won the game!".format(winners[0])),
                size_hint=(None, None), size=(400, 400))
                popup.open()
            elif len(winners)>1:
                popup = Popup(title='Draw!',
                content=Label(text="The board was collapsed so that several\npeople have winning moves."),
                size_hint=(None, None), size=(400, 400))
                popup.open()

        firstMove=Button(text="First move")
        notFirstMove=Button(text="Second move")
        box=BoxLayout()
        box.add_widget(firstMove)
        box.add_widget(notFirstMove)
        self.popup=Popup(title="Collapsing menu",content=box,auto_dismiss=False,size_hint=(None,None),size=(300,100),pos_hint={'top':1})
        firstMove.bind(on_press=firstMoveCollapse)
        notFirstMove.bind(on_press=secondMoveCollapse)
        self.popup.open()

    def loadFile(self, path, filename):
        with open(os.path.join(path, filename[0]).replace("/savedGames/savedGames/","/savedGames/") ,"rb") as f:
            p=pickle.load(f)
            self.moveNumber=p.moveNumber
            self.firstMove=p.firstMove
            self.collapsedBoard=p.collapsedBoard
            self.superPositionBoard=p.superPositionBoard
            self.grid.clear_widgets()
            for index,quantumTile in numpy.ndenumerate(self.superPositionBoard):
                text=p.superPositionBoardText[index]
                if text!='':
                    text+=' '
                tile=Tile(text=text,font_size=p.superPositionBoardFontSize[index],xLoc=index[0],yLoc=index[1])
                tile.bind(on_press=self.makeMove)
                self.grid.add_widget(tile)
                self.superPositionBoard[index].guiTile=tile
                quantumTile.game=self
        self.dismissPopup()

    def saveFile(self, path, filename):
        with open(os.path.join(path, filename), 'wb') as f:
            p=self.Pickler(self.moveNumber,self.firstMove,self.collapsedBoard,self.superPositionBoard,self.QuantumTile)
            pickle.dump(p,f)
        self.dismissPopup()


    class Pickler:
        def __init__(self,moveNumber,firstMove,collapsedBoard,superPositionBoard,QuantumTile):
            self.moveNumber=moveNumber
            self.firstMove=firstMove
            self.collapsedBoard=collapsedBoard
            self.superPositionBoard=numpy.ndarray((3,3),dtype=numpy.dtype(QuantumTile))
            self.superPositionBoardText=numpy.chararray((3,3),unicode=True,itemsize=100)
            self.superPositionBoardFontSize=numpy.chararray((3,3),unicode=True,itemsize=100)
            for index,quantumTile in numpy.ndenumerate(superPositionBoard):
                newIndex=index[::-1]
                self.superPositionBoard[newIndex]=superPositionBoard[index]
                self.superPositionBoardText[newIndex]=quantumTile.guiTile.text
                self.superPositionBoardFontSize[newIndex]=quantumTile.guiTile.font_size
                quantumTile.guiTile=None
                quantumTile.game=None


    class QuantumTile:
        def __init__(self,id,game,x,y):
            self.x=x
            self.y=y
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
            self.collapsed=True
            self.guiTile.text="{}{}".format(self.game.collapsedBoard.symbols[(collapsingMoveNumber-1)%len(self.game.collapsedBoard.players)],self.game.moveNumRepr(collapsingMoveNumber))
            self.guiTile.font_size="45sp"
            for moveNumber,tile in self.quantumStates.items():
                if moveNumber!=collapsingMoveNumber:
                    if not tile.collapsed:
                        tile.collapse(moveNumber)
            self.game.collapsedBoard.placeMove((self.x,self.y),self.game.collapsedBoard.symbols[(collapsingMoveNumber-1)%len(self.game.collapsedBoard.players)])


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
