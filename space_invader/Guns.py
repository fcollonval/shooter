from random import uniform
from time import time

from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from bullets import PlayerBullet


class RepeaterGun(Widget):    
    space_game = ObjectProperty(None)
    name = "pgun"
    level = 1
    gun_cooldown = 0
    gun_fire_interval = 0.3
    bullet_strength = 70

    def __init__(self, **kwargs):
        super(RepeaterGun, self).__init__(**kwargs)
        self.gun_cooldown = time()
        self.laser = None  # SoundLoader.load('laser.ogg')
        # self.laser.stop()
        # self.laser.loop = False

    def shoot(self):
        ret = True

        if self.parent.gun_level == 1:
            gun_fire_interval = 0.3
            bullet_speed = 6
            bullet_damage = 100
            bullet_angle = uniform(-0.3, 0.3)

            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()
                self.space_game.add_player_bullet(
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_x=bullet_angle,
                    velocity_y=bullet_speed,
                    health=bullet_damage,
                )
                self.gun_cooldown = time() + gun_fire_interval
                self.parent.parent.score -= 1

        elif self.parent.gun_level == 2:
            gun_fire_interval = 0.15
            bullet_speed = 7
            bullet_damage = 100
            bullet_angle = uniform(-0.3, 0.3)
            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()
                self.space_game.add_player_bullet(
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_y=bullet_speed,
                    velocity_x=bullet_angle,
                    health=bullet_damage,
                )
                self.gun_cooldown = time() + gun_fire_interval
                self.parent.parent.score -= 1

        return ret


class SpreadGun(Widget):
    name = "pgun"
    gun_cooldown = 0

    def __init__(self, **kwargs):
        super(SpreadGun, self).__init__(**kwargs)
        self.gun_cooldown = time()
        self.laser = None  # SoundLoader.load('laser.ogg')

    def shoot(self):
        ret = True

        if self.parent.gun_level == 1:
            gun_fire_interval = 0.4
            bullet_speed = 6
            bullet_damage = 100
            bullet_angle = -5

            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()
                self.space_game.add_player_bullet(
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_y=bullet_speed,
                    velocity_x=0,
                    health=bullet_damage,
                )
                
                for _ in range(2):
                    self.space_game.add_player_bullet(
                        x=self.parent.center_x,
                        y=self.parent.top,
                        velocity_y=bullet_speed,
                        velocity_x=bullet_angle,
                        health=bullet_damage,
                    )
                    bullet_angle += 10

                self.gun_cooldown = time() + gun_fire_interval
                self.space_game.score -= 1

        elif self.parent.gun_level == 2:
            gun_fire_interval = 0.35
            bullet_speed = 6
            bullet_damage = 100
            bullet_angle = -7.5

            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()
                self.space_game.add_player_bullet(
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_y=bullet_speed,
                    velocity_x=0,
                    health=bullet_damage,
                )
                for _ in range(4):
                    self.space_game.add_player_bullet(
                        x=self.parent.center_x,
                        y=self.parent.top,
                        velocity_y=bullet_speed,
                        velocity_x=bullet_angle,
                        health=bullet_damage,
                    )
                    bullet_angle += 5

                self.gun_cooldown = time() + gun_fire_interval
                self.space_game.score -= 1

        return ret
