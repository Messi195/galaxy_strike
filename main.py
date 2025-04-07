import pygame
import sys
import random
from typing import List

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# FPS settings
FPS = 60
clock = pygame.time.Clock()

# Load and rotate the spaceship image
fl_image_load = pygame.image.load("fl.png").convert_alpha()
fl_image = pygame.transform.rotate(fl_image_load, 180)

class Ship:
    def __init__(self):
        self.width, self.height = fl_image.get_size()
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 7
        self.last_shot_time = 0

    def draw(self) -> None:
        """Draw the ship on the screen."""
        screen.blit(fl_image, (self.x, self.y))

    def move(self, keys: List[bool]) -> None:
        """Move the ship based on key inputs."""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self, bullets: List["Bullet"]) -> None:
        """Shoot a bullet if enough time has passed since the last shot."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 350:
            bullets.append(Bullet(self.x + self.width // 2, self.y))
            self.last_shot_time = current_time

class Bullet:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 5

    def draw(self) -> None:
        """Draw the bullet on the screen."""
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def update(self) -> bool:
        """Update the bullet position. Return False if the bullet goes off-screen."""
        self.y -= self.speed
        return self.y > 0

class Enemy:
    def __init__(self) -> None:
        self.width, self.height = 50, 50
        self.x = random.randint(0, WIDTH - self.width)
        self.y = 100
        self.speed_x = 3
        self.alive = True

    def draw(self) -> None:
        """Draw the enemy on the screen."""
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def update(self) -> None:
        """Update the enemy's position."""
        if self.alive:
            self.x += self.speed_x
            if self.x <= 0 or self.x >= WIDTH - self.width:
                self.speed_x = -self.speed_x

    def reset(self) -> None:
        """Reset the enemy's position and speed when it's destroyed."""
        self.x = random.randint(0, WIDTH - self.width)
        self.speed_x = abs(self.speed_x) + 0.5 if self.speed_x < 0 else -abs(self.speed_x) - 5
        self.alive = True

def game_loop() -> None:
    """Main game loop."""
    ship = Ship()
    bullets = []
    enemy = Enemy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        ship.move(keys)
        if keys[pygame.K_e]:
            ship.shoot(bullets)

        bullets[:] = [bullet for bullet in bullets if bullet.update()]

        for bullet in bullets:
            if enemy.alive and enemy.x < bullet.x < enemy.x + enemy.width and enemy.y < bullet.y < enemy.y + enemy.height:
                enemy.alive = False
                bullets.remove(bullet)

        if not enemy.alive:
            enemy.reset()

        enemy.update()

        screen.fill(BLACK)
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        if enemy.alive:
            enemy.draw()

        pygame.display.flip()
        clock.tick(FPS)

# Start the game
game_loop()
