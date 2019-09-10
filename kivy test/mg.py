from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
Builder.load_file("mg.kv")
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    h=3
    w=4
    grid=ObjectProperty(None)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
a=SettingsScreen(name='settings')
for y in range(SettingsScreen.h):
    for x in range(SettingsScreen.w):
        a.grid.add_widget(Button(text="{} . {}".format(x,y)))
sm.add_widget(a)
class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
