from cmu_graphics import *
from PIL import Image
from start_screen import *
from menu_screen import *
from draw_side_menu import *
from balloons import *
import os, pathlib

# GAME HEAVILY INSPIRED BY BLOONS TOWER DEFENSE 1 BY NINJA KIWI

def onAppStart(app):
    
    loadImages(app)
    loadSounds(app)
    app.music.setVolume(.5)
    app.music.play(loop = True)

    # [red, blue, green, yellow] balloons in each round
    app.rounds = [
        [12, 0, 0, 0], [25, 0, 0, 0], [24, 5, 0, 0], [10, 24, 0, 0],
        [30, 25, 0, 0], [0, 0, 15, 0], [0, 75, 0, 0], [70, 70, 0, 0],
        [0, 50, 15, 0], [0, 0, 35, 0], [0, 0, 0, 15], [0, 25, 25, 3],
        [40, 75, 28, 0], [0, 0, 0, 28], [0, 30, 60, 0], [0, 70, 75, 0],
        [0, 140, 45, 0], [0, 30, 25, 27], [0, 0, 90, 0], [0, 0, 24, 48],
        [0, 10, 85, 35], [0, 0, 0, 45], [0, 0, 35, 64], [0, 30, 50, 42],
        [0, 0, 70, 53], [0, 0, 0, 85], [0, 100, 0, 50], [0, 0, 0, 125], 
        [0, 0, 250, 0], [0, 40, 55, 85], [0, 0, 50, 100], [0, 0, 0, 150],
        [0, 100, 0, 100], [0, 0, 85, 110], [0, 0, 100, 115], [0, 0, 0, 220],
        [0, 200, 100, 0], [0, 150, 0, 200], [100, 100, 100, 100], [0, 0, 0, 300]
        ]

    # captions that appear every ten rounds at bottom of screen
    app.captions = {
        0: ['Welcome to Bloons Tower Defense! Over 40 rounds, stop the', 
            'bloons from escaping by building towers. As you get more money,', 
            'build more towers or upgrade existing ones.'],
        10: ['Congrats on making it to Round 10! Every ten rounds, the map will',
             'switch up, so be prepared to put down a new formation of towers!',],
        20: ['Yellow bloons incoming! Beware, yellow bloons will cost you four',
             'lives if they escape, so get those towers down!'],
        30: ["Don't forget to upgrade your towers to make them stronger!",
             'Round 30 is tough, so get ready for a BIG wave of bloons!'],
        40: ['Here comes the final wave! Place down your last towers, buy your',
             'last upgrades, and prepare for a whole bunch of bloons!'],
        'money': ['Not enough money']
    }

    # balloon change in position per step
    app.balloonSpeeds = {'red': 5, 'blue': 6, 'green': 7, 'yellow': 8}
    app.iconSize = 49 # width and height of tower icons

    restart(app)

# all images taken from the Bloons TD Wiki page accessed at this link:
# https://bloons.fandom.com/wiki/Bloons_Wiki
def loadImages(app):
    # balloon images
    redURL = CMUImage(Image.open('images/balloons/red_balloon.png'))
    blueURL = CMUImage(Image.open('images/balloons/blue_balloon.png'))
    greenURL = CMUImage(Image.open('images/balloons/green_balloon.png'))
    yellowURL = CMUImage(Image.open('images/balloons/yellow_balloon.png'))
    frozenURL = CMUImage(Image.open('images/balloons/frozen_balloon.png'))
    poppedURL = CMUImage(Image.open('images/balloon_pop.png'))
    app.balloonurls = {'red': redURL, 'blue': blueURL, 'green': greenURL, 
                       'yellow': yellowURL, 'frozen': frozenURL, 
                       'popped': poppedURL}
    # tower sprites
    app.dartTowerURL = Image.open('images/dart_monkey_spritesheet.png')
    app.tackTowerURL = Image.open('images/tack_tower_spritesheet.png')
    app.iceTowerURL = Image.open('images/ice_tower_spritesheet.png')
    app.bombTowerURL = Image.open('images/bomb_tower_spritesheet.png')
    app.superMonkeyURL = Image.open('images/super_monkey_spritesheet.png')
    # tower icon images
    app.dartIconURL = CMUImage(Image.open('images/icons/dart_tower_icon.png'))
    app.tackIconURL = CMUImage(Image.open('images/icons/tack_tower_icon.png'))
    app.iceIconURL = CMUImage(Image.open('images/icons/ice_tower_icon.png'))
    app.bombIconURL = CMUImage(Image.open('images/icons/bomb_tower_icon.png'))
    app.superIconURL = CMUImage(Image.open('images/icons/super_tower_icon.png'))
    # other images used
    app.menuMonkeyURL = CMUImage(Image.open('images/menu_monkey.png'))
    # image taken form Bloons Tower Defense Wikipedia page accessed at this link:
    # https://en.wikipedia.org/wiki/Bloons_Tower_Defense
    app.startingScreen = CMUImage(Image.open('images/starting_screen.png'))

# 112 TA assisted with loading sounds, unfortunately I didn't get a name
def loadSounds(app): 
    # Bloon popping sound from Bloons TD 6 accessed at this link:
    # https://www.youtube.com/watch?v=FmVSyKy6aKs
    poppingAbsPath = os.path.abspath('sounds/popping_sound.mp3')
    poppingSound = pathlib.Path(poppingAbsPath).as_uri()
    app.poppingSound = Sound(poppingSound)
    # 'Tribes & Tribulations' from Bloons TD 6 accessed at this link:
    # https://www.youtube.com/watch?v=7CJtN9ke8p0
    musicAbsPath = os.path.abspath('sounds/bloons_td_music.mp3')
    music = pathlib.Path(musicAbsPath).as_uri()
    app.music = Sound(music)
    # cannon sound taken from this link: 
    # https://www.youtube.com/watch?v=4hVuKDWl-54
    cannonAbsPath = os.path.abspath('sounds/bomb_tower_sound.mp3')
    cannon = pathlib.Path(cannonAbsPath).as_uri()
    app.cannonSound = Sound(cannon)

# runs if 'Start Round' button is pressed or "Auto-Start" is enabled
def startRound(app, roundJump):
    app.round = app.rounds[app.roundNum - 1] # starts at index 0 of app.rounds
    # money awarded for completing round decreases by $1 each round
    # checks if user jumped forward rounds in menu
    if roundJump == None:
        app.moneyAwarded -= 1
    else:
        app.moneyAwarded -= roundJump
    # finds total amount of balloons in round
    app.totalBalloons = sum(app.round)
    app.colorList = findColors(app) # returns shuffled list of balloon colors
    # returns correlating balloon speed based on color
    app.speedList = calculateSpeeds(app)
    app.balloons = [] # round begins with no balloons on map
    app.counter = 0 # balloon spawns every 10th step (when app.counter % 10 == 0)
    app.playing = True # begins round

def game_redrawAll(app):
    
    # if screen size is not too small
    if not app.height/app.width > 0.635 and not app.width/app.height > 1.8:
        # draws cells of map
        drawMap(app)
        if app.playing: # draws balloons if round is ongoing
            drawBalloons(app)
        drawMenu(app) # draws right-side menu
        drawIcons(app) # draws tower icons

    for tower in app.placedTowers: # draws tower attributes if selected
        if tower.selected:
            drawUpgrades(app, tower)

    # draws tower info window when mouse hovers over icon
    for tower in app.towers:
        if tower.infoShowing:
            drawInfo(app, tower)

    # if round is over, draws 'Start Round' button
    if app.startRoundButton:
        drawRect(734*app.sx, 564*app.sy, 197*app.sx, 68*app.sy, 
                 fill = rgb(39,136,0))
        drawLabel('Start Round', 833*app.sx, 598*app.sy, fill = 'white', 
                  align = 'center', size = 27*app.aspRat, font = 'montserrat')
        
    # if auto-start is enabled, draw 'Auto-Start Enabled' button
    if app.autoStart:
        drawRect(680*app.sx, 564*app.sy, 300*app.sx, 68*app.sy, 
                 fill = rgb(39,136,0))
        drawLabel('Auto-Start Enabled', 830*app.sx, 598*app.sy, fill = 'white', 
                  align = 'center', size = 27*app.aspRat, font = 'montserrat')
    
    drawTowers(app) # draws tower on board and currently placing

    drawMenuButton(app) # draws menu button in top-left corner
    drawCaptions(app) # draws any captions that may appear
    
    # shuts down game if dimensions of screen are changed while round is ongoing
    if app.restart:
        drawRect(0, 0, app.width, app.height)
        drawLabel("CAN'T CHANGE SCREEN SIZE DURING ROUND", app.width/2,
                  app.height/2, size = 34*app.aspRat, fill = 'red')
        drawLabel("press any key to restart", app.width/2, 
                  app.height/2 + 34*app.sy, size = 20*app.aspRat, fill = 'red')
    
    if app.gameOver: # draws 'Game Over' screen
        drawGameOver(app)
    
    if app.wonGame: # draws 'You Won' screen
        drawWinningScreen(app)

    # appears if screen ratio is too small
    if app.height/app.width > 0.635 or app.width/app.height > 1.8:
        drawRect(0, 0, app.width, app.height)
        drawLabel("SCREEN TOO SMALL. CHANGE SCREEN SIZE TO CONTINUE.", 
                  app.width/2, app.height/2, size = 20*app.aspRat, fill = 'red')
        
def drawMap(app):
    for row in range(app.map.rows):
        for col in range(app.map.cols):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            # colors the path grey and the background green
            fill = 'grey' if (row, col) in app.map.path else 'lightGreen'
            # colors first cell green and last cell red
            if (row, col) == app.startCell: fill = rgb(39,136,0)
            elif (row, col) == app.map.path[-1]: fill = rgb(188, 58, 58)
            drawRect(cellLeft, cellTop, app.cellSize, app.cellSize, 
                     fill = fill, border = fill)
    
def drawTowers(app):
    selectedTower = None
    # draws towers already placed on map
    for tower in app.placedTowers:
        cx, cy = tower.position
        if tower.selected: 
            selectedTower = tower
            selectcx, selectcy = cx, cy
        else: 
            # draws tower
            drawImage(tower.sprite[tower.spriteIndex], cx, cy, 
                      width = tower.width*app.sx, height = tower.height*app.sy, 
                      align = 'center', rotateAngle = tower.rotateAngle)
    # selected tower is drawn on top of all other towers
    if selectedTower:
        # draws tower range
        drawCircle(selectcx, selectcy, selectedTower.range*app.aspRat, 
                   fill = 'white', opacity = 50)
        # draws tower
        drawImage(selectedTower.sprite[selectedTower.spriteIndex], selectcx, 
                  selectcy, width = selectedTower.width*app.sx, 
                  height = selectedTower.height*app.sy, align = 'center', 
                  rotateAngle = selectedTower.rotateAngle)
    
    # draws towers that are currently being placed
    for tower in app.towers:
        if tower.placing:
            cx, cy = tower.position
            # range radius will be red if tower cannot be placed in position
            fill = 'red' if not tower.legalPlacement else 'white'
            # draws tower range
            drawCircle(cx, cy, tower.range*app.aspRat, fill = fill, opacity = 50)
            # draws tower
            drawImage(tower.sprite[tower.spriteIndex], cx, cy, 
                      width = tower.width*app.sx, height = tower.height*app.sy, 
                      align='center')

# draw menu button in top-left corner
def drawMenuButton(app):
    drawLine(15*app.sx, 20*app.sy, 45*app.sx, 20*app.sy, fill = 'white')
    drawLine(15*app.sx, 30*app.sy, 45*app.sx, 30*app.sy, fill = 'white')
    drawLine(15*app.sx, 40*app.sy, 45*app.sx, 40*app.sy, fill = 'white')

# draws captions at bottom of screen
def drawCaptions(app):
    mapWidth = app.map.cols*app.cellSize
    for caption in app.captions:
        if app.captionCounters[caption] != 0: # caption is currently displayed
            # draws caption box
            drawRect(0, app.height - 100*app.sy, mapWidth, 100*app.sy, 
                     fill = 'white')
            # finds correlating caption
            captionLines = app.captions[caption]
            for i in range(len(captionLines)):
                line = captionLines[i]
                # draws each line of caption
                drawLabel(line, 20*app.sx, app.height - 80*app.sy + (25*i)*app.sy, 
                          size = 20*app.aspRat, align = 'left-top')
    
# draws 'Game Over' screen if user reaches 0 lives
def drawGameOver(app):
    drawRect(app.width/2, app.height/2, 800*app.sx, 500*app.sy, align = 'center', 
             fill = rgb(180, 109, 109), border = 'darkRed', 
             borderWidth = 5*app.aspRat)
    drawLabel('GAME OVER', app.width/2, app.height/2 - 150*app.sy, font = 'arial', 
              size = 100*app.aspRat, bold = True)
    drawLabel("Don't let those pesky bloons escape!", app.width/2, 
              app.height/2 - 50*app.sy, size = 40*app.aspRat, bold = True)
    drawLabel("PRESS ANY KEY TO RESTART", app.width/2, app.height/2 + 150*app.sy, 
              size = 40*app.aspRat, bold = True, fill = 'white')

# draws 'You Won' screen if user completes all 40 rounds
def drawWinningScreen(app):
    drawRect(app.width/2, app.height/2, 800*app.sx, 500*app.sy, align = 'center', 
             fill = rgb(165, 223, 180), border = 'darkGreen', 
             borderWidth = 5*app.aspRat)
    drawLabel('YOU WON', app.width/2, app.height/2 - 150*app.sy, font = 'arial', 
              size = 100*app.aspRat, bold = True, fill = 'darkGreen')
    drawLabel("Congratulations!", app.width/2, app.height/2 - 50*app.sy, 
              size = 40*app.aspRat, bold = True)
    drawLabel("You've defeated all of the bloons!", app.width/2, app.height/2, 
              size = 40*app.aspRat, bold = True)
    drawLabel("PRESS ANY KEY TO RESTART", app.width/2, app.height/2 + 150*app.sy, 
              size = 40*app.aspRat, bold = True, fill = 'white')

def game_onStep(app):
    # determines if screen dimensions are changed (stops game if round ongoing)
    if (
        not almostEqual(app.sx, app.width/1028) or
        not almostEqual(app.sy, app.height/633)
    ):
        if app.playing: 
            app.restart = True
            app.playing = False 
        else:
            # adjusts placed towers' positions to new screen size
            oldCanvasWidth = app.sx*1028
            oldCanvasHeight = app.sy*633
            widthRatio = oldCanvasWidth/app.width
            heightRatio = oldCanvasHeight/app.height
            for tower in app.placedTowers:
                towerx, towery = tower.position
                tower.position = [towerx/widthRatio, towery/heightRatio]

    # adjusts scaling based on screen size
    app.sx = app.width/1028
    app.sy = app.height/633
    app.aspRat = min(app.sx, app.sy)
    app.cellSize = app.height/app.map.rows

    # decreases time caption is displayed each step
    for caption in app.captionCounters:
        if app.captionCounters[caption] != 0:
            app.captionCounters[caption] -= 1

    # if user lost game
    if app.lives <= 0: app.gameOver = True

    if app.playing:
        # 'Start Round' button will not appear when round is ongoing
        app.startRoundButton = False
        if not app.gameOver and not app.wonGame and not app.restart:
            takeStep(app)
    else:
        if not app.autoStart:
            app.startRoundButton = True
        else:
            # round will start immediately if auto-start is enabled
            startRound(app, None)

def takeStep(app):
    # makes balloons speed up in fast mode
    app.stepsPerSecond = 1000 if app.fastMode else 20

    # spawns balloon if all balloons haven't been spawned yet
    if app.counter//10 < sum(app.round) and app.counter % 10 == 0:
        balloon = Balloon(app, app.counter//10, app.speedList, app.colorList)
        app.balloons.append(balloon)
    app.counter += 1

    # despawns or changes colors of popped balloons
    for balloon in app.balloons:
        balloon.popBalloon(app)

    # changes sprite frame and checks for popped balloons
    # keeps track of which towers have finished animation if balloons are gone
    indexCounter = 0
    # if there are any towers on board
    for tower in app.placedTowers:
        tower.shoot(app)
        # ends round if all balloons are popped or escaped
        if app.totalBalloons == 0 and tower.spriteIndex == 0:
            indexCounter += 1
            # all tower animations must be completed before round ends
            if indexCounter == len(app.placedTowers):
                app.playing = False # ends round
                if app.roundNum == 40: # game ends if player completes round 40
                    app.wonGame = True
                    return
                else:
                    app.roundNum += 1
                    app.money += app.moneyAwarded # awards player money
                # every ten rounds, another map will be generated
                # towers will despawn
                # user will get all money back for prior rounds
                # round caption will appear
                if app.roundNum % 10 == 0:
                    app.map = Map()
                    generateRandomPath(app)
                    findTurns(app)
                    app.captionCounters[app.roundNum] = 200
                    app.placedTowers = []
                    app.autoStart = False
                    regenerateMoney(app) # calculates money user receives

def game_onMouseMove(app, mouseX, mouseY):
    if not app.gameOver and not app.wonGame:
        for tower in app.towers:
            tower.infoShowing = False
            checkInIcon(app, mouseX, mouseY) # check if hovering over icon

            # tower follows mouse if tower is in placement mode
            if tower.placing:
                tower.position = [mouseX, mouseY]
                tower.legalPlacement =  placementIsLegal(app, tower, mouseX, 
                                                         mouseY)

def checkInIcon(app, mouseX, mouseY):
    for i in range(len(app.towers)):
        cx = (app.iconSize + 10)*i + 707 # center x of each icon
        cy = 211 # center y of each icon
        r = (app.iconSize/2)*app.aspRat # radius of each icon
        mouseDistance = distance(cx*app.sx, cy*app.sy, mouseX, mouseY)
        # if mouse is within radius of icon, show tower info
        app.towers[i].infoShowing = (mouseDistance <= r)
   
def placementIsLegal(app, tower, mouseX, mouseY):
    # checks tower overlap
    for placedTower in app.placedTowers:
        towerx, towery = placedTower.position
        if ((towerx - 40*app.sx < mouseX < towerx + 40*app.sx) and
            (towery - 40*app.sy < mouseY < towery + 40*app.sy)):
            return False
    # checks if tower is far away enough from path and not in menu
    return ((tower.getPlacementCell(app, mouseX + 20*app.sx, mouseY) not in 
             app.map.path) and
            (tower.getPlacementCell(app, mouseX - 20*app.sx, mouseY) not in 
             app.map.path) and
            (tower.getPlacementCell(app, mouseX, mouseY + 20*app.sy) not in 
             app.map.path) and
            (tower.getPlacementCell(app, mouseX, mouseY - 20*app.sy) not in 
             app.map.path) and 
            (mouseX + 20*app.aspRat < app.map.cols*app.cellSize))

def game_onMousePress(app, mouseX, mouseY):
    if not app.wonGame and not app.gameOver:
        for tower in app.towers:
            # cannot select a tower when another is being placed
            if app.towersPlacing == None and tower.infoShowing:
                if tower.cost <= app.money: # if user can afford tower
                    app.money -= tower.cost
                    tower.position = [mouseX, mouseY]
                    tower.placing = True
                    app.towersPlacing = tower
                    tower.legalPlacement = False
                else:
                    # shows 'not enough money' caption if user can't afford tower
                    app.captionCounters['money'] = 100
            
            elif tower.placing and tower.legalPlacement:
                app.towersPlacing = None
                tower.placing = False # place tower
                towerType = type(tower) # finds which tower was placed
                # adds that tower to placed towers
                app.placedTowers.append(towerType(app, [mouseX, mouseY]))

        # checks if 'Start Round' button was pressed
        checkStartRound(app, mouseX, mouseY)
        # checks if a placed tower was clicked on
        checkTowerSelection(app, mouseX, mouseY)
        # checks if upgrade was selected
        checkUpgradeSelection(app, mouseX, mouseY)
        # checks if a placed tower was sold
        checkTowerSold(app, mouseX, mouseY)
        # checks if top-left menu button was clicked
        checkMenuOpen(app, mouseX, mouseY)

def checkStartRound(app, mouseX, mouseY):
    if app.startRoundButton: # if button is displayed
        # if mouse is pressed within 'Start Round' button
        if (
            (mouseX >= 734*app.sx and mouseX <= 932*app.sx) and
            (mouseY >= 564*app.sy and mouseY <= 632*app.sy)
        ):
            startRound(app, None)

def checkTowerSelection(app, mouseX, mouseY):
    for tower in app.placedTowers:
        towerx, towery = tower.position
        # checks if mouse was clicked within tower radius
        if ((towerx - 30*app.sx < mouseX < towerx + 30*app.sx) and 
            (towery - 30*app.sy < mouseY < towery + 20*app.sy)):
            # deselects any other selected tower
            for oldTower in app.placedTowers:
                oldTower.selected = False
            tower.selected = True # selects tower
        # deselects tower if mouse is pressed outside of range on map
        elif ((distance(mouseX, mouseY, towerx, towery) > tower.range*app.aspRat) and
              (mouseX < (app.map.cols*app.cellSize))):
            tower.selected = False

def checkUpgradeSelection(app, mouseX, mouseY):
    for tower in app.placedTowers:
        # checks if 2 upgrades are visible (super monkey only has 1)
        if tower.selected and not isinstance(tower, SuperMonkey):
            if not tower.upgrade1['owned']:
                # if mouse pressed in upgrade 1 box
                if ((mouseX >= 692*app.sx and mouseX <= 828*app.sx) and
                    (mouseY >= 360*app.sy and mouseY <= 496*app.sy)):
                    # gets upgrade if user has enough money
                    if app.money >= tower.upgrade1['cost']:
                        tower.getUpgrade1(app)
                    # displays 'not enough money' caption if user cannot afford
                    else:
                        app.captionCounters['money'] = 100
            if not tower.upgrade2['owned']:
                # if mouse pressed in upgrade 2 box
                if ((mouseX >= 836*app.sx and mouseX <= 972*app.sx) and 
                    (mouseY >= 360*app.sy and mouseY <= 496*app.sy)):
                    if app.money >= tower.upgrade2['cost']:
                        tower.getUpgrade2(app)
                    else:
                        app.captionCounters['money'] = 100
        # if tower is super monkey
        elif tower.selected:
            if not tower.upgrade1['owned']:
                # if mouse is pressed in upgrade box
                if ((mouseX >= 760*app.sx and mouseX <= 896*app.sx) and
                    (mouseY >= 360*app.sy and mouseY <= 496*app.sy)):
                    if app.money >= tower.upgrade1['cost']:
                        tower.getUpgrade1(app)
                    else:
                        app.captionCounters['money'] = 100

def checkTowerSold(app, mouseX, mouseY):
    for tower in app.placedTowers:
        if tower.selected:
            # checks if mouse pressed in 'sell tower' box
            if ((mouseX >= 692*app.sx and mouseX <= 972*app.sx) and
                (mouseY >= 503*app.sy and mouseY <= 551*app.sy)):
                app.money += tower.sellPrice # adds tower value to user's money
                app.placedTowers.remove(tower)

def game_onKeyPress(app, key):
    if app.gameOver or app.wonGame or app.restart:
        restart(app)
        app.captionCounters[0] = 200 # displays round 0 caption
        
def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def main():
    runAppWithScreens(initialScreen = 'start', width = 1028, height = 633)

main()