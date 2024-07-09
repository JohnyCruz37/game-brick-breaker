import pygame
from dataclasses import dataclass

@dataclass
class Score:
    value: int = 0
    font_name: str = "Arial"
    font_size: int = 30
    color: tuple = (255, 255, 255)

    def increase(self, amount: int = 1):
        self.value += amount
    
    def draw(self, screen):
        font = pygame.font.SysFont(self.font_name, self.font_size)
        score_surface = font.render(f"Score: {self.value}", True, self.color)
        screen.blit(score_surface, (10, 10))
    
    def reset(self):
        self.value = 0