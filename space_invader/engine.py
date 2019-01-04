from time import time

from kivy.core.audio import SoundLoader
from kivy.properties import DictProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager

from enemies import EnemyHive
from playership import PlayerShip


class ActorsContainer(FloatLayout):
    player = ObjectProperty(None, allownone=True)
    enemies = ObjectProperty(None)

    options = DictProperty({"start_lives": 1})

    def __init__(self, **kwargs):
        super(ActorsContainer, self).__init__(**kwargs)
        self.player = PlayerShip(self)
        self.enemies = EnemyHive(self)

    def init_game(self, pause_time):
        if self.player.lives == 0:
            self.clear_widgets()
            # Reset the player
            self.player.x = self.width / 2
            self.player.y = 30
            self.player.lives = self.options["start_lives"]
            self.add_widget(self.player)
            # Reset the hive
            self.enemies.clear()
            self.enemies.start_time = time()
            self.enemies.add_enemy()  # This call initiate a first enemy to start the hive growth
        else:
            self.enemies.start_time += pause_time


class SpaceGame(Screen):
    container = ObjectProperty(None)
    menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SpaceGame, self).__init__(**kwargs)
        self.leave_time = time()

    def on_pre_enter(self, *args):
        self.container.init_game(time() - self.leave_time)
        super(SpaceGame, self).on_pre_enter(*args)

    def on_pre_leave(self, *args):
        self.leave_time = time()
        self.menu.but_launch.text = "Play"
        if self.container.player.lives > 0:
            self.menu.but_launch.text = "Resume"
        super(SpaceGame, self).on_pre_leave(*args)


class ShooterGame(ScreenManager):
    def __init__(self, **kwargs):
        kwargs["transition"] = FadeTransition()
        super(ShooterGame, self).__init__(**kwargs)
        self.bg_music = None  # SoundLoader.load('music.ogg')
        if self.bg_music:
            self.bg_music.play()
            self.bg_music.loop = True
