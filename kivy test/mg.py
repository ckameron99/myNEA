from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
import time
Builder.load_file("mg.kv")
class MenuScreen(Screen):
    def __init__(self,**kwargs):
        self.xDim=3
        self.yDim=3
        self.test=0
        super(MenuScreen,self).__init__(**kwargs)
        #self.settingsScreen=SettingsScreen(name='game',w=self.yDim,h=self.xDim)
        #sm.add_widget(self.settingsScreen)
    def update(self,x,y):
        if x!=None:
            self.xDim=int(x)
        if y!=None:
            self.yDim=int(y)
    def start(self):
        if self.test:
            sm.remove_widget(self.settingsScreen)
        self.test=1
        self.settingsScreen=SettingsScreen(name='game',w=self.yDim,h=self.xDim)
        sm.add_widget(self.settingsScreen)
        self.manager.current='game'



class SettingsScreen(Screen):
    grid=ObjectProperty(None)
    def getw(self):
        return self.w
    def __init__(self,w,h,**kwargs):
        self.b=[]
        self.w=w
        super(SettingsScreen,self).__init__(**kwargs)
        for y in range(h):
            self.b.append([])
            for x in range(w):
                self.b[-1].append(Button(text="{} . {}".format(x,y)))
                self.grid.add_widget(self.b[-1][-1])

# Create the screen manager
sm = ScreenManager()
b=MenuScreen(name="menu")
#width=TextInput(text="3", multiline=False,height=50, size_hint= (None,None))
#height=TextInput(text="3", multiline=False,height=50, size_hint= (None,None))
#b.add_widget(width)
#b.add_widget(height)
sm.add_widget(b)
sm.current='menu'
class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
