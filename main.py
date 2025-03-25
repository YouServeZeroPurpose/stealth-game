import pygame
from levels import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()
window_width, window_height = 500, 500

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Stealth Game')

menu_background = pygame.image.load('menu.png')

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.hitbox = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.hitbox.x, self.hitbox.y))

game = True

while game:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

    pygame.display.update()
    clock.tick(FPS)