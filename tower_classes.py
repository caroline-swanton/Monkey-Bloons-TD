from cmu_graphics import *
import math

class Tower:
    def __init__(self):
        self.spriteIndex = 0 # curr frame of sprite
        self.placing = False # placing tower on map
        self.infoShowing = False # hovering over tower icon
        self.legalPlacement = False # True if tower is placeable
        self.pauseCounter = 0 # pauses sprite after one loop
        self.selected = False # displays range and upgrade options if selected
    
    # finds balloons in range of tower and balloon closest to end in range
    def balloonsPopped(self, app):
        towerx, towery = self.position
        balloonsInRange = set() # stores balloons in range of tower
        for balloon in app.balloons:
            ballooncx = balloon.left + balloon.width/2 # balloon center x
            ballooncy = balloon.top + balloon.height/2 # balloon center y
            if (distance(ballooncx, ballooncy, towerx, towery) <= 
                self.range*app.aspRat):
                balloonsInRange.add(balloon)
        # finds first balloon in range
        farthestDistanceTravelled = 0
        poppedBalloon = None
        for balloon in balloonsInRange:
            if balloon.distanceTravelled > farthestDistanceTravelled:
                farthestDistanceTravelled = balloon.distanceTravelled
                poppedBalloon = balloon
        return poppedBalloon, balloonsInRange
    
    # checks if balloon is close enough to another popped balloon to be pierced
    # (only for dart monkey and super monkey)
    def pierceBalloons(self, balloonsInRange, poppedBalloon):
        poppedx, poppedy = poppedBalloon.left, poppedBalloon.top
        piercedBalloons = {poppedBalloon}
        for balloon in balloonsInRange:
            balloonx, balloony = balloon.left, balloon.top
            if ((abs(balloonx - poppedx) < balloon.width and
                 abs(balloony - poppedy) < balloon.height)):
                piercedBalloons.add(balloon)
        return piercedBalloons
    
    # finds cell when mouse is clicked while placing tower
    def getPlacementCell(self, app, x, y):
        row = math.floor(y / app.cellSize)
        col = math.floor(x / app.cellSize)
        return(row, col)
    
    # determines how tower rotates towards balloon it is shooting
    # (only for dart, bomb, and super towers)
    def rotate(self, poppedBalloon):
        towerx, towery = self.position
        balloonx = poppedBalloon.left + poppedBalloon.width/2
        balloony = poppedBalloon.top + poppedBalloon.height/2
        hypSide = distance(towerx, towery, balloonx, balloony)
        oppSide = balloony - towery
        if balloonx < towerx:
            self.rotateAngle = -math.degrees(math.pi - math.acos(oppSide/hypSide))
        else:
            self.rotateAngle = math.degrees(math.pi/2 + math.asin(oppSide/hypSide))

class DartTower(Tower):
    def __init__(self, app, position):
        Tower.__init__(self)
        self.name = 'Dart Tower'
        self.url = app.dartTowerURL
        self.icon = app.dartIconURL

        # list of sprite frames
        self.loadSprite = loadSpritePilImages(self.url, 9, 200, 800)
        self.sprite = [CMUImage(pilImage) for pilImage in self.loadSprite]

        self.width = 60 # width in px of tower
        self.height = 230 # height in px of tower
        # stores (cx, cy) of tower; position is None if tower is not placed yet
        self.position = position
        self.rotateAngle = 0 # stores tower angle
        self.range = 140 # area in px where tower can shoot balloons
        self.pauseDuration = 15 # steps tower must wait before shooting again
        self.cost = 250
        self.sellPrice = 200
        self.speed = 'Fast'
        self.description =  ['Shoots a single dart.', 
                             'Can upgrade to piercing darts',
                             'and long range darts.']
        # stores tower upgrade attributes
        self.upgrade1 = {'name': 'Piercing Darts', 'cost': 210, 'worth': 168,
                         'owned': False}
        self.upgrade2 = {'name': 'Long Range Darts', 'cost': 100, 'worth': 80,
                         'owned': False}
        
    def shoot(self, app):
        poppedBalloon, balloonsInRange = Tower.balloonsPopped(self, app)
        # frames continue to switch if animation is not finished
        if poppedBalloon != None or self.spriteIndex != 0:
            if self.pauseCounter > 0: # sprite is paused
                self.pauseCounter -= 1
            else:
                # jump to next frame
                self.spriteIndex = (self.spriteIndex + 1) % len(self.sprite)
                if poppedBalloon != None:
                    if self.spriteIndex == 3: # rotates on 3rd frame if shooting
                        self.rotate(poppedBalloon)
                    elif self.spriteIndex == 6: # pops balloon on 6th frame
                        # dart towers cannot pop frozen balloons
                        # pops only first balloon if piercing upgrade not owned
                        if (not self.upgrade1['owned'] and 
                            poppedBalloon.freezeDuration == 0):
                            poppedBalloon.url = app.balloonurls['popped']
                        else:
                            # finds which balloons were pieced
                            piercedBalloons = Tower.pierceBalloons(self, 
                                                                    balloonsInRange,
                                                                    poppedBalloon)
                            for balloon in piercedBalloons:
                                if balloon.freezeDuration == 0:
                                    balloon.url = app.balloonurls['popped']
                # sprite pauses after one full loop
                if self.spriteIndex == 0:
                    self.pauseCounter = self.pauseDuration

    # piercing upgrade
    def getUpgrade1(self, app):
        self.upgrade1['owned'] = True
        self.sellPrice += self.upgrade1['worth']
        app.money -= self.upgrade1['cost']
           
    # range upgrade
    def getUpgrade2(self, app):
        self.upgrade2['owned'] = True
        self.range += 20
        self.sellPrice += self.upgrade2['worth']
        app.money -= self.upgrade2['cost']

class TackTower(Tower):
    def __init__(self, app, position):
        Tower.__init__(self)
        self.name = 'Tack Tower'
        self.url =  app.tackTowerURL
        self.icon = app.tackIconURL

        self.loadSprite = loadSpritePilImages(self.url, 5, 702, 700)
        self.sprite = [CMUImage(pilImage) for pilImage in self.loadSprite]

        self.width = 210
        self.height = 210
        self.position = position
        self.rotateAngle = 0 # note: tack tower does not rotate
        self.range = 110
        self.pauseDuration = 40
        self.cost =  400
        self.sellPrice = 320
        self.speed =  'Medium'
        self.description = ['Shoots volley of tacks',
                            'that hits every bloon in range.',
                            'Can upgrade its shoot speed',
                            'and its range.']
        self.upgrade1 = {'name': 'Faster Shooting', 'cost': 250, 'worth': 200,
                         'owned': False}
        self.upgrade2 = {'name': 'Extra Range Tacks', 'cost': 150, 'worth': 120,
                         'owned': False}
        
    def shoot(self, app):
        poppedBalloon, balloonsInRange = Tower.balloonsPopped(self, app)
        if poppedBalloon != None or self.spriteIndex != 0:
            if self.pauseCounter > 0:
                self.pauseCounter -= 1
            else:
                self.spriteIndex = (self.spriteIndex + 1) % len(self.sprite)
                if poppedBalloon != None:
                    if self.spriteIndex == 3: # shoots on 3rd frame
                        for balloon in balloonsInRange:
                            # tacks cannot pop frozen balloons
                            if balloon.freezeDuration == 0:
                                balloon.url = app.balloonurls['popped']
                if self.spriteIndex == 0:
                    self.pauseCounter = self.pauseDuration

    # faster shooting upgrade
    def getUpgrade1(self, app):
        self.upgrade1['owned'] = True
        self.pauseDuration -= 7
        self.sellPrice += self.upgrade1['worth']
        app.money -= self.upgrade1['cost']

    # range upgrade
    def getUpgrade2(self, app):
        self.upgrade2['owned'] = True
        self.range += 20
        self.sellPrice += self.upgrade2['worth']
        app.money -= self.upgrade2['cost']
        
class IceTower(Tower):
    def __init__(self, app, position):
        Tower.__init__(self)
        self.name = 'Ice Tower'
        self.url =  app.iceTowerURL
        self.icon = app.iceIconURL

        self.loadSprite = loadSpritePilImages(self.url, 5, 500, 500)
        self.sprite = [CMUImage(pilImage) for pilImage in self.loadSprite]

        self.width = 175
        self.height = 175
        self.position = position
        self.rotateAngle = 0
        self.range = 100
        self.pauseDuration = 80
        self.freezeDuration = 50 # how many steps balloons stay frozen
        self.cost =  850
        self.sellPrice = 680
        self.speed =  'Slow'
        self.description = ['Freezes nearby bloons.',
                            'Frozen bloons are immune',
                            'to darts and tacks, but',
                            'bombs will destroy them.',
                            'Can upgrade to increased',
                            'freeze time and larger',
                            'freeze radius.']
        self.upgrade1 = {'name': 'Long Freeze Time', 'cost': 450, 'worth': 340,
                         'owned': False}
        self.upgrade2 = {'name': 'Wide Freeze Radius', 'cost': 300, 'worth': 240,
                         'owned': False}

    def shoot(self, app):
            poppedBalloon, balloonsInRange = Tower.balloonsPopped(self, app)
            if poppedBalloon != None or self.spriteIndex != 0:
                if self.pauseCounter > 0:
                    self.pauseCounter -= 1
                else:
                    self.spriteIndex = (self.spriteIndex + 1) % len(self.sprite)
                    if poppedBalloon != None:
                        if self.spriteIndex == 4: # freezes balloons on 4th frame
                            # ice tower hits all balloons in range
                            for balloon in balloonsInRange:
                                balloon.freezeDuration = self.freezeDuration
                    if self.spriteIndex == 0:
                        self.pauseCounter = self.pauseDuration

    # freeze time upgrade
    def getUpgrade1(self, app):
        self.upgrade1['owned'] = True
        self.freezeDuration += 20
        self.sellPrice += self.upgrade1['worth']
        app.money -= self.upgrade1['cost']

    # range upgrade
    def getUpgrade2(self, app):
        self.upgrade2['owned'] = True
        self.range += 20
        self.sellPrice += self.upgrade2['worth']
        app.money -= self.upgrade2['cost']

class BombTower(Tower):
    def __init__(self, app, position):
        Tower.__init__(self)
        self.name = 'Bomb Tower'
        self.url =  app.bombTowerURL
        self.icon = app.bombIconURL

        self.loadSprite = loadSpritePilImages(self.url, 9, 600, 1200)
        self.sprite = [CMUImage(pilImage) for pilImage in self.loadSprite]

        self.width = 220
        self.height = 400
        self.position = position
        self.rotateAngle = 0
        self.range = 140
        self.pauseDuration = 50
        self.cost =  900
        self.sellPrice = 720
        self.blastRadius = 50 # will pop all balloons in this range
        self.speed =  'Medium'
        self.description = ['Launches a bomb that',
                            'explodes on impact.',
                            'Bombs blast through all',
                            'layers of bloons.',
                            'Can upgrade to bigger',
                            'bombs and bigger range.']
        self.upgrade1 = {'name': 'Bigger Bombs', 'cost': 650, 'worth': 520,
                         'owned': False}
        self.upgrade2 = {'name': 'Extra Range Bombs', 'cost': 250, 'worth': 200,
                         'owned': False}
        
    def shoot(self, app):
        poppedBalloon, balloonsInRange = Tower.balloonsPopped(self, app)
        if poppedBalloon != None or self.spriteIndex != 0:
            if self.pauseCounter > 0:
                self.pauseCounter -= 1
            else:
                self.spriteIndex = (self.spriteIndex + 1) % len(self.sprite)
                if poppedBalloon != None:
                    if self.spriteIndex == 1: # rotates on 1st frane
                        self.rotate(poppedBalloon)
                    # finds balloons in blast radius
                    poppedBalloons = self.balloonsExploded(app, poppedBalloon, 
                                                           balloonsInRange)
                    if self.spriteIndex == 5: # pops balloons on 5th frame
                            # plays cannon sound
                            app.cannonSound.play(restart = True)
                            for balloon in poppedBalloons:
                                balloon.url = app.balloonurls['popped']
                                # blasts through all layers of balloon
                                balloon.color = 'red'
                if self.spriteIndex == 0:
                    self.pauseCounter = self.pauseDuration

    def balloonsExploded(self, app, poppedBalloon, balloonsInRange):
        poppedx, poppedy = poppedBalloon.left, poppedBalloon.top
        explodedBalloons = {poppedBalloon}
        for balloon in balloonsInRange:
            balloonx, balloony = balloon.left, balloon.top
            if ((abs(balloonx - poppedx) < balloon.width + 
                 self.blastRadius*app.aspRat and
                 abs(balloony - poppedy) < balloon.height + 
                 self.blastRadius*app.aspRat)):
                explodedBalloons.add(balloon)
        return explodedBalloons

    # blast radius upgrade
    def getUpgrade1(self, app):
        self.upgrade1['owned'] = True
        self.blastRadius += 20
        self.sellPrice += self.upgrade1['worth']
        app.money -= self.upgrade1['cost']

    # range upgrade
    def getUpgrade2(self, app):
        self.upgrade2['owned'] = True
        self.range += 20
        self.sellPrice += self.upgrade2['worth']
        app.money -= self.upgrade2['cost']
        
class SuperMonkey(Tower):
    def __init__(self, app, position):
        Tower.__init__(self)
        self.name = 'Super Monkey'
        self.url =  app.superMonkeyURL
        self.icon = app.superIconURL

        self.loadSprite = loadSpritePilImages(self.url, 7, 200, 800)
        self.sprite = [CMUImage(pilImage) for pilImage in self.loadSprite]

        self.width = 65
        self.height = 240
        self.position = position
        self.rotateAngle = 0
        self.range = 140
        self.pauseDuration = 1
        self.cost =  4000
        self.sellPrice = 3200
        self.speed =  'Hypersonic'
        self.description = ['Super monkey shoots',
                            'a continuous stream of',
                            'darts and can pierce through',
                            'even the fastest and',
                            'most stubborn bloons.']
        self.upgrade1 = {'name': 'Epic Range', 'cost': 2400, 'worth': 2200,
                         'owned': False}

    def shoot(self, app):
        poppedBalloon, balloonsInRange = Tower.balloonsPopped(self, app)
        if poppedBalloon != None or self.spriteIndex != 0:
            if self.pauseCounter > 0:
                self.pauseCounter -= 1
            else:
                self.spriteIndex = (self.spriteIndex + 1) % len(self.sprite)
                if poppedBalloon != None:
                    if self.spriteIndex == 2: # rotates on 2nd frame
                        self.rotate(poppedBalloon)
                    elif self.spriteIndex == 4: # pops balloon on 4th frame
                        # always has piercing ability
                        piercedBalloons = Tower.pierceBalloons(self, 
                                                               balloonsInRange,
                                                               poppedBalloon)
                        for balloon in piercedBalloons:
                            # cannot pop frozen balloons
                            if balloon.freezeDuration == 0:
                                balloon.url = app.balloonurls['popped']
                if self.spriteIndex == 0:
                    self.pauseCounter = self.pauseDuration

    # range upgrade
    def getUpgrade1(self, app):
        self.upgrade1['owned'] = True
        self.range += 40
        self.sellPrice += self.upgrade1['worth']
        app.money -= self.upgrade1['cost']
    
# configured from sprite demo
def loadSpritePilImages(url, frames, frameWidth, frameHeight):
    spritePilImages = []
    for i in range(frames):
        spriteImage = url.crop((frameWidth*i, 0, frameWidth*(i + 1), frameHeight))
        spritePilImages.append(spriteImage)
    return spritePilImages