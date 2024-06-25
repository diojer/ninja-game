from .imports import *

from .camera import YSortCameraGroup
from pytmx.util_pygame import load_pygame

class Tilemap:
    def __init__(self, level, tile_size = TILE_SIZE):
        self.level: str = level
        self.tile_size = tile_size
        self.tmx = load_pygame(f"data/tilemaps/{self.level}.tmx")
        self.layers: dict[str, list[pygame.sprite.Group] | pygame.sprite.Group] = {
            # Anything with floor is always drawn under the player
            "floor": [],
            
            # Anything with collision will collide with the player
            "collision": [],
            
            # This will not collide with the player but will be drawn as a Y-sorted sprite
            "decorations": [],
            
            # This is an object group which contains all spawn points
            "spawns": [],
            
            # This is an object group which contains all doors
            "doors": [],
            
            # Anything with top is always drawn over the player.
            "top": []
        }
        self.colliders = {}
        for gid, colliders in self.tmx.get_tile_colliders():
            for collider in colliders:
                
                # This works because we are only using one collider per tile.
                self.colliders[gid] = collider
        tile_layers = list(self.tmx.visible_tile_layers)
        obj_layers = list(self.tmx.visible_object_groups)

        for i in tile_layers:
            group = pygame.sprite.Group()
            layer = self.tmx.layers[i]
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
        
        for i in obj_layers:
            group = pygame.sprite.Group()
            layer = self.tmx.layers[i]
            for obj in layer:
                sprite = Obj(group, obj, (obj.x, obj.y), layer.name.lower(), size=(obj.width, obj.height))
            for type in self.layers:
                if type in layer.name.lower():
                    self.layers[type].append(group)
                    break
    
    def draw(self, surf, offset = Vector2(0, 0)):
        for type in self.layers:
            for layer in self.layers[type]:
                layer.draw_tile(surf, offset)
                
class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, image: Surface, pos, layer_name: str, collider = None, obj = None, size: int = TILE_SIZE):
        super().__init__(groups)
        self.image: Surface = image
        self.rect: Rect = Rect(pos, (size, size))
        self.pos = self.rect.topleft
        self.layer_name: str = layer_name
                
        if collider:
            self.hitbox: Rect = Rect(collider.x, collider.y, collider.width, collider.height).move(self.rect.x, self.rect.y)
        
        if obj:
            self.obj = obj
            self.name = obj.name

class Obj(pygame.sprite.Sprite):
    def __init__(self, groups, obj, pos, layer_name: str, size: tuple = (TILE_SIZE, TILE_SIZE)):
        super().__init__(groups)
        self.obj = obj
        self.rect: Rect = Rect(pos, size)
        self.pos = self.rect.topleft
        self.layer_name: str = layer_name
        self.name = obj.name