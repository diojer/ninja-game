from imports import *
from .entities import KinematicBody
from .camera import YSortCameraGroup
from .tilemap import Tilemap

class Level:
    def __init__(self, name: str) -> None:
        self.name = name
        self.map = Tilemap(self.name)
        
        self.characters = []
        self.foreground = YSortCameraGroup()
        self.background = YSortCameraGroup()
        
    def run(self, surf):
        self.update()
        self.render(surf)
        
    def update(self):
        pass
    
    def render(self, surf):
        pass
        
    def add_character(self, character: KinematicBody):
        self.characters.append(character)
    
    def add_characters(self, characters: list[KinematicBody]):
        for character in characters:
            self.add_character(character)