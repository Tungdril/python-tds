# import all the modules

import GUI
import actionHandler

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
print(pygame.version.ver)

# class definitions
class Path(pygame.sprite.Sprite):
    def __init__(self, screen, color, points, width):
        # calls constructor of parent class
        pygame.sprite.Sprite.__init__(self)

        # draws a polygon based on the points given on the screen
        pygame.draw.polygon(screen, color, points, width)

# pygame Sprite group definitions
# all obejcts which are collidable should be added to this group
groupColliders = pygame.sprite.Group()

def main():

    pygame.init() # initialize pygame

    pygame.display.set_caption("Python TDS") # set the window title
    screen = pygame.display.set_mode((1200, 800)) # create a window 

    GUI.main(screen) # run the main function in GUI.py
    createMapPath(screen)
    mainPath = actionHandler.main()

    # main loop 
    while True:

        if groupColliders.collide(pygame.mouse.get_pos()):
            print("Mouse is on path")

        for event in pygame.event.get():

            print(event) # print all events

            if event.type == pygame.QUIT: # if the user clicks the close button, exit
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button pressed")

        pygame.display.update() # update the screen

def createMapPath(screen):

    # defines path corners
    points = [(0, 380), (320, 380), (320, 160), (640, 160), (640, 630), (360 , 630), (360, 700), (930, 700), (930, 520), (700, 520), (700, 290), (960, 290), (960, 60), (700, 60), (700, 0), (1300, 0), (1030, 0), (1030, 350), (760, 350), (760, 460), (1000, 460), (1000, 760), (290, 760), (290, 560), (560, 560), (560, 220), (390, 220), (390, 440), (0, 440)]                                                                                            

    #create new Path object
    mainPath = Path(screen, (255, 0, 0), points, 2)

    mainPath.add(groupColliders)

    return mainPath


main()