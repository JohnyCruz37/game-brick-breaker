import pygame, os
from dataclasses import dataclass
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH

@dataclass
class Ball:
    position_x: float
    position_y: float
    radius: float
    color: tuple
    speed_x: float = 0.0
    speed_y: float = 0.0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), self.radius)

    def update(self):
        self.position_x += self.speed_x
        self.position_y += self.speed_y
        self.check_collisions_with_walls()
    
    def reset(self, paddle):
        self.position_x = paddle.position_x + paddle.width // 2
        self.position_y = paddle.position_y - self.radius
        self.speed_x = 0
        self.speed_y = 0
    
    def check_collisions_with_walls(self):
        if self.position_x - self.radius <= 0 or self.position_x + self.radius >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.position_y - self.radius <= 0 or self.position_y + self.radius >= SCREEN_HEIGHT:
            self.speed_y *= -1
    
    def check_collisions_with_paddle(self, paddle, ball_attached):
        if (self.position_y + self.radius >= paddle.position_y 
            and paddle.position_x <= self.position_x <= paddle.position_x + paddle.width):
            self.speed_y = -self.speed_y
            self.position_y = paddle.position_y - self.radius # Evita que a bola fique dentro do objeto
            return True
        return False
    
    def check_collisions_with_bricks(self, brick):
        if (brick.position_x <= self.position_x <= brick.position_x + brick.width and 
            brick.position_y <= self.position_y <= brick.position_y + brick.height):
            self.speed_y = -self.speed_y
            brick.is_active = False
            return True
        return False
    
