import pygame
import random

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 18)


class Qitem:
    def __init__(self,x,y):
        self.row = x
        self.col = y

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Cell:
    def __init__(self, pos, value):
        self.size = 20
        self.weight = 1
        self.cellValue = value
        self.pos = pos
        self.sourceCellLocated = False
        self.destinationCellLocated = False
        self.isValid = False
        self.pathCellLocated = False
        self.wallSelected = False
        self.Tpath = None


    def createCell(self, surface):
        pygame.draw.rect(surface, (50,50,50), (self.pos[0], self.pos[1], self.size, self.size))

    def drawCell(self, surface, buttonSelected):
        if buttonSelected == "Start":
            if self.sourceCellLocated:
                pygame.draw.rect(surface, (255,255,255), (self.pos[0], self.pos[1], self.size, self.size))
            else:
                pygame.draw.rect(surface, (50,50,50), (self.pos[0], self.pos[1], self.size, self.size))
        elif buttonSelected == "End":
            if self.destinationCellLocated:
                pygame.draw.rect(surface, (255, 0, 0), (self.pos[0], self.pos[1], self.size, self.size))
            else:
                pygame.draw.rect(surface, (50,50,50), (self.pos[0], self.pos[1], self.size, self.size))
        elif buttonSelected == "Wall":
            if self.wallSelected:
                pygame.draw.rect(surface, (255, 153, 51), (self.pos[0], self.pos[1], self.size, self.size))
            else:
                pygame.draw.rect(surface, (50,50,50), (self.pos[0], self.pos[1], self.size, self.size))
        elif buttonSelected == "Visualize":
            if self.pathCellLocated:
                pygame.draw.rect(surface, (255, 255, 102), (self.pos[0], self.pos[1], self.size, self.size))
            elif self.isValid:
                pygame.draw.rect(surface, (153,153,225), (self.pos[0], self.pos[1], self.size, self.size))





class Grid:

    def __init__(self):
        self.cells = []
        self.SDCoordinates = [[-1 for x in range(2)] for y in range(2)]
        self.listOfWalls = []
        self.multipleDestinations = []
        self.openList = None
        self.path = None

        for y in range(35): 
            self.cells.append([])
            for x in range(45):
                self.cells[y].append(Cell((x*20, y*20),False))

        self.lines = []

        for y in range(1, 36, 1): 
            temp = []
            temp.append((0, y * 20))
            temp.append((900, y * 20))
            self.lines.append(temp)

        for x in range(1, 46, 1):
            temp = []
            temp.append((x*20, 0))
            temp.append((x*20, 700))
            self.lines.append(temp)


# redrawLines()

    # Every time a cell is created or modified, the lines need to be recreated
    def redrawLines(self,x,y,surface):
        pygame.draw.line(surface, (0, 125, 0), self.lines[y-1][0], self.lines[y-1][1])
        pygame.draw.line(surface, (0, 125, 0), self.lines[(x+35)-1][0], self.lines[(x+35)-1][1]) #45

#Draw
    def draw(self, surface):
        for row in self.cells:
            for cell in row:
                cell.createCell(surface)
        for line in self.lines:
            pygame.draw.line(surface, (0, 125, 0), line[0], line[1])

# iswithinBounds()

    # Check whether x and y are within the bounds of the boards
    def isWithinBounds(self, x, y):
        return x >= 0 and x < 45 and y >= 0 and y < 35

# randomWeigh()

    # Assign's random weights to cells
    def randomWeight(self,algorithm):
        if algorithm == "Astar":
            for row in range(0,35):
                for cell in range(0,45):
                    self.cells[row][cell].weight = random.randint(1,10)
        elif algorithm == "Dijkstra":
            randomList = list(range(1,1576))
            random.shuffle(randomList)
            counter = 0
            for row in range(0,35):
                for cell in range(0,45):
                    self.cells[row][cell].weight = randomList[counter]
                    counter+=1

# removeWall()

    # Removes a wall located at (x,y)
    def removeWall(self, x, y, surface, buttonSelected):
        if not self.isWithinBounds(x,y):
            return
        if self.cells[y][x].cellValue == True:
            self.cells[y][x].cellValue = False
            self.cells[y][x].wallSelected = False
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x, y, surface)


# removeAllWalls()

    # Removes all walls on the board
    def removeAllWalls(self, surface, buttonSelected):
        for row in range(0,len(self.listOfWalls)):
            if self.cells[self.listOfWalls[row][0]][self.listOfWalls[row][1]].cellValue != False:
                self.cells[self.listOfWalls[row][0]][self.listOfWalls[row][1]].cellValue = False
                self.cells[self.listOfWalls[row][0]][self.listOfWalls[row][1]].wallSelected = False
                self.cells[self.listOfWalls[row][0]][self.listOfWalls[row][1]].drawCell(surface, buttonSelected)
                self.redrawLines(self.listOfWalls[row][1],self.listOfWalls[row][0],surface)

# markSource()  
         
    # Marks the source cell
    def markSource(self, x, y,surface, Button):
        if not self.isWithinBounds(x, y):
            return

        validPosition = False
        if self.listOfWalls != []:
            for row in range(0,len(self.listOfWalls)):
                if self.listOfWalls[row][0] == y and self.listOfWalls[row][1] == x:
                    validPosition = True
                    break

        if validPosition != True and self.cells[y][x].destinationCellLocated != True:
            if self.SDCoordinates[0][0]!=-1 and self.SDCoordinates[0][1]!=-1:
                self.cells[self.SDCoordinates[0][0]][self.SDCoordinates[0][1]].sourceCellLocated = False
                self.cells[self.SDCoordinates[0][0]][self.SDCoordinates[0][1]].drawCell(surface, Button)
                self.redrawLines(self.SDCoordinates[0][1],self.SDCoordinates[0][0],surface)

            self.cells[y][x].sourceCellLocated = True
            self.cells[y][x].drawCell(surface, Button)
            self.SDCoordinates[0][0], self.SDCoordinates[0][1] = y, x
            self.redrawLines(x,y,surface)

# markDestination()            
 
    # Marks the destination cell
    def markDestination(self,x,y,surface, buttonSelected, multipleDestinationsState=0):
        if not self.isWithinBounds(x, y):
            return

        validPosition = False
        if self.listOfWalls != []:
            for row in range(0,len(self.listOfWalls)):
                if self.listOfWalls[row][0] == y and self.listOfWalls[row][1] == x:
                    validPosition = True
                    break
        if validPosition != True and self.cells[y][x].sourceCellLocated != True:

            if multipleDestinationsState == 0:
            
                # Removes the previous destination cell so that only one exists
                if self.SDCoordinates[1][0] != -1 and self.SDCoordinates[1][1] != -1:
                    self.cells[self.SDCoordinates[1][0]][self.SDCoordinates[1][1]].destinationCellLocated = False
                    self.cells[self.SDCoordinates[1][0]][self.SDCoordinates[1][1]].drawCell(surface, buttonSelected)
                    self.redrawLines(self.SDCoordinates[1][1],self.SDCoordinates[1][0],surface)

                self.cells[y][x].destinationCellLocated = True
                self.cells[y][x].drawCell(surface, buttonSelected)
                self.redrawLines(x,y,surface)
                self.SDCoordinates[1][0], self.SDCoordinates[1][1] = y, x

            if multipleDestinationsState == 1:
                self.cells[y][x].destinationCellLocated = True
                self.cells[y][x].drawCell(surface, buttonSelected)
                self.redrawLines(x,y,surface)
                temp = []; temp.append(y); temp.append(x)
                self.multipleDestinations.append(temp)

# destinationFound()            
 
    # Checks if destination is found
    def destinationFound(self,y,x, multipleDestinationsState=0, numitr=0):
        if multipleDestinationsState == 0:
            if self.SDCoordinates[1][0] == y and self.SDCoordinates[1][1] == x:
                return True
        else:
            for row in range(0,len(self.multipleDestinations)):
                if self.multipleDestinations[row][0] == y and self.multipleDestinations[row][1] == x:
                    return True
            return False

# sourceFound()        

    # Checks if source is found
    def sourceFound(self, y, x, multipleDestinationsState=0, numberOfiterations=0):
        if multipleDestinationsState == 1:
            if numberOfiterations < len(self.multipleDestinations)-1:
                if y == self.SDCoordinates[0][0] and x == self.SDCoordinates[0][1]:
                    return True
            return False


# markWalls()            

    # Mark a cell as a wall
    def markWalls(self,x,y,surface, buttonSelected):
        if not self.isWithinBounds(x, y):
            return

        # Stores the coordinates of every cell that is a wall
        temp = []; temp.append(y); temp.append(x)
        self.listOfWalls.append(temp)

        # As long as the cell is not the source cell and not the destination cell
        if self.cells[y][x].sourceCellLocated != True and self.cells[y][x].destinationCellLocated != True:
            self.cells[y][x].cellValue = True
            self.cells[y][x].wallSelected = True
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x,y,surface)

# generateRandomMaze()

    # Generates a random maze
    def generateRandomMaze(self,surface, buttonSelected):
        for row in range(0,35):
            for col in range(0,45):
                randomNumber = random.randint(1,10)
                if randomNumber >= 8:
                    self.markWalls(col, row, surface, buttonSelected)
                    pygame.display.flip()
                    pygame.time.delay(10)

# showPath()
    def showPath(self, surface, buttonSelected, path, open_list):
        if path != []:
            for row in range(1,len(path)-1):
                self.cells[path[row][0]][path[row][1]].pathCellLocated = True
                self.cells[path[row][0]][path[row][1]].drawCell(surface, buttonSelected)
                self.redrawLines(path[row][1],path[row][0],surface)
                pygame.display.flip()
                pygame.time.delay(5)


# BFS
    def BFS(self, Ys, Xs, Yd, Xd, surface, buttonSelected):

        def BFS_Moving_Functionality(y, x):
            self.cells[y][x].cellValue = True
            if self.destinationFound(y, x):
                return True
            self.cells[y][x].isValid = True
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x,y,surface)
            pygame.display.flip()
            pygame.time.delay(1)
            return False
        
        def BFS_Path_Functionality(y, x):
            if self.destinationFound(y, x):
                return True
            self.cells[y][x].pathCellLocated = True
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x,y,surface)
            return False

        source = Qitem(Ys,Xs)
        end = Qitem(Yd,Xd)
        nums = []
        nums.append("")
        ShPath = "" 
        q = []
        traversedNodes = [] 
        path = []
        q.append(source)
        self.cells[source.row][source.col].cellValue = True
        while(len(q)!=0):
            p = Qitem(q[0].row, q[0].col)
            q.pop(0)
            ShPath = nums.pop(0)

            # If destination is found
            if p.row == end.row and p.col == end.col:
                for direction in ShPath:
                    if direction == "U":
                        source.row -= 1
                        path.append(Qitem(source.row, source.col))
                        if BFS_Path_Functionality(source.row, source.col):
                            break
                    elif direction == "D":
                        source.row += 1
                        path.append(Qitem(source.row, source.col))
                        if BFS_Path_Functionality(source.row, source.col):
                            break
                    elif direction == "L":
                        source.col -= 1
                        path.append(Qitem(source.row, source.col))
                        if BFS_Path_Functionality(source.row, source.col):
                            break
                    else:
                        source.col += 1
                        path.append(Qitem(source.row, source.col))
                        if BFS_Path_Functionality(source.row, source.col):
                            break
                return

            # Moving up
            if p.row-1 >=0 and self.cells[p.row-1][p.col].cellValue == False:
                q.append(Qitem(p.row-1,p.col))
                traversedNodes.append(Qitem(p.row-1,p.col))
                nums.append(ShPath + "U")
                if BFS_Moving_Functionality(p.row-1,p.col):
                    continue
            # Moving down
            if p.row+1 < 35 and self.cells[p.row+1][p.col].cellValue == False:
                q.append(Qitem(p.row+1,p.col))
                traversedNodes.append(Qitem(p.row+1,p.col))
                nums.append(ShPath + "D")
                if BFS_Moving_Functionality(p.row+1, p.col):
                    continue
            # Moving left
            if p.col-1 >=0 and self.cells[p.row][p.col-1].cellValue == False:
                q.append(Qitem(p.row,p.col-1))
                traversedNodes.append(Qitem(p.row,p.col-1))
                nums.append(ShPath + "L")
                if BFS_Moving_Functionality(p.row, p.col-1):
                    continue
            # Moving right
            if p.col+1 < 45 and self.cells[p.row][p.col+1].cellValue == False:
                q.append(Qitem(p.row,p.col+1))
                traversedNodes.append(Qitem(p.row,p.col+1))
                nums.append(ShPath + "R")
                if BFS_Moving_Functionality(p.row, p.col+1):
                    continue
        return



#Astar
    def Astar(self,start,end,surface, buttonSelected, multipleDestinationsState, iterationNumber):

        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        open_list = []
        closed_list = []
        traversedNodes = []
        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                
                self.showPath(surface, buttonSelected, path[::-1], open_list)

                # If there are more than one destination nodes marked on the grid
                if multipleDestinationsState:
                    for row in range(0,len(open_list)):
                        self.cells[open_list[row].position[0]][open_list[row].position[1]].cellValue = False
                    if iterationNumber == 0:
                        return
                    tempS = ()
                    tempD = ()
                    end = list(tempD)
                    start = list(tempS)
                    start.append(self.multipleDestinations[iterationNumber][0]), start.append(self.multipleDestinations[iterationNumber][1])
                    end.append(self.multipleDestinations[iterationNumber-1][0]), end.append(self.multipleDestinations[iterationNumber-1][1])
                    self.Astar(tuple(start), tuple(end), surface, buttonSelected, multipleDestinationsState, iterationNumber-1)

                return

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:#(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                                # len(self.cells) - 1                                    #(len(self.cells[len(self.cells)-1]) -1)
                if node_position[0] > (35-1) or node_position[0] < 0 or node_position[1] > (45-1) or node_position[1] < 0:
                    continue

                if self.cells[node_position[0]][node_position[1]].cellValue != False:
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)
            for child in children:
                isClosed = False
                isOpened = False
                for closed_child in closed_list:
                    if child == closed_child:
                        isClosed = True
                        break
                if isClosed:
                    continue
                child.g = current_node.g + self.cells[child.position[0]][child.position[1]].weight
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) 
                child.f = child.g + child.h
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        isOpened = True
                        break
                if isOpened:
                    continue

                open_list.append(child)
                traversedNodes.append(child)
                if self.destinationFound(child.position[0],child.position[1], multipleDestinationsState, iterationNumber):
                    continue
                if self.sourceFound(child.position[0], child.position[1], multipleDestinationsState, iterationNumber):
                    continue
                self.cells[child.position[0]][child.position[1]].isValid = True
                self.cells[child.position[0]][child.position[1]].drawCell(surface, buttonSelected)
                self.redrawLines(child.position[1],child.position[0],surface)
                pygame.display.flip()
                pygame.time.delay(2)

        return



# Dijkstra
    def Dijkstra(self, start, end, surface, buttonSelected):
        start_node = Node(None, start)
        start_node.g = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.f = 0
        open_list = []
        closed_list = []
        open_list.append(start_node)
        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                self.showPath(surface, buttonSelected, path[::-1], open_list)

                return

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                                    # len(self.cells) - 1
                if node_position[0] > (34) or node_position[0] < 0 or node_position[1] > (44) or node_position[1] < 0:
                    continue

                if self.cells[node_position[0]][node_position[1]].cellValue != False:
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                isClosed = False
                isOpened = False
                for closed_child in closed_list:
                    if child == closed_child:
                        isClosed = True
                        break
                if isClosed:
                    continue
                child.g = current_node.g + self.cells[child.position[0]][child.position[1]].weight
                child.f = child.g

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        isOpened = True
                        break
                if isOpened:
                    continue

                open_list.append(child)
                if self.destinationFound(child.position[0],child.position[1]):
                    continue
                if self.sourceFound(child.position[0], child.position[1]):
                    continue

                self.cells[child.position[0]][child.position[1]].isValid = True
                self.cells[child.position[0]][child.position[1]].drawCell(surface, buttonSelected)
                self.redrawLines(child.position[1],child.position[0],surface)
                pygame.display.flip()

        return


# DFS
    def DFS(self, Ys, Xs, Yd, Xd, surface, buttonSelected):

        def DFS_Moving_Functionality(y, x):
            self.cells[y][x].cellValue = True
            if self.destinationFound(y, x):
                return True
            self.cells[y][x].isValid = True
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x,y,surface)
            pygame.display.flip()
            pygame.time.delay(1)
            return False
        
        def DFS_Path_Functionality(y, x):
            if self.destinationFound(y, x):
                return True
            self.cells[y][x].pathCellLocated = True
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x,y,surface)
            return False

        source = Qitem(Ys,Xs)
        end = Qitem(Yd,Xd)
        nums = []
        nums.append("")
        ShPath = "" 
        s = []
        traversedNodes = [] 
        path = []
        s.append(source)
        self.cells[source.row][source.col].cellValue = True
        while(len(s)!=0):
            p = Qitem(s[-1].row, s[-1].col)
            s.pop(-1)
            ShPath = nums.pop(-1)

            # If destination is found
            if p.row == end.row and p.col == end.col:
                for direction in ShPath:
                    if direction == "U":
                        source.row -= 1
                        path.append(Qitem(source.row, source.col))
                        if DFS_Path_Functionality(source.row, source.col):
                            break
                    elif direction == "D":
                        source.row += 1
                        path.append(Qitem(source.row, source.col))
                        if DFS_Path_Functionality(source.row, source.col):
                            break
                    elif direction == "L":
                        source.col -= 1
                        path.append(Qitem(source.row, source.col))
                        if DFS_Path_Functionality(source.row, source.col):
                            break
                    else:
                        source.col += 1
                        path.append(Qitem(source.row, source.col))
                        if DFS_Path_Functionality(source.row, source.col):
                            break
                return

            # Moving up
            if p.row-1 >=0 and self.cells[p.row-1][p.col].cellValue == False:
                s.append(Qitem(p.row-1,p.col))
                traversedNodes.append(Qitem(p.row-1,p.col))
                nums.append(ShPath + "U")
                if DFS_Moving_Functionality(p.row-1,p.col):
                    continue
            # Moving down
            if p.row+1 < 35 and self.cells[p.row+1][p.col].cellValue == False:
                s.append(Qitem(p.row+1,p.col))
                traversedNodes.append(Qitem(p.row+1,p.col))
                nums.append(ShPath + "D")
                if DFS_Moving_Functionality(p.row+1, p.col):
                    continue
            # Moving left
            if p.col-1 >=0 and self.cells[p.row][p.col-1].cellValue == False:
                s.append(Qitem(p.row,p.col-1))
                traversedNodes.append(Qitem(p.row,p.col-1))
                nums.append(ShPath + "L")
                if DFS_Moving_Functionality(p.row, p.col-1):
                    continue
            # Moving right
            if p.col+1 < 45 and self.cells[p.row][p.col+1].cellValue == False:
                s.append(Qitem(p.row,p.col+1))
                traversedNodes.append(Qitem(p.row,p.col+1))
                nums.append(ShPath + "R")
                if DFS_Moving_Functionality(p.row, p.col+1):
                    continue
        return


# Hansel & Gretel Search Algorithm 
    def HG(self, Ys, Xs, Yd, Xd, surface, buttonSelected):

        # Finds the path to the destination
        def findPath(ShPathS, source):
            for elem in ShPathS:
                if elem == "U":
                    source.row-=1
                    self.cells[source.row][source.col].pathCellLocated = True
                    self.cells[source.row][source.col].drawCell(surface, buttonSelected)
                    self.redrawLines(source.col,source.row,surface)
                if elem == "D":
                    source.row+=1
                    self.cells[source.row][source.col].pathCellLocated = True
                    self.cells[source.row][source.col].drawCell(surface, buttonSelected)
                    self.redrawLines(source.col,source.row,surface)
                if elem == "L":
                    source.col-=1
                    self.cells[source.row][source.col].pathCellLocated = True
                    self.cells[source.row][source.col].drawCell(surface, buttonSelected)
                    self.redrawLines(source.col,source.row,surface)
                if elem == "R":
                    source.col+=1
                    self.cells[source.row][source.col].pathCellLocated = True
                    self.cells[source.row][source.col].drawCell(surface, buttonSelected)
                    self.redrawLines(source.col,source.row,surface)

        # Returns the Reversed Path
        def reversePath(y, x):
            reversedPath = self.cells[y][x].Tpath[-2::-1]
            newPath = ""

            for j in range(len(reversedPath)):
                if reversedPath[j] == "U":
                    newPath += "D"
                elif reversedPath[j] == "D":
                    newPath += "U"
                elif reversedPath[j] == "L":
                    newPath += "R"
                elif reversedPath[j] == "R":
                    newPath += "L"

            return newPath

        # If two nodes intersect
        def intersect(y, x, path, source, direction):
            path += (direction + reversePath(y, x))
            self.cells[y][x].Tpath = '3'
            findPath(path, source)

        # HG functionality
        def HG_Functionality(y, x, direction, path, side):
            self.cells[y][x].cellValue = True
            self.cells[y][x].Tpath = side + (path + direction)
            self.cells[y][x].isValid = True
            self.cells[y][x].drawCell(surface, buttonSelected)
            self.redrawLines(x,y,surface)
            pygame.display.flip()
            pygame.time.delay(1)

        source = Qitem(Ys,Xs)   # Coordinates of the source cell
        end = Qitem(Yd,Xd)      # Coordinates of the destination cell
        numsS = []
        numsD = []
        numsS.append("")
        numsD.append("")
        ShPathS = ""
        ShPathD = ""
        sourceQueue = []
        destinationQueue = []
        traversedNodes = [] # records all visited nodes
        path = []
        sourceQueue.append(source)
        destinationQueue.append(end)

        self.cells[source.row][source.col].cellValue = True
        self.cells[source.row][source.col].Tpath = "1"

        self.cells[end.row][end.col].cellValue = True
        self.cells[end.row][end.col].Tpath = "2"

        while(len(sourceQueue)!=0 or len(destinationQueue)!=0):

            pS = Qitem(sourceQueue[0].row, sourceQueue[0].col)
            pD = Qitem(destinationQueue[0].row, destinationQueue[0].col)
            sourceQueue.pop(0)
            destinationQueue.pop(0)
            ShPathS = numsS.pop(0)
            ShPathD = numsD.pop(0)

        # Source traversal -------------------------------------------------------

        #moving up
            if pS.row-1 >=0:
                if self.cells[pS.row-1][pS.col].cellValue == False:
                    sourceQueue.append(Qitem(pS.row-1,pS.col))
                    numsS.append(ShPathS + "U")
                    HG_Functionality(pS.row-1, pS.col,"U", ShPathS, "1")
                else:
                    if self.cells[pS.row-1][pS.col].wallSelected:
                        pass
                    else:
                        if self.cells[pS.row-1][pS.col].Tpath[0] == '2':
                            intersect(pS.row-1, pS.col, ShPathS, source, "U")
                            return
        #moving down
            if pS.row+1 < 35:
                if self.cells[pS.row+1][pS.col].cellValue == False:
                    sourceQueue.append(Qitem(pS.row+1,pS.col))
                    numsS.append(ShPathS + "D")
                    HG_Functionality(pS.row+1, pS.col,"D", ShPathS, "1")
                else:
                    if self.cells[pS.row+1][pS.col].wallSelected:
                        pass
                    else:
                        if self.cells[pS.row+1][pS.col].Tpath[0] == '2':
                            intersect(pS.row+1, pS.col, ShPathS, source, "D")
                            return
        #moving left
            if pS.col-1 >=0:
                if self.cells[pS.row][pS.col-1].cellValue == False:
                    sourceQueue.append(Qitem(pS.row,pS.col-1))
                    numsS.append(ShPathS + "L")
                    HG_Functionality(pS.row, pS.col-1,"L", ShPathS, "1")
                else:
                    if self.cells[pS.row][pS.col-1].wallSelected:
                        pass
                    else:
                        if self.cells[pS.row][pS.col-1].Tpath[0] == '2':
                            intersect(pS.row, pS.col-1, ShPathS, source, "L")
                            return

        #moving right
            if pS.col+1 < 45:
                if self.cells[pS.row][pS.col+1].cellValue == False:
                    sourceQueue.append(Qitem(pS.row,pS.col+1))
                    numsS.append(ShPathS + "R")
                    HG_Functionality(pS.row, pS.col+1, "R", ShPathS, "1")
                else:
                    if self.cells[pS.row][pS.col+1].wallSelected:
                        pass
                    else:
                        if self.cells[pS.row][pS.col+1].Tpath[0] == '2':
                            intersect(pS.row, pS.col+1, ShPathS, source, "R")
                            return


        # Destination traversal -------------------------------------------------

        #moving up
            if pD.row-1 >=0:
                if self.cells[pD.row-1][pD.col].cellValue == False:
                    destinationQueue.append(Qitem(pD.row-1,pD.col))
                    numsD.append(ShPathD + "U")
                    HG_Functionality(pD.row-1, pD.col, "U", ShPathD, "2")
                else:
                    if self.cells[pD.row-1][pD.col].wallSelected:
                        pass
                    else:
                        if self.cells[pD.row-1][pD.col].Tpath[0] == '1':
                            intersect(pD.row-1, pD.col, ShPathD, end, "U")
                            return
        #moving down
            if pD.row+1 < 35:
                if self.cells[pD.row+1][pD.col].cellValue == False:
                    destinationQueue.append(Qitem(pD.row+1,pD.col))
                    numsD.append(ShPathD + "D")
                    HG_Functionality(pD.row+1, pD.col, "D", ShPathD, "2")
                else:
                    if self.cells[pD.row+1][pD.col].wallSelected:
                        pass
                    else:
                        if self.cells[pD.row+1][pD.col].Tpath[0] == '1':
                            intersect(pD.row+1, pD.col, ShPathD, end, "D")
                            return
        #moving left
            if pD.col-1 >=0:
                if self.cells[pD.row][pD.col-1].cellValue == False:
                    destinationQueue.append(Qitem(pD.row,pD.col-1))
                    numsD.append(ShPathD + "L")
                    HG_Functionality(pD.row, pD.col-1, "L", ShPathD, "2")
                else:
                    if self.cells[pD.row][pD.col-1].wallSelected:
                        pass
                    else:
                        if self.cells[pD.row][pD.col-1].Tpath[0] == '1':
                            intersect(pD.row, pD.col-1, ShPathD, end, "L")
                            return

        #moving right
            if pD.col+1 < 45:
                if self.cells[pD.row][pD.col+1].cellValue == False:
                    destinationQueue.append(Qitem(pD.row,pD.col+1))
                    numsD.append(ShPathD + "R")
                    HG_Functionality(pD.row, pD.col+1, "R", ShPathD, "2")
                else:
                    if self.cells[pD.row][pD.col+1].wallSelected:
                        pass
                    else:
                        if self.cells[pD.row][pD.col+1].Tpath[0] == '1':
                            intersect(pD.row, pD.col+1, ShPathD, end, "R")
                            return


        return



#search
    def search(self,algorithmSelected, surface, buttonSelected, multipleDestinationsState):

        # BFS ------------------------------
        if algorithmSelected == "BFS":
            self.BFS(self.SDCoordinates[0][0], self.SDCoordinates[0][1], self.SDCoordinates[1][0], self.SDCoordinates[1][1],surface, buttonSelected)

        # Astar ----------------------------
        elif algorithmSelected == "A*":
            self.randomWeight("Astar")
            tempS = ()
            tempD = ()
            start = list(tempS)
            end = list(tempD)
            start.append(self.SDCoordinates[0][0]), start.append(self.SDCoordinates[0][1])

            if multipleDestinationsState:
                end.append(self.multipleDestinations[len(self.multipleDestinations)-1][0]), end.append(self.multipleDestinations[len(self.multipleDestinations)-1][1])
                self.Astar(tuple(start),tuple(end),surface, buttonSelected, multipleDestinationsState, len(self.multipleDestinations)-1)
            else:
                end.append(self.SDCoordinates[1][0]), end.append(self.SDCoordinates[1][1])
                self.Astar(tuple(start),tuple(end),surface, buttonSelected, multipleDestinationsState, 0)

        # Dijkstra ------------------------
        elif algorithmSelected == "Dijkstra":
            self.randomWeight("Dijkstra")
            tempS = ()
            tempD = ()
            start = list(tempS)
            end = list(tempD)
            start.append(self.SDCoordinates[0][0]), start.append(self.SDCoordinates[0][1])
            
            self.cells[self.SDCoordinates[1][0]][self.SDCoordinates[1][1]].weight = 0
            end.append(self.SDCoordinates[1][0]), end.append(self.SDCoordinates[1][1])
            self.Dijkstra(tuple(start),tuple(end),surface, buttonSelected)

        # DFS --------------------------------
        elif algorithmSelected == "DFS":
            self.DFS(self.SDCoordinates[0][0], self.SDCoordinates[0][1], self.SDCoordinates[1][0], self.SDCoordinates[1][1],surface, buttonSelected)

        # Hansel and gretel ------------------
        elif algorithmSelected == "H&G":
            self.HG(self.SDCoordinates[0][0], self.SDCoordinates[0][1], self.SDCoordinates[1][0], self.SDCoordinates[1][1],surface, buttonSelected)
        


    # Reload the window 
    def reload(self, surface):
        for row in range(0,35):
            for cell in range(0,45):

                # Set the weight of every cell to 1
                self.cells[row][cell].weight = 1                            

                # If the value of a cell is 'True', set it to False
                # When a cell's value is 'True', it means that the cell has been visited therefore it is unreachable
                if self.cells[row][cell].cellValue == True:
                    self.cells[row][cell].cellValue = False

                
                if self.cells[row][cell].sourceCellLocated == True:
                    self.cells[row][cell].sourceCellLocated = False
                    self.cells[row][cell].createCell(surface)
                    self.redrawLines(cell,row,surface)

                elif self.cells[row][cell].destinationCellLocated == True:
                    self.cells[row][cell].destinationCellLocated = False
                    self.cells[row][cell].createCell(surface)
                    self.redrawLines(cell,row,surface)

                if self.cells[row][cell].isValid == True:
                    self.cells[row][cell].isValid = False
                    self.cells[row][cell].createCell(surface)
                    self.redrawLines(cell,row,surface)

                elif self.cells[row][cell].wallSelected == True:
                    self.cells[row][cell].wallSelected = False
                    self.cells[row][cell].createCell(surface)
                    self.redrawLines(cell,row,surface)

                if self.cells[row][cell].pathCellLocated == True:
                    self.cells[row][cell].pathCellLocated = False
                    self.cells[row][cell].createCell(surface)
                    self.redrawLines(cell,row,surface)

        self.Coordinates = [[-1 for x in range(2)] for y in range(2)]
        self.multipleDestinations.clear()
        self.listOfWalls.clear()
        self.openList = None
        self.path = None
