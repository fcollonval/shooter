from random import uniform
from time import time

from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from bullets import PlayerBullet


class Gun(Widget):

    def __init__(self, **kwargs):
        super(Gun, self).__init__(**kwargs)
        self.gun_fire_interval = 0.3


class RepeaterGun(Gun):
    space_game = ObjectProperty(None)
    level = 1
    bullet_strength = 70

    def __init__(self, **kwargs):
        super(RepeaterGun, self).__init__(**kwargs)
        self.gun_fire_interval = 0.3
        self.gun_cooldown = time()
        self.laser = None  # SoundLoader.load('laser.ogg')
        # self.laser.stop()
        # self.laser.loop = False

    def shoot(self):
        ret = True

        if self.parent.gun_level == 1:
            self.gun_fire_interval = 0.3
            bullet_speed = 6 * 60
            bullet_damage = 100
            bullet_angle = uniform(-0.3, 0.3) * 60

            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()

                bullet = PlayerBullet(
                    self.space_game.enemies,
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_x=bullet_angle,
                    velocity_y=bullet_speed,
                )
                self.space_game.add_widget(bullet)
                bullet.fire()
                self.gun_cooldown = time() + self.gun_fire_interval
                self.parent.score -= 1

        elif self.parent.gun_level == 2:
            self.gun_fire_interval = 0.15
            bullet_speed = 7 * 60
            bullet_damage = 100
            bullet_angle = uniform(-0.3, 0.3) * 60
            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()
                bullet = PlayerBullet(
                    self.space_game.enemies,
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_y=bullet_speed,
                    # velocity_x=bullet_angle,
                )
                self.space_game.add_widget(bullet)
                bullet.fire()
                self.gun_cooldown = time() + self.gun_fire_interval
                self.parent.score -= 1

        return ret


class SpreadGun(Gun):
    gun_cooldown = 0

    def __init__(self, **kwargs):
        super(SpreadGun, self).__init__(**kwargs)
        self.gun_cooldown = time()
        self.laser = None  # SoundLoader.load('laser.ogg')

    def shoot(self):
        ret = True

        if self.parent.gun_level == 1:
            self.gun_fire_interval = 0.4
            bullet_speed = 360
            bullet_damage = 100
            bullet_angle = -300

            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()
                bullet = PlayerBullet(
                    self.space_game.enemies,
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_y=bullet_speed,
                    velocity_x=0,
                )
                self.space_game.add_widget(bullet)
                bullet.fire()

                for _ in range(2):
                    bullet = PlayerBullet(
                        self.space_game.enemies,
                        x=self.parent.center_x,
                        y=self.parent.top,
                        velocity_y=bullet_speed,
                        velocity_x=bullet_angle,
                        health=bullet_damage,
                    )
                    self.space_game.add_widget(bullet)
                    bullet.fire()
                    bullet_angle += 10

                self.gun_cooldown = time() + self.gun_fire_interval
                self.parent.score -= 1

        elif self.parent.gun_level == 2:
            self.gun_fire_interval = 0.35
            bullet_speed = 360
            bullet_damage = 100
            bullet_angle = -7.5 * 60

            if time() > self.gun_cooldown:
                if self.laser:
                    self.laser.play()

                bullet = PlayerBullet(
                    self.space_game.enemies,
                    x=self.parent.center_x,
                    y=self.parent.top,
                    velocity_y=bullet_speed,
                    velocity_x=0,
                )
                self.space_game.add_widget(bullet)
                bullet.fire()
                for _ in range(4):
                    bullet = PlayerBullet(
                        self.space_game.enemies,
                        x=self.parent.center_x,
                        y=self.parent.top,
                        velocity_y=bullet_speed,
                        velocity_x=bullet_angle,
                    )
                    self.space_game.add_widget(bullet)
                    bullet.fire()
                    bullet_angle += 5

                self.gun_cooldown = time() + self.gun_fire_interval
                self.parent.score -= 1

        return ret
