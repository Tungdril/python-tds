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
    img_wave = pygame.transform.scale(img_wave, (60, 40))

    global img_health
    img_health = pygame.image.load(path + "/assets/heart.png").convert_alpha()
    img_health = pygame.transform.scale(img_health, (40, 40))

    global img_mouse_right
    img_mouse_right = pygame.image.load(path + "/assets/mouse_right.png").convert_alpha()
    img_mouse_right = pygame.transform.scale(img_mouse_right, (20, 30))

    global img_mouse_left
    img_mouse_left = pygame.image.load(path + "/assets/mouse_left.png").convert_alpha()
    img_mouse_left = pygame.transform.scale(img_mouse_left, (20, 30))

    global img_main_menu
    img_main_menu = pygame.image.load(path + "/assets/main_menu.png").convert()
    img_main_menu = pygame.transform.scale(img_main_menu, (1200, 800))

print("Assets loaded")

def background(screen):
    screen.blit(img_background, (0, 0))

def mainMenu(screen):
    screen.blit(img_main_menu, (0, 0))

def wave(screen, wave):
    text = font.render("       " + str(wave) + "/10", True, (0,0,0))
    screen.blit(text, (10, 20))
    screen.blit(img_wave, (10, 10))

def health(screen, health):
    text = font.render("       " + str(health), True, (0,0,0))
    screen.blit(text, (10, 70))
    screen.blit(img_health, (15, 60))

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
    screen.blit(img_mouse_left, (location[0] - 30, location[1]))

def showResellValue(screen, tower, location):
    resellPrice = int(tower.price * 0.25)
    location = (location[0] - 20, location[1] - 40)

    text = font.render(str(resellPrice) + "$", True, (255,255,255), (0,0,0))
    screen.blit(text, location)
    screen.blit(img_mouse_right, (location[0] - 30, location[1]))

def healthBar(screen, health, maxHealth, location, image, type):
    spriteWidth = image.get_size()[0]

    # draw red part of health bar, width equal to width of sprite
    pygame.draw.rect(screen, (255, 0, 0), (location[0], location[1] - 20, spriteWidth, 5))

    # calculate width of green part of health bar
    greenWidth = int(spriteWidth * (health / maxHealth))
    pygame.draw.rect(screen, (0, 255, 0), (location[0], location[1] - 20, greenWidth, 5))