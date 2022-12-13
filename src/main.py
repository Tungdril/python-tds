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

# print pygame version
print(pygame.version.ver)

pygame.init() # initialize pygame

pygame.display.set_caption("Python TDS") # set the window title
screen = pygame.display.set_mode((1200, 800)) # create a window 

GUI.main(screen) # run the main function in GUI.py
actionHandler.main()

# main loop 
while True:
    for event in pygame.event.get():

        #print(event) # print all events

        if event.type == pygame.QUIT: # if the user clicks the close button, exit
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button pressed")

    pygame.display.update() # update the screen