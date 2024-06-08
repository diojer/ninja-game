from .imports import *

class KinematicBody(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game: "Game"):
        super().__init__(groups)
        self.pos: Vector2 = pos
        self.game: "Game" = game
        self.movement = dict(left = False, right = False, up = False, down = False)
        self.vel: Vector2 = Vector2(1, 1)

    def update(self):
        self.pos.x += (self.movement["right"] - self.movement["left"]) * self.vel.x
        self.pos.y += (self.movement["down"] - self.movement["up"]) * self.vel.y

    def dir(self):
        return Vector2((self.movement["right"] - self.movement["left"]), (self.movement["down"] - self.movement["up"]))


class Player(KinematicBody):
    def __init__(self, pos, groups, game: "Game"):
        super().__init__(pos, groups, game)
        self.assets = self.game.assets["cave_girl"]
        self.action: str = ""
        self.image = self.assets["idle"][0]
        self.animation = False
        self.rect: Rect = Rect(self.pos, self.image.get_size())
        self.going = dict(left = False, right = False, up = False, down = False)
        self.facing = dict(left = False, right = False, up = False, down = False)
        self.moving = False

    
    def set_action(self, action: str):
        if not action == self.action:
            self.action = action
            self.animation = self.assets[self.action].copy()
    
    def update(self):
        self.moving = False
        if not self.dir().length() == 0:
            self.moving = True
            for direction in self.going:
                if self.going[direction]:
                    self.facing[direction] = True
                else:
                    self.facing[direction] = False
        self.movement = self.going.copy()
        print(self.facing)
        
        if self.animation:
            self.animation.update()
            self.image = self.animation.img()
        self.render()
        self.rect = Rect(self.pos, self.image.get_size())
        
        super().update()
    
    def render(self):
        if not self.moving:
            # down  = 0
            # up    = 1
            # left  = 2
            # right = 3
            if self.facing["down"]:
                self.image = self.assets["idle"][0]
            if self.facing["up"]:
                self.image = self.assets["idle"][1]
            if self.facing["left"]:
                self.image = self.assets["idle"][2]
            if self.facing["right"]:
                self.image = self.assets["idle"][3]