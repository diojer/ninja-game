from scripts.imports import *


from scripts.levels import LEVELS
from scripts.assets import ASSETS
from scripts.utils import dir_dict

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = SCREEN
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_CAPTION)
        
        self.assets = ASSETS
        self.levels = LEVELS
        self.set_level("living_room_3")
        
        self.next_lvl = None
        self.fading_opc = 255


    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.display.fill((0, 0, 0))
            
            if self.next_lvl:
                faded = self.fade_out()
                self.player.going = dir_dict.copy()
                pygame.event.set_blocked(PAUSED_EVENTS)
                if faded:
                    self.set_level(self.next_lvl)
                    self.reset_fade()
            
            self.currentlevel.run(self.display)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.going["up"] = True
                    if event.key == pygame.K_a:
                        self.player.going["left"] = True
                    if event.key == pygame.K_s:
                        self.player.going["down"] = True
                    if event.key == pygame.K_d:
                        self.player.going["right"] = True
                    if event.key == pygame.K_l:
                        self.set_level("heart_level")
                    if event.key == pygame.K_r:
                        self.set_level("rocky_plains")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.going["up"] = False
                    if event.key == pygame.K_a:
                        self.player.going["left"] = False
                    if event.key == pygame.K_s:
                        self.player.going["down"] = False
                    if event.key == pygame.K_d:
                        self.player.going["right"] = False
                if event.type == LVL_EVENT:
                    self.next_lvl = event.name
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60) #60fps
    
    def set_level(self, level_name: str):
        kwargs = {}
        if hasattr(self, "player"):
            self.currentlevel.del_player()
            kwargs["lastdoor"] = self.player.lastdoor
            kwargs["flipped"] = self.player.flip
        self.currentlevel = LEVELS[level_name]
        self.player = self.currentlevel.add_Player(**kwargs)
        
        
    def fade(self, length, out: bool = True, color = "black"):
        fade_tmr = pygame.time.Clock()
        fading_time = 0
        rect = Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        color = pygame.Color(0, 0, 0, 0)
        
        opacity: int
        opacity = 128
        while fading_time < length:
            color = pygame.Color(0, 0, 0, opacity)
            pygame.draw.rect(self.display, color, rect)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60) #60fps
            # opacity = (opacity + 1) % 255
            fading_time += fade_tmr.tick()
    
    def fade_out(self):
        self.display.set_alpha(self.fading_opc)
        self.fading_opc -= 10
        if self.fading_opc < 0:
            return True
        return False

    def reset_fade(self):
        self.display.set_alpha(255)
        pygame.event.set_allowed(PAUSED_EVENTS)
        self.next_lvl = None
        self.fading_opc = 255
            
Game().run()