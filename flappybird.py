import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Bird properties
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_X = 50
BIRD_Y = SCREEN_HEIGHT // 2 - BIRD_HEIGHT // 2
BIRD_FLAP_SPEED = -9
GRAVITY = 0.5

# Pipe properties
PIPE_WIDTH = 60
PIPE_HEIGHT = SCREEN_HEIGHT - 200
GAP_SIZE = 150
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 120

# Font
font = pygame.font.Font(None, 36)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(BIRD_X, BIRD_Y))
        self.vel_y = 0

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

    def flap(self):
        # Flap the bird
        self.vel_y = BIRD_FLAP_SPEED

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, 0))

    def update(self):
        # Move the pipe to the left
        self.rect.x -= PIPE_SPEED

class Game:
    def __init__(self):
        # Initialize game variables
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = pygame.sprite.Group()
        self.score = 0
        self.state = MENU

    def run(self):
        # Main game loop
        while True:
            if self.state == MENU:
                self.menu()
            elif self.state == PLAYING:
                self.playing()
            elif self.state == GAME_OVER:
                self.game_over()

    def menu(self):
        # Menu screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = PLAYING

        # Display menu text
        self.screen.fill(WHITE)
        text = font.render("Press SPACE to Play", True, BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        self.clock.tick(30)

    def playing(self):
        # Game logic for playing state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

        # Update bird
        self.bird.update()

        # Spawn pipes
        if pygame.time.get_ticks() % PIPE_SPAWN_INTERVAL == 0:
            pipe = Pipe(SCREEN_WIDTH)
            self.pipes.add(pipe)

        # Update pipes
        self.pipes.update()

        # Check for collisions with pipes
        if pygame.sprite.spritecollide(self.bird, self.pipes, False):
            self.state = GAME_OVER

        # Remove off-screen pipes and update score
        for pipe in self.pipes:
            if pipe.rect.right < 0:
                pipe.kill()
                self.score += 1

        # Display score
        self.screen.fill(WHITE)
        score_text = font.render(str(self.score), True, BLUE)
        self.screen.blit(score_text, (10, 10))

        # Draw bird and pipes
        self.screen.blit(self.bird.image, self.bird.rect)
        self.pipes.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(30)

    def game_over(self):
        # Game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__init__()

        # Display game over text
        self.screen.fill(WHITE)
        text = font.render(f"Game Over! Score: {self.score}. Press SPACE to Play Again", True, BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        self.clock.tick(30)

# Main function
if __name__ == "__main__":
    game = Game()
    game.run()
