from .imports import *
from pytmx.util_pygame import load_pygame

class Tilemap:
    def __init__(self, level, tile_size = 16):
        self.level: str = level
        self.tile_size = tile_size
        self.tmx = load_pygame(f"data/tilemaps/{self.level}.tmx")
        self.layers: list[pygame.sprite.Group] = []
        for layer in self.tmx.layers:
            group = pygame.sprite.Group()
            for x, y, tile in layer.tiles():
                sprite = Tile(group, 16, tile, (x,y))
            self.layers.append(group)
    
    def draw(self, surf):
        for layer in self.layers:
            layer.draw(surf)
        
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, size, image, pos):
        super().__init__(groups)
        self.image = image
        self.rect = pygame.Rect(pos, (size, size))
