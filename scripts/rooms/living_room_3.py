from .imports import *

def commands(self: Level):
    if self.player.interacting:
        for obj in self.player.interacting:
            if "door" in obj.name:
                match obj.name:
                    case "w_door":
                        pygame.event.post(pygame.event.Event(LVL_EVENT, dict(name="living_room")))
                    case "e_door":
                        pygame.event.post(pygame.event.Event(LVL_EVENT, dict(name="bath_room")))

LEVELS["living_room_3"] = Level("living_room_3", commands)