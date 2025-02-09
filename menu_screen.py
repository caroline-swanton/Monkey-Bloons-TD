from cmu_graphics import *
from tower_classes import *
from random_map_generator import *
from PIL import Image

def restart(app):

    # adjusts scaling based on screen size
    app.sx = app.width/1028
    app.sy = app.height/633
    app.aspRat = min(app.sx, app.sy)

    # tower classes
    app.dartTower = DartTower(app, None)
    app.tackTower = TackTower(app, None)
    app.iceTower = IceTower(app, None)
    app.bombTower = BombTower(app, None)
    app.superMonkey = SuperMonkey(app, None)
    # keeps track of tower attributes based on type (not individual towers)
    app.towers = (app.dartTower, app.tackTower, app.iceTower, app.bombTower, 
                  app.superMonkey)

    # game status
    app.gameOver = False
    app.wonGame = False

    app.playing = False # must press 'Start Round' to play
    app.fastMode = False # toggle in menu (speeds up balloons and towers)
    app.autoStart = False # toggle in manu (automatically starts next round)
    app.restart = False # activated if screen size changed during round
    app.towersPlacing = None # keeps track of towers currently being placed

    app.roundNum = 1
    app.money = 650 # begin with $650
    app.lives = 40 # begin with 40 lives
    # awarded $100 first round (decreases by $1 each startRound)
    app.moneyAwarded = 101
    app.startRoundButton = True # button is initially diplayed

    # keeps track of how long captions stay on screen
    app.captionCounters = {0: 0, 10: 0, 20: 0, 30: 0, 40: 0, 'money': 0}

    app.map = Map() # stores map attributes
    generateRandomPath(app) # randomizes path on map
    findTurns(app) # finds (row, col) of turn cells
    app.cellSize = app.height/app.map.rows # finds size of each cell on map
    
    # no towers currently on board
    app.placedTowers = []

def checkMenuOpen(app, mouseX, mouseY):
        # if top-left menu button is clicked
        if ((10*app.sx <= mouseX <= 50*app.sx) and 
            (10*app.sy <= mouseY <= 50*app.sy) and not app.gameOver):
            setActiveScreen("menu")

def menu_redrawAll(app):
    # draws menu background
    drawRect(0, 0, app.width, app.height, fill = rgb(110, 171, 112))
    # draws dart monkey image
    drawImage(app.menuMonkeyURL, 30*app.sx, 100*app.sy, width = 400*app.aspRat, 
              height = 400*app.aspRat)
    # draws 'X' in top-left corned
    drawLine(15*app.sx, 15*app.sy, 40*app.aspRat, 40*app.aspRat, fill = 'white')
    drawLine(40*app.sx, 15*app.sy, 15*app.aspRat, 40*app.aspRat, fill = 'white')
    drawRoundJumps(app) # draws 'Jump to Round' and 'Restart' buttons
    drawMenuToggles(app) # draws 'Fast Mode' and 'Auto-Start' buttons

def drawRoundJumps(app):
    # draws 'Jump to Round' buttons
    rounds = ('10', '20', '30')
    for i in range(len(rounds)):
        round = rounds[i]
        drawRect(app.width/2, (50 + 100*i)*app.sy, 400*app.sx, 90*app.sy, 
                 fill = 'darkGreen')
        drawLabel(f'Jump to Round {round}', app.width/2 + 200*app.sx, 
                  (95 + (100*i))*app.sy, fill = 'white', size = 40*app.aspRat, 
                  bold = True)
    # draws Restart button
    drawRect(app.width/2 + 100*app.sx, 350*app.sy, 200*app.sx, 90*app.sy, 
             fill = 'darkGreen')
    drawLabel('Restart', app.width/2 + 200*app.sx, 395*app.sy, fill = 'white', 
              size = 40*app.aspRat, bold = True)
    
def drawMenuToggles(app):
    # draws 'Auto-Start' toggle button
    fill = 'darkGreen' if app.autoStart else 'white'
    drawCircle(app.width/2 + 90*app.sx, 500*app.sy, 15*app.aspRat, 
               border = 'black', fill = fill)
    drawLabel('Enable Auto-Start', app.width/2 + 120*app.sx, 490*app.sy, 
              size = 25*app.aspRat, align = 'left-top', bold = True)
    
    # draws 'Fast Mode' toggle button
    fill = 'darkGreen' if app.fastMode else 'white'
    drawCircle(app.width/2 + 90*app.sx, 550*app.sy, 15*app.aspRat, 
               border = 'black', fill = fill)
    drawLabel('Enable Fast Mode', app.width/2 + 120*app.sx, 540*app.sy, 
              size = 25*app.aspRat, align = 'left-top', bold = True)

def menu_onMousePress(app, mouseX, mouseY):
    # if 'X' is pressed
    if ((15*app.sx <= mouseX <= 55*app.sx) and 
        (15*app.sy <= mouseY <= 55*app.sy)):
        setActiveScreen("game")
    # checks if 'Jump to Round' button is pressed
    checkRoundButton(app, mouseX, mouseY)
    # checks if 'Restart' button is pressed
    checkRestart(app, mouseX, mouseY)
    # checks if 'Auto-Start' or 'Fast Mode' is toggled
    checkModeToggle(app, mouseX, mouseY)

def checkRoundButton(app, mouseX, mouseY):
    # jumps to round 10
    if ((app.width/2 <= mouseX <= app.width/2 + 400*app.sx) and
        (50*app.sy <= mouseY <= 140*app.sy)):
        app.roundNum = 10
    # jumps to round 20
    elif ((app.width/2 <= mouseX <= app.width/2 + 400*app.sx) and
          (150*app.sy <= mouseY <= 240*app.sy)):
        app.roundNum = 20
    # jumps to round 30
    elif ((app.width/2 <= mouseX <= app.width/2 + 400*app.sx) and
          (250*app.sy <= mouseY <= 340*app.sy)):
        app.roundNum = 30
    else: return # none are pressed
    app.captionCounters[app.roundNum] = 200
    regenerateMoney(app) # calculates correlating app.money for round
    app.map = Map()
    generateRandomPath(app) # generates new random path
    findTurns(app) # finds turn cells associated to new path
    app.playing = False # ends round
    app.placedTowers = [] # clears placed towers
    app.autoStart = False # disables auto-start
    setActiveScreen("game")

# calculates how much money user regains every ten rounds after towers despawn
def regenerateMoney(app):
    app.money = 0
    moneyAwarded = 100 # money awarded each round (goes down by 1 each round)
    for roundNum in range(app.roundNum):
        app.money += moneyAwarded
        moneyAwarded -= 1
        for i in range(len(app.rounds[roundNum])):
            balloons = app.rounds[roundNum][i]
            app.money += balloons*(i + 1) # gains money based on color of balloon

def checkRestart(app, mouseX, mouseY):
    # checks if 'Restart' button is pressed
    if ((app.width/2 + 100*app.sx <= mouseX <= app.width/2 + 300*app.sx) and 
        (350*app.sy <= mouseY <= 440*app.sy)):
        restart(app)
        app.captionCounters[0] = 200 # displays round 0 caption
        setActiveScreen("game")

def checkModeToggle(app, mouseX, mouseY):
    # finds distance from mouse click to center of toggle button
    distFromAuto = distance(mouseX, mouseY, app.width/2 + 90*app.sx, 500*app.sy)
    distFromFast = distance(mouseX, mouseY, app.width/2 + 90*app.sx, 550*app.sy)
    # checks if mosue is pressed within radius of toggle button
    if distFromAuto <= 15*app.aspRat:
        app.autoStart = not app.autoStart
    elif distFromFast <= 15*app.aspRat:
        app.fastMode = not app.fastMode

def menu_onStep(app):
    # determines if screen dimensions are changed
    if (
        not almostEqual(app.sx, app.width/1028) or
        not almostEqual(app.sy, app.height/633)
    ):
        # adjusts scaling based on screen size
        app.sx = app.width/1028
        app.sy = app.height/633
        app.aspRat = min(app.sx, app.sy)
        app.cellSize = app.height/app.map.rows