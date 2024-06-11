from .imports import *

class KinematicBody(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game: "Game"):
        super().__init__(groups)
        self.pos: Vector2 = pos
        self.game: "Game" = game
        self.movement = dict(left = False, right = False, up = False, down = False)
        self.vel: Vector2 = Vector2(1, 1)
        self.rect: FRect
        self.hitbox: FRect

    def update(self):
        
        # We increment x and y separately for collision detection reasons.
        
        self.net_movement = Vector2(self.movement["right"] - self.movement["left"], self.movement["down"] - self.movement["up"])
        
        self.hitbox.x += self.dir().x * self.vel.x
        for group in self.game.currentlevel.layers["collision"]:
            for sprite in group.sprites():
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.dir().x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.dir().x <= 0:
                        self.hitbox.left = sprite.hitbox.right
        
        self.hitbox.y += self.dir().y * self.vel.y
        for group in self.game.currentlevel.layers["collision"]:
            for sprite in group.sprites():
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.dir().y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.dir().y <= 0:
                        self.hitbox.top = sprite.hitbox.bottom
        
        self.rect.topleft = self.hitbox.topleft

    def dir(self):
        direction = Vector2((self.movement["right"] - self.movement["left"]), (self.movement["down"] - self.movement["up"]))
        if direction.length(): direction = direction.normalize()
        return direction

class AnimatedBody(KinematicBody):
    def __init__(self, pos, groups, game: "Game", asset: str):
        super().__init__(pos, groups, game)
        
        #----- Sprite set-up
        self.assets = self.game.assets[asset]
        
            #----- Idle asset should be a list of images not an animation
        self.image = self.assets["idle"][0]
        self.rect = FRect(self.pos, self.image.get_size())
            #----- If sprite is 16x16 this is a good hitbox
        self.hitbox = self.rect.inflate(-2, -4)
        
        #----- Dictionaries for keeping track of key-inputs and facing direction
        self.moving = False
        self.going = dict(left = False, right = False, up = False, down = False)
        self.facing = dict(left = False, right = False, up = False, down = False)
        
        #----- Animation
        self.action: str = ""
        self.flip = False
        self.animation = False
        
    def set_action(self, action: str):
        """Sets the current animation

        Args:
            action (str): String pointing to an animation object in assets.
        """
        
        if action == "idle":
            self.action = action
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
        
        # For pixel perfect movement
        if self.dir().length():
            self.old_movement = self.movement.copy()
        else:
            self.old_movement = self.going.copy()
        
        self.movement = self.going.copy() # copy our key inputs into our movement inputs
        
        if not self.old_movement == self.movement:
            self.hitbox.x = round(self.hitbox.x)
            self.hitbox.y = round(self.hitbox.y)


        # This KinematicBody update() method updates our position
        super().update()
        
        # For sprites, we need to set self.image and self.rect every frame.
        # self.render() sets the self.image
        self.render()
    
    def render(self):
        if not self.moving:
            self.set_action("idle")
            
            # If we are idle:
            if self.facing["up"]:
                self.image = self.assets["idle"][1]
            if self.facing["down"]:
                self.image = self.assets["idle"][0]
            if self.facing["left"] or self.facing["right"]:
                self.image = self.assets["idle"][2]
            
            # down  = 0
            # up    = 1
            # left  = 2
            # right = 3
        else:
            if self.facing["up"]:
                self.set_action("walk_u")
            elif self.facing["down"]:
                self.set_action("walk_d")
            elif self.facing["left"] or self.facing["right"]:
                self.set_action("walk_s")
            
        if self.animation: # if we are being animated
            self.animation.update()
            self.image = self.animation.img()
        
        if not (self.facing["up"] or self.facing["down"]):
            if self.facing["right"]:
                self.flip = True
            elif self.facing["left"]:
                self.flip = False