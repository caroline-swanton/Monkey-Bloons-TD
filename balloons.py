from cmu_graphics import *
from PIL import Image
import random

def findColors(app):
    colors = []
    red = app.round[0] # finds num of red balloons
    blue = app.round[1] # finds num of blue balloons
    green = app.round[2] # finds num of green balloons
    yellow = app.round[3] # finds num of yellow balloons
    # makes list with every balloons color
    for _ in range(red):
        colors.append('red')
    for _ in range(blue):
        colors.append('blue')
    for _ in range(green):
        colors.append('green')
    for _ in range(yellow):
        colors.append('yellow')
    # allows balloons to be drawn randomly
    random.shuffle(colors)
    return colors

# finds speed of balloons based on color (red slowest, yellow fastest)
def calculateSpeeds(app):
    speeds = []
    for color in app.colorList:
        speeds.append(app.balloonSpeeds[color])
    return speeds

class Balloon():
    def __init__(self, app, i, speedList, colorList):
        self.width = 33*app.sx # width of balloon img in px
        self.height = 43*app.sy # height of balloon img in px
        self.pathIndex = -1 # balloon cell in app.map.path (starts off-screen)
        self.turnIndex = 0 # index of balloon's next turn in app.map.turns
        self.dir = app.dirs[0] # balloon current direction
        self.speed = speedList[i] # finds corresponding speed
        self.color = colorList[i] # finds corresponding color
        self.url = app.balloonurls[self.color] # finds corresponding url
        # current coordinates of balloons
        self.left, self.top = self.findStartingCoord(app)
        # finds cell balloon is in
        self.cell = getCell(app, self.left, self.top)
        self.freezeDuration = 0 # stores steps that balloons stay frozen
        self.distanceTravelled = 0 # stores how many px balloon has travelled

    # finds starting position of balloon based on starting edge
    def findStartingCoord(self, app):
        row, col = app.startCell
        startLeft, startTop = getCellLeftTop(app, row, col)
        if self.dir == 'right':
            return -self.width, startTop
        elif self.dir == 'left':
            return app.map.cols*app.cellSize, startTop
        elif self.dir == 'up':
            return startLeft, app.height
        elif self.dir == 'down':
            return startLeft, -self.height

    # determines how balloon moves on path
    def calculateMove(self, app):
        # balloon doesn't move if frozen
        if self.freezeDuration > 0:
            self.freezeDuration -= 1
            if self.freezeDuration == 0: # balloon becomes unfrozen
                self.url = app.balloonurls[self.color]
            return

        if self.distanceTravelled >= 100*app.aspRat:
            self.checkBalloonEscape(app) # determines if balloon has gone off map

        self.findDir(app) # determines if balloon turns or changes cell

        # moves balloon in associated direction
        if self.dir == 'right':
            self.left += self.speed*app.aspRat
        elif self.dir == 'left':
            self.left -= self.speed*app.aspRat
        elif self.dir == 'down':
            self.top += self.speed*app.aspRat
        elif self.dir == 'up':
            self.top -= self.speed*app.aspRat
        self.distanceTravelled += self.speed*app.aspRat

    # checks if balloon has escaped based on coordinates
    def checkBalloonEscape(self, app):
        if ((app.map.endEdge == 'top' and self.top < -self.height) or
            (app.map.endEdge == 'left' and self.left < -self.width) or
            (app.map.endEdge == 'bottom' and self.top > app.height) or
            (app.map.endEdge == 'right' and self.left > app.map.cols*app.cellSize)):
            # more powerful balloons take more lives
            if self.color == 'red':
                app.lives -= 1
            elif self.color == 'blue':
                app.lives -= 2
            elif self.color == 'green':
                app.lives -= 3
            else:
                app.lives -= 4
            if app.lives < 0: # cannot have negative balloons
                app.lives = 0
            app.balloons.remove(self)
            app.totalBalloons -= 1
        
    def findDir(self, app):
        newCell = getCell(app, self.left, self.top) # finds balloon curr cell
        # if balloon in new cell, then change balloon's cell to that cell
        if self.cell != newCell:
            self.cell = newCell
            self.pathIndex += 1

        if self.turnIndex < len(app.map.turns):
            # finds next cell balloon should turn
            turnRow, turnCol = app.map.turns[self.turnIndex]
            # finds top left coords of turn cell
            turnX, turnY = getCellLeftTop(app, turnRow, turnCol)
            # change balloon dir if top left is greater than turn cell's top left
            if ((self.dir == 'right' and self.left > turnX) or
                (self.dir == 'left' and self.left < turnX)or
                (self.dir == 'up' and self.top < turnY) or
                (self.dir == 'down' and self.top > turnY)):
                self.dir = app.dirs[self.pathIndex]
                self.turnIndex += 1

    # pops balloon if hit
    def popBalloon(self, app):
        self.calculateMove(app) # determines how balloons move
        if self.url == app.balloonurls['popped']: # balloon was popped
            # plays balloon popping sound
            app.poppingSound.play(restart = True)
            # based on color, balloon either changes color or completely pops
            if self.color == 'red':
                # stops drawing if base balloon has been popped
                app.balloons.remove(self)
                app.totalBalloons -= 1
            elif self.color == 'blue':
                self.color = 'red'
                self.speed = app.balloonSpeeds['red']
                self.url = app.balloonurls['red']
            elif self.color == 'green':
                self.color = 'blue'
                self.speed = app.balloonSpeeds['blue']
                self.url = app.balloonurls['blue']
            else:
                self.color = 'green'
                self.speed = app.balloonSpeeds['green']
                self.url = app.balloonurls['green']
            app.money += 1 # awarded for each balloon popped

def drawBalloons(app):
    for balloon in app.balloons:
        # changes img of frozen balloons
        if balloon.freezeDuration > 0 and balloon.url != app.balloonurls['popped']:
            balloon.url = app.balloonurls['frozen']
        drawImage(balloon.url, balloon.left, balloon.top, width = balloon.width, 
                  height = balloon.height)
        
def getCellLeftTop(app, row, col):
    left = app.cellSize*col
    top = app.cellSize*row
    return left, top

def getCell(app, x, y):
    row = rounded(y / app.cellSize)
    col = rounded(x / app.cellSize)
    return(row, col)