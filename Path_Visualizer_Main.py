import pygame
from Path_Visualizer_Functionality import Grid
from enum import Enum, auto
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,100) 

surface = pygame.display.set_mode((1200, 700)) 
pygame.display.set_caption('Path Finding Visualizer')

algorithmChoice = 0
buttonChoice = 0
isAnyOperationValid = True

# If the 'multipleDestinationsState' variable is equal to 0, then there is only one desination.
# Otherwise , there are multiple destinations.
multipleDestinationsState = 0

class States(Enum):
    running = auto()


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()


# Configuration for Action buttons
def actionButton(x,y,w,h,msg,Ri,Gi,Bi,Ra,Ga,Ba,actionSelected):
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(surface, (Ra, Ga, Ba), (x,y,w,h))
        if pygame.mouse.get_pressed()[0]:
            global buttonChoice, isAnyOperationValid
            global isAnyOperationValid
            if actionSelected == "Start":
                buttonChoice = 1
                return
            elif actionSelected == "End":
                buttonChoice = 2
                return
            elif actionSelected == "Visualize":
                buttonChoice = 3
                return
            elif actionSelected == "Wall":
                buttonChoice = 4
                return
            elif actionSelected == "RemoveWall":
                buttonChoice = 5
                return
            elif actionSelected == "RemoveAllWalls" and isAnyOperationValid:
                grid.removeAllWalls(surface, "Wall")   
                buttonChoice = 0
                return
            elif actionSelected == "TryAgain":
                buttonChoice = 7
                return
            elif actionSelected == "Quit":
                buttonChoice = 8
                return
            elif actionSelected == "GenerateRandomMaze" and isAnyOperationValid:  
                grid.generateRandomMaze(surface, "Wall")    
                buttonChoice = 0
                return
            elif actionSelected == "AddMoreDestinations" and isAnyOperationValid == True:
                global multipleDestinationsState
                multipleDestinationsState = 1
                return
    else:
        pygame.draw.rect(surface, (Ri, Gi, Bi), (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg,smallText)
    textRect.center = (int(x+(w/2)), int(y+(h/2)))
    surface.blit(textSurf, textRect)

# Configuration for Algorithm buttons
def algorithmButton(x,y,w,h,msg,Ri,Gi,Bi,Ra,Ga,Ba,algorithmSelected):
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(surface, (Ra, Ga, Ba), (x,y,w,h))
        if pygame.mouse.get_pressed()[0]:
            global algorithmChoice
            if algorithmSelected == "BFS":
                algorithmChoice = 1
                return
            elif algorithmSelected == "A*":
                algorithmChoice = 2
                return
            elif algorithmSelected == "Dijkstra":
                algorithmChoice = 3
                return
            elif algorithmSelected == "DFS":
                algorithmChoice = 4
                return
            elif algorithmSelected == "H&G":
                algorithmChoice = 5
                return
    else:
        pygame.draw.rect(surface, (Ri, Gi, Bi), (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg,smallText)
    textRect.center = (int(x+(w/2)), int(y+(h/2)))
    surface.blit(textSurf, textRect)


state = States.running
grid = Grid()
grid.draw(surface)
runningState = True



while runningState:

    # Button creation ----------------------------------------------------------------------
    actionButton(920,20,60,35,"Start",192,192,192,160,160,160,"Start")
    actionButton(990,20,60,35,"End",192,192,192,160,160,160,"End")
    actionButton(1060,20,60,35,"Wall",192,192,192,160,160,160,"Wall")
    algorithmButton(920,460,60,35,"BFS",192,192,192,160,160,160,"BFS")
    algorithmButton(990,460,60,35,"A*",192,192,192,160,160,160,"A*")
    algorithmButton(1060,460,80,35,"Dijkstra",192,192,192,160,160,160,"Dijkstra")
    algorithmButton(920,500,75,35,"DFS",192,192,192,160,160,160,"DFS")
    algorithmButton(1005,500,60,35,"H&G",192,192,192,160,160,160,"H&G")
    actionButton(920,70,105,40,"Visualize",102,102,255,51,51,255,"Visualize")
    actionButton(1040,70,140,40,"Remove Wall",192,192,192,160,160,160,"RemoveWall")
    actionButton(920,120,155,40,"Remove Walls",192,192,192,160,160,160,"RemoveAllWalls")
    actionButton(1080,120,115,40,"Try again",192,192,192,160,160,160,"TryAgain")
    actionButton(920,170,60,40,"Quit",192,192,192,160,160,160,"Quit")
    actionButton(920,220,245,40,"Generate Random Maze",192,192,192,160,160,160,"GenerateRandomMaze")
    actionButton(920,270,200,40,"Add multiple ends",192,192,192,160,160,160,"AddMoreDestinations")

    
    #mouse = pygame.mouse.get_pos()
    # 'Wall'   
    if buttonChoice == 4 and isAnyOperationValid:
        if pygame.mouse.get_pressed()[0]:
            mousePosition = pygame.mouse.get_pos()
            if mousePosition[0]//20 >= 0 and mousePosition[0]//20 < 45*20 and mousePosition[1]//20 >= 0 and mousePosition[1]//20 < 45*20:
                grid.markWalls(mousePosition[0]//20, mousePosition[1]//20, surface, "Wall")
        
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN and state == States.running:
            if pygame.mouse.get_pressed()[0]:
                # 'Start' 
                if buttonChoice == 1 and isAnyOperationValid:
                    mousePosition = pygame.mouse.get_pos()
                    grid.markSource(mousePosition[0]//20, mousePosition[1]//20,surface, "Start")

                # 'End'  
                elif buttonChoice == 2 and isAnyOperationValid:
                    mousePosition = pygame.mouse.get_pos()
                    grid.markDestination(mousePosition[0]//20, mousePosition[1]//20, surface, "End", multipleDestinationsState)

                # 'Visualize'  
                elif buttonChoice == 3 and isAnyOperationValid:

                    if(algorithmChoice != 2 and multipleDestinationsState == 1):
                        pass
                    elif algorithmChoice == 1:
                        isAnyOperationValid = False
                        grid.search("BFS",surface, "Visualize", multipleDestinationsState)

                    elif algorithmChoice == 2:
                        isAnyOperationValid = False
                        validCells = grid.search("A*",surface, "Visualize", multipleDestinationsState)

                    elif algorithmChoice == 3:
                        isAnyOperationValid = False
                        grid.search("Dijkstra", surface, "Visualize", multipleDestinationsState)

                    elif algorithmChoice == 4:
                        isAnyOperationValid = False
                        grid.search("DFS", surface, "Visualize", multipleDestinationsState)

                    elif algorithmChoice == 5:
                        isAnyOperationValid = False
                        grid.search("H&G", surface, "Visualize", multipleDestinationsState)

                # 'Remove Wall' 
                elif buttonChoice == 5 and isAnyOperationValid:
                    mousePosition = pygame.mouse.get_pos()
                    grid.removeWall(mousePosition[0]//20, mousePosition[1]//20, surface, "Wall")
 

                # 'Try Again' 
                elif buttonChoice == 7:
                    isAnyOperationValid = True
                    algorithmChoice = 0
                    buttonChoice = 0
                    multipleDestinationsState = 0
                    grid.reload(surface)

                # 'Quit'  
                elif buttonChoice == 8:
                    runningState = False
                
                    

        elif event.type == pygame.QUIT:
            runningState = False

    pygame.display.flip()
