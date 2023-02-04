import pygame
import os

def init():
    global path
    path = (os.getcwd())

    pygame.mixer.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    pygame.mixer.music.load(path + "/assets/sound/backgroundmusic.wav")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

    global cash
    cash = pygame.mixer.Sound(path + "/assets/sound/cash.wav")

    global damage
    damage = pygame.mixer.Sound(path + "/assets/sound/damage.wav")

    global enemydeath
    enemydeath = pygame.mixer.Sound(path + "/assets/sound/enemydeath.wav")

    global error
    error = pygame.mixer.Sound(path + "/assets/sound/error.wav")

    global gameover
    gameover = pygame.mixer.Sound(path + "/assets/sound/gameover.wav")

    global spawn
    spawn = pygame.mixer.Sound(path + "/assets/sound/spawn.wav")

    global towerplaceing
    towerplaceing = pygame.mixer.Sound(path + "/assets/sound/towerplaceing.wav")

    global wavespawn
    wavespawn = pygame.mixer.Sound(path + "/assets/sound/wavespawn.wav")

    print("Sounds loaded")

def playMusic():
    pygame.mixer.music.unpause()

def stopMusic():
    pygame.mixer.music.pause()

def playSound(sound):
    sound.play()