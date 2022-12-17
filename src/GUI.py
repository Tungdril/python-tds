import pygame
import os

path = (os.getcwd())

def main(screen):
    img = pygame.image.load(path +"/assets/mapPlaceholder.png")
    img.convert()

    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))