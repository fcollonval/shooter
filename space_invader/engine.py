from random import randint, uniform
from time import time

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager

from enemies import EnemyHive
from playership import PlayerShip


class ActorsContainer(FloatLayout):
    player = ObjectProperty(None, allownone=True)
    enemies = ObjectProperty(None)

    game_start_time = NumericProperty(0)
    debris = ListProperty()
    player_lives = NumericProperty(0)
    score = NumericProperty(0)

    options = DictProperty({"start_lives": 1})

    def __init__(self, **kwargs):
        super(ActorsContainer, self).__init__(**kwargs)
        self.enemies = EnemyHive()

    def on_player_lives(self, instance, value):
        if value == 0:
            # TODO should be moved in PlayerShip    
            if self.player is not None:
                self.remove_widget(self.player)

            info = Label(text="Game over!", font_size=50, bold=True)
            self.add_widget(info)

    def init_game(self):
        if self.player_lives == 0:
            self.game_start_time = time()
            self.player_lives = self.options["start_lives"]
            self.score = 0
            self.game_start_time = time()
            self.clear_widgets()
            self.player = PlayerShip(space_game=self, x=self.width / 2, y=30)
            self.add_widget(self.player)

    def update_game(self, dt):
        # for child in self.children:
        #     if hasattr(
        #         child, "update"
        #     ):  # TODO as actor inherit from the same class? better use Animation
        #         child.update()

        # for bullet in self.pbullets:
        #     for enemy in self.enemies:
        #         if bullet.check_collision(enemy):
        #             self.score += 10

        # for bullet in self.ebullets:
        #     bullet.check_collision(self.player)

        # for enemy in self.enemies:
        #     enemy.check_collision(self.player)

        if len(self.enemies) < int((time() - self.game_start_time) / 10) + 1:
            enemy = self.enemies.add_enemy(
                space_game=self,
                x=randint(0, self.width),
                y=self.height + 50,
                velocity_y=uniform(-2, -1) * 60,
                velocity_x=uniform(-2, 2) * 60,
            )
            self.add_widget(enemy)
            enemy.move()


class SpaceGame(Screen):
    container = ObjectProperty(None)
    menu = ObjectProperty(None)

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
        self.menu.but_launch.text = "Survival Mode"
        if self.container.player_lives > 0:
            self.menu.but_launch.text = "Resume"
        super(SpaceGame, self).on_pre_leave(*args)


class ShooterGame(ScreenManager):
    start_lives = NumericProperty(1)

    def __init__(self, **kwargs):
        kwargs["transition"] = FadeTransition()
        super(ShooterGame, self).__init__(**kwargs)
        self.bg_music = None  # SoundLoader.load('music.ogg')
        if self.bg_music:
            self.bg_music.play()
            self.bg_music.loop = True
