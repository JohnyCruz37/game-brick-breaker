import pygame

class TextRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, size, position_x, position_y, color=(255, 255, 255)):
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(position_x, position_y))
        self.screen.blit(text_surface, text_rect)