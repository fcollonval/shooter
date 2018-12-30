from random import randint, uniform
from time import time

from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from enemies import EnemyShip
from menus import GameOver, PauseMenu, StartMenu
from playership import PlayerShip


class ShooterGame(Widget):
    pbullets = []
    ebullets = []
    enemies = []
    debris = []
    keyboard_inputs = []
    game_state = "start_menu"
    player_lives = 1
    start_lives = 1
    player_dead = False
    dead_time = 0
    score = 0
    game_start_time = 0
    game_mode = "survival"

    def __init__(self, width, height, **kwargs):
        super(ShooterGame, self).__init__(**kwargs)
        self.width = width
        self.height = height
        self.game_start_time = time()
        self.bg_music = None  # SoundLoader.load('music.ogg')
        if self.bg_music:
            self.bg_music.play()
            self.bg_music.loop = True

    def game_update(self, dt):
        ret = True
        pbullets = []
        ebullets = []
        enemies = []
        players = []

        if self.game_state == "start_menu":
            start_menu = StartMenu()
            start_menu.width = self.width
            start_menu.height = self.height
            self.add_widget(start_menu)
            ret = False
        elif self.game_state == "game_over":
            gameover_menu = GameOver()
            gameover_menu.width = self.width
            gameover_menu.height = self.height
            self.add_widget(gameover_menu)
            ret = False
        elif self.game_state == "pause_menu":
            pause_menu = PauseMenu()
            pause_menu.width = self.width
            pause_menu.height = self.height
            self.add_widget(pause_menu)
            ret = False
        elif self.game_state == "loading":
            self.player_lives = self.start_lives
            self.score = 0
            self.game_start_time = time()
            self.game_state = "playing"
            for child in self.children:
                self.remove_widget(child)
            player1 = PlayerShip(self.width / 2, 30)
            self.add_widget(player1)

            self.score_label = Label(text="Score: " + str(self.score))
            self.score_label.x = 0
            self.score_label.y = 0
            self.add_widget(self.score_label)

            self.lives_label = Label(text="Lives: " + str(self.player_lives))
            self.lives_label.x = self.width - 200
            self.lives_label.y = 0
            self.add_widget(self.lives_label)
        elif self.game_state == "playing":

            for child in self.children:
                child_name = None
                try:
                    child_name = child.name
                    if child.update():
                        if child_name == "pbullet":
                            pbullets.append(child)
                        elif child_name == "ebullet":
                            ebullets.append(child)
                        elif child_name == "enemy":
                            enemies.append(child)
                        elif child_name == "player":
                            players.append(child)
                except:
                    pass

            for bullet in pbullets:
                for enemy in enemies:
                    if bullet.check_collision(enemy):
                        self.score += 10

            for bullet in ebullets:
                for player in players:
                    bullet.check_collision(player)

            for player in players:
                for enemy in enemies:
                    enemy.check_collision(player)

            if self.player_dead == True and time() > self.dead_time + 3:
                if self.player_lives <= 0:
                    self.player_dead = False
                    self.game_state = "game_over"
                    for child in self.children:
                        self.remove_widget(child)
                else:
                    self.player_dead = False
                    player1 = PlayerShip(self.width / 2, 30)
                    self.add_widget(player1)

            if self.game_mode == "survival":
                if len(enemies) < int((time() - self.game_start_time) / 10) + 1:
                    enemy = EnemyShip(randint(0, self.width), self.height + 50)
                    enemy.velocity_y = uniform(-2, -1)
                    enemy.velocity_x = uniform(-2, 2)
                    self.add_widget(enemy)

            self.score_label.text = "Score: " + str(self.score)
            self.lives_label.text = "Lives: " + str(self.player_lives)

        return ret
