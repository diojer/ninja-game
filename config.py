import pygame


DEBUG = False

DISPLAY_SCALE = 5

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DISPLAY_WIDTH = SCREEN_WIDTH // DISPLAY_SCALE
DISPLAY_HEIGHT = SCREEN_HEIGHT // DISPLAY_SCALE

GAME_CAPTION = "Ninja Game"

TILE_SIZE = 16