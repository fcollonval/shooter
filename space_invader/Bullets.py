from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector


class PlayerBullet(Widget):
    space_game = ObjectProperty(None)
    name = "pbullet"
    health = NumericProperty(100)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(6)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def check_collision(self, target):
        ret = False
        if target.collide_point(self.center_x, self.center_y):
            target.health -= self.health
            self.health = 0
            ret = True
        return ret

    def update(self):
        ret = True
        self.pos = Vector(*self.velocity) + self.pos

        if (
            self.y > self.parent.top + 100
            or self.y < -100
            or self.x > self.parent.width + 100
            or self.x < -100
        ):
            ret = False
        elif self.health <= 0:
            ret = False
        if ret == False:
            self.space_game.remove_player_bullet(self)
        return ret


class EnemyBullet(Widget):
    space_game = ObjectProperty(None)
    name = "ebullet"
    health = NumericProperty(100)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(-4)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def check_collision(self, target):
        ret = False
        if target.collide_point(self.center_x, self.center_y):
            target.health -= self.health
            self.health = 0
            ret = True
        return ret

    def update(self):
        ret = True
        self.pos = Vector(*self.velocity) + self.pos

        if (
            self.y > self.parent.top + 100
            or self.y < -100
            or self.x > self.parent.width + 100
            or self.x < -100
        ):
            ret = False
        elif self.health <= 0:
            ret = False
        if ret == False:
            self.space_game.remove_enemy_bullet(self)
        return ret
