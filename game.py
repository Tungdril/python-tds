# import all the modules
import src.GUI as GUI
import src.readWaves as readWaves
import src.sound as sound

import os
import math
import random
import sys

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

# class definitions
class Path(pygame.sprite.Sprite):
    def __init__(self, screen, color, points, width):
        # calls constructor of parent class
        pygame.sprite.Sprite.__init__(self)

        #DEBUG: draws a polygon based on the points given on the screen
        #pygame.draw.polygon(screen, color, points, width)

class PathCollider(pygame.sprite.Sprite):
    def __init__(self, screen, rect):
        pygame.sprite.Sprite.__init__(self)

        self.position = (rect[0], rect[1])
        self.size = (rect[2], rect[3])
        self.screen = screen

        # neccessary for collision detection
        self.rect = pygame.draw.rect(screen, (255,255,0), rect, 2)

        # creates a surface to be blitted later
        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(50)

        groupPathColliders.add(self)
        groupSprites.add(self)

    def draw(self):
        self.screen.blit(self.surface, self.position)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, position, type):
        pygame.sprite.Sprite.__init__(self)

        # initializes screen, position and type
        self.screen = screen
        self.position = position
        self.type = type

        # loads the image, scales it to 50x50, makes alpha channel transparent
        self.imgPath = os.getcwd() + "/assets/enemies/" + type + ".png"
        img = pygame.image.load(self.imgPath).convert_alpha()
        self.image = img

        # sets waypoints to follow
        self.waypoints = [(-50, 530), (225, 530), (225, 325), (460, 325), (460, 490), (645, 490), (645, 20), (805, 20), (805, 145), (1115, 145), (1115, 335), (935, 335), (935, 520), (1200, 520), (1250,520)]
        
        # offsets by 10 pixels, centers the enemy on the path better
        for i in range(len(self.waypoints)):
            self.waypoints[i] = (self.waypoints[i][0] - 10, self.waypoints[i][1] - 10)

        # duplicates the waypoints for the boss/heavy enemy, since they need to be offset on the y-axis
        self.waypointsBoss = self.waypoints.copy()
        for i in range(len(self.waypointsBoss)):
            self.waypointsBoss[i] = (self.waypointsBoss[i][0], self.waypointsBoss[i][1] -30)

        self.waypointsIndex = 0

        # determines which enemy to spawn based on the type given
        self.determineType()

    def spawnLightEnemy(self):
        self.health = 25
        self.maxHealth = self.health
        self.speed = 3.25
        self.damage = 1

        self.image = pygame.transform.scale(self.image, (50, 60))
      
        # draws a rectangle over the image, used for collision detection
        self.rect = self.image.get_rect(center=self.position)

        print("Light enemy spawned")

    def spawnHeavyEnemy(self):  
        self.health = 100
        self.maxHealth = self.health
        self.speed = 2.25
        self.damage = 5

        self.image = pygame.transform.scale(self.image, (50, 90))

        # because of its size, this needs to use the boss waypoints
        self.waypoints = self.waypointsBoss

        self.rect = self.image.get_rect(center=self.position)

        print("Heavy enemy spawned")

    def spawnFastEnemy(self):  
        self.health = 35
        self.maxHealth = self.health
        self.speed = 5
        self.damage = 2

        self.image = pygame.transform.scale(self.image, (50, 70))
        
        self.rect = self.image.get_rect(center=self.position)

        print("Fast enemy spawned")

    def spawnBossEnemy(self):
        self.health = 800
        self.maxHealth = self.health
        self.speed = 1
        self.damage = 100
        self.image = pygame.transform.scale(self.image, (52, 80))

        # use the boss waypoints
        self.waypoints = self.waypointsBoss

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

    def draw(self):
        # draws the enemy continuously on screen, kills the enemy if health is below 0
        if self.health <= 0:
            self.killEnemy()
            self.calculateReward()
        self.screen.blit(self.image, self.rect)

    def calculateReward(self):
        # adds a random amount of money to the player's wallet
        reward = random.randint(2, 15)

        global money
        money += reward

    def killEnemy(self):
        # removes the enemy from all groups, preventing it from being drawn
        self.kill()
        print("Enemy", self.type, "killed")
        sound.playSound(sound.enemydeath)

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

                #if enemy reaches final waypoint, subtract damage from health
                global health
                health -= self.damage
                sound.playSound(sound.damage)
                
                #remove enemy object
                self.killEnemy()
                print(self.type, "reached final waypoint, commencing purge")

class Tower(pygame.sprite.Sprite):
    def __init__(self, screen, position, type, price):
        # calls constructor of parent class
        pygame.sprite.Sprite.__init__(self)

        # initializes cooldown 
        self.last = pygame.time.get_ticks()

        # initializes screen, position and type
        self.screen = screen
        self.position = position
        self.type = type
        self.price = price

        # loads the image, scales it to 50x50, makes alpha channel transparent
        self.imgPath = os.getcwd() + "/assets/towers/" + type + ".png"
        img = pygame.image.load(self.imgPath).convert_alpha()  
        self.image = img

        self.buildmode = True

        # determines which tower to spawn based on the type given
        self.determineType()

    def spawnMgTower(self):
        self.damage = 2
        self.range = 150
        self.fireRate = 500

        self.image = pygame.transform.scale(self.image, (110, 80))

        self.rect = self.image.get_rect(center=self.position)

        print("Bank tower spawned")
    
    def spawnSniperTower(self):
        self.damage = 10
        self.range = 300
        self.fireRate = 2000

        self.image = pygame.transform.scale(self.image, (45, 130))

        self.rect = self.image.get_rect(center=self.position)

        print("Sniper tower spawned")

    def spawnFlamerTower(self):
        self.damage = 1
        self.range = 120
        self.fireRate = 100

        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect(center=self.position)

        print("Flamer tower spawned")

    def spawnBarracksTower(self):
        self.damage = 10
        self.range = 100
        self.fireRate = 3000

        self.image = pygame.transform.scale(self.image, (100, 70))

        self.rect = self.image.get_rect(center=self.position)

        print("Barracks tower spawned")

    def spawnBankTower(self):
        self.damage = random.randint(10, 50)
        self.fireRate = 5000
        self.range = 80

        self.image = pygame.transform.scale(self.image, (180, 120))

        self.rect = self.image.get_rect(center=self.position)
        
        print("Bank tower spawned")
    
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

        groupBuildingTowers.add(self)
        groupSprites.add(self)
    
    def move(self):
        # moves the tower along with the mouse
        if self.buildmode:

            self.rect.center = pygame.mouse.get_pos()
            collision = pygame.sprite.spritecollide(self, groupPathColliders, False) or pygame.sprite.spritecollide(self, groupStaticTowers, False)

            if collision:
                # draws a circle/rect around the tower to show the range, red if colliding with path, green if not
                self.drawRange((255, 0, 0))
                self.collision = True
            
            else:
                self.drawRange((0, 255, 0))
                self.collision = False
        else:
            # set own position to the center of the rect, stops update from moving the tower
            self.collision = False
            self.position = self.rect.center
     
    def draw(self):
        # draws the tower continuously on screen
        self.screen.blit(self.image, self.rect)

    def drawRange(self, color):
        # increases rect size to encompass the entire sprite
        rect = self.rect[0] - 5, self.rect[1] - 10, self.rect[2] + 10, self.rect[3] + 20

        # draws the range of the tower, draw rect for bank, draw circle for other towers
        if self.type == "bank":
            pygame.draw.rect(self.screen, color, rect, 3, 10)
            return
        else:
            pygame.draw.circle(self.screen, color, self.rect.center, self.range, 3)

    def shoot(self):
        # shoots a projectile towards the closest enemy
        #different behavior for bank and barracks projectiles, since target is not an enemy
        if self.type == "bank":
            self.target = self
        else:
            self.target = getClosestEnemy(self)

        # get the current time
        now = pygame.time.get_ticks()

        # if the current time is greater or equal to the last time the tower shot + the fire rate, shoot
        if (now - self.last >= self.fireRate) and (self.buildmode == False) and not (self.target == None):
            self.last = now
            Projectile(self.screen, self.rect.center, self.target, (self.type + "Projectile"), self.damage, self.range)
        else:
            pass

    def killTower(self, fullRefund):
        # if fullRefund is true, refund the full price of the tower
        if fullRefund:
            global money
            money += self.price
            print("Tower", self.type, "killed, full refund")
            
        self.kill()
        print("Tower", self.type, "killed")

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, position, target, type, damage, range):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.position = self.getProjectileOffset(position, type)
        self.target = target
        self.type = type
        self.damage = damage
        self.range = range
        # speed is inverse; higher speed = slower projectile
        self.speed = 5

        if self.type == "bankProjectile":
            # sets the target above the tower
            target.x = target.rect.x + (target.rect.width / 2) - 5
            target.y = target.rect.y - 100
            self.speed = 20
        elif self.type == "barracksProjectile":
            target.x = target.rect.x + 25
            target.y = target.rect.y + 25
            self.speed = 10
        else:
            # get x and y coordinates of the target, added 25 to center the coordinates, only for non bank/barracks projectiles
            target.x = target.rect.x + 25
            target.y = target.rect.y + 25

        # get random sniper projectiles
        if self.type != "sniperProjectile":
            self.imgPath = os.getcwd() + "/assets/projectiles/" + type + ".png"
        else:
            self.imgPath = self.getRandSniperProjectile()
        
        img = pygame.image.load(self.imgPath).convert_alpha()

        # scale the projectile differently depending on the type
        if self.type == "bankProjectile" or self.type == "barracksProjectile":
            img = pygame.transform.scale(img, (50, 50))
        else:
            img = pygame.transform.scale(img, (25, 25))

        self.image = img

        self.rect = self.image.get_rect(center=(self.position))
        #DEBUGINFO
        #print(target.x, target.y)

        groupProjectiles.add(self)
        groupSprites.add(self)

    # constantly moves the projectile towards the target
    def move(self):

        if self.type == "barracksProjectile":
            hitboxOffset = 10
        else:
            hitboxOffset = 25

        # if the projectile is close enough to the target, kill it
        if self.rect.x > self.target.x - hitboxOffset and self.rect.x < self.target.x + hitboxOffset and self.rect.y > self.target.y - hitboxOffset and self.rect.y < self.target.y + hitboxOffset:
            
            if self.type == "bankProjectile":
                global money
                money += self.damage
                self.killProjectile()
            else:
                self.target.health -= self.damage
                self.killProjectile()

        # move the projectile towards the target
        self.rect.x += (self.target.x - self.rect.x) / self.speed
        self.rect.y += (self.target.y - self.rect.y) / self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)
            
    def getProjectileOffset(self, position, type):
        # get the offset position of the projectile, so it spawns at the correct position
        if type == "mgProjectile":
            offsetPosition = (position[0], position[1] - 30)
        elif type == "sniperProjectile":
            offsetPosition = (position[0] - 5, position[1] - 60)
        elif type == "flamerProjectile":
            offsetPosition = (position[0], position[1])
        else:
            offsetPosition = position

        return offsetPosition

    def getRandSniperProjectile(self):
        # get a random sniper projectile
        rand = random.randint(0, 13)

        img = os.getcwd() + "/assets/projectiles/" + self.type + str(rand) + ".png"
        return img

    def killProjectile(self):
        self.kill()

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, screen, buttonType, position):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load(os.getcwd() +"/assets/buttons/" + buttonType + ".png").convert_alpha()
        img = pygame.transform.scale(img, (100, 100))
        self.image = img

        self.screen = screen
        self.type = buttonType
        self.position = position
        
        self.initialDraw()
        groupSprites.add(self)

    def initialDraw(self):
        # for some reason, rect doesn't originate from the center of the image, so we need to use topleft
        self.rect = self.image.get_rect(topleft=self.position)
        groupMenuButtons.add(self)

    def draw(self):
        self.screen.blit(self.image, self.position)

    def buttonPressed(self):

        if groupBuildingTowers.sprites() != []:
            # if there is a tower being built, kill it so the player can build a new one
            groupBuildingTowers.sprites()[0].killTower(fullRefund=True)

        # depending on the button type pressed, build a tower
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

# ---------------------------------------------------------------------------------------------------- #

# initialize pygame
pygame.init()

# set a clock, used for framerate
clock = pygame.time.Clock()

# pygame Sprite group definitions, not all are used, but it's easier to just define them all
groupEnemies = pygame.sprite.Group()

groupSprites = pygame.sprite.Group()

groupBuildingTowers = pygame.sprite.Group()

groupStaticTowers = pygame.sprite.Group()

groupMenuButtons = pygame.sprite.Group()

groupProjectiles = pygame.sprite.Group()

groupPathColliders = pygame.sprite.Group()

groupActiveAllies = pygame.sprite.Group()

def main(screen):

    # deactivates console by default
    consoleActive = False

    # spawn first batch of enemies
    spawnEnemy(screen)

    # draw the build menu
    generateBuildingMenu(screen)

    # draw collide rects
    generatePathCollision(screen)

    # main loop
    while 1:

        # set framerate, time is not normalized, so speed is affected by framerate
        clock.tick(30)

        # DEBUGINFO
        fps = clock.get_fps()
        fps = int(fps * 100) / 100

        # draw the background
        GUI.background(screen)

        # draw all static towers continuously, and shoot if possible, load first to avoid draw order issues
        for tower in groupStaticTowers:
            tower.draw()
            tower.move()
            tower.shoot()

            #draw tower range if mouse hovers over tower
            if tower.rect.collidepoint(pygame.mouse.get_pos()):
                tower.drawRange((0, 255, 0))
                GUI.showResellValue(screen, tower, pygame.mouse.get_pos())

        # yeah I know globals are bad practice, but this is easiest and practical enough
        global currentWave
        GUI.wave(screen, currentWave)

        global health
        GUI.health(screen, health)

        global money
        GUI.money(screen, money)

        # DEBUGINFO FPS
        #font = pygame.font.SysFont("Arial", 40)
        #fps_display = font.render(str(fps), True, (255, 0, 0))
        #screen.blit(fps_display, (1100, 760))

        # draw the path
        createMapPath(screen)

        #if health is less than or equal to 0, call looseState()
        if health <= 0:
            sound.stopMusic()
            looseState(screen)

        # check if all enemies are dead, if so, spawn new wave, only if health is above 0
        if len(groupEnemies) == 0 and health > 0:
            # check if all waves are done, if so, go to win state
            if currentWave > 9:
                sound.stopMusic()
                winState(screen)
            elif health > 0:
                currentWave += 1

                # reward player for clearing a wave
                waveReward = 50 * currentWave
                money += waveReward
                print("Wave " + str(currentWave) + " cleared, reward: " + str(waveReward))
                
                # spawn new enemies
                spawnEnemy(screen)  
            
        for event in pygame.event.get():

            # exit if the user clicks the close button
            if event.type == pygame.QUIT: # if the user clicks the close button, exit
                pygame.quit()
                sys.exit()
            # DEEBUG: kills enemy/tower if it is clicked 1: LMB, 2: MMB, 3: RMB; 4: ScrUP, 5: ScrDOWN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if left mouse button is clicked
                if event.button == 1:
                    #DEBUG
                    #for enemy in groupEnemies:
                    #    if enemy.rect.collidepoint(event.pos):
                    #        enemy.killEnemy()
                    for tower in groupBuildingTowers:
                        if tower.rect.collidepoint(event.pos):
                            #set buildmode to false, so the tower stays in place
                            if not tower.collision:
                                tower.buildmode = False
                                sound.playSound(sound.towerplaceing)

                                #remove the tower from the building group and add it to the static group
                                groupBuildingTowers.remove(tower)
                                groupStaticTowers.add(tower)
                            else:
                                sound.playSound(sound.error)
                    for button in groupMenuButtons:
                            if button.rect.collidepoint(event.pos):
                                button.buttonPressed()

                # if right mouse button is clicked
                elif event.button == 3:
                    # refund 25% of the tower's price if it is right clicked
                    for tower in groupStaticTowers:
                        if tower.rect.collidepoint(event.pos):
                            money += int(tower.price * 0.25)
                            sound.playSound(sound.cash)
                            tower.killTower(fullRefund=False)
                    # kill the tower if it is right clicked while being built, full refund
                    for tower in groupBuildingTowers:
                        if tower.rect.collidepoint(event.pos):
                            tower.killTower(fullRefund=True)
                            sound.playSound(sound.cash)

            # check if a key has been pressed
            if event.type == pygame.KEYDOWN:

                # show/hide console
                if event.key == pygame.K_c:
                    consoleActive = True
                    print("Console activated, press X to hide")
                elif event.key == pygame.K_x:
                    consoleActive = False
                    print("Console deactivated, press C to show")
                #DEBUG
                #elif event.key == pygame.K_k:
                #    health = 0
                #elif event.key == pygame.K_b:
                #    for enemy in groupEnemies:
                #        enemy.killEnemy()

            # print all events if flag is set
            if consoleActive:
                print(event)

        # draw, move all towers in buildmode continuously
        for tower in groupBuildingTowers:
            tower.rect.move(pygame.mouse.get_pos())
            tower.move()
            tower.draw()
            
        # draw, move all enemies continuously
        for enemy in groupEnemies:
            enemy.draw()
            enemy.move()
            GUI.healthBar(screen, enemy.health, enemy.maxHealth, (enemy.rect.x, enemy.rect.y), enemy.image, enemy.type)

        # draw all menu buttons continuously
        for button in groupMenuButtons:
            button.draw()
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                GUI.showPrice(screen, button.type, pygame.mouse.get_pos())
            
        # draw all projectiles continuously
        for projectile in groupProjectiles:
            projectile.draw()
            projectile.move()

        #DEBUG
        #for collider in groupPathColliders:
        #    collider.draw()
            
        # update the screen continuously    
        pygame.display.update()

# ---------------------------------------------------------------------------------------------------- #

def createMapPath(screen):

    # defines path corners
    points = [(-50, 530), (225, 530), (225, 325), (460, 325), (460, 490), (645, 490), (645, 20), (805, 20), (805, 145), (1115, 145), (1115, 335), (935, 335), (935, 520), (1200, 520), (1250,520), (1250, 900), (-50, 900)]

    for i in range(len(points)):
            points[i] = (points[i][0] - 10, points[i][1] - 10)

    waypointsBoss = points.copy()
    
    for i in range(len(waypointsBoss)):
        waypointsBoss[i] = (waypointsBoss[i][0], waypointsBoss[i][1]-30)

    # gives a visual representation of the paths for debugging
    Path(screen, (255, 0, 0), points, 2)
    Path(screen, (0, 255, 0), waypointsBoss, 2)
    
def generatePathCollision(screen):

    # it's easiest to define a bunch of rects and then draw them, polygonal collison is kinda hard
    # x,y, width, height, 
    colRect0 = [0, 600, 1200, 400]
    colRect1 = [0,510,220,60]
    colRect2 = [220,310,50,260]
    colRect3 = [270,310,240,50]
    colRect4 = [460,360,50,180]
    colRect5 = [510,480,130,60]
    colRect6 = [640,10,50,530]
    colRect7 = [690,10,160,60]
    colRect8 = [800,70,50,120]
    colRect9 = [850,140,260,50]
    colRect10 = [1110,140,60,180]
    colRect11 = [930,320,240,60]
    colRect12 = [930,380,50,180]
    colRect13 = [980,510,220,50]

    # add all colRects to a list
    colRects = [colRect0, colRect1, colRect2, colRect3, colRect4, colRect5, colRect6, colRect7, colRect8, colRect9, colRect10, colRect11, colRect12, colRect13]

    # create a collider for each colRect, add it to the collision group
    for i in range(len(colRects)):
        PathCollider(screen, colRects[i])

def generateBuildingMenu(screen):
    posX = 180

    # create the menu buttons, not perfecly aligned, but close enough
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

    # iterate through the list of enemies to be spawned, spawns each enemy offset by 150 px each
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

    sound.playSound(sound.wavespawn)

def buildTower(screen, type):
    position = pygame.mouse.get_pos()

    # check if there is enough money to build the tower, returns the price of the tower
    towerPrice = checkPrice(type)

    # subtracts the price of the tower from money
    if towerPrice != None:
        global money
        money -= towerPrice
        sound.playSound(sound.cash)

        Tower(screen, position, type, towerPrice)

def checkPrice(type):

    # probably better to set these as attributes of the tower class, but works good enough
    if type == "mg":
        towerPrice = 100
    elif type == "sniper":
        towerPrice = 200
    elif type == "flamer":
        towerPrice = 500
    elif type == "barracks":
        towerPrice = 500
    elif type == "bank":
        towerPrice = 1000

    global money
    if towerPrice <= money:
        return towerPrice
    else:
        print("Not enough money!")
        sound.playSound(sound.error)
        towerPrice = None
        return towerPrice

def getClosestEnemy(tower):
    distances = []

    for enemy in groupEnemies:
        
        # get the distance between the enemy and the tower
        distance = math.hypot(enemy.rect.x - tower.rect.x, enemy.rect.y - tower.rect.y)

        # add all distances to a list if the enemy is in range of the tower, add 20 px to compensate for the hitbox
        if distance <= (tower.range + 20):
            distances.append([distance, enemy])

    # sort the list by the distance, key gets the first item in the list (distance)
    sortedDistances = sorted(distances, key=lambda x: x[0])

    if len(sortedDistances) == 0:
        #print("No enemies in range!")
        return None
    elif len(sortedDistances) > 0: 
        # DEBUGINFO
        #print(sortedDistances)
        #print(sortedDistances[0][0])
        return sortedDistances[0][1]
    
def winState(screen):
    GUI.win(screen)

    for sprite in groupSprites:
        sprite.kill()

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                print("Restarting game...")
                mainMenu()

def looseState(screen):
    GUI.gameOver(screen)

    for sprite in groupSprites:
        sprite.kill()
    
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                mainMenu()

def mainMenu():
    # reset main values
    global currentWave
    currentWave = 1

    global money
    money = 500

    global health
    health = 100

    groupMainMenuButtons = pygame.sprite.Group()

    class MainMenuButton(pygame.sprite.Sprite):
        def __init__(self, type, position):
            super().__init__()
            self.image = pygame.image.load(os.getcwd() + "/assets/buttons/" + type + ".png")
            self.image = pygame.transform.scale(self.image, (280, 100))
            self.rect = self.image.get_rect()
            self.rect.x = position[0]
            self.rect.y = position[1]
            self.type = type

            groupMainMenuButtons.add(self)

        def buttonPressed(self):
            if self.type == "button_play":
                return True
            elif self.type == "button_quit":
                pygame.quit()
                sys.exit()

        def draw(self):
            screen.blit(self.image, (self.rect.x, self.rect.y))

    pygame.display.set_caption("Novus Ordo Seclorum") # set the window title
    screen = pygame.display.set_mode((1200, 800)) # create a window 

    icon = pygame.image.load(os.getcwd() + "/assets/icon.png")
    pygame.display.set_icon(icon)

    # initialize the GUI, needs to be done after the screen is created
    GUI.init()

    sound.init()

    sound.playMusic()

    MainMenuButton("button_quit", (120, 300))
    MainMenuButton("button_play", (780, 300))

    notDone = True

    while notDone:

        GUI.mainMenu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            for sprite in groupMainMenuButtons:
                if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                    if sprite.buttonPressed():
                        notDone = False
                        main(screen)
        
        groupMainMenuButtons.draw(screen)

        pygame.display.update()
    
if __name__ == "__main__":
    mainMenu()