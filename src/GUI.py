import pygame
import os

path = (os.getcwd())

def main(screen):
    img = pygame.image.load(path +"/assets/mapPlaceholder.png")
    img.convert()

    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))


def test():
    targetList = [(100, 100), (200, 200), (300, 300), (400, 400), (500, 500)]

    i = 0

    l = len(targetList)
    #print(len(targetList))
    
    while i < l:
        print(targetList[i][0])
        i += 1
test()