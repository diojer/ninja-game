from .imports import *
import os
from functools import wraps

BASE_IMG_PATH = "data/sprites/"




# Function to transform a horizontal spritesheet as a list of images.
# size = sprite size
# ss: spritesheet
def get_spritesheet_images(size: tuple, ss: pygame.Surface, vert: bool = False) -> list[pygame.Surface]:
    """Takes a horizontal spritesheet and returns it as a list of pygame Surfaces

    Args:
        size(tuple): Width and height of one frame
        ss(pygame.Surface): Spritesheet

    Returns:
        list[pygame.Surface]: list of pygame.Surface objects
    """
    img_list: list[pygame.Surface] = []
    
    length = ss.get_width() if not vert else ss.get_height()
    step_size = size[0] if not vert else size[1]

    for i in range(0, length, step_size):
        img = pygame.Surface((size[0], size[1]))
        img.blit(ss, (-i * (not vert), -i * vert))
        img.set_colorkey((0, 0, 0))
        img_list.append(img)
    return img_list

def get_sheet_images(size: tuple, sheet: pygame.Surface) -> list[list[pygame.Surface]]:
    """Takes a tilesheet and returns it as a 2D array of pygame Surfaces

    Args:
        size (tuple): Tile size
        sheet (pygame.Surface): Tile sheet

    Returns:
        list[list[pygame.Surface]]: List of a list of pygame Surface objects
    """
    
    img_list: list[list[pygame.Surface]] = []
    
    for row_num in range(0, sheet.get_height(), size[1]):
        tiles: list[pygame.Surface] = []
        for col_num in range(0, sheet.get_width(), size[0]):
            img = pygame.Surface(size)
            img.blit(sheet, (-row_num, -col_num))
            img.set_colorkey((0, 0, 0))
            tiles.append(img)
        img_list.append(tiles)
    return img_list

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path) -> list[pygame.Surface]:
    """Returns all images inside a folder

    Args:
        path (str): Folder path

    Returns:
        list[pygame.Surface]: list of pygame Surface objects
    """
    images: list[pygame.Surface] = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + "/" + img_name))
    return images   

@dataclass
class Animation:
    images: list[pygame.Surface]
    img_duration: int
    loop: bool = True
    done: bool = field(init=False, default=False)
    frame: int = field(init=False, default=0)

    def __len__(self):
        return self.img_duration * len(self.images)

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) -1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    

def round_vector(vector: Vector2):
    return Vector2(round(vector.x), round(vector.y)).copy()

dir_dict_trans = {
    0: "down",
    1: "up",
    2: "left",
    3: "right"
}

dir_dict = {
    "left": False,
    "right": False,
    "up": False,
    "down": False
}

def add_method(cls):
    def decorator(func):
        @wraps(func) 
        def wrapper(self, *args, **kwargs): 
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator