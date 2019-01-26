from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


class Map(Screen):
    tx_map = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)
        t = CoreImage("img/map.jpg").texture
        self.tx_map = t
