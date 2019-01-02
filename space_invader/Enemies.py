import math
from random import choice, random
from time import time

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from spaceship import Actor, SpaceShip, SpaceShipHive
from bullets import EnemyBullet
from misc_objects import Debris


class EnemyShip(SpaceShip, Actor):

    def __init__(self, **kwargs):
        Actor.__init__(self, **kwargs)
        SpaceShip.__init__(self)
        
        self.min_y = 200
        self.boom = None  # SoundLoader.load('boom.ogg')

    def move(self):
        super(EnemyShip, self).move()
        Clock.schedule_once(
            self.shot, self.gun_cooldown_time + self.gun_fire_interval * random()
        )

    def on_stop(self, instance, value):
        if self.center_y == self.min_y:
            self.animation.cancel_all(self)
            self.velocity_y *= -1.0
            super(EnemyShip, self).move()
        else:
            self.alive = False
            self.animation.cancel_all(self)

    def shot(self, dt):
        if self.alive:
            bullet = EnemyBullet(
                self.space_game.player,
                x=self.x + self.width / 2,
                y=self.y,
                velocity_y=-240,
            )
            self.space_game.add_widget(bullet)
            bullet.fire()
            Clock.schedule_once(
                self.shot, self.gun_cooldown_time + self.gun_fire_interval * random()
            )

    def on_alive(self, instance, value):
        if not self.alive and self.parent is not None:
            if self.boom:
                self.boom.play()
            x, y = (self.center_x, self.center_y)

            dirs = [-2, -1, 0, 1, 2]
            for _ in range(10):
                tmp_debris = Debris(x, y)
                tmp_debris.velocity_x = choice(dirs)
                tmp_debris.velocity_y = choice(dirs)
                self.parent.add_widget(tmp_debris)
            
            self.parent.remove_widget(self)

    def collide_ammo(self, ammo):
        pass

    # def check_collision(self, target):
    #     if target.collide_widget(self):
    #         target.health -= self.health
    #         self.health = 0


class EnemyHive(SpaceShipHive):
    def add_enemy(self, **kwargs):
        enemy = EnemyShip(**kwargs)
        self.hive.append(enemy)
        return enemy
