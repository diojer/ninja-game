from .imports import *

class KinematicBody(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game: "Game"):
        super().__init__(groups)
        self.pos: Vector2 = pos
        self.game: "Game" = game
        self.movement = dict(left = False, right = False, up = False, down = False)
        self.vel: Vector2 = Vector2(1, 1)

    def update(self):
        
        # We increment x and y separately for collision detection reasons.
        self.pos.x += (self.movement["right"] - self.movement["left"]) * self.vel.x
        self.pos.y += (self.movement["down"] - self.movement["up"]) * self.vel.y

    def dir(self):
        return Vector2((self.movement["right"] - self.movement["left"]), (self.movement["down"] - self.movement["up"]))


class Player(KinematicBody):
    def __init__(self, pos, groups, game: "Game"):
        super().__init__(pos, groups, game)
        
        #----- Sprite set-up
        self.assets = self.game.assets["Ginger"]
        self.image = self.assets["idle"][0]
        self.rect: Rect = Rect(self.pos, self.image.get_size())
        
        #----- Dictionaries for keeping track of key-inputs and facing direction
        self.moving = False
        self.going = dict(left = False, right = False, up = False, down = False)
        self.facing = dict(left = False, right = False, up = False, down = False)
        
        #----- Animation
        self.action: str = ""
        
        self.animation = False

    def set_action(self, action: str):
        """Sets the current animation

        Args:
            action (str): String pointing to an animation object in assets.
        """
        
        if action == "idle":
            self.animation = False
            # "idle" does not point to an animation object in our assets, it points to a list of images.
            # We do not want to be animated while we are idle.
        elif not action == self.action:
            self.action = action
            self.animation = self.assets[self.action].copy()
    
    def update(self):
        self.moving = False
        
        #---- Check if we are moving
        if not self.dir().length() == 0:
            self.moving = True
            self.facing = self.movement.copy() # self.facing will contain last direction we moved before stopping
        self.movement = self.going.copy() # copy our key inputs into our movement inputs
        
        if self.animation: # if we are being animated
            self.animation.update()
            self.image = self.animation.img()
            
        # For sprites, we need to set self.image and self.rect every frame.
        # self.render() sets the self.image
        self.render()
        
        # Here we set self.rect to our current position and size
        self.rect = Rect(self.pos, self.image.get_size())
        
        # This KinematicBody update() method updates our position
        super().update()
    
    def render(self):
        if not self.moving:
            
            # If we are idle:
            if self.facing["up"]:
                self.image = self.assets["idle"][1]
            if self.facing["down"]:
                self.image = self.assets["idle"][0]
            if self.facing["left"]:
                self.image = self.assets["idle"][2]
            if self.facing["right"]:
                self.image = self.assets["idle"][3]
            
            # down  = 0
            # up    = 1
            # left  = 2
            # right = 3