# https://www.pygame.org/docs/
# https://pygame.readthedocs.io/en/latest/index.html

# import all the modules

import GUI
import enemySpawner

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

        # determines which enemy to spawn based on the type given
        self.determineType()

    def spawnLightEnemy(self):
        self.health = 100
        self.isArmored = False
        self.speed = 1
        self.damage = 1
        self.color = (255, 0, 0)

        pygame.draw.circle(self.screen, self.color, self.position, 10)

        print("Light enemy spawned")

    def spawnHeavyEnemy(self):          
        self.health = 200
        self.isArmored = True
        self.speed = 0.5
        self.damage = 1
        self.color = (0, 0, 255)

        pygame.draw.circle(self.screen, self.color, self.position, 10)

        print("Heavy enemy spawned")

    def spawnFastEnemy(self):  
        self.health = 100
        self.isArmored = False
        self.speed = 2
        self.damage = 1
        self.color = (0, 255, 0)

        pygame.draw.circle(self.screen, self.color, self.position, 10)

        print("Fast enemy spawned")

    def spawnBossEnemy(self):
        self.health = 500
        self.isArmored = True
        self.speed = 1
        self.damage = 2
        self.color = (255, 255, 0)

        pygame.draw.circle(self.screen, self.color, self.position, 10)

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
        print("Current enemies:", len(groupEnemies.sprites()))

    def draw(self):
        for enemy in groupEnemies:
            pygame.draw.circle(self.screen, self.color, self.position, 10)

    def killEnemy(self):
        self.kill()
        #self.remove(groupEnemies)

pygame.init() # initialize pygame

# pygame Sprite group definitions
# all obejcts which are collidable should be added to this group
groupColliders = pygame.sprite.Group()

groupEnemies = pygame.sprite.Group()

enemyList = []

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

        # run the main function in GUI.py
        GUI.main(screen)
         
        # draw the path
        createMapPath(screen)

        for event in pygame.event.get():

            # exit if the user clicks the close button
            if event.type == pygame.QUIT: # if the user clicks the close button, exit
                exit()
            # test if mouse is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button pressed")
            
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
                    print(enemyList)

            # print all events if flag is set
            if consoleActive:
                print(event)

        # draw all enemies continuously
        for enemy in groupEnemies:
            enemy.draw()
            
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

    enemySpawner.main(1, screen)

    #for i in range(0, 10):
    #    position = (100+(i*50), 100)
    #    type = "light"
    #    # creates a new enemy object
    #    enemy = Enemy(screen, position, type)
#
    #    # adds the enemy to the enemyList
    #    enemyList.append(enemy)
#
    #return


if __name__ == "__main__":
    main()