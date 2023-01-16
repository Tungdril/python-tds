import pygame
import os

path = (os.getcwd())



def background(screen):
    img = pygame.image.load(path +"/assets/map.png").convert()
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