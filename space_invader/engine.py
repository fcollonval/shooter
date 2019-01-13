from time import time

from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp, Metrics
from kivy.properties import DictProperty, ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.vector import Vector

from enemies import EnemyHive
from playership import PlayerShip

from spaceship import FPS
from utils import load_sound


class ActorsContainer(FloatLayout):
    player = ObjectProperty(None, allownone=True)
    enemies = ObjectProperty(None)

    options = DictProperty({"start_lives": 3})

    def __init__(self, **kwargs):
        super(ActorsContainer, self).__init__(**kwargs)
        self.player = PlayerShip(self)
        self.enemies = EnemyHive(self)

    def init_game(self, pause_time):
        if self.player.lives == 0:
            self.clear_widgets()
            # Reset the player
            self.add_widget(self.player)
            self.player.reset(self.options["start_lives"])
            # Reset the hive
            self.enemies.clear()
            self.enemies.start_time = time()
            self.enemies.add_enemy()  # This call initiate a first enemy to start the hive growth
        else:
            self.enemies.start_time += pause_time


class Background(Widget):
    tx_space = ObjectProperty(None)
    SPEED = Vector(0.0, 0.2)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        t = CoreImage("img/bg/blue.png").texture
        t.wrap = "repeat"
        self.tx_space = t

    def on_size(self, instance, value):
        # Duplicate the background texture to fill the widget size
        self.tx_space.uvsize = (
            value[0] / dp(self.tx_space.width),
            value[1] / dp(self.tx_space.height),
        )
        self.property("tx_space").dispatch(self)  # Force update

    def update(self, dt):
        # Change the origin of the texture to emulate motion
        t = self.tx_space
        t.uvpos = (
            (t.uvpos[0] + dp(self.SPEED.x) * dt) % self.width,
            (t.uvpos[1] + dp(self.SPEED.y) * dt) % self.height,
        )
        self.property("tx_space").dispatch(self)  # Force update


class SpaceGame(Screen):
    background = ObjectProperty(None)
    container = ObjectProperty(None)
    lives = ObjectProperty(None)
    menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SpaceGame, self).__init__(**kwargs)
        self.leave_time = time()
        self.bg_event = None

    def on_pre_enter(self, *args):
        self.container.player.bind(lives=self.update_lives)
        self.container.init_game(time() - self.leave_time)
        self.bg_event = Clock.schedule_interval(self.update, FPS)
        super(SpaceGame, self).on_pre_enter(*args)

    def on_pre_leave(self, *args):
        self.bg_event.cancel()
        self.leave_time = time()
        self.container.player.unbind(lives=self.update_lives)
        self.menu.but_launch.text = "Play"
        if self.container.player.lives > 0:
            self.menu.but_launch.text = "Resume"
        super(SpaceGame, self).on_pre_leave(*args)

    def update(self, dt):
        self.background.update(dt)

    def update_lives(self, instance, value):
        self.lives.canvas.clear()
        WIDTH = dp(16)
        with self.lives.canvas:
            for i in range(value):
                Rectangle(
                    pos=(
                        self.lives.padding[0] * (i + 1) + i * WIDTH,
                        self.lives.padding[1] + self.lives.y,
                    ),
                    size=(WIDTH, dp(13)),
                    source="atlas://img/space_invader/playerLife1_blue",
                )


class ShooterGame(ScreenManager):
    def __init__(self, **kwargs):
        kwargs["transition"] = FadeTransition()
        super(ShooterGame, self).__init__(**kwargs)
        self.bg_music = load_sound("sounds/StarCommander1.ogg")
        if self.bg_music:
            self.bg_music.play()
            self.bg_music.loop = True
