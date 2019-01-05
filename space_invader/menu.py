from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


# Builder.load_file('menu.kv')

class Menu(Screen):
    but_launch = ObjectProperty(None)
