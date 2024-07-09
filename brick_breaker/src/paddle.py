import pygame
from dataclasses import dataclass
from src.settings import SCREEN_WIDTH

@dataclass
class Paddle:
    def __init__(self, position_x, position_y, width, height, color):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)


    def move_left(self):
        self.position_x -= self.speed
        if self.position_x < 0:
            self.position_x = 0
    
    def move_right(self):
        self.position_x += self.speed
        if self.position_x > SCREEN_WIDTH - self.width:
            self.position_x = SCREEN_WIDTH - self.width
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def reset(self):
        self.position_x = SCREEN_WIDTH // 2 - self.width // 2
        self.rect.x = self.position_x