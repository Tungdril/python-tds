# https://www.pygame.org/docs/
# https://pygame.readthedocs.io/en/latest/index.html

# import all the modules

import GUI
import readWaves
import os

try:
    import pygame # check if pygame is installed, import if it is
except ImportError:

    # if pygame is not installed, attempt to install it using pip
    print("Pygame not installed. Attempting to install")
    try:
        import pip
    except ImportError:
        print("Pip not installed. Install pip and try again")
        exit()
    else:
        try:
            pip.main(["install", "pygame"])
        except:
            print("Erorr installing pygame. Install pygame manually and try again")
            exit()
        else:
            print("Pygame installed")
            import pygame

# ---------------------------------------------------------------------------------------------------- #    

# print pygame version
# print(pygame.version.ver)

# class definitions
class Path(pygame.sprite.Sprite):
    def __init__(self, screen, color, points, width):
        # calls constructor of parent class
        pygame.sprite.Sprite.__init__(self)

        # draws a polygon based on the points given on the screen
        pygame.draw.polygon(screen, color, points, width)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, position, type):
        # calls constructor of parent class
        pygame.sprite.Sprite.__init__(self)

        # initializes screen, position and type
        self.screen = screen
        self.position = position
        self.type = type

        # loads the image, scales it to 50x50, makes alpha channel transparent
        self.imgPath = os.getcwd() + "/assets/" + type + ".png"
        img = pygame.image.load(self.imgPath).convert_alpha()
        img = pygame.transform.scale(img, (50, 50))
        self.image = img

        # sets waypoints to follow
        self.waypoints = [(-50, 390), (330, 390), (330, 170), (580, 170), (580, 580), (310, 580), (310, 710), (940, 710), (940, 470), (710, 460), (710, 300), (970, 290), (970, 5), (700, 5), (700,-50)]
        self.waypointsIndex = 0

        # determines which enemy to spawn based on the type given
        self.determineType()

    def spawnLightEnemy(self):
        self.health = 100
        self.isArmored = False
        self.speed = 5
        self.damage = 1
        self.color = (255, 0, 0)
      
        # draws a rectangle over the image, used for collision detection
        self.rect = self.image.get_rect(center=self.position)

        print("Light enemy spawned")

    def spawnHeavyEnemy(self):  
        self.health = 200
        self.isArmored = True
        self.speed = 5
        self.damage = 1
        self.color = (0, 0, 255)

        self.rect = self.image.get_rect(center=self.position)

        print("Heavy enemy spawned")

    def spawnFastEnemy(self):  
        self.health = 100
        self.isArmored = False
        self.speed = 5
        self.damage = 1
        self.color = (0, 255, 0)

        self.rect = self.image.get_rect(center=self.position)

        print("Fast enemy spawned")

    def spawnBossEnemy(self):
        self.health = 500
        self.isArmored = True
        self.speed = 5
        self.damage = 2
        self.color = (255, 255, 0)

        self.rect = self.image.get_rect(center=self.position)

        print("Boss enemy spawned")

    def determineType(self):
        # determines which enemy to spawn based on the type given
        if self.type == "light":
            self.spawnLightEnemy()
        elif self.type == "heavy":
            self.spawnHeavyEnemy()
        elif self.type == "fast":
            self.spawnFastEnemy()
        elif self.type == "boss":
            self.spawnBossEnemy()
        
        # after spawning the enemy, add it to the groupEnemies group
        groupEnemies.add(self)
        groupSprites.add(self)
        print("Current enemies:", len(groupEnemies.sprites()))

    def draw(self):
        # draws the enemy continuously on screen
        groupEnemies.draw(self.screen)

    def killEnemy(self):
        # removes the enemy from all groups, preventing it from being drawn
        self.kill()
        print(self.type, "killed")

    def move(self):
        # moves the enemy along a predefined path
        # if own position on x-axis is less than target position, increment x-axis by speed
        if self.rect.x < self.waypoints[self.waypointsIndex][0]:
            self.rect.x += self.speed
        # if own position on x-axis is greater than target position, decrement x-axis by speed
        elif self.rect.x > self.waypoints[self.waypointsIndex][0]:
            self.rect.x -= self.speed
        # if own position on y-axis is less than target position, increment y-axis by speed
        if self.rect.y < self.waypoints[self.waypointsIndex][1]:
            self.rect.y += self.speed
        # if own position on y-axis is greater than target position, decrement y-axis by speed
        elif self.rect.y > self.waypoints[self.waypointsIndex][1]:
            self.rect.y -= self.speed

        # if own position is equal to target position, increment waypoint index
        if self.rect.x == self.waypoints[self.waypointsIndex][0] and self.rect.y == self.waypoints[self.waypointsIndex][1]:
            # if waypoint index is less than the length of the waypoints list, increment waypoint index
            if self.waypointsIndex < len(self.waypoints) - 1:
                self.waypointsIndex += 1
                print(self.type, "reached waypoint", self.waypointsIndex -1, "moving to waypoint", self.waypointsIndex)
            # if waypoint index is equal to the length of the waypoints list, reset waypoint index to 0
            else:
                self.waypointsIndex = 0
                self.killEnemy()
                print(self.type, "reached final waypoint, commencing purge")
            

# initialize pygame
pygame.init()

# set a clock, used for framerate
clock = pygame.time.Clock()

# pygame Sprite group definitions
# all obejcts which are collidable should be added to this group
groupColliders = pygame.sprite.Group()

# all enemies should be added to this group
groupEnemies = pygame.sprite.Group()

# all Sprites should be added to this group
groupSprites = pygame.sprite.Group()

def main():

    # deactivates console by default
    consoleActive = True

    pygame.display.set_caption("Python TDS") # set the window title
    screen = pygame.display.set_mode((1200, 800)) # create a window 
    
    #TODO determine current wave, pass it to the spawnEnemy function
    #enemySpawner.main(1, screen)

    spawnEnemy(screen)

    #for i in range(0, 10):
#
    #    pos = (100+(i*50), 100)
#
    #    Enemy(screen, pos, "light")

    # main loop 
    while True:

        # set framerate
        clock.tick(30)

        # run the main function in GUI.py
        GUI.main(screen)
         
        # draw the path
        createMapPath(screen)

        for event in pygame.event.get():

            # exit if the user clicks the close button
            if event.type == pygame.QUIT: # if the user clicks the close button, exit
                exit()
            # DEEBUG: kills enemy if it is clicked 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for enemy in groupEnemies:
                    if enemy.rect.collidepoint(event.pos):
                        enemy.killEnemy()
            
            # check if a key has been pressed
            if event.type == pygame.KEYDOWN:

                # show/hide console
                if event.key == pygame.K_c:
                    consoleActive = True
                    print("Console activated, press X to hide")
                elif event.key == pygame.K_x:
                    consoleActive = False
                    print("Console deactivated, press C to show")
                elif event.key == pygame.K_k:
                    print(groupEnemies.sprites())

            # print all events if flag is set
            if consoleActive:
                print(event)

        # draw, move all enemies continuously
        for enemy in groupEnemies:
            enemy.draw()
            enemy.move()
            
        # update the screen continuously    
        pygame.display.update()

def createMapPath(screen):

    # defines path corners
    points = [(0, 380), (320, 380), (320, 160), (640, 160), (640, 630), (360 , 630), (360, 700), (930, 700), (930, 520), (700, 520), (700, 290), (960, 290), (960, 60), (700, 60), (700, 0), (1030, 0), (1030, 350), (760, 350), (760, 460), (1000, 460), (1000, 760), (290, 760), (290, 560), (560, 560), (560, 220), (390, 220), (390, 440), (0, 440)]                                                                                            

    # create new Path object
    mainPath = Path(screen, (255, 0, 0), points, 2)

    mainPath.add(groupColliders)

    return mainPath

def spawnEnemy(screen):

    # pass the current wave to the readWaves function, returns a list of enemies to be spawned
    toBeSpawned = readWaves.read(1)
    print(toBeSpawned)

   #[0]: amountLight, [1]: typeLight, [2]: amountHeavy, [3]: typeHeavy, [4]: amountFast, [5]: typeFast, [6]: amountBoss, [7]: typeBoss
    amountLight = int(toBeSpawned[0])
    amountHeavy = int(toBeSpawned[2])
    amountFast = int(toBeSpawned[4])
    amountBoss = int(toBeSpawned[6])

    typeLight = toBeSpawned[1]
    typeHeavy = toBeSpawned[3]
    typeFast = toBeSpawned[5]
    typeBoss = toBeSpawned[7]

    #iterate through the list of enemies to be spawned, spawns each enemy
    for i in range(0, amountLight):
        pos = (100+(i*50), 100)
        Enemy(screen, pos, typeLight)
        
    for i in range(0, amountHeavy):
        pos = (100+(i*50), 200)
        Enemy(screen, pos, typeHeavy)

    for i in range(0, amountFast):
        pos = (100+(i*50), 300)
        Enemy(screen, pos, typeFast)

    for i in range(0, amountBoss):
        pos = (100+(i*50), 400)
        Enemy(screen, pos, typeBoss)

if __name__ == "__main__":
    main()