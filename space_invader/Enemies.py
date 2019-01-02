from random import choice
from time import time

from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from misc_objects import Debris


class EnemyShip(Widget):
    space_game = ObjectProperty(None)
    name = "enemy"
    min_y = NumericProperty(200)
    health = NumericProperty(100)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    gun_cooldown = time()
    gun_fire_interval = 1.2

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):
        super(EnemyShip, self).__init__(**kwargs)
        self.boom = None  # SoundLoader.load('boom.ogg')

    def spawn_debris(self, x, y):
        dirs = [-2, -1, 0, 1, 2]
        for _ in range(10):
            tmp_debris = Debris(x, y)
            tmp_debris.velocity_x = choice(dirs)
            tmp_debris.velocity_y = choice(dirs)
            self.space_game.add_widget(tmp_debris)

    def check_collision(self, target):
        if target.collide_widget(self):
            target.health -= self.health
            self.health = 0

    def update(self):
        ret = True
        self.pos = Vector(*self.velocity) + self.pos
        if time() > self.gun_cooldown:
            self.space_game.add_enemy_bullet(x=self.x + self.width / 2, y=self.y, velocity_y=-240)
            self.gun_cooldown = time() + self.gun_fire_interval

        if self.y < self.min_y and self.velocity_y < 0:
            self.velocity_y *= -1
        if (
            self.y > self.space_game.top + 100
            or self.y < -100
            or self.x > self.space_game.width + 100
            or self.x < -100
        ):
            ret = False
        elif self.health <= 0:
            self.spawn_debris(self.x, self.y)
            if self.boom:
                self.boom.play()
            ret = False
        if ret == False:
            self.space_game.remove_enemy(self)
        return ret
