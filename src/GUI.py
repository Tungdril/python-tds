import pygame
import os

def init():
    global path
    path = (os.getcwd())

    global font
    font = pygame.font.Font(path + "/assets/DaytonaPro-Semibold-custom.ttf", 30)

def background(screen):
    img = pygame.image.load(path +"/assets/map.jpeg").convert()
    img = pygame.transform.scale(img, (1200, 800))

    screen.blit(img, (0, 0))

def wave(screen, wave):
    text = font.render("Wave: " + str(wave) + "/10", True, (0,0,0))
    screen.blit(text, (10, 10))

def health(screen, health):
    text = font.render("Health: " + str(health), True, (0,0,0))
    screen.blit(text, (10, 40))

def money(screen, money):
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

    text = font.render(str(towerPrice) + "$", True, (255,255,255), (0,0,0))
    screen.blit(text, location)

def showResellValue(screen, tower, location):
    resellPrice = int(tower.price * 0.25)
    location = (location[0] - 20, location[1] - 40)

    text = font.render(str(resellPrice) + "$", True, (255,255,255), (0,0,0))
    screen.blit(text, location)

def healthBar(screen, health, maxHealth, location, image, type):
    spriteWidth = image.get_size()[0]

    # draw red part of health bar, width equal to width of sprite
    pygame.draw.rect(screen, (255, 0, 0), (location[0], location[1] - 20, spriteWidth, 5))

    # calculate width of green part of health bar
    greenWidth = int(spriteWidth * (health / maxHealth))
    pygame.draw.rect(screen, (0, 255, 0), (location[0], location[1] - 20, greenWidth, 5))
