from .imports import *

class Collection(pygame.sprite.Group):
    def __init__(self, sprites = []):
        super().__init__(sprites)
    
    def draw(self, surf: pygame.Surface):
        for sprite in self.sprites():
            surf.blit(pygame.transform.flip(sprite.image, sprite.flip, False), sprite.rect.topleft)