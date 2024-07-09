import pygame, os
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, BACKGROUND_COLOR
from src.ball import Ball
from src.paddle import Paddle
from src.brick import Brick
from src.score import Score
from src.text_renderer import TextRenderer

class Game:
    def __init__(self, base_dir):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.base_dir = base_dir #encontrar arquivos

        self.ball = Ball(position_x=SCREEN_WIDTH // 2, position_y=SCREEN_HEIGHT // 2, radius=10, color=(255, 0, 0), base_dir=self.base_dir)
        self.paddle = Paddle(position_x=SCREEN_WIDTH // 2 - 50, position_y=SCREEN_HEIGHT - 30, width=100, height=10, color=(0, 255, 0))
        self.bricks = self.create_bricks()
        self.score = Score()
        self.lives = 3
        self.ball_attached = True

        self.load_sounds()
        self.text_renderer = TextRenderer(self.screen)
    
    def load_sounds(self):
        collision_sound_path = os.path.join("brick_breaker", 'assets', 'sounds', 'collision.wav')
        brick_break_sound_path = os.path.join("brick_breaker", 'assets', 'sounds', 'ball.wav')
        victory_sound_path = os.path.join("brick_breaker", 'assets', 'sounds', 'victory.wav')
        ball_paddle_sound_path = os.path.join("brick_breaker", 'assets', 'sounds', 'ball-paddle.wav')

        self.collision_sound = pygame.mixer.Sound(collision_sound_path)
        self.brick_break_sound = pygame.mixer.Sound(brick_break_sound_path)
        self.victory_sound = pygame.mixer.Sound(victory_sound_path)
        self.ball_paddle_sound = pygame.mixer.Sound(ball_paddle_sound_path)
    
    def create_bricks(self):
        brincks = []
        for row in range(5):
            for b in range(9):
                brinck = Brick(position_x= 80 * b + 10, position_y= 30 * row + 10, width=70, height=20, color=(0, 0, 255))
                brincks.append(brinck)
        return brincks
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "menu" and event.key == pygame.K_RETURN:
                    self.reset_game()
                    self.state = "playing"
                elif self.state == "playing" and event.key == pygame.K_SPACE:
                    self.state = "paused"
                elif self.state == "paused":
                    if event.key == pygame.K_SPACE:
                        self.state = "playing"
                    elif event.key == pygame.K_m:
                        self.state = "menu"

        keys = pygame.key.get_pressed()
        if self.state == "playing":
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
                if self.ball_attached:
                    self.ball_attached = False
                    self.ball.speed_x = 5.0
                    self.ball.speed_y = -5.0

            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()
                if self.ball_attached:
                    self.ball_attached = False
                    self.ball.speed_x = -5.0
                    self.ball.speed_y = -5.0
    
    def update(self):
        if self.state == "playing":
            if self.ball_attached:
                self.ball.position_x = self.paddle.position_x + self.paddle.width // 2
                self.ball.position_y = self.paddle.position_y - self.ball.radius
            else:
                self.ball.update()
            self.check_collision()

    def check_collision(self):
        if self.ball.check_collisions_with_paddle(self.paddle, self.ball_attached):
            if not self.ball_attached:
                self.ball_paddle_sound.play()

        for brick in self.bricks:
            if brick.is_active:
                self.ball.check_collisions_with_bricks(brick)
                if not brick.is_active:
                    self.brick_break_sound.play()
                    self.score.increase()
        
        if self.ball.position_y + self.ball.radius >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives == 0:
                self.state = "menu"
            else:
                self.paddle.reset()
                self.ball.reset(self.paddle)
                self.ball_attached = True
            self.collision_sound.play()

        if all(not brick.is_active for brick in self.bricks):
            self.victory_sound.play()
            self.state = "menu"

    def reset_game(self):
        self.lives = 3
        self.paddle.reset()
        self.ball.reset(self.paddle)
        self.bricks = self.create_bricks()
        self.score.reset()
        self.ball_attached = True

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        if self.state == "menu":
            self.text_renderer.draw_text("Pressione o ENTER para jogar", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        if self.state == "playing":
            self.ball.draw(self.screen)
            self.paddle.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            self.score.draw(self.screen)
            self.text_renderer.draw_text(f"Vidas: {self.lives}",30, SCREEN_WIDTH - 100, 30)

        if self.state == "paused":
            self.text_renderer.draw_text("Paused", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            self.text_renderer.draw_text("Press SPACE to Continue", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.text_renderer.draw_text("Press M to Return to Menu", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

        pygame.display.flip()

    def quit(self):
        pygame.quit()