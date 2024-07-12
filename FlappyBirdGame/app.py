import logging
import pygame
from settings import initialize_screen, GRAVITY, JUMP_STRENGTH, BIRD_SPEED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import random

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

class Cylinder:
    def __init__(self, x, gap_y, gap_size):
        self.x = x
        self.gap_y = gap_y
        self.gap_size = gap_size
        self.width = 50

    def update(self):
        self.x -= BIRD_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.gap_y + self.gap_size, self.width, screen.get_height() - (self.gap_y + self.gap_size)))

def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main():
    screen, width, height = initialize_screen()
    clock = pygame.time.Clock()
    bird = Bird(width // 4, height // 2)
    cylinders = []
    score = 0

    game_state = "start"
    countdown = 3
    countdown_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if game_state == "start":
                    game_state = "countdown"
                    countdown_timer = pygame.time.get_ticks()
                elif game_state == "playing":
                    bird.jump()
                elif game_state == "game_over":
                    game_state = "countdown"
                    countdown = 3
                    countdown_timer = pygame.time.get_ticks()
                    bird = Bird(width // 4, height // 2)
                    cylinders = []
                    score = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"

        screen.fill((135, 206, 235))  # Sky blue background

        if game_state == "start":
            draw_text(screen, "Click to Start", 50, width // 2, height // 2)
        elif game_state == "countdown":
            current_time = pygame.time.get_ticks()
            if current_time - countdown_timer > 1000:
                countdown -= 1
                countdown_timer = current_time
            if countdown == 0:
                game_state = "playing"
            draw_text(screen, str(countdown), 100, width // 2, height // 2)
        elif game_state == "playing":
            bird.update()
            pygame.draw.circle(screen, (255, 255, 0), (int(bird.x), int(bird.y)), 20)  # Yellow bird

            if len(cylinders) == 0 or cylinders[-1].x < width - 300:
                gap_y = random.randint(100, height - 200)
                gap_size = random.randint(150, 250)
                cylinders.append(Cylinder(width, gap_y, gap_size))

            for cylinder in cylinders:
                cylinder.update()
                cylinder.draw(screen)

                if cylinder.x + cylinder.width < bird.x and not hasattr(cylinder, 'passed'):
                    score += 1
                    cylinder.passed = True

                if (bird.x + 20 > cylinder.x and bird.x - 20 < cylinder.x + cylinder.width and
                    (bird.y - 20 < cylinder.gap_y or bird.y + 20 > cylinder.gap_y + cylinder.gap_size)):
                    game_state = "game_over"

            cylinders = [c for c in cylinders if c.x + c.width > 0]

            if bird.y > height or bird.y < 0:
                game_state = "game_over"

            draw_text(screen, f"Score: {score}", 30, width // 2, 30)
            draw_text(screen, "Press 'P' to Pause", 20, width // 2, 60)
        elif game_state == "paused":
            for cylinder in cylinders:
                cylinder.draw(screen)
            pygame.draw.circle(screen, (255, 255, 0), (int(bird.x), int(bird.y)), 20)  # Yellow bird
            draw_text(screen, "PAUSED", 50, width // 2, height // 2)
            draw_text(screen, "Press 'P' to Resume", 30, width // 2, height // 2 + 50)
        elif game_state == "game_over":
            draw_text(screen, "Game Over", 50, width // 2, height // 2 - 50)
            draw_text(screen, f"Final Score: {score}", 30, width // 2, height // 2)
            draw_text(screen, "Click to Restart", 30, width // 2, height // 2 + 50)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
