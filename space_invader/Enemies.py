import math
from random import choice, randint, random, uniform
from time import time

from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from bullets import EnemyBullet
from misc_objects import Debris
from spaceship import Actor, SpaceShip, SpaceShipHive


class EnemyShip(SpaceShip, Actor):
    def __init__(self, space_game, **kwargs):
        SpaceShip.__init__(self, space_game)
        Actor.__init__(self, **kwargs)
        self.min_y = 200
        self.boom = None  # SoundLoader.load('boom.ogg')

    def move(self):
        super(EnemyShip, self).move()
        Clock.schedule_once(
            self.shot, self.gun_cooldown_time + self.gun_fire_interval * random()
        )

    def on_stop(self, animation, widget):
        if self.center_y == self.min_y:
            self.animation.cancel_all(self)
            self.velocity_y *= -1.0
            if self.parent is None:
                self.alive = False
            else:
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
                tmp_debris = Debris(
                    x=x,
                    y=y,
                    velocity_x=choice(dirs) * 60.0,
                    velocity_y=choice(dirs) * 60.0,
                )
                self.parent.add_widget(tmp_debris)

            self.parent.remove_widget(self)

    def collide_ammo(self, ammo):
        if self.collide_widget(ammo) and self.alive:
            self.space_game.player.score += 10
            self.alive = False
            return True
        return False


class EnemyHive(SpaceShipHive):
    def __init__(self, space_game):
        super(EnemyHive, self).__init__(space_game)
        self.start_time = time()
        Clock.schedule_once(lambda dt: self.add_enemy(dt), random())

    def add_enemy(self, dt):
        if self.space_game.player.alive:
            enemy = EnemyShip(
                self.space_game,
                x=randint(0, self.space_game.width),
                y=self.space_game.height + 50,
                velocity_y=uniform(-2, -1) * 60,
                velocity_x=uniform(-2, 2) * 60,
            )
            self.space_game.add_widget(enemy)
            enemy.move()
            self.hive.append(enemy)
        Clock.schedule_once(
            # TODO decrease time interval between two calls
            self.add_enemy,
            random(),
        )
