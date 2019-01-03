from kivy.animation import Animation
from kivy.properties import (
    BoundedNumericProperty,
    NumericProperty,
)
from kivy.uix.floatlayout import FloatLayout

from spaceship import FPS


class Debris(FloatLayout):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    red = BoundedNumericProperty(1.0, min=0.0, max=1.0)
    green = BoundedNumericProperty(0.5, min=0.0, max=1.0)

    DURATION = 25.

    def __init__(self, **kwargs):
        super(Debris, self).__init__(**kwargs)
        a = Animation(
            center_x=self.center_x + self.DURATION * FPS * self.velocity_x,
            center_y=self.center_y + self.DURATION * FPS * self.velocity_y,
            height=7.5,
            red=0.5 * self.red,
            green=0.0,
            d=self.DURATION * FPS,
            s=FPS,
        )
        a.bind(on_complete=self.on_stop)
        a.start(self)

    def on_stop(self, animation, widget):
        if self.parent is not None:
            self.parent.remove_widget(self)
