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
from kivy.lang import Builder

Builder.load_file('style.kv')

from bullets import EnemyBullet, PlayerBullet
from enemies import Debris, EnemyShip
from engine import ShooterGame, SpaceGame
from game_ui import IconButton
from menu import Menu
from playership import PlayerShip

Builder.load_file('menu.kv')
Builder.load_file('credits.kv')

class ShooterApp(App):
    def build(self):
        return ShooterGame(width=WIDTH, height=HEIGHT)


if __name__ == "__main__":
    ShooterApp().run()
