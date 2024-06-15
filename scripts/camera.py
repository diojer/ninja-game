from .imports import *

from .utils import round_vector

if TYPE_CHECKING:
    from .tilemap import Tile

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, game: "Game", sprites = []):
        super().__init__(sprites)
        self.offset = Vector2(0, 0)
        self.game = game
        self.half_width = self.game.display.get_size()[0] // 2
        self.half_height = self.game.display.get_size()[1] // 2
        
    def draw(self, surf: pygame.Surface):
        top_layer: "list[Tile]" = []
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if hasattr(sprite, "flip"):
                surf.blit(pygame.transform.flip(sprite.image, sprite.flip, False), sprite.rect.topleft - self.offset)
                if self.game.debug:
                    pygame.draw.rect(surf, (15, 197, 247), sprite.rect.move(-self.offset.x, -self.offset.y), 1)
            else:
                if hasattr(sprite, "layer_name"):
                    if "top" in sprite.layer_name:
                        top_layer.append(sprite)
                    else:
                        surf.blit(sprite.image, sprite.rect.topleft - self.offset)
        for tile in top_layer:
            surf.blit(tile.image, tile.rect.topleft - self.offset)

    
    def update(self, player):
        self.offset.x = player.hitbox.centerx - self.half_width
        self.offset.y = player.hitbox.centery - self.half_height
        for sprite in self.sprites():
            sprite.update()