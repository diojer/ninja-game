from .imports import *

LEVELS["living_room_2"] = Level("living_room_2")

LEVELS["living_room_2"].add_NPCs([
    dict(name="kid", pos=Vector2(90, 90), asset="Ginger")
])

LEVELS["living_room_2"].player_loc = Vector2(0, 80)

level_characters = LEVELS["living_room_2"].characters


def commands(self: Level):
    
    kid = level_characters["kid"]
    
    pos = Vector2(kid.rect.left, kid.rect.top)
    target = Vector2(self.player.rect.left, self.player.rect.top)
    
    direction = (target - pos)
    direction.x = round(direction.x)
    direction.y = round(direction.y)
    distance = 0.0
    if direction:
        distance = abs(direction.length())
        direction = direction.normalize()
    
    if distance > 20:
        kid.set_dir(direction)
    else:
        kid.stop()
        

setattr(LEVELS["living_room_2"], "commands", commands)