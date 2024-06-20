from dataclasses import dataclass, field
import pygame, sys
from pygame import Vector2, Rect, FRect, Surface
from .utils import round_vector
from typing import TYPE_CHECKING
from config import *
if TYPE_CHECKING:
    from game import Game
    from .levels import Level