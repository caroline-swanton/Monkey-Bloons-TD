from cmu_graphics import *
from PIL import Image
import random, copy

# generates a path with at least 35 cells and 3 steps in each dir before turning
def generateRandomPath(app, minCells = 35, minSteps = 3):
    # chooses a random edge of the screen for path to start on
    startEdge = random.choice(['left', 'right', 'top', 'bottom'])
    startRow, startCol = getStartCell(app, startEdge) # first cell in path
    # keeps track of cells already in path
    visited = {(startRow, startCol)}
    # keeps track of path
    path = [(startRow, startCol)]
    app.map.path = generatePath(app, path, startRow, startCol, visited, None, 
                                0, startEdge, minCells, minSteps)
    
    # finds edge path ends on based on last path cell
    if app.map.path[-1][0] == 0: app.map.endEdge = 'top'
    elif app.map.path[-1][0] == app.map.rows - 1: app.map.endEdge = 'bottom'
    elif app.map.path[-1][1] == app.map.cols - 1: app.map.endEdge = 'right'
    else: app.map.endEdge = 'left'

    # convert path into directions
    dirs = []
    prevRow, prevCol = startRow, startCol
    for i in range(len(app.map.path)):
        currRow, currCol = app.map.path[i]
        if currRow < prevRow:
            dirs.append('up')
        elif currRow > prevRow:
            dirs.append('down')
        elif currCol < prevCol:
            dirs.append('left')
        elif currCol > prevCol:
            dirs.append('right')
        prevRow, prevCol = currRow, currCol
    app.dirs = dirs
    app.startCell = (startRow, startCol)

# return a random non-corner starting cell based on the starting edge
def getStartCell(app, edge):
    if edge == 'left':
        return random.randint(1, app.map.rows - 2), 0
    elif edge == 'right':
        return random.randint(1, app.map.cols - 2), app.map.cols - 1
    elif edge == 'top':
        return 0, random.randint(1, app.map.cols - 2)
    elif edge == 'bottom':
        return app.map.rows - 1, random.randint(1, app.map.cols - 2)

# recursively generates random path that follows conditions
def generatePath(app, path, currRow, currCol, visited, lastDir, 
                 stepsInCurrentDir, startEdge, minCells, minSteps):
    
    # stop if path is long enough and has a valid end cell (base case)
    if len(path) >= minCells and isEndValid(app, currRow, currCol):
        return path
    
    # recursive case
    else:
        # allows path to reach end if generated enough cells
        allowEdges = len(path) >= minCells

        # generate potential moves
        dirs = []
        if isValidMove(app, currRow, currCol + 1, visited, path, allowEdges):
            dirs.append(('right', currRow, currCol + 1))
        if isValidMove(app, currRow - 1, currCol, visited, path, allowEdges):
            dirs.append(('up', currRow - 1, currCol))
        if isValidMove(app, currRow + 1, currCol, visited, path, allowEdges):
            dirs.append(('down', currRow + 1, currCol))
        if isValidMove(app, currRow, currCol - 1, visited, path, allowEdges):
            dirs.append(('left', currRow, currCol - 1))

        # enforce minSteps before turning
        if lastDir and stepsInCurrentDir < minSteps:
            drow = 1 if lastDir == 'down' else -1 if lastDir == 'up' else 0
            dcol = 1 if lastDir == 'right' else -1 if lastDir == 'left' else 0
            newRow, newCol = currRow + drow, currCol + dcol
            dirs = []
            if isValidMove(app, newRow, newCol, visited, path, allowEdges):
                dirs.append((lastDir, newRow, newCol))

        # shuffle for randomness
        random.shuffle(dirs)

        # checks if path can be generated from this new point in path
        for dir, newRow, newCol in dirs:
            visited.add((newRow, newCol))
            path.append((newRow, newCol))
            nextStepsInCurrentDir = (stepsInCurrentDir + 1 if dir == lastDir else 1)
            result = generatePath(app, path, newRow, newCol, visited, dir, 
                                  nextStepsInCurrentDir, startEdge, minCells, 
                                  minSteps)
            if result != None:  # found valid path
                return result
            # backtrack
            path.pop()
            visited.remove((newRow, newCol))
        return None
    
# checks if move stays within bounds and avoids edges unless allowed
def isValidMove(app, row, col, visited, currentPath, allowEdges):
        # ensure move within bounds
        if not (0 <= row < app.map.rows and 0 <= col < app.map.cols):
            return False
        # ensure cell not already visited
        elif (row, col) in visited:
            return False
        # avoid edges unless explicitly allowed
        elif not allowEdges and (row == 0 or row == app.map.rows - 1 or col == 0 
                                 or col == app.map.cols - 1):
            return False
        # ensure no touching visited cells unless consecutive
        for drow, dcol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            adjacentCell = (row + drow, col + dcol)
            if adjacentCell in visited and adjacentCell != currentPath[-1]:
                return False
        return True

# checks if curr position meets the end edge condition (no corners)
def isEndValid(app, row, col):
    if (col == app.map.cols - 1 and row != 0 and row != app.map.rows - 1):
        return True
    elif (col == 0 and row != 0 and row != app.map.rows - 1):
        return True
    elif (row == 0 and col != 0 and col != app.map.cols - 1):
        return True
    elif (row == app.map.rows - 1 and col != 0 and col != app.map.cols - 1):
        return True
    return False

class Map:
    def __init__(self):
        self.rows = 13
        self.cols = 13
        self.path = [] # stores cells in path
        self.turns = [] # stores cells where balloons turn

# finds cells balloons turn in
def findTurns(app):
    prevDir = app.dirs[0]
    for i in range(len(app.dirs)):
        if app.dirs[i] != prevDir:
            app.map.turns.append(app.map.path[i])
        prevDir = app.dirs[i]
