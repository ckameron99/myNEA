#! /usr/bin/python3
#import local python files
from user import User
from board import Board
from scoreboard import Scoreboard
import aiAlgorithms
#numpy is a library that I used for multi-dimensional array data structure and multi-dimensional enumeration
import numpy
#os is a library that I used for file interaction for saving and loading games
import os
#pickle is a library used in order to serialize objects that represent the game state in order to save them to a file, or deserialize loaded game states in order to load a game
import pickle
#the kivy library provides all the GUI components used to render the game
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
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty,NumericProperty

import installer
installer.init()


class CustomDropDown(BoxLayout):
    pass

class MenuScreen(Screen):
    """The MenuScreen class is a class that represents the main menu that the user is greeted with when the game is first run. This includes handling the various settings that the user can change from the main menu, and creating a new game when the user decides to start a game."""
    def __init__(self,**kwargs):
        #set the default dimensions of the n by n board to be a 3 by 3 board, which is the standard version of tic tac toe
        self.xDim=3
        self.yDim=3
        super(MenuScreen,self).__init__(**kwargs)
        #create the dropdown menu to allow the user to choose which AI to play against
        self.dropdown=CustomDropDown()
        self.add_widget(self.dropdown)
        self.dropdown.ids.dropdown.dismiss()
        self.ids.loginButton1.on_press=self.login1
        self.ids.loginButton2.on_press=self.login2

    def update(self,x,y):
        #update the dimensions of the n by n tic tac toe board
        if x!=None:
            self.xDim=int(x)
        if y!=None:
            self.yDim=int(y)

    def startGame(self,type):
        #start a new game of the specified type with the AI selected by the dropdown menu
        aiKey={
        'None':aiAlgorithms.NoneAI,
        'NaiveMinimax':aiAlgorithms.NaiveMiniMax,
        'Minimax':aiAlgorithms.MiniMax,
        'NABPMM':aiAlgorithms.NABPMM,
        'ABPMM':aiAlgorithms.ABPMM,
        'Choose AI':aiAlgorithms.NoneAI,
        'Random':aiAlgorithms.Random,
        'Easy':aiAlgorithms.Easy,
        'Medium':aiAlgorithms.Medium,
        'Hard':aiAlgorithms.Hard
        }
        games={
        'NByN':NByN,
        'Ultimate':UltimateTicTacToe,
        'Quantum':QuantumTicTacToe
        }
        #create the new game
        ai=aiKey[self.dropdown.ids.mainbutton.text]
        self.game=games[type](name='game',w=self.yDim,h=self.xDim,ai=ai,user1=self.loginScreen1.user,user2=self.loginScreen2.user)
        #add the new game to the screen manager
        self.manager.add_widget(self.game)
        self.manager.transition.direction='left'
        #change the current screen to the new game
        self.manager.current='game'

    def startNByN(self):
        self.startGame('NByN')

    def startUltimate(self):
        self.startGame('Ultimate')

    def startQuantum(self):
        self.startGame('Quantum')

    def dismissPopup(self):
        self.popup.dismiss()

    def login1(self):
        self.manager.transition.direction='down'
        self.manager.current ='login1'

    def login2(self):
        self.manager.transition.direction='down'
        self.manager.current ='login2'

    def logout1(self):
        self.ids.loginButton1.text='Login (Guest 1)'
        self.loginScreen1.user=None
        self.ids.loginButton1.on_press=self.login1

    def logout2(self):
        self.ids.loginButton2.text='Login (Guest 2)'
        self.loginScreen2.user=None
        self.ids.loginButton2.on_press=self.login2


class LoginScreen(Screen):
    def __init__(self,menu,number,**kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.username=''
        self.password=''
        self.user=None
        self.menu=menu
        self.number=number
    def updateUsername(self,username):
        self.username=username.replace("username: ","")
    def updatePassword(self,password):
        self.password=password.replace("password: ","")
    def login(self):
        user=User(self.username,password=self.password)
        loginButtons=[self.menu.ids.loginButton1,self.menu.ids.loginButton2]
        logouts=[self.menu.logout1,self.menu.logout2]
        if user.loaded:
            self.user=user
            self.ids.messageBox.text=''
            self.ids.box1.text=''
            self.ids.box2.text=''
            loginButtons[self.number-1].text='Logout ({})'.format(user.id)
            self.manager.transition.direction='up'
            self.manager.current = 'menu'
            loginButtons[self.number-1].on_press=logouts[self.number-1]

        else:
            self.ids.messageBox.text='invalid username or password'


class CreateUserScreen(Screen):
    def __init__(self,**kwargs):
        super(CreateUserScreen,self).__init__(**kwargs)
        self.username=''
        self.forename=''
        self.surname=''
        self.password=''
        self.confirmingPassword=''
        self.user=None
        self.passwordConfirmed=False
    def updateUsername(self,username):
        self.username=username
    def updateForename(self,forename):
        self.forename=forename
    def updateSurname(self,surname):
        self.surname=surname
    def updatePassword(self,password):
        self.password=password
        if self.password==self.confirmingPassword:
            self.passwordConfirmed=True
        else:
            self.passwordConfirmed=False
    def confirmPassword(self,password):
        self.confirmingPassword=password
        if self.password==self.confirmingPassword:
            self.passwordConfirmed=True
        else:
            self.passwordConfirmed=False
    def createNewUser(self):
        if self.forename and self.surname and self.password:
            if self.passwordConfirmed:
                user=User(self.username,password=self.password)
                if user.userFound:
                    self.ids.messageBox.color=(1,0,0,1)
                    self.ids.messageBox.text='user already exists'
                else:
                    self.ids.messageBox.color=(0,1,0,1)
                    self.ids.messageBox.text='user created'
                    user=User(self.username)
                    user.create(self.forename,self.surname,self.password)
            else:
                self.ids.messageBox.color=(1,0,0,1)
                self.ids.messageBox.text='passwords do not match'
        else:
            self.ids.messageBox.color=(1,0,0,1)
            self.ids.messageBox.text='all fields are required to create a new user'

class NByN(Screen):
    """The NByN class is a class which represents a tic tac toe game of custom dimensions, and is also used to represent a 3 by 3 game. The class will manage the flow of the game, and contain all the data structures needed to store the game state, and the AI, if present."""
    grid=ObjectProperty(None)
    def __init__(self,w,h,ai,user1,user2,**kwargs):
        self.b=[]
        self.w=w
        self.h=h
        self.winner=None
        self.board=Board(dimensions=[w,h],user1=user1,user2=user2)
        self.ai=ai(self.board)
        self.user1=user1
        self.user2=user2
        super(NByN,self).__init__(**kwargs)
        for y in range(h):
            self.b.append([])
            for x in range(w):
                self.b[-1].append(Tile(text="",xLoc=x,yLoc=y))
                self.b[-1][-1].bind(on_press=self.makeMove)
                self.grid.add_widget(self.b[-1][-1])

    def makeMove(self,instance):
        #when the user clicks on a tile, it calls this method, and passes the graphical tile through as 'instance', allowing aspects of the visual representation of that tile to be changed
        if self.board.cells[instance.xLoc][instance.yLoc]=="0.0": #This ensures that the board will only react if the tile is vacent
            location=(instance.xLoc,instance.yLoc)
            value=self.board.players[self.board.currentPlayerNum].value
            name=self.board.players[self.board.currentPlayerNum].name
            self.board.placeMove(location,value) #Change the logical representation of the board to contain the new move
            instance.text=str(value) #Change the graphical representation of the board to contain the move, so that the user has feedback of their move
            if self.board.checkWin(cells=self.board.cells,value=value,nInARow=min(self.board.sizes)): #Check if the user has now won the game
                self.winner=self.board.currentPlayerNum
                popup = Popup(title='Winner!',
                content=Label(text="{} has won the game!".format(name)),
                size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                popup.open()
                return True
            #check for a draw, as if the user did not win, then there are no more empty cells left
            emptyCells=0
            for index,value in numpy.ndenumerate(self.board.cells):
                if value=="0.0":
                    emptyCells+=1
            if emptyCells==0:
                popup = Popup(title='Draw!',
                content=Label(text="Neither player has won the game!"),
                size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                popup.open()
                return True
            #change the player
            self.board.currentPlayerNum+=1
            self.board.currentPlayerNum%=len(self.board.players)
            #get the move from the AI
            move=self.ai.getMove(self.board.currentPlayerNum) #if the game is in two player mode, then the move will be None
            value=self.board.players[self.board.currentPlayerNum].value
            name=self.board.players[self.board.currentPlayerNum].name
            if move: #If the AI exists, then play the AI's move, otherwise, leave the incremented player to allow the second player to place their move
                self.board.placeMove(move,value) #Change the logical representation of the board to contain the new move
                self.b[move[1]][move[0]].text=str(value) #Change the graphical representation of the board to contain the move, so that the user has feedback of their move
                if self.board.checkWin(cells=self.board.cells,value=value,nInARow=min(self.board.sizes)): #Check if the AI has now won the game
                    self.winner=self.board.currentPlayerNum
                    popup = Popup(title='Winner!',
                    content=Label(text="{} has won the game!".format(name)),
                    size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                    popup.open()
                    return True
                self.board.currentPlayerNum+=1
                self.board.currentPlayerNum%=len(self.board.players)
                #check for a draw, as if the user did not win, then there are no more empty cells left
                emptyCells=0
                for index,value in numpy.ndenumerate(self.board.cells):
                    if value=="0.0":
                        emptyCells+=1
                if emptyCells==0:
                    popup = Popup(title='Draw!',
                    content=Label(text="Neither player has won the game!"),
                    size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                    popup.open()
                    return True

    def loadFileGUI(self):
        #create the load file popup
        content = LoadDialog(load=self.loadFile, cancel=self.dismissPopup)
        self.popup = Popup(title="Load game", content=content,
                            size_hint=(0.75, 0.75))
        self.popup.open()

    def loadFile(self, path, filename):
        #load the file selected by the load file popup
        with open(os.path.join(path, filename[0]).replace("/savedGames/savedGames/","/savedGames/") ,"rb") as f: #the load file popup duplicates the directory it started in, so any duplicate default directories have to be removed.
            self.board=pickle.load(f)
            self.boardToGUI() #reconstruct elements of the board and GUI that were not saved from the piece of the board that was saved
        self.dismissPopup()

    def saveFileGUI(self):
        #create the load file popup
        content = SaveDialog(save=self.saveFile, cancel=self.dismissPopup)
        self.popup = Popup(title="Save game", content=content,
                            size_hint=(0.75, 0.75))
        self.popup.open()

    def saveFile(self, path, filename):
        ##save the file in the directory selected by the save file popup with the name selected by the popup
        with open(os.path.join(path, filename), 'wb') as f:
            pickle.dump(self.board,f)
        self.dismissPopup()

    def dismissPopup(self): #create a method to dismiss the popup
        self.popup.dismiss()

    def boardToGUI(self):
        #used to construct other elements of the game from the saved board
        self.ai=aiAlgorithms.ABPMM(self.board)
        #remove current GUI elements of the board
        self.grid.clear_widgets()
        self.b=[]
        for y in range(self.h):
            self.b.append([])
            for x in range(self.w):
                #create the GUI cells with the relavent text
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
    """The NByN class is a class which represents an ultimate game of tic tac toe. The class will manage the flow of the game, and contain all the data structures needed to store the game state."""
    grid=ObjectProperty(None)
    def __init__(self,w=3,h=3,ai=None,user1=None,user2=None,**kwargs):
        self.w=9
        self.user1=user1
        self.user2=user2
        self.mainBoard=Board(dimensions=[w,h],user1=user1,user2=user2) #represents the board of won subboards
        self.subBoards=numpy.ndarray((3,3),dtype=numpy.dtype(Board)) #contains all the subboards in the same shape as the board of won subboards
        for index,x in numpy.ndenumerate(self.subBoards):
            self.subBoards[index]=Board(dimensions=[3,3],user1=user1,user2=user2)
        self.ai=ai(self.mainBoard)
        super(NByN,self).__init__(**kwargs)
        for cellNum in range(81): #create the 9x9 ((3x3)x3x3)
            mainBoardY=cellNum//27
            subBoardY=(cellNum%27)//9
            mainBoardX=(cellNum%9)//3
            subBoardX=cellNum%3
            tile=UltimateTile(text="",mainBoardX=mainBoardX,mainBoardY=mainBoardY,subBoardX=subBoardX,subBoardY=subBoardY)
            tile.bind(on_press=self.makeMove)
            self.grid.add_widget(tile)

    def makeMove(self,instance):
        name=self.mainBoard.players[self.mainBoard.currentPlayerNum].name
        if self.subBoards[instance.mainBoardX][instance.mainBoardY].cells[instance.subBoardX][instance.subBoardY]=="0.0" and self.subBoards[instance.mainBoardX][instance.mainBoardY].winnerIndex==-1: #only make the move if the cell is empty and the subboard that the cell belongs to has not already been won
            instance.text=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value) #change the GUI to reflect the player's move
            self.subBoards[instance.mainBoardX][instance.mainBoardY].placeMove((instance.subBoardX,instance.subBoardY),str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)) #change the logical representation of the game to reflect the move
            if self.subBoards[instance.mainBoardX][instance.mainBoardY].checkWin(value=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)):
                self.subBoards[instance.mainBoardX][instance.mainBoardY].setWinner(str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)) #if the subboard is won, prevent further moves from being placed in it
                self.mainBoard.placeMove((instance.mainBoardX,instance.mainBoardY),str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)) #if the subboard is won, place a move in the mainboard and check if the main board is now won
                if self.mainBoard.checkWin(value=str(self.mainBoard.players[self.mainBoard.currentPlayerNum].value)):
                    self.winner=self.mainBoard.currentPlayerNum
                    popup = Popup(title='Winner!',
                    content=Label(text="{} has won the game!".format(name)),
                    size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                    popup.open()
                    return True
            self.mainBoard.currentPlayerNum=(self.mainBoard.currentPlayerNum+1)%len(self.mainBoard.players)

    def loadFile(self, path, filename):
        with open(os.path.join(path, filename[0]).replace("/savedGames/savedGames/","/savedGames/") ,"rb") as f:
            self.subBoards=pickle.load(f) #write the data to the subboards
            self.boardToGUI()
        self.dismissPopup()

    def saveFile(self, path, filename):
        with open(os.path.join(path, filename), 'wb') as f:
            pickle.dump(self.subBoards,f) #dump the subboard's data, as everything else can be constructed from the subboard
        self.dismissPopup()

    def boardToGUI(self):
        #clear the current GUI components
        self.grid.clear_widgets()
        numMoves=0
        for cellNum in range(81):
            mainBoardY=cellNum//27
            subBoardY=(cellNum%27)//9
            mainBoardX=(cellNum%9)//3
            subBoardX=cellNum%3
            #set up the cells with the appropriate text
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

    def __init__(self,w=3,h=3,ai=None,user1=None,user2=None,**kwargs):
        self.w=w
        self.moveNumber=1
        self.user1=user1
        self.user2=user2
        self.firstMove=True #used to keep track of which move each player is on, as each turn each player places two moves
        self.collapsedBoard=Board(dimensions=[3,3],user1=user1,user2=user2) #track the collapsed moves, to detect a win
        self.superPositionBoard=numpy.ndarray((3,3),dtype=numpy.dtype(self.QuantumTile)) #used to contain the quantum tiles, which manage the GUI aspect of the cells, and track the entanglementes between themselves
        gen=self.seq()
        self.ai=ai(self.collapsedBoard)
        for index,x in numpy.ndenumerate(self.superPositionBoard):
            xPos=index[1]
            yPos=index[0]
            self.superPositionBoard[index]=self.QuantumTile(next(gen),self,xPos,yPos)
        super(NByN,self).__init__(**kwargs)
        for y in range(3):
            for x in range(3):
                #create the GUI cells and allocate them to the quantum tile objects
                tile=Tile(text="",xLoc=x,yLoc=y)
                tile.bind(on_press=self.makeMove)
                self.grid.add_widget(tile)
                self.superPositionBoard[x][y].guiTile=tile


    def makeMove(self,instance):
        if not self.superPositionBoard[instance.xLoc][instance.yLoc].collapsed: #do not allow the move if the cell is already collapsed
            if self.firstMove:
                self.firstMove^=1 #change to second move
                self.firstMoveX=instance.xLoc
                self.firstMoveY=instance.yLoc
                instance.text+="{}{} ".format(self.collapsedBoard.players[self.collapsedBoard.currentPlayerNum].value,self.moveNumRepr(self.moveNumber)) #add the first move to the GUI
            else:
                if not (instance.xLoc==self.firstMoveX and instance.yLoc==self.firstMoveY): #ensure that the player does not place both their moves in the same cell
                    self.firstMove^=1 #change back to first move
                    instance.text+="{}{} ".format(self.collapsedBoard.players[self.collapsedBoard.currentPlayerNum].value,self.moveNumRepr(self.moveNumber)) #add the second move to the GUI
                    if instance.text.count(" ")%3==0:
                        instance.text+="\n"
                    #check for cyclic entanglements, as cycles necessitate a collapse
                    if self.superPositionBoard[instance.xLoc][instance.yLoc].id!=self.superPositionBoard[self.firstMoveX][self.firstMoveY].id: #if the id's of the tiles of the two moves don't match, make them match
                        self.superPositionBoard[instance.xLoc][instance.yLoc].updateTileId(self.superPositionBoard[self.firstMoveX][self.firstMoveY].id)
                        self.superPositionBoard[instance.xLoc][instance.yLoc].quantumStates[self.moveNumber]=self.superPositionBoard[self.firstMoveX][self.firstMoveY]
                        self.superPositionBoard[self.firstMoveX][self.firstMoveY].quantumStates[self.moveNumber]=self.superPositionBoard[instance.xLoc][instance.yLoc]
                    else: #if the id's of the tiles match, then begin the collapse, after finding which way they should collapse
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
            for player in self.collapsedBoard.players:
                if self.collapsedBoard.checkWin(value=player.value):
                    winners.append(player.name)
            if len(winners)==1:
                popup = Popup(title='Winner!',
                content=Label(text="{} has won the game!".format(winners[0])),
                size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                popup.open()
            elif len(winners)>1: #when the board collapses, both players can gain a row of three moves, which still results in a draw
                popup = Popup(title='Draw!',
                content=Label(text="The board was collapsed so that several\npeople have winning moves."),
                size_hint=(None, None), size=(max(min(self.width,self.height)/3*2,200),max(min(self.width,self.height)/3*2,200)))
                popup.open()
        #create and open a popup asking how the board should collapse
        firstMove=Button(text="First move")
        notFirstMove=Button(text="Second move")
        box=BoxLayout()
        box.add_widget(firstMove)
        box.add_widget(notFirstMove)
        self.popup=Popup(title="Collapsing menu",content=box,auto_dismiss=False,size_hint=(0.5,0.2),pos_hint={'top':1})
        firstMove.bind(on_press=firstMoveCollapse)
        notFirstMove.bind(on_press=secondMoveCollapse)
        self.popup.open()

    def loadFile(self, path, filename): #load the game from a pickled file which contains a picklable version of the game
        with open(os.path.join(path, filename[0]).replace("/savedGames/savedGames/","/savedGames/") ,"rb") as f:
            p=pickle.load(f)
            self.moveNumber=p.moveNumber
            self.firstMove=p.firstMove
            self.collapsedBoard=p.collapsedBoard
            self.superPositionBoard=p.superPositionBoard
            #recreate the GUI to reflect the new logical representation of the game
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
            p=self.Pickler(self.moveNumber,self.firstMove,self.collapsedBoard,self.superPositionBoard,self.QuantumTile) #create the picklable version of the game, as the GUI aspects can't be pickled
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
                #save unique aspects of GUI components
                self.superPositionBoardText[newIndex]=quantumTile.guiTile.text
                self.superPositionBoardFontSize[newIndex]=quantumTile.guiTile.font_size
                #remove GUI components
                quantumTile.guiTile=None
                quantumTile.game=None


    class QuantumTile:
        def __init__(self,id,game,x,y):
            self.x=x
            self.y=y
            self.id=id #used to detect cyclical graph
            self.quantumStates={} #stores edges to other quantum tiles which act as nodes in a entanglement graph
            self.collapsed=False
            self.guiTile=None
            self.game=game

        def updateTileId(self,id): #update the id of the object and all objects entangled with it to be the same as the id of the new entangled tile
            self.id=id
            for moveNumber, tile in self.quantumStates.items():
                if tile.id!=id:
                    tile.updateTileId(id)

        def collapse(self,collapsingMoveNumber): #collapse the tile
            self.collapsed=True
            self.guiTile.text="{}{}".format(self.game.collapsedBoard.players[(collapsingMoveNumber-1)%len(self.game.collapsedBoard.players)].value,self.game.moveNumRepr(collapsingMoveNumber))
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
        sm = ScreenManager() #manages each screen that the user sees, such as the main menu and the game screen
        b=MenuScreen(name="menu")
        sm.add_widget(b)
        b.loginScreen1=LoginScreen(b,name='login1',number=1)
        b.loginScreen2=LoginScreen(b,name='login2',number=2)
        b.createUserScreen=CreateUserScreen(name='createUser')
        sm.current='menu'
        sm.add_widget(b.loginScreen1)
        sm.add_widget(b.loginScreen2)
        sm.add_widget(b.createUserScreen)
        return sm

def main():
    MainApp().run()

if __name__=="__main__":
    main()
