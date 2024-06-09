from dataclasses import dataclass, field
import pygame, sys
from pygame import Vector2, Rect, FRect
from .utils import round_vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game