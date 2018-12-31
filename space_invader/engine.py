# from enum import IntEnum
from random import randint, uniform
from time import time

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    ListProperty,
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty,
    DictProperty,
)

from enemies import EnemyShip
from playership import PlayerShip


# class GameState(IntEnum):
#     START = 0
#     PAUSE = 1
#     PLAY = 2
#     OPTIONS = 3


class ActorsContainer(FloatLayout):
    game_start_time = NumericProperty(0)
    player = ObjectProperty(None)
    pbullets = ListProperty()
    ebullets = ListProperty()
    enemies = ListProperty()
    debris = ListProperty()
    player_lives = NumericProperty(0)
    player_dead = BooleanProperty(True)
    dead_time = NumericProperty(0)
    score = NumericProperty(0)

    options = DictProperty({"start_lives": 1})

    def init_game(self):
        if self.player_lives == 0:
            self.player_lives = self.options["start_lives"]
            self.score = 0
            self.game_start_time = time()
            self.clear_widgets()
            self.player = PlayerShip(x=self.width / 2, y=30)
            self.add_widget(self.player)

    def update_game(self, dt):
        pbullets = []
        ebullets = []

        for child in self.children:
            child_name = None
            try:
                child_name = child.name
                if child.update():
                    if child_name == "pbullet":
                        pbullets.append(child)
                    elif child_name == "ebullet":
                        ebullets.append(child)
            except:
                pass

        for bullet in pbullets:
            for enemy in self.enemies:
                if bullet.check_collision(enemy):
                    self.score += 10

        for bullet in ebullets:
            bullet.check_collision(self.player)

        for enemy in self.enemies:
            enemy.check_collision(self.player)

        if self.player_dead == True and time() > self.dead_time + 3:
            if self.player_lives <= 0:
                self.player_dead = False
                self.clear_widgets()

        if len(self.enemies) < int((time() - self.game_start_time) / 10) + 1:
            enemy = EnemyShip(randint(0, self.width), self.height + 50, space_game=self)
            enemy.velocity_y = uniform(-2, -1)
            enemy.velocity_x = uniform(-2, 2)
            self.enemies.append(enemy)
            self.add_widget(enemy)


class SpaceGame(Screen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SpaceGame, self).__init__(**kwargs)
        self._update_event = None

    def on_pre_enter(self, *args):
        self.container.init_game()
        self._update_event = Clock.schedule_interval(
            self.container.update_game, 1.0 / 60.0
        )
        super(SpaceGame, self).on_pre_enter(*args)

    def on_pre_leave(self, *args):
        self._update_event.cancel()
        super(SpaceGame, self).on_pre_leave(*args)


class ShooterGame(ScreenManager):
    start_lives = NumericProperty(1)

    def __init__(self, **kwargs):
        super(ShooterGame, self).__init__(**kwargs)
        self.game_start_time = time()
        self.bg_music = None  # SoundLoader.load('music.ogg')
        if self.bg_music:
            self.bg_music.play()
            self.bg_music.loop = True
