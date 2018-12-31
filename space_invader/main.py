#!/usr/bin/env python
from kivy.config import Config

# Config.set should be used before importing any other Kivy modules
# src: https://kivy.org/doc/stable/api-kivy.config.html
WIDTH = 800
HEIGHT = 600
Config.set("graphics", "width", WIDTH)
Config.set("graphics", "height", HEIGHT)
Config.set("kivy", "keyboard_mode", "system")

from kivy.app import App
from kivy.clock import Clock

from engine import ShooterGame, SpaceGame
from menu import Menu
from playership import PlayerShip
from enemies import Debris, EnemyShip
from bullets import EnemyBullet, PlayerBullet


class ShooterApp(App):
    def build(self):
        game = ShooterGame(WIDTH, HEIGHT)
        # Clock.schedule_interval(game.game_update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    ShooterApp().run()
