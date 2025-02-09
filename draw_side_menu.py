from cmu_graphics import *
from tower_classes import *
from PIL import Image

def drawMenu(app):
    menuWidth = app.width - (app.map.cols*app.cellSize)
    # draws menu background
    drawRect(app.map.cols*app.cellSize, 0, menuWidth, app.height, 
             fill = 'lightGreen')
    drawRect(app.map.cols*app.cellSize, 0, menuWidth, app.height, 
             fill = rgb(112,155,112), opacity = 70)
    
    statsLabels = ['Round:', 'Money:', 'Lives:']
    stats = [str(app.roundNum), str(app.money), str(app.lives)]
    # draws stats
    for i in range(3):
        drawLabel(statsLabels[i], app.width - 368*app.sx, (36*i + 20)*app.sy, 
                  align = 'left-top', size = 34*app.aspRat, fill = 'white', 
                  font = 'montserrat')
        drawLabel(stats[i], app.width - 48*app.sx, (36*i + 20)*app.sy, 
                  align = 'right-top', size = 34*app.aspRat, fill = 'white', 
                  font = 'montserrat')
        
    # draws towers label
    drawLabel('Build Towers', 830*app.sx, 156*app.sy, size = 34*app.aspRat, 
              fill = 'white', font = 'montserrat')
    drawLine(721*app.sx, 173*app.sy, 938*app.sx, 173*app.sy, fill = 'white', 
             lineWidth = 3.5*app.aspRat)

def drawIcons(app):
    # distance from one icon's center to next icon's center
    iconGap = app.iconSize + 10
    for i in range(len(app.towers)): # draws each tower icon
        drawImage(app.towers[i].icon, (iconGap*i + 707)*app.sx, 211*app.sy, 
                  width = app.iconSize*app.sx, height = app.iconSize*app.sy, 
                  align = 'center')

def drawUpgrades(app, tower):
    # draws background of tower info window
    drawRect(680*app.sx, 245*app.sy, 300*app.sx, 313*app.sy, 
             fill = rgb(190,218,201))
    
    # draws upgrade info (name, speed, range)
    drawLabel(tower.name, 830*app.sx, 272*app.sy, fill = 'darkGreen', 
              size = 34*app.aspRat, font = 'montserrat')
    drawLine(690*app.sx, 292*app.sy, 966*app.sx, 292*app.sy, fill = 'darkGreen', 
             lineWidth = 2*app.aspRat)
    drawLabel(f'Speed: {tower.speed}', 830*app.sx, 313*app.sy, 
              fill = 'darkGreen', size = 27*app.aspRat, font = 'montserrat')
    drawLabel(f'Range: {int(tower.range*app.aspRat)}', 830*app.sx, 340*app.sy, 
              fill = 'darkGreen', size = 27*app.aspRat, font = 'montserrat')

    # first upgrade
    # super monkey only has one upgrade, so it is drawn in the middle
    dx = 68 if isinstance(tower, SuperMonkey) else 0 
    # upgrade box is dark green if upgrade is owned
    if tower.upgrade1['owned']:
        fill = rgb(20,100,20)
        upgradeText = 'Upgrade Owned'
        textSize = 17
    # upgrade box is red if user can't afford upgrade
    elif tower.upgrade1['cost'] >= app.money:
        fill = 'darkRed'
        cost = str(tower.upgrade1['cost'])
        upgradeText = f"Can't Afford: {cost}"
        textSize = 15
    # upgrade box is light green if user can afford but doesn't have upgrade
    else:
        fill = rgb(39,136,0)
        cost = str(tower.upgrade1['cost'])
        upgradeText = f'Buy For: {cost}'
        textSize = 20
    # draw upgrade box
    drawRect((692 + dx)*app.sx, 360*app.sy, 136*app.sx, 136*app.sy, fill = fill, 
             opacity = 70)
    # draws upgrade name w/ each word on new line
    for i in range(len(tower.upgrade1['name'].split(' '))):
        word = tower.upgrade1['name'].split(' ')[i]
        drawLabel(word, (760 + dx)*app.sx, (381 + (31*i))*app.sy, 
                  fill = 'white', size = 27*app.aspRat, bold = True)
    # draws upgrade cost and ownership status
    drawLabel(upgradeText, (760 + dx)*app.sx, 476*app.sy, fill = 'white', 
              size = textSize*app.aspRat, bold = True, opacity = 80)

    # second upgrade
    if not isinstance(tower, SuperMonkey): # super monkey has no upgrade 2
        if tower.upgrade2['owned']:
            fill = rgb(20,100,20)
            upgradeText = 'Upgrade Owned'
            textSize = 17
        elif tower.upgrade2['cost'] >= app.money:
            fill = 'darkRed'
            cost = str(tower.upgrade2['cost'])
            upgradeText = f"Can't Afford: {cost}"
            textSize = 15
        else:
            fill = rgb(39,136,0)
            cost = str(tower.upgrade2['cost'])
            upgradeText = f'Buy For: {cost}'
            textSize = 20
        drawRect(836*app.sx, 360*app.sy, 136*app.sx, 136*app.sy, fill = fill, 
                 opacity = 70)
        for i in range(len(tower.upgrade2['name'].split(' '))):
            word = tower.upgrade2['name'].split(' ')[i]
            drawLabel(word, 904*app.sx, (381 + (31*i))*app.sy, fill = 'white', 
                      size = 27*app.aspRat, bold = True)
        drawLabel(upgradeText, 904*app.sx, 476*app.sy, fill = 'white', 
                  size = textSize*app.aspRat, bold = True, opacity = 80)

    # sell button
    drawRect(692*app.sx, 503*app.sy, 281*app.sx, 48*app.sy, fill = 'darkRed', 
             opacity = 70)
    drawLabel(f'Sell For: {str(tower.sellPrice)}', 830*app.sx, 524*app.sy, 
              size = 27*app.aspRat, fill = 'white', bold = True, opacity = 80)

def drawInfo(app, tower):
    # draws background of tower info window
    drawRect(680*app.sx, 245*app.sy, 302*app.sx, 313*app.sy, 
             fill = rgb(190,218,201))
    
    # draws tower info (name, cost, speed)
    drawLabel(tower.name, 830*app.sx, 272*app.sy, fill = 'darkGreen', 
              size = 34*app.aspRat, font = 'montserrat')
    drawLine(690*app.sx, 292*app.sy, 966*app.sx, 292*app.sy, fill = 'darkGreen', 
             lineWidth = 2*app.aspRat)
    drawLabel(f'Cost: {tower.cost}', 830*app.sx, 313*app.sy, fill = 'darkGreen', 
              size = 27*app.aspRat, font = 'montserrat')
    drawLabel(f'Speed: {tower.speed}', 830*app.sx, 340*app.sy, 
              fill = 'darkGreen', size = 27*app.aspRat, font = 'montserrat')
    
    # draws each line of text in tower description
    for i in range(len(tower.description)):
        drawLabel(tower.description[i], 830*app.sx, (27*i + 374)*app.sy, 
                  fill = 'darkGreen', size = 20*app.aspRat, font = 'montserrat')