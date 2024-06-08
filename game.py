from scripts.imports import *

from scripts.utils import Animation, get_spritesheet_images, load_image
from scripts.entities import Player

SCALE = 6

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen_size: tuple = (1280, 720)
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]), pygame.RESIZABLE)
        self.display = pygame.Surface((self.screen_size[0]//SCALE, self.screen_size[1]//SCALE))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Ninja Game")
        
        #------------ Assets
        
        self.assets = {
            "cave_girl": {
                "idle": get_spritesheet_images((16, 16), load_image("cave_girl/idle.png")),
                "walk_d": Animation(get_spritesheet_images((16, 16), load_image("cave_girl/walk_d.png"), True), 5),
                "walk_u": Animation(get_spritesheet_images((16, 16), load_image("cave_girl/walk_u.png"), True), 5),
                "walk_s": Animation(get_spritesheet_images((16, 16), load_image("cave_girl/walk_s.png"), True), 5)
            }
        }
        
        #------------ Sprites
        
        self.foreground = pygame.sprite.Group()
        self.player = Player(Vector2(0, 0), [self.foreground], self)

    def run(self):
        while True:
            self.display.fill((150, 220, 255))
            
            self.player.update()
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
            
Game().run()