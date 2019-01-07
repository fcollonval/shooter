import sys

from kivy.core.audio import SoundLoader

def load_sound(filename):
    """Helper function loading sounds only on non-windows platform
    
    On Windows, GStream is poping annoying warnings.
    """
    if sys.platform == "win32":
        return None
    else:
        return SoundLoader.load(filename)
