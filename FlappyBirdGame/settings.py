import pygame

def initialize_screen():
    pygame.init()
    infoObject = pygame.display.Info()
    width, height = int(infoObject.current_w * 0.8), int(infoObject.current_h * 0.8)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Bird")
    return screen, width, height

# Game physics
GRAVITY = 0.5
JUMP_STRENGTH = 10
BIRD_SPEED = 3
