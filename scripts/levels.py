from .imports import *
from .entities import AnimatedBody, NPC, Player
from .camera import YSortCameraGroup
from .tilemap import Tilemap

class Level:
    def __init__(self, name: str, commands: Callable):
        
        self.set_map(name)
        self.characters: dict[str, NPC] = {}
        self.commands = commands
        self.player_loc = None
        self.player_asset = None
        
        self.spawns = {}
        for spawn_group in self.map.layers["spawns"]:
            for spawn in spawn_group.sprites():
                self.spawns[spawn.name] = spawn
        
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
        
    def add_character(self, entity: NPC):
        self.characters[entity.name] = entity
    
    def add_characters(self, characters: list[NPC]):
        for character in characters:
            self.add_character(character.name, character)
    
    def add_NPC(self, name: str, pos: Vector2, asset: str):
        self.add_character(NPC(pos, [self.foreground], self, name, asset))
        
    def add_NPCs(self, npcs: list[dict[str, str | Vector2]]):
        for npc in npcs:
            self.add_NPC(npc["name"], npc["pos"], npc["asset"])
            
    def add_Player(self, lastdoor: str = None):
        kwargs = {
            "groups": [self.foreground],
            "level": self,
        }
        if self.player_asset: kwargs["asset"] = self.player_asset
        if lastdoor:
            kwargs["lastdoor"] = lastdoor
            pos: Vector2
            if lastdoor == "e_door":
                pos = self.spawns["player_w"].pos
            elif lastdoor == "w_door":
                pos = self.spawns["player_e"].pos
            elif lastdoor == "n_door":
                pos = self.spawns["player_s"].pos
            elif lastdoor == "s_door":
                pos = self.spawns["player_n"].pos
            kwargs["pos"] = pos
        else:
            if self.player_loc: kwargs["pos"] = self.player_loc
        
        self.player = Player(**kwargs)
        
        return self.player
    
    def del_character(self, name: str):
        self.foreground.remove(self.characters[name])
        del self.characters[name]
    
    def del_player(self):
        self.foreground.remove(self.player)
        
    def set_map(self, name):
        self.map = Tilemap(name)
        self.foreground = YSortCameraGroup()
        self.background = YSortCameraGroup()
        
        for type in self.map.layers:
            for group in self.map.layers[type]:
                for sprite in group.sprites():
                    if type == "floor":
                        self.background.add(sprite)
                    elif not type == "spawns" and not type == "doors":
                        self.foreground.add(sprite)

# ---- Level config

LEVELS: dict[str, Level] = {}

from .rooms.living_room import *
from .rooms.living_room_2 import *
from .rooms.bath_room import *