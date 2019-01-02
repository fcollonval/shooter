import math 
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector

EPS = 1e-8  # Avoid dividing by zero
MARGIN = 100  # Number of pixels outside the screen for element displacement

class Bullet(Widget):
    health = NumericProperty(100)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    def __init__(self, target, **kwargs):
        """
        Args:
            target: Spaceship(s) targeted
        """        
        super(Bullet, self).__init__(**kwargs)
        self._target = target
        self._animation = None

    def fire(self):
        # Cannot be done in __init__ as the parent needs to be set
        # to start the animation (screen size needed)
        if self.parent is None:
            raise RuntimeError("Bullet needs a parent to be fired")
        vx = self.velocity_x + EPS
        vy = self.velocity_y + EPS
        width, height = self.parent.size
        tx = math.inf
        ty = math.inf
        animated_props = {}
        if abs(self.velocity_x) > EPS:
            tx = max((width + MARGIN - self.x) / vx, - (self.right + MARGIN) / vx)
            animated_props['center_x'] = max(math.copysign(width + MARGIN, self.velocity_x), math.copysign(MARGIN, self.velocity_x))
        if abs(self.velocity_y) > EPS:
            ty = max((height + MARGIN - self.y) / vy, - (self.top + MARGIN) / vy)
            animated_props['center_y'] = max(math.copysign(height + MARGIN, self.velocity_y), math.copysign(MARGIN, self.velocity_y))
            
        self.animation = Animation(**animated_props, duration=min(tx, ty))
        self.animation.bind(on_start=self.on_start)
        self.animation.bind(on_progress=self.on_progress)
        self.animation.bind(on_complete=self.on_stop)
        self.animation.start(self)

    def on_start(self, instance, value):
        # TODO add here animation of fire
        pass

    def on_progress(self, instance, value, progression):
        # TODO
        # if self.target.collide_ammo(self):
        #     self.animation.stop(self)
        pass

    def on_stop(self, instance, value):
        self.parent.remove_widget(self)

    # def check_collision(self, target):
    #     ret = False
    #     if target.collide_point(self.center_x, self.center_y):
    #         target.health -= self.health
    #         self.health = 0
    #         ret = True
    #     return ret

    # def update(self):
    #     ret = True
    #     self.pos = Vector(*self.velocity) + self.pos

    #     if (
    #         self.y > self.parent.top + 100
    #         or self.y < -100
    #         or self.x > self.parent.width + 100
    #         or self.x < -100
    #     ):
    #         ret = False
    #     elif self.health <= 0:
    #         ret = False
    #     if ret == False:
    #         # self.space_game.remove_player_bullet(self)  # TODO
    #         pass

    #     return ret

class PlayerBullet(Bullet):
    pass

class EnemyBullet(Bullet):
    pass
