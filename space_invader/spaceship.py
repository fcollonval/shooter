from itertools import cycle
import math
from random import choice

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
    ReferenceListProperty,
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from constants import EPS, MARGIN, FPS, PROPULSION_FREQUENCY
from misc_objects import Debris


class Actor(Widget):
    min_y = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):
        super(Actor, self).__init__(**kwargs)
        self.animation = None

    def move(self):
        # Cannot be done in __init__ as the parent needs to be set
        # to start the animation (screen size needed)
        if self.parent is None:
            raise RuntimeError("{} needs a parent to be animated.".format(type(self).__qualname__))
        vx = self.velocity_x + EPS
        vy = self.velocity_y + EPS
        width, height = self.parent.size
        d_x = math.inf
        d_y = math.inf
        if abs(self.velocity_x) > EPS:
            d_x = max((width + MARGIN - self.x) / vx, -(self.right + MARGIN) / vx)
            new_x = max(
                math.copysign(width + MARGIN, self.velocity_x),
                math.copysign(MARGIN, self.velocity_x),
            )            
        if abs(self.velocity_y) > EPS:
            d_y = max(
                (height + MARGIN - self.y) / vy, (self.min_y - self.top) / vy
            )
            new_y = max(
                math.copysign(height + MARGIN, self.velocity_y),
                math.copysign(self.min_y, - self.velocity_y),
            )
        
        props = {}
        if d_x < d_y:
            if math.isfinite(d_y):
                props["center_y"] = self.center_y + d_x * self.velocity_y
            props["center_x"] = new_x
            props["duration"] = d_x
        else:
            if math.isfinite(d_x):
                props["center_x"] = self.center_x + d_y * self.velocity_x
            props["center_y"] = new_y
            props["duration"] = d_y

        self.animation = Animation(**props, step=FPS)
        if self.animation is not None:
            self.animation.bind(on_start=self.on_start)
            self.animation.bind(on_progress=self.on_progress)
            self.animation.bind(on_complete=self.on_stop)
            self.animation.start(self)

    def on_start(self, animation, widget):
        pass

    def on_progress(self, animation, widget, progression):
        pass

    def on_stop(self, animation, widget):
        self.animation.cancel_all(self)
        if self.parent is not None:
            self.parent.remove_widget(self)


class SpaceShip(Widget):
    orientation = NumericProperty(180)
    space_game = ObjectProperty(None)
    propulsion_texture = ObjectProperty(CoreImage("atlas://img/space_invader/spaceEffects_005").texture)
    REACTOR_SPRITE = [
            CoreImage("atlas://img/space_invader/spaceEffects_005").texture,
            CoreImage("atlas://img/space_invader/spaceEffects_006").texture,
            CoreImage("atlas://img/space_invader/spaceEffects_007").texture,
            CoreImage("atlas://img/space_invader/spaceEffects_006").texture,
        ]
    alive = BooleanProperty(True)

    gun_cooldown_time = NumericProperty(0.1)
    gun_fire_interval = NumericProperty(2.4)

    def __init__(self, space_game, **kwargs):
        self.space_game = space_game
        self.propulsion = cycle(SpaceShip.REACTOR_SPRITE)
        self.propulsion_counter = 0
        super(SpaceShip, self).__init__(**kwargs)
        self.event = Clock.schedule_interval(self.animate_propulsion, FPS)
    
    def on_alive(self, instance, value):
        if not self.alive:
            if self.event is not None:
                self.event.cancel()

            if self.parent is not None:
                Animation.cancel_all(self)
                if self.boom:
                    self.boom.play()
                self.add_debris()

                self.parent.remove_widget(self)

    def add_debris(self):
        dirs = [-2, -1, 0, 1, 2]
        for _ in range(10):
            tmp_debris = Debris(
                velocity_x=choice(dirs) * 60.0,
                velocity_y=choice(dirs) * 60.0,
            )
            self.parent.add_widget(tmp_debris)
            tmp_debris.center = self.center
            tmp_debris.launch()

    def collide_ammo(self, ammo):
        raise NotImplementedError()

    def animate_propulsion(self, dt):

        self.propulsion_counter += 1
        if self.propulsion_counter % PROPULSION_FREQUENCY == 0:
            self.propulsion_texture = next(self.propulsion)


class SpaceShipHive(SpaceShip):
    def __init__(self, space_game):
        super(SpaceShipHive, self).__init__(space_game)
        self.hive = list()  # List[SpaceShip]

    def __len__(self):
        return len(self.hive)

    def collide_ammo(self, ammo):
        for i, ship in enumerate(self.hive):
            impact = ship.collide_ammo(ammo)
            if impact:
                self.hive.pop(i)
                return True
        return False

    def clear(self):
        self.hive.clear()
