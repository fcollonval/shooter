import math
from random import randint, random, uniform
from time import time

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp

from bullets import EnemyBullet
from constants import FPS, FX_VOLUME
from spaceship import Actor, SpaceShip, SpaceShipHive
from utils import load_sound

PERIOD = 10.0  # Time elapse after which more enemies will be on the screen


class EnemyShip(SpaceShip, Actor):
    def __init__(self, space_game, **kwargs):
        SpaceShip.__init__(self, space_game)
        Actor.__init__(self, **kwargs)
        self.min_y = dp(200)
        self.boom = load_sound("sounds/boom.ogg", volume=FX_VOLUME)

    def move(self):
        super(EnemyShip, self).move()
        Clock.schedule_once(
            self.shot, self.gun_cooldown_time + 2. * self.gun_fire_interval * random()
        )

    def on_stop(self, animation, widget):
        self.animation.cancel_all(self)

        if self.parent is None:
            self.alive = False
        else:
            width, height = self.parent.size
            if self.top > height or self.y < self.min_y:
                self.velocity_y *= -1.0
            if self.right > width or self.x < 0.:
                self.velocity_x *= -1.0
            super(EnemyShip, self).move()

    def shot(self, dt):
        if self.alive and self.parent is not None:
            bullet = EnemyBullet(
                self.space_game.player,
                velocity_y=-240,
            )
            self.space_game.add_widget(bullet)
            bullet.center_x = self.center_x
            bullet.y = self.y
            bullet.fire()
            Clock.schedule_once(
                self.shot, self.gun_cooldown_time + self.gun_fire_interval * random()
            )

    def collide_ammo(self, ammo):
        if self.collide_widget(ammo) and self.alive:
            self.space_game.player.score += 10
            self.alive = False
            return True
        return False


class EnemyHive(SpaceShipHive):
    # Generator algorithm
    #   try to have n_enemies = passed time since beginning in decaseconds
    #   i.e. at 44s: Generate enemies to have 4 enemies in the game

    def __init__(self, space_game):
        super(EnemyHive, self).__init__(space_game)

    def add_enemy(self):
        dt = time() - self.start_time
        target_n = int(dt / 10.0) + 1
        remaining_time = max(FPS, 10.0 - dt % 10)

        for i, ship in enumerate(self.hive):
            # Clean the list of alive enemy here, some may die by reaching screen edges
            if not ship.alive:
                self.hive.pop(i)

        if self.space_game.player.alive and len(self.hive) < target_n:
            half_w = self.width
            enemy = EnemyShip(
                self.space_game,
                center=(
                    randint(half_w, self.space_game.width - half_w),
                    self.space_game.height + dp(50),
                ),
                velocity_y=uniform(-2, -1) * 60,
                velocity_x=uniform(-2, 2) * 60,
            )
            self.space_game.add_widget(enemy)
            enemy.move()
            self.hive.append(enemy)

        Clock.schedule_once(
            lambda dt: self.add_enemy(), remaining_time / (target_n + 1)
        )
