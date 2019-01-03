import math 
from kivy.properties import BooleanProperty

from spaceship import Actor


class Bullet(Actor):
    alive = BooleanProperty(True)

    def __init__(self, target, **kwargs):
        """
        Args:
            target: Spaceship(s) targeted
        """        
        super(Bullet, self).__init__(**kwargs)
        self._target = target

    def fire(self):
        self.move()

    def on_start(self, animation, widget):
        # TODO add here animation of fire
        pass

    def on_progress(self, animation, widget, progression):
        # TODO
        # if self.target.collide_ammo(self):
        #     self.animation.stop(self)
        pass

    def on_stop(self, animation, widget):
        super(Bullet, self).on_stop(animation, widget)

    # def check_collision(self, target):
    #     ret = False
    #     if target.collide_point(self.center_x, self.center_y):
    #         target.health -= self.health
    #         self.health = 0
    #         ret = True
    #     return ret


class PlayerBullet(Bullet):
    pass


class EnemyBullet(Bullet):
    pass
