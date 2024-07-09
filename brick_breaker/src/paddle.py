import pygame
from dataclasses import dataclass
from src.settings import SCREEN_WIDTH

@dataclass
class Paddle:
    position_x: float
    position_y: float
    width: float
    height: float
    color: tuple
    speed: float = 5.0


    def move_left(self):
        self.position_x -= self.speed
        if self.position_x < 0:
            self.position_x = 0
    
    def move_right(self):
        self.position_x += self.speed
        if self.position_x > SCREEN_WIDTH - self.width:
            self.position_x = SCREEN_WIDTH - self.width
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position_x, self.position_y, self.width, self.height))
    
    def reset(self):
        self.position_x = (SCREEN_WIDTH - self.width) // 2