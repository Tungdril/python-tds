import pygame
import os

path = (os.getcwd())

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

def main(screen):
    screen.fill(WHITE)

    img = pygame.image.load(path +"/assets/mapPlaceholder.png")
    img.convert()

    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))