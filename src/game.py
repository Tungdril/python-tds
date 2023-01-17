# https://www.pygame.org/docs/
# https://pygame.readthedocs.io/en/latest/index.html

# import all the modules

import GUI
import readWaves
import os
import math

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
            print("Error installing pygame. Install pygame manually and try again")
            exit()
        else:
            print("Pygame installed")
            import pygame

# ---------------------------------------------------------------------------------------------------- #    

# print pygame version
# print(pygame.version.ver)

currentWave = 1

health = 100

money = 1000

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
        self.speed = 3.5
        self.damage = 1
      
        # draws a rectangle over the image, used for collision detection
        self.rect = self.image.get_rect(center=self.position)

        print("Light enemy spawned")

    def spawnHeavyEnemy(self):  
        self.health = 200
        self.isArmored = True
        self.speed = 1.5
        self.damage = 5

        self.rect = self.image.get_rect(center=self.position)

        print("Heavy enemy spawned")

    def spawnFastEnemy(self):  
        self.health = 100
        self.isArmored = False
        self.speed = 5
        self.damage = 150

        self.rect = self.image.get_rect(center=self.position)

        print("Fast enemy spawned")

    def spawnBossEnemy(self):
        self.health = 500
        self.isArmored = True
        self.speed = 1
        self.damage = 100

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
        print("Enemy", self.type, "killed")

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
                #DEBUGINFO
                #print(self.type, "reached waypoint", self.waypointsIndex -1, "moving to waypoint", self.waypointsIndex)
            # if waypoint index is equal to the length of the waypoints list, reset waypoint index to 0
            else:
                self.waypointsIndex = 0

                #if enemy reaches final waypoint, substract damage from health
                global health
                health -= self.damage
                #if health is less than or equal to 0, call looseState()
                if health <= 0:
                    looseState()          
                
                #remove enemy object
                self.killEnemy()
                print(self.type, "reached final waypoint, commencing purge")

class Tower(pygame.sprite.Sprite):
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
        img = pygame.transform.scale(img, (100, 100))
        self.image = img

        self.buildmode = True

        # determines which tower to spawn based on the type given
        self.determineType()

    def spawnMgTower(self):
        self.damage = 1
        self.range = 100
        self.fireRate = 10
        self.price = 100

        self.rect = self.image.get_rect(center=self.position)
    
    def spawnSniperTower(self):
        self.damage = 2
        self.range = 200
        self.fireRate = 2

        self.rect = self.image.get_rect(center=self.position)

        print("Sniper tower spawned")

    def spawnFlamerTower(self):
        self.damage = 0.5
        self.range = 50
        self.fireRate = 10


        self.rect = self.image.get_rect(center=self.position)

        print("Flamer tower spawned")

    def spawnBarracksTower(self):
        self.range = 100
        self.spawnRate = 1

        self.rect = self.image.get_rect(center=self.position)

        print("Barracks tower spawned")

    def spawnBankTower(self):
        self.spawnRate = 5

        self.rect = self.image.get_rect(center=self.position)
        
        print("Barracks tower spawned")
    
    def determineType(self):    
        if self.type == "mg":
            self.spawnMgTower()
        elif self.type == "sniper":
            self.spawnSniperTower()
        elif self.type == "flamer":
            self.spawnFlamerTower()
        elif self.type == "barracks":
            self.spawnBarracksTower()
        elif self.type == "bank":
            self.spawnBankTower()
        else:
            print("Invalid tower type")

        groupTowers.add(self)
        groupSprites.add(self)

        #self.moveTower()
    
    def move(self):
        # moves the tower along with the mouse
        if self.buildmode:
            self.rect.center = pygame.mouse.get_pos()
        else:
            #set own position to the center of the rect, stops update from moving the tower
            self.position = self.rect.center
     
    def draw(self):
        # draws the tower continuously on screen
        groupTowers.draw(self.screen)

        #DEBUGINFO
        #closestEnemy = getClosestEnemy(self)
        #closestEnemy.posx = closestEnemy.rect.x
        #closestEnemy.posy = closestEnemy.rect.y
        #print(closestEnemy.posx, closestEnemy.posy)

    def shoot(self):
        # shoots a projectile towards the closest enemy
        self.target = getClosestEnemy(self)
        if self.buildmode == False:
            Projectile(self.screen, self.rect.center, self.target, "basicBullet")

    def killTower(self):
        self.kill()
        print("Tower", self.type, "killed")

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, position, target, type):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.position = position
        self.target = target
        self.type = type

        # get x and y coordinates of the target, added 25 to center the coordinates
        target.x = target.rect.x + 25
        target.y = target.rect.y + 25   

        self.imgPath = os.getcwd() + "/assets/" + type + ".png"
        img = pygame.image.load(self.imgPath).convert_alpha()
        img = pygame.transform.scale(img, (25, 25))
        self.image = img

        #self.rect = self.image.get_rect(center=self.position)

        self.rect = self.image.get_rect(center=(target.x, target.y))
        print(target.x, target.y)

        groupProjectiles.add(self)

        self.speed = 10

    def draw(self):
        groupProjectiles.draw(self.screen)

    def killProjectile(self):
        self.kill()
        print("Projectile", self.type, "killed")

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, screen, buttonType, position):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load(os.getcwd() +"/assets/" + buttonType + ".png").convert_alpha()
        img = pygame.transform.scale(img, (100, 100))
        self.image = img

        self.screen = screen
        self.type = buttonType
        self.position = position
        
        self.initialDraw()

    def initialDraw(self):
        # for some reason, rect doesn't originate from the center of the image, so we need to use topleft
        self.rect = self.image.get_rect(topleft=self.position)
        groupMenuButtons.add(self)

    def draw(self):
        # self.draw messes with semi-transparent images, so we need to use self.screen.blit, which in turn doesn't work with movement
        self.screen.blit(self.image, self.position)

    def buttonPressed(self):
        if self.type == "buttonMg":
            buildTower(self.screen, "mg")
        elif self.type == "buttonSniper":
            buildTower(self.screen, "sniper")
        elif self.type == "buttonFlamer":
            buildTower(self.screen, "flamer")
        elif self.type == "buttonBarracks":
            buildTower(self.screen, "barracks")
        elif self.type == "buttonBank":
            buildTower(self.screen, "bank")
        else:
            print("Invalid button type")

# initialize pygame
pygame.init()

# set a clock, used for framerate
clock = pygame.time.Clock()

# pygame Sprite group definitions
groupColliders = pygame.sprite.Group()

groupEnemies = pygame.sprite.Group()

groupSprites = pygame.sprite.Group()

groupTowers = pygame.sprite.Group()

groupMenuButtons = pygame.sprite.Group()

groupProjectiles = pygame.sprite.Group()

def main():

    # deactivates console by default
    consoleActive = False

    pygame.display.set_caption("Python TDS") # set the window title
    screen = pygame.display.set_mode((1200, 800)) # create a window 
    
    #TODO determine current wave, pass it to the spawnEnemy function

    # spawn all enemies DEBUG
    spawnEnemy(screen)

    # draw the build menu
    generateBuildingMenu(screen)

    # main loop 
    while True:

        # set framerate
        clock.tick(30)

        # draw the background
        GUI.background(screen)

        global currentWave
        GUI.wave(screen, currentWave)

        global health
        GUI.health(screen, health)

        global money
        GUI.money(screen, money)

        # draw the path
        createMapPath(screen)

        for event in pygame.event.get():

            # exit if the user clicks the close button
            if event.type == pygame.QUIT: # if the user clicks the close button, exit
                exit()
            # DEEBUG: kills enemy/tower if it is clicked 1: LMB, 2: MMB, 3: RMB; 4: ScrUP, 5: ScrDOWN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if left mouse button is clicked
                if event.button == 1:
                    for enemy in groupEnemies:
                        if enemy.rect.collidepoint(event.pos):
                            enemy.killEnemy()
                    for tower in groupTowers:
                        if tower.rect.collidepoint(event.pos):
                            #set buildmode to false, so the tower stays in place
                            tower.buildmode = False
                            tower.shoot()
                            #getClosestEnemy(tower)
                    for button in groupMenuButtons:
                        if button.rect.collidepoint(event.pos):
                            button.buttonPressed()
                # if right mouse button is clicked
                elif event.button == 3:
                    for tower in groupTowers:
                        if tower.rect.collidepoint(event.pos):
                            tower.killTower()

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
                elif event.key == pygame.K_b:
                    #DEBUG: kill all enemies
                    for enemy in groupEnemies:
                        enemy.killEnemy()
                    #newBullet = Projectile(screen, (100, 100), "closest", "basicBullet")
                    pass

            # print all events if flag is set
            if consoleActive:
                print(event)

        # draw, move all enemies continuously
        for enemy in groupEnemies:
            enemy.draw()
            enemy.move()

        # check if all enemies are dead, if so, spawn new wave
        if len(groupEnemies) == 0:
            # check if all waves are done, if so, go to win state
            if currentWave > 9:
                winState()
            else:
                currentWave += 1
                spawnEnemy(screen)


        # draw, move all towers continuously
        for tower in groupTowers:
            tower.rect.move(pygame.mouse.get_pos())
            tower.move()
            tower.draw()

        # draw all menu buttons continuously
        for button in groupMenuButtons:
            button.draw()

        # draw all projectiles continuously
        for projectile in groupProjectiles:
            projectile.draw()
            #projectile.move()
            
        # update the screen continuously    
        pygame.display.update()

def createMapPath(screen):

    # defines path corners
    points = [(0, 380), (320, 380), (320, 160), (640, 160), (640, 630), (360 , 630), (360, 700), (930, 700), (930, 520), (700, 520), (700, 290), (960, 290), (960, 60), (700, 60), (700, 0), (1030, 0), (1030, 350), (760, 350), (760, 460), (1000, 460), (1000, 760), (290, 760), (290, 560), (560, 560), (560, 220), (390, 220), (390, 440), (0, 440)]                                                                                            

    # create new Path object
    mainPath = Path(screen, (255, 0, 0), points, 2)

    mainPath.add(groupColliders)

    return mainPath

def generateBuildingMenu(screen):
    posX = 180

    MenuButton(screen, "buttonMg", (posX, 685))
    MenuButton(screen, "buttonSniper", (posX*2, 685))
    MenuButton(screen, "buttonFlamer", (posX*3, 685))
    MenuButton(screen, "buttonBarracks", (posX*4, 685))
    MenuButton(screen, "buttonBank", (posX*5, 685))

def spawnEnemy(screen):

    # pass the current wave to the readWaves function, returns a list of enemies to be spawned
    toBeSpawned = readWaves.read(currentWave)
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
        pos = (-100-(i*150), 500)
        Enemy(screen, pos, typeLight)
        
    for i in range(0, amountHeavy):
        pos = (-100-(i*150), 500)
        Enemy(screen, pos, typeHeavy)

    for i in range(0, amountFast):
        pos = (-100-(i*150), 500)
        Enemy(screen, pos, typeFast)

    for i in range(0, amountBoss):
        pos = (-100-(i*150), 500)
        Enemy(screen, pos, typeBoss)

def buildTower(screen, type):
    position = pygame.mouse.get_pos()

    if checkPrice(type):
        #TODO: check if tower can be placed, if not, change color
        Tower(screen, position, type)

def checkPrice(type):

    if type == "mg":
        towerPrice = 100
    elif type == "sniper":
        towerPrice = 200
    elif type == "flamer":
        towerPrice = 500
    elif type == "barracks":
        towerPrice = 500
    elif type == "bank":
        towerPrice = 300

    global money
    if towerPrice <= money:
        money -= towerPrice
        return True
    else:
        print("Not enough money!")
        return False

def getClosestEnemy(tower):
    distances = []

    for enemy in groupEnemies:
        
        # get the distance between the enemy and the tower
        distance = math.hypot(enemy.rect.x - tower.rect.x, enemy.rect.y - tower.rect.y)

        # add the distance and enemy instance to the list
        distances.append([distance, enemy])

    # sort the list by the distance, key gets the first item in the list (distance)
    sortedDistances = sorted(distances, key=lambda x: x[0])

    # DEBUGINFO
    #print(sortedDistances)
    #print(sortedDistances[0][1])

    return sortedDistances[0][1]

def winState():
    print("You win!")
    pygame.quit()
    return

def looseState():
    print("You loose!")
    pygame.quit()
    return

if __name__ == "__main__":
    main()

#   TOWERS:
#       Towers cost money
#       Projectiles/Actual damage
#       Tower Upgrades
#       Tower Range
#       Towers can't intersect with each other and path
#       Change color in buildmode/intersection   
#       Sell towers
#
#   GUI/GAMEPLAY:
#       Base Health 
#       Wave System
#       Money System
#       Game over Screen
#       Main menu
#       Pause between waves/start wave button
#
#   TBD:
#   Hard to implement damage system:
#       Barracks or different tower? (Minefield)
#       Flamer or different tower? (Cannon)
#
#   SOUND:
#       Tower shooting
#       Enemy dying
#       Enemy spawning
#       Tower building
#       Tower upgrading
#       Tower selling
#       Game over
#       Background music
#       Wave start
#       Wave end
#
#   PARTICLES:
#       Tower shooting
#       Enemy dying
#       Enemy spawning
#       Tower building
#       Tower upgrading
#       Tower selling
#       Projectile hitting enemy
#
#   GRAPHICS:
#       Map
#       Towers including different upgrades
#       Enemies 
#       Projectiles
#       GUI
#       Icons: Money, Health, Wave, Tower, Sell, Upgrade, Start Wave, Window favicon