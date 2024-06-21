from .imports import *
from .utils import dir_dict, dir_dict_trans
from .assets import ASSETS

import random

if TYPE_CHECKING:
    from .tilemap import Tile

            

class KinematicBody(pygame.sprite.Sprite):
    def __init__(self, pos, groups, level: "Level"):
        super().__init__(groups)
        self.pos: Vector2 = pos
        self.level: "Level" = level
        self.movement = dir_dict.copy()
        self.colliding = dir_dict.copy()
        self.vel: Vector2 = Vector2(1, 1)
        self.rect: FRect
        self.hitbox: FRect

    def update(self):
        
        # We increment x and y separately for collision detection reasons.        
        self.hitbox.x += self.dir().x * self.vel.x
        for group in self.level.map.layers["collision"]:
            for sprite in group.sprites():
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.dir().x > 0:
                        self.colliding["right"] = True
                        self.hitbox.right = sprite.hitbox.left
                    if self.dir().x <= 0:
                        self.colliding["left"] = True
                        self.hitbox.left = sprite.hitbox.right
        
        self.hitbox.y += self.dir().y * self.vel.y
        for group in self.level.map.layers["collision"]:
            for sprite in group.sprites():
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.dir().y > 0:
                        self.colliding["down"] = True
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.dir().y <= 0:
                        self.colliding["up"] = True
                        self.hitbox.top = sprite.hitbox.bottom
        
        self.rect.center = self.hitbox.center

    def dir(self):
        direction = Vector2((self.movement["right"] - self.movement["left"]), (self.movement["down"] - self.movement["up"]))
        if direction.length(): direction = direction.normalize()
        return direction

    def reset_collisions(self):
        self.colliding = dir_dict.copy()
        

class AnimatedBody(KinematicBody):
    def __init__(self, pos, groups, level: "Level", asset: str):
        super().__init__(pos, groups, level)
        
        #----- Sprite set-up
        self.assets = ASSETS[asset]
        
            #----- Idle asset should be a list of images not an animation
        self.image = self.assets["idle"][0]
        self.rect = FRect(self.pos, self.image.get_size())
            #----- If sprite is 16x16 this is a good hitbox
        self.hitbox = self.rect.inflate(-2, -4)
        
        #----- Dictionaries for keeping track of key-inputs and facing direction
        self.moving = False
        self.going = dir_dict.copy()
        self.facing = dir_dict.copy()
        
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
        
        #-------------- For pixel perfect movement
        if self.dir().length():
            self.old_movement = self.movement.copy()
        else:
            self.old_movement = self.going.copy()
        
        self.movement = self.going.copy() # copy our key inputs into our movement inputs
        
        if not self.old_movement == self.movement:
            self.hitbox.x = round(self.hitbox.x)
            self.hitbox.y = round(self.hitbox.y)

        #--------------

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

class Player(AnimatedBody):
    def __init__(self, pos, groups, level: "Level", asset: str):
        super().__init__(pos, groups, level, asset)
        self.vel = Vector2(1.5, 1.5)
        self.hitbox = self.rect.inflate(-2, -8)
        self.prox = self.rect.inflate(20, 20) # self.prox will be a hitbox used to interact with objects/NPCs
        self.interactables: list[NPC | "Tile"] = []
        self.interactables.extend(self.level.characters) # Adds all NPCs to things we can interact with
        self.interaction: function | None = None
    
    def update(self):
        
        #---- Check if we are moving
        if not self.dir().length() == 0:
            self.facing = self.movement.copy() # self.facing will contain last direction we moved before stopping
            
        #-------------- Checking interaction collisions
        
        found_interaction = False
        for interactable in self.interactables:
            if self.prox.colliderect(interactable.hitbox):
                self.interaction = interactable.interaction
                found_interaction = True
        
        if not found_interaction:
            self.interaction = None
        
        super().update()
        
        self.rect.bottom = self.hitbox.bottom
        self.prox.center = self.rect.center
    
    def draw(self, surf):
        super().draw()
        if DEBUG:
            pygame.draw.rect(surf, "red", self.prox.move(-self.level.foreground.offset.x, -self.level.foreground.offset.y), 1)

class NPC(AnimatedBody):
    def __init__(self, pos, groups, level: "Level", asset: str, aggressive: bool = False):
        super().__init__(pos, groups, level, asset)
        self.timer = pygame.time.Clock()
        self.aggressive = aggressive
        
        # Ticks the clock for the first time
        self.timer.tick()
        self.time_waiting = 0
        self.waiting = False
        
        # Instructions set if the NPC is given walk commands
        self.instructions: list[str] | None = None
        self.paused: bool = False # Paused will be set to true when we're interacting with NPCs.

    def set_dir(self, dir: Vector2):
        self.going = dir_dict.copy()
        if dir.x:
            if dir.x > 0:
                self.going["right"] = True
            elif dir.x < 0:
                self.going["left"] = True
        if dir.y:
            if dir.y > 0:
                self.going["down"] = True
            if dir.y < 0:
                self.going["up"] = True
        self.facing = self.going.copy()
    
    def face_random(self):
        new_dir = random.randint(0, 3)
        
        
        
        # Sets randomly chosen direction as the current facing direction.
        # All other directions get set to false.
        
        self.facing = dir_dict.copy()
        if self.facing[dir_dict_trans[new_dir]]:
            # If we randomly select the direction already being faced pick a new random direction.
            self.face_random()
        else:
            self.facing[dir_dict_trans[new_dir]] = True
    
    def instruct(self, instruction_str: str, important: bool = False):
#   Possible instructions:
#         f         : face
#         g         : go
#             u,d,l,r,* : up, down, left, right, random
#                       : go followed by nothing goes forward
#                       : go syntax looks like, e.g., /g,2000,u/ where 2000 = number of milliseconds to go for.
#                       : face syntax looks like, e.g., /f,d/
#         w         : wait
#                       : wait is followed by a number
#         /         : separate commands
        
        # ----------- Writing out functionality for the instructions
        
        # All of the following functions (wait, go, face) will return True when they've completed their action and False when they need more time to finish.
        def wait(time: int):
            
            # On the first time we call wait(), set self.waiting = True
            if not self.waiting:
                self.waiting = True
                
                # Clock ticks so we'll know exactly how long we've been waiting for
                self.timer.tick()
            
            # Record the amount of time since the command began
            self.time_waiting += self.timer.tick()
            if self.time_waiting > time:
                # The time has passed
                self.waiting = False
                return True
            else:
                self.going = dir_dict.copy()
                
                # Keep returning false so that the command is not .pop()'d from the list
                return False
        
        def go( time: int, dir: str | None = None):
            
            if not self.waiting:
                self.waiting = True
                self.timer.tick()
            
            
            self.time_waiting += self.timer.tick()
            if self.time_waiting > time:
                # The time has passed
                self.waiting = False
                return True
            else:
                # Keep walking
                
                # If a direction was provided:
                if dir:
                    for direction in self.going:
                        
                        # If dir = u and direction = up, e.g., this will be true:
                        if dir == direction[0]:
                            self.going[direction] = True
                        else:
                            self.going[direction] = False
                
                # If no direction was provided:
                else:
                    self.going = self.facing.copy()
                return False
            
            
        
        def face(dir: str):
            if dir == "*":
                self.face_random()
                return True
            for direction in self.facing:
                if dir == direction[0]:
                    # If dir = u and direction = up, e.g., this will be true.
                    self.facing[direction] = True
                    
                else:
                    self.facing[direction] = False
            return True
        # -----------

        if (not self.instructions) or important:
            # If there are no current instructions restart the instructions
            # Or, if the instructions are important.
            
            self.instructions = instruction_str.split("/")
        
        # Instructions are stored in an array.
        # Every time self.instruct() is called, the latest instruction is executed.
            # Once it has finished being executed it is removed from the array
        # Once the array is empty self.instructions is set to None.
        # This allows it to be reset.
        
        parameters = self.instructions[0].split(",")
        # The first element, parameters[0] is a character representing the command
        # The second/third elements vary depending on the initial command
        
        
        if not self.paused:
            # the completed variable records whether the chosen command function returns True or False
            completed = False
            match parameters[0]:
                case "f":
                    # parameters[1] in this case contains the direction
                    cmd_dir = parameters[1]
                    completed = face(cmd_dir)
                    
                case "g":
                    if len(parameters) == 2:
                        # No direction included
                        
                        # parameters[1] contains the time to go for
                        cmd_time = int(parameters[1])
                        completed = go(cmd_time)
                    elif len(parameters) == 3:
                        # Direction included
                        
                        # parameters[1] is the time to go for and parameters[2] is the direction to go
                        cmd_time = int(parameters[1])
                        cmd_dir = parameters[2]
                        completed = go(cmd_time, cmd_dir)
                    else:
                        # Too many/too few arguments given
                        raise Exception(f"Error in NPC instruct(): g command given {len(parameters)} arguments")
                case "w":
                    # parameters[1] contains the time to wait for
                    cmd_time = int(parameters[1])
                    completed = wait(cmd_time)
                case _:
                    raise Exception(f"Error in NPC instruct(): command {parameters[0]} does not exist.")
            if completed:
                # If our command is completed, we remove the top action from the list
                self.instructions.pop(0)
                
                # We also have to reset the self.time_waiting so that we can start counting from the
                    # beginning of the next command
                self.time_waiting = 0
                
                # If the list is now empty:
                if not self.instructions:
                    self.instructions = None

    def interaction(self):
        pass
        