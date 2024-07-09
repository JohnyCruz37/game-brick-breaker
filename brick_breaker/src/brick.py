import pygame
from dataclasses import dataclass

@dataclass
class Brick:
    def __init__(self, position_x, position_y, width, height, color):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color
        self.is_active = True
        self.rect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)

    def draw(self, screen):
        if self.is_active:
            pygame.draw.rect(screen, self.color, self.rect)