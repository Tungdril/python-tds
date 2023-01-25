import pygame
import os

path = (os.getcwd())

def background(screen):
    img = pygame.image.load(path +"/assets/map.jpeg").convert()
    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))

def wave(screen, wave):
    font = pygame.font.SysFont("daytona", 40)
    text = font.render("Wave: " + str(wave) + "/10", True, (0,0,0))
    screen.blit(text, (10, 10))

def health(screen, health):
    font = pygame.font.SysFont("daytona", 40)
    text = font.render("Health: " + str(health), True, (0,0,0))
    screen.blit(text, (10, 40))

def money(screen, money):
    font = pygame.font.SysFont("daytona", 40)
    text = font.render("Money: " + str(money) + "$", True, (0,0,0))
    screen.blit(text, (10, 760))

def gameOver(screen):
    img = pygame.image.load(path +"/assets/game_over.png").convert()
    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))

def win(screen):
    img = pygame.image.load(path +"/assets/win.png").convert_alpha()
    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))

def showPrice(screen, buttonType, location):

    if buttonType == "buttonMg":
        towerPrice = 100
    elif buttonType == "buttonSniper":
        towerPrice = 200
    elif buttonType == "buttonFlamer":
        towerPrice = 500
    elif buttonType == "buttonBarracks":
        towerPrice = 500
    elif buttonType == "buttonBank":
        towerPrice = 1000

    location = (location[0] - 30, location[1] - 40)

    font = pygame.font.SysFont("daytona", 40)
    text = font.render(str(towerPrice) + "$", True, (255,255,255), (0,0,0))
    screen.blit(text, location)

def showResellValue(screen, tower, location):
    resellPrice = int(tower.price * 0.25)
    location = (location[0] - 20, location[1] - 40)

    font = pygame.font.SysFont("daytona", 40)
    text = font.render(str(resellPrice) + "$", True, (255,255,255), (0,0,0))
    screen.blit(text, location)