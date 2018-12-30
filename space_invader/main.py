#!/usr/bin/env python

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config

from engine import ShooterGame

WIDTH = 800
HEIGHT = 600
Config.set("graphics", "width", WIDTH)
Config.set("graphics", "height", HEIGHT)
Config.write()


class ShooterApp(App):
    def build(self):
        global WIDTH
        global HEIGHT
        game = ShooterGame(WIDTH, HEIGHT)
        Clock.schedule_interval(game.game_update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    ShooterApp().run()
