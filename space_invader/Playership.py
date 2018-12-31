from random import choice
from time import time

from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from guns import RepeaterGun
from misc_objects import Debris


class PlayerShip(Widget):
    name = "player"
    health = 100
    gun_cooldown = time()
    gun_fire_interval = 0.1
    bullet_strength = 70
    gun_level = 2
    vel = 4

    keyboard_inputs = []
    _keyboard = None

    def __init__(self, **kwargs):
        super(PlayerShip, self).__init__(**kwargs)
        if self._keyboard == None:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)
            self._keyboard.bind(on_key_up=self._on_key_up)

        self.gun = RepeaterGun()
        self.add_widget(self.gun)
        self.boom = None  # SoundLoader.load('boom.ogg')

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

    def spawn_debris(self, x, y):
        dirs = [-2, -1, 0, 1, 2]
        for _ in range(15):
            tmp_debris = Debris(x, y)
            tmp_debris.velocity_x = choice(dirs)
            tmp_debris.velocity_y = choice(dirs)
            self.parent.add_widget(tmp_debris)

    def update(self):
        ret = True

        if self.health <= 0:
            if self.boom:
                self.boom.play()
            self.spawn_debris(self.x, self.y)
            self.parent.player_lives -= 1

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

        value = Vector(velocity_x, velocity_y) + self.pos
        self.pos = (
            min(max(0, value[0]), self.parent.width - self.width),
            min(max(0, value[1]), self.parent.height - self.height),
        )

        return ret

