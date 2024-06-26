from .imports import *


def commands(self: Level):
    
    kid = level_characters["kid"]
    kid.vel = Vector2(1.3, 1.3)
    
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
        
    
    if self.player.interacting:
        for obj in self.player.interacting:
            if "door" in obj.name:
                match obj.name:
                    case "e_door":
                        pygame.event.post(pygame.event.Event(LVL_EVENT, dict(name="living_room")))
                    
        

LEVELS["living_room_2"] = Level("living_room_2", commands)

LEVELS["living_room_2"].add_NPCs([
    dict(name="kid", pos=Vector2(90, 90), asset="Ginger")
])

LEVELS["living_room_2"].player_loc = Vector2(0, 80)

level_characters = LEVELS["living_room_2"].characters