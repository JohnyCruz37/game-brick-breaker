import pygame, os
from dataclasses import dataclass
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH

@dataclass
class Ball:
    position_x: float
    position_y: float
    radius: float
    color: tuple
    base_dir: str
    speed_x: float = 0.0
    speed_y: float = 0.0

    def __post_init__(self):
        image_path = os.path.join(self.base_dir, 'assets', 'images', 'esfera-amarela.jfif')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect(center = (self.position_x, self.position_y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        self.position_x += self.speed_x
        self.position_y += self.speed_y
        self.rect.center = (self.position_x, self.position_y)
        self.check_collisions_with_walls()
    
    def check_collisions_with_walls(self):
        if self.position_x - self.radius <= 0 or self.position_x + self.radius >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.position_y - self.radius <= 0 or self.position_y + self.radius >= SCREEN_HEIGHT:
            self.speed_y *= -1
    
    def check_collisions_with_paddle(self, paddle, ball_attached):
        if self.rect.colliderect(paddle.rect):
            self.speed_y *= -1
            if not ball_attached:
                self.rect.bottom = paddle.rect.top - 1
            return True
        return False
    
    def check_collisions_with_bricks(self, brick):
        if brick.is_active:
            if self.rect.colliderect(brick.rect):
                self.speed_y *= -1
                brick.is_active = False
    
    def reset(self, paddle):
        self.position_x = paddle.position_x + paddle.width // 2
        self.position_y = paddle.position_y - self.radius
        self.speed_x = 0
        self.speed_y = 0
        self.rect.center = (self.position_x, self.position_y)