from .imports import *
from ..utils import load_image



class backgroundImage(pygame.sprite.Sprite):
    def __init__(self, groups, image, rect):
        super().__init__(groups)
        self.image = image
        self.rect = rect
        self.layer_name = "collision"
    
    def draw(self, surf: Surface):
        surf.blit(self.image, self.rect)
        print("hi")

def loader(self: Level):
    self.backgroundI = load_image("backgrounds/testbackground.png")
    self.background1 = backgroundImage(self.background, self.backgroundI, Rect((0, 0), (self.backgroundI.get_width(), self.backgroundI.get_height())))
    print("bathroom loaded")


def commands(self: Level):
    pass

LEVELS["bath_room"] = Level("bathroom", commands, loader)
