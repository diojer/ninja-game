from .imports import *
from .entities import AnimatedBody, NPC, Player
from .camera import YSortCameraGroup
from .tilemap import Tilemap

class Level:
    def __init__(self, name: str):
        
        self.set_map(name)
        self.characters: list[NPC] = []
        self.player_loc = None
        self.player_asset = None
        
    def run(self, surf):
        self.update()
        self.render(surf)
        
    def update(self):
        self.background.update(self.player)
        self.foreground.update(self.player)
        self.commands(self)
        
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
            
    def add_Player(self, loc = None, asset = None):
        kwargs = {
            "groups": [self.foreground],
            "level": self,
        }
        if self.player_loc: kwargs["pos"] = self.player_loc
        if self.player_asset: kwargs["asset"] = self.player_asset
        
        self.player = Player(**kwargs)
        
        # self.add_character(self.player)
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
    
    def commands(self, etc):
        pass

# ---- Level config

LEVELS: dict[str, Level] = {
    "rocky_plains": Level("rocky_plains"),
    "heart_level": Level("heart_level"),
    "living_room": Level("living_room"),
    "living_room_2": Level("living_room_2")
}

LEVELS["living_room_2"].player_loc = Vector2(0, 80)
LEVELS["living_room"].player_loc = Vector2(0, 80)

LEVELS["living_room_2"].add_NPCs({
    "Ginger": Vector2(80, 80)
})

def living_room_2(self: Level):
    for character in self.characters:
        pos = Vector2(character.rect.left, character.rect.top)
        target = Vector2(self.player.rect.left, self.player.rect.top)
        
        direction = (target - pos)
        direction.x = round(direction.x)
        direction.y = round(direction.y)
        if direction: direction = direction.normalize()
        character.set_dir(direction)
        

setattr(LEVELS["living_room_2"], "commands", living_room_2)