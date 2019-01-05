from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from spaceship import FPS


class Menu(Screen):
    but_launch = ObjectProperty(None)
    # but2 = ObjectProperty(None)
    but3 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self._update_event = None

    def on_pre_enter(self, *args):
        self._update_event = Clock.schedule_interval(self.update, 2. * FPS)
        super(Menu, self).on_pre_enter(*args)

    def on_pre_leave(self, *args):
        Clock.unschedule(self._update_event)
        super(Menu, self).on_pre_leave(*args)

    def update(self, dt):
        x, y = Window.mouse_pos
        buttons = [
            self.but_launch,
            # self.but2,
            self.but3,
        ]

        for button in buttons:
            if button.collide_point(x, y):
                button.font_size = 70
                button.color = (1, 0.8, 0.1, 1)
            else:
                button.font_size = 50
                button.color = (1, 1, 1, 1)
