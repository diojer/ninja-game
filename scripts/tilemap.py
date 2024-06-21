from .imports import *

from .camera import YSortCameraGroup
from pytmx.util_pygame import load_pygame

class Tilemap:
    def __init__(self, level, tile_size = TILE_SIZE):
        self.level: str = level
        self.tile_size = tile_size
        self.tmx = load_pygame(f"data/tilemaps/{self.level}.tmx")
        self.layers: dict[str, list[pygame.sprite.Group]] = {
            "floor": [],
            "collision": [],
            "breakable": [],
            "decorations": [],
            "top": []
        }
        self.colliders = {}
        for gid, colliders in self.tmx.get_tile_colliders():
            for collider in colliders:
                self.colliders[gid] = collider
        
        for layer in self.tmx.layers:
            group = pygame.sprite.Group()
            i = self.tmx.layers.index(layer)
            for x, y, img in layer.tiles():
                gid = self.tmx.get_tile_gid(x, y, i)
                if gid in self.colliders:
                    sprite = Tile(group, img, (x * self.tile_size, y * self.tile_size), layer.name.lower(), self.colliders[gid])
                else:
                    sprite = Tile(group, img, (x * self.tile_size, y * self.tile_size), layer.name.lower())
            for type in self.layers:
                if type in layer.name.lower():
                    self.layers[type].append(group)
                    break
    
    def draw(self, surf, offset = Vector2(0, 0)):
        for type in self.layers:
            for layer in self.layers[type]:
                layer.draw_tile(surf, offset)
                
class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, image: Surface, pos, layer_name: str, collider = None, size: int = TILE_SIZE):
        super().__init__(groups)
        self.image: Surface = image
        self.rect: Rect = Rect(pos, (size, size))
        self.layer_name: str = layer_name
        
        if collider:
            self.hitbox: Rect = Rect(collider.x, collider.y, collider.width, collider.height).move(self.rect.x, self.rect.y)
            # self.hitbox.bottom = self.rect.bottom
        
