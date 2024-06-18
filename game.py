from scripts.imports import *

from scripts.tilemap import Tilemap
from scripts.utils import Animation, get_spritesheet_images, load_image
from scripts.entities import AnimatedBody, NPC, Player
from scripts.camera import YSortCameraGroup




class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_size: tuple = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]))
        self.display = pygame.Surface((self.screen_size[0]//DISPLAY_SCALE, self.screen_size[1]//DISPLAY_SCALE))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_CAPTION)
        
        #------------ Assets
        
        from scripts.assets import ASSETS
        self.assets = ASSETS
        
        #------------ Sprites
        
        self.foreground = YSortCameraGroup()
        self.background = YSortCameraGroup()
        
        self.characters = [
            NPC(Vector2(20, 20), [self.foreground], self, "dalmatian"),
            NPC(Vector2(35, 40), [self.foreground], self, "knight"),
            NPC(Vector2(25, 60), [self.foreground], self, "wizard")
        ]
        
        self.player = Player(Vector2(0, 0), [self.foreground], self, "Ginger")
        self.player.vel = Vector2(1.5, 1.5)
        
            #--- Adding all entities to an array for ease of use.
        self.entities = []
        self.entities.append(self.player)
        self.entities.extend(self.characters)

        
        #------------ Levels
        
        self.levels = {
            "rocky_plains": Tilemap("rocky_plains"),
            "heart_level": Tilemap("heart_level")
        }
        self.set_level("rocky_plains")


    def run(self):
        while True:
            self.display.fill((150, 220, 255))
            
            # draw background
            self.background.update(self.player)
            self.background.draw(self.display)
            
            # Update all in the foreground
            self.foreground.update(self.player)
            
            for character in self.characters:
                character.instruct("f,r/g,1000/w,2000/f,d/g,2000/w,1000/f,u/g,2000/f,l/g,1000/w,2000")
            
            self.foreground.draw(self.display)
            
            
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
    
    def set_level(self, level_name: str):
        self.currentlevel = self.levels[level_name]
        self.foreground = YSortCameraGroup()
        self.background = YSortCameraGroup()
        
        #---- Adding Player and NPCs
        for entity in self.entities:
            self.foreground.add(entity)
        
        #---- Setting the map
        for type in self.currentlevel.layers:
            for group in self.currentlevel.layers[type]:
                for sprite in group.sprites():
                    sprite.layer_name = type
                    if type == "floor":
                        self.background.add(sprite)
                    else:
                        self.foreground.add(sprite)
Game().run()