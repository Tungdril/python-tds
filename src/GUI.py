import pygame
import os

def init():
    global path
    path = (os.getcwd())

    global font
    font = pygame.font.Font(path + "/assets/DaytonaPro-Semibold-custom.ttf", 30)

    # load assets once, saves memory and drastically improves performance
    global img_background
    img_background = pygame.image.load(path + "/assets/map.jpeg").convert()
    img_background = pygame.transform.scale(img_background, (1200, 800))

    global img_game_over
    img_game_over = pygame.image.load(path + "/assets/game_over.png").convert()
    img_game_over = pygame.transform.scale(img_game_over, (1200, 800))

    global img_win
    img_win = pygame.image.load(path + "/assets/win.png").convert()
    img_win = pygame.transform.scale(img_win, (1200, 800))

    global img_wave
    img_wave = pygame.image.load(path + "/assets/wave.png").convert_alpha()
    img_wave = pygame.transform.scale(img_wave, (50, 50))

    #img_health = pygame.image.load(path + "/assets/health.png").convert_alpha()
    #img_health = pygame.transform.scale(img_health, (50, 80))

print("Assets loaded")

def background(screen):
    screen.blit(img_background, (0, 0))

def wave(screen, wave):
    text = font.render("Wave: " + str(wave) + "/10", True, (0,0,0))
    screen.blit(text, (10, 10))
    screen.blit(img_wave, (10, 10))

def health(screen, health):
    text = font.render("Health: " + str(health), True, (0,0,0))
    screen.blit(text, (10, 40))

def money(screen, money):
    text = font.render(str(money) + "$", True, (0,0,0))

    screen.blit(text, (1080, 10))

def gameOver(screen):
    screen.blit(img_game_over, (0, 0))

def win(screen):
    screen.blit(img_win, (0, 0))

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
