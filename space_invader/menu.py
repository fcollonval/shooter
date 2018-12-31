from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class Menu(Screen):
    but_launch = ObjectProperty(None)
    # but2 = ObjectProperty(None)
    but3 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self._update_event = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def on_pre_enter(self, *args):
        self._update_event = Clock.schedule_interval(self.update, 1.0 / 30.0)
        super(Menu, self).on_pre_enter(*args)

    def on_pre_leave(self, *args):
        self._update_event.cancel()
        super(Menu, self).on_pre_leave(*args)

    def update(self, dt):
        x, y = Window.mouse_pos
        buttons = [
            self.but_launch,
            # self.but2,
            self.but3,
        ]

        for button in buttons:
            if button.collide_point(x, y):
                button.font_size = 70
                button.color = (1, 0.8, 0.1, 1)
            else:
                button.font_size = 50
                button.color = (1, 1, 1, 1)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers, *args):
        # Keycode is composed of an integer + a string
        if keycode[1] == "escape" and self.manager.state == "pause":
            self.manager.current = "main"

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
