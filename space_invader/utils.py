import sys

from kivy.core.audio import SoundLoader


def load_sound(filename, **kwargs):
    """Helper function loading sounds only on non-windows platform
    
    On Windows, GStream is poping annoying warnings.
    """
    if sys.platform == "win32":
        return None
    else:
        sound = SoundLoader.load(filename)
        for key, value in kwargs.items():
            setattr(sound, key, value)
        return sound
