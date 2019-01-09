import math
from random import choice
import sys
from time import time

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.vector import Vector

from guns import RepeaterGun
from misc_objects import Debris
from spaceship import SpaceShip, FPS
from utils import load_sound

DPI = dp(96)


class PlayerShip(SpaceShip):
    lives = NumericProperty(0)
    score = NumericProperty(0)

    gun_cooldown = time()
    bullet_strength = 70
    gun_level = 2
    vel = 4

    keyboard_inputs = []
    _keyboard = None

    def __init__(self, space_game, **kwargs):
        SpaceShip.__init__(self, space_game, **kwargs)
        self.score = 0
        self.gun_fire_interval = 0.1
        if self._keyboard == None and platform not in ("android", "ios"):
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)
            self._keyboard.bind(on_key_up=self._on_key_up)

        self.gun = RepeaterGun(space_game=self.space_game)
        self.add_widget(self.gun)
        self.gun.center_x = self.center_x
        self.gun.center_y = self.center_y
        self.boom = load_sound('sounds/boom.ogg')

        # Add touch events layer
        self.player_speed = Vector(0, 0)
        self.bullet_rate = 0.0
        self.player_motion = None
        self.bullet_fire = None
        touch_layer = FloatLayout(pos_hint=(0, 0), size_hint=(1., 1.))
        touch_layer.bind(
            on_touch_down=self.on_touch_down,
            on_touch_move=self.on_touch_move,
            on_touch_up=self.on_touch_up,
        )
        self.add_widget(touch_layer)

        self._update_event = Clock.schedule_interval(self.update, FPS)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers, *args):
        commands = ["a", "s", "d", "w", "spacebar", "escape"]
        if keycode[1] in commands and keycode[1] not in self.keyboard_inputs:
            self.keyboard_inputs.append(keycode[1])
            # Return True to accept the key. Otherwise, it will be used by
            # the system.
        return True

    def _on_key_up(self, keyboard, keycode, *args):
        commands = ["a", "s", "d", "w", "spacebar", "escape"]
        if keycode[1] in commands:
            try:
                self.keyboard_inputs.remove(keycode[1])
            except:
                pass
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def on_touch_down(self, touch):
        vec = Vector(touch.x, touch.y)
        if touch.x < self.parent.center_x:
            touch.ud["lstick"] = vec
        else:
            touch.ud["rstick"] = vec
        return True

    def on_touch_move(self, touch):
        # print("in on_touch_move")
        vec = Vector(touch.x, touch.y)
        if touch.ud.get("lstick", None) is not None:
            r = vec - touch.ud["lstick"]
            if self.player_motion is not None:
                self.player_motion.cancel()  # Cancel previously set trigger
            # Presume screen DPI => 1inch max. should match more than 4
            # print(r)
            self.player_speed = r * 6 / DPI
            self.player_motion = Clock.schedule_interval(
                lambda dt: self.move(self.player_speed), FPS
            )
        elif touch.ud.get("rstick", None) is not None:
            r = vec - touch.ud["rstick"]
            if self.bullet_fire is not None:
                self.bullet_fire.cancel()  # Cancel previously set trigger
            self.bullet_rate = (1.0 - self.gun.gun_fire_interval) * math.exp(
                -5 * r.length() / DPI
            ) + self.gun.gun_fire_interval
            self.bullet_fire = Clock.schedule_interval(
                lambda dt: self.gun.shoot(), self.bullet_rate
            )
        return True

    def on_touch_up(self, touch):
        # print("in up ", touch.ud, self.bullet_fire)
        if touch.ud.get("lstick", None) is not None:
            if self.player_motion is not None:
                self.player_motion.cancel()
            touch.ud["lstick"] = None
        elif touch.ud.get("rstick", None) is not None:
            if self.bullet_fire is not None:
                self.bullet_fire.cancel()
            touch.ud["rstick"] = None
        return True

    def on_lives(self, instance, value):
        self.alive = self.lives != 0

    def on_alive(self, instance, value):
        if not self.alive and self.parent is not None:
            if self.player_motion is not None:
                Clock.unschedule(self.player_motion)
            if self.bullet_fire is not None:
                Clock.unschedule(self.bullet_fire)

            if self.boom:
                self.boom.play()

            dirs = [-2, -1, 0, 1, 2]
            for _ in range(15):
                tmp_debris = Debris(
                    velocity_x=choice(dirs) * 60.0,
                    velocity_y=choice(dirs) * 60.0,
                )
                self.parent.add_widget(tmp_debris)
                tmp_debris.center = self.center
                tmp_debris.launch()

            info = Label(
                text="Game over!",
                font_size=sp(50),
                bold=True,
            )
            self.parent.add_widget(info)
            self.parent.remove_widget(self)

    def collide_ammo(self, ammo):
        if self.collide_widget(ammo) and self.alive:
            self.lives -= 1
            return True
        return False

    def move(self, speed):
        value = speed + self.center
        half_w = 0.5 * self.width
        half_h = 0.5 * self.height
        self.center = (
            min(max(half_w, value[0]), self.space_game.width - half_w),
            min(max(half_h, value[1]), self.space_game.height - half_h),
        )

    def reset(self, lives):
        self.center = self.parent.center_x, dp(30)
        self.lives = lives
        self.score = 0

    def update(self, dt):
        if self.parent is None:
            return

        velocity_x = 0
        velocity_y = 0
        if "a" in self.keyboard_inputs:
            velocity_x -= self.vel
        if "d" in self.keyboard_inputs:
            velocity_x += self.vel
        if "w" in self.keyboard_inputs:
            velocity_y += self.vel
        if "s" in self.keyboard_inputs:
            velocity_y -= self.vel

        if "spacebar" in self.keyboard_inputs:
            self.gun.shoot()

        self.move(Vector(velocity_x, velocity_y))
