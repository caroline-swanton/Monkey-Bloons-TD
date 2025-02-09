from cmu_graphics import *
from PIL import Image

# draws starting screen
def start_redrawAll(app):
    drawImage(app.startingScreen, 0, 0, width = app.width, height = app.height,
              align = 'left-top')
    # draws 'start' button
    drawRect(app.width/2, app.height - 100*app.sy, 300*app.sx, 100*app.sy, 
             fill = rgb(16, 52, 105), align = 'center', border = 'white', 
             borderWidth = 3*app.aspRat)
    drawLabel('START', app.width/2, app.height - 100*app.sy, fill = 'white', 
              size = 40*app.aspRat, bold = True)

def start_onStep(app):
    # determines if screen dimensions have changed
    if (
        not almostEqual(app.sx, app.width/1028) or
        not almostEqual(app.sy, app.height/633)
    ):
        # adjusts scaling based on screen size
        app.sx = app.width/1028
        app.sy = app.height/633
        app.aspRat = min(app.sx, app.sy)
        app.cellSize = app.height/app.map.rows

def start_onMousePress(app, mouseX, mouseY):
    # if 'start' button is pressed
    if ((app.width/2 - 150*app.sx <= mouseX <= app.width/2 + 150*app.sx) and
        (app.height - 150*app.sy <= mouseY <= app.height - 50*app.sy)):
        setActiveScreen("game")
        app.captionCounters[0] = 200 # displays round 0 caption