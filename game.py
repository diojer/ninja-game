from scripts.imports import *


from scripts.levels import LEVELS
from scripts.assets import ASSETS

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = SCREEN
        self.display = pygame.Surface((SCREEN_WIDTH//DISPLAY_SCALE, SCREEN_HEIGHT//DISPLAY_SCALE))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_CAPTION)
        
        #------------ Assets
        
        
        self.assets = ASSETS
        
        #------------ Levels
        
        self.levels = LEVELS
        self.set_level("rocky_plains")
        


    def run(self):
        while True:
            self.display.fill((150, 220, 255))
            
            # draw background
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
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60) #60fps
    
    def set_level(self, level_name: str, player_loc: Vector2 = Vector2(0, 0), player_asset = "Ginger"):
        self.currentlevel = LEVELS[level_name]
        self.player = self.currentlevel.add_Player(player_loc, player_asset)
Game().run()