from .imports import *
from .utils import *

ASSETS: dict[str, dict[str, Animation | list[pygame.Surface]]] = {
    "Ginger": {
        "idle": get_spritesheet_images((16, 16), load_image("Ginger/idle.png")),
        "walk_d": Animation(get_spritesheet_images((16, 16), load_image("Ginger/walking_d.png")), 5),
        "walk_u": Animation(get_spritesheet_images((16, 16), load_image("Ginger/walking_u.png")), 5),
        "walk_s": Animation(get_spritesheet_images((16, 16), load_image("Ginger/walking_s.png")), 5)
    },
    "cave_girl": {
        "idle": get_spritesheet_images((16, 16), load_image("cave_girl/idle.png")),
        "walk_d": Animation(get_spritesheet_images((16, 16), load_image("cave_girl/walk_d.png"), True), 5),
        "walk_u": Animation(get_spritesheet_images((16, 16), load_image("cave_girl/walk_u.png"), True), 5),
        "walk_s": Animation(get_spritesheet_images((16, 16), load_image("cave_girl/walk_s.png"), True), 5)
    },
    "dalmatian": {
        "idle": get_spritesheet_images((21, 19), load_image("dalmatian/idle.png")),
        "walk_d": Animation(get_spritesheet_images((21, 19), load_image("dalmatian/walk_d.png")), 3),
        "walk_u": Animation(get_spritesheet_images((21, 19), load_image("dalmatian/walk_u.png")), 3),
        "walk_s": Animation(get_spritesheet_images((21, 19), load_image("dalmatian/walk_s.png")), 3)
    },
    "knight": {
        "idle": get_spritesheet_images((16, 20), load_image("knight/idle.png")),
        "walk_d": Animation(get_spritesheet_images((16, 20), load_image("knight/walk_d.png")), 5),
        "walk_u": Animation(get_spritesheet_images((16, 20), load_image("knight/walk_u.png")), 5),
        "walk_s": Animation(get_spritesheet_images((16, 20), load_image("knight/walk_s.png")), 5)
    },
    "wizard": {
        "idle": get_spritesheet_images((16, 20), load_image("wizard/idle.png")),
        "walk_d": Animation(get_spritesheet_images((16, 20), load_image("wizard/walk_d.png")), 5),
        "walk_u": Animation(get_spritesheet_images((16, 20), load_image("wizard/walk_u.png")), 5),
        "walk_s": Animation(get_spritesheet_images((16, 20), load_image("wizard/walk_s.png")), 5)
    },
        "mother": {
        "idle": get_spritesheet_images((32, 32), load_image("mother/idle.png")),
        "walk_d": Animation(get_spritesheet_images((32, 32), load_image("mother/walk_d.png")), 8),
        "walk_u": Animation(get_spritesheet_images((32, 32), load_image("mother/walk_u.png")), 8),
        "walk_s": Animation(get_spritesheet_images((32, 32), load_image("mother/walk_s.png")), 8)
    }
}