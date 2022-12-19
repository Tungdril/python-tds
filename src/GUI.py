import pygame
import os

path = (os.getcwd())

def background(screen):
    img = pygame.image.load(path +"/assets/map.png").convert()
    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))

#def buildingMenu(screen):
#
#    #TODO replace with actual images
#    towerList = ["towerUI", "towerUI", "towerUI", "towerUI", "towerUI"]
#
#    # loop through the list of towers and draw them on the screen
#    for i in range(len(towerList)):
#        img = pygame.image.load(path +"/assets/" + towerType + ".png").convert_alpha()
#        img = pygame.transform.scale(img, (100, 100))
#
#        # not perfectly centered, but close enough 
#        screen.blit(img, ((i+1)*180, 685))