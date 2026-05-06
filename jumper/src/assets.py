import os
import pygame

class AssetManager:
    def __init__(self, asset_root=None):
        self.asset_root = asset_root or os.path.join(os.path.dirname(__file__), '..', 'assets')
        self.images = {}
        self.sounds = {}

    def _full_path(self, subpath):
        return os.path.join(self.asset_root, subpath)

    def load_image(self, key, path, convert_alpha=True):
        full = self._full_path(path)
        img = pygame.image.load(full)
        if convert_alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        self.images[key] = img
        return img

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, key, path):
        # Try the given path first, then prefer OGG/WAV variants if present
        root, ext = os.path.splitext(path)
        candidates = [path, root + '.ogg', root + '.wav']
        sound = None
        for p in candidates:
            full = self._full_path(p)
            if not os.path.isfile(full):
                continue
            try:
                sound = pygame.mixer.Sound(full)
                break
            except Exception:
                sound = None
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        return self.sounds.get(key)
