from .imports import *
from .entities import AnimatedBody, NPC, Player
from .camera import YSortCameraGroup
from .tilemap import Tilemap

class Level:
    def __init__(self, name: str):
        
        self.set_map(name)
        self.characters: list[AnimatedBody] = []
        
        
    def run(self, surf):
        self.update()
        self.render(surf)
        
    def update(self):
        self.background.update(self.player)
        self.foreground.update(self.player)
        
    def render(self, surf):
        self.background.draw(surf)
        self.foreground.draw(surf)
        
    def add_character(self, character: AnimatedBody):
        self.characters.append(character)
    
    def add_characters(self, characters: list[AnimatedBody]):
        self.characters.extend(characters)
    
    def add_NPC(self, pos: Vector2, asset: str):
        self.add_character(NPC(pos, [self.foreground], self, asset))
        
    def add_NPCs(self, data: dict[str, Vector2]):
        for asset in data:
            pos = data[asset]
            self.add_character(NPC(pos, [self.foreground], self, asset))
            
    def add_Player(self, pos: Vector2, asset: str):
        self.player = Player(pos, [self.foreground], self, asset)
        self.add_character(self.player)
        return self.player
    
    def del_character(self, character: AnimatedBody):
        self.characters.remove(character)
        self.foreground.remove(character)
        
    def set_map(self, name):
        self.map = Tilemap(name)
        self.foreground = YSortCameraGroup()
        self.background = YSortCameraGroup()
        
        for type in self.map.layers:
            for group in self.map.layers[type]:
                for sprite in group.sprites():
                    if type == "floor":
                        self.background.add(sprite)
                    else:
                        self.foreground.add(sprite)
                    

# ---- Level config

LEVELS: dict[str, Level] = {
    "rocky_plains": Level("rocky_plains"),
    "heart_level": Level("heart_level")
}

LEVELS["rocky_plains"].add_NPCs({
    "dalmatian": Vector2(20, 20),
    "knight": Vector2(35, 40),
    "wizard": Vector2(25, 60)
})