import pygame
import sys
import math
import random

pygame.init()
(WINDOW_WIDTH, WINDOW_HEIGHT) = 600, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ellipseScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
fadeScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
infoScreen = pygame.surface.Surface((6*WINDOW_WIDTH//10, 6*WINDOW_HEIGHT//10))
clock = pygame.time.Clock()
ellipseScreen.set_alpha(180)
fadeScreen.set_alpha(20)

# Constants -------------------------------------------------------------------------

graphSize = ((WINDOW_WIDTH**2+WINDOW_HEIGHT**2)**(1/2))/3
SUN = (1000, (WINDOW_WIDTH//30+graphSize/2, WINDOW_HEIGHT//2)) # Mass, pos.
sunVectorPos = pygame.Vector2(SUN[1])
G = 1 # Uni. Gravitational C.

# Classes ---------------------------------------------------------------------------

class planet:
    def __init__(self, m, epsilon, majorA, colour, theta): # We'll start at aphelion, so r(pixels) = major axis(AU) * auInPixels.
        self.mass = m * (10**24)
        self.theta = theta
        self.e = epsilon
        self.a = majorA
        self.b = ((1 - (self.e**2))*(self.a**2))**(1/2)
        x, y = self.a*(1+self.e), 0
        x, y = x*pygame.Vector2(math.cos(theta), math.sin(theta)), y*pygame.Vector2(-math.sin(theta), math.cos(theta))
        self.pos = pygame.Vector2(x, y)

        # force = (G*m*M)/r^2
        # force * distance(r) / mass(m) = velocity
        # velocity = (G*M)/r
        # controlled using eccentricity using coefficient, k
        # k = (1-e)**(1/2)
        v_circular = math.sqrt(G * SUN[0] / self.a)
        k = (1 - self.e)**(1/2)
        self.vel = pygame.Vector2(0, -k * v_circular)
        self.colour = colour

class button:
    def __init__(self):
        self.buttonPressed = False

# Variables ---------------------------------------------------------------------------
planets = {"Mercury" : planet(0.33, 0.206, 0.387, (162, 211, 38), 2*math.pi), "Venus" : planet(4.87, 0.0067, 0.723, (211,46,57), 2*math.pi), "Earth" : planet(5.97, 0.167, 1, (135,177,211), 0)} # {"Name" : planetObject} # Three planets for the moment # later adding the ability to add planets maybe?? For the moment built-in planets
clearButton = button()
resetButton = button()

time = 0
dt = 0.001
colourRandom = (230, 87, 76)
largestOrbitPLanet = ""
auInPixels = 0
text = pygame.font.SysFont("arial", 11)
title = pygame.font.SysFont("arial", 21)
newPlanetA = 0
size = 1
planetToDisplayInfo = None
pos = pygame.mouse.get_pos()


# Subprograms -------------------------------------------------------------------------

def drawText(text, font, colour, pos, rotate):
    if not rotate:
        screen.blit(font.render(text, True, colour), pos)
    else:
        screen.blit(pygame.transform.rotate(font.render(text, True, colour), 90), pos)

def reset(pDict):
    for i in pDict:
        self = pDict.get(i)
        theta = self.theta
        x, y = self.a*(1+self.e), 0
        x, y = x*pygame.Vector2(math.cos(theta), math.sin(theta)), y*pygame.Vector2(-math.sin(theta), math.cos(theta))

        v_circular = math.sqrt(G * SUN[0] / self.a)
        k = (1 - self.e)**(1/2)
        pDict.get(i).vel = pygame.Vector2(0, -k * v_circular)

        pDict.get(i).pos = pygame.Vector2(x, y)

def closestPlanet(pos, pDict):
    smallestDist = 99999999
    closestPlanet = ""

    for i in pDict:
        distance = (pDict.get(i).pos[0] - pos[0]) ** 2 + (pDict.get(i).pos[1] - pos[1]) ** 2
        if distance < smallestDist:
            smallestDist = distance
            closestPlanet = i
    
    return closestPlanet

def displayInfo(planet, pDict):
    pygame.draw.rect(screen, "white", pygame.rect.Rect(graphSize + WINDOW_WIDTH//20 + WINDOW_WIDTH//30 + 40, 4*WINDOW_HEIGHT//20, 7*WINDOW_WIDTH//20, 15*WINDOW_HEIGHT//20), 5, 3)
    drawText("Name: ", title, "white", (graphSize + 3*WINDOW_WIDTH//20 + 10, 4*WINDOW_HEIGHT//20 + 20), False)
    drawText("Mass: ", title, "white", (graphSize + 3*WINDOW_WIDTH//20 + 10, 4*WINDOW_HEIGHT//20 + 51), False)
    drawText("Major axis: ", title, "white", (graphSize + 3*WINDOW_WIDTH//20 + 10, 4*WINDOW_HEIGHT//20 + 82), False)
    drawText("Minor axis: ", title, "white", (graphSize + 3*WINDOW_WIDTH//20 + 10, 4*WINDOW_HEIGHT//20 + 113), False)
    drawText("Eccentricity: ", title, "white", (graphSize + 3*WINDOW_WIDTH//20 + 10, 4*WINDOW_HEIGHT//20 + 144), False)
    drawText("Velocity: ", title, "white", (graphSize + 3*WINDOW_WIDTH//20 + 10, 4*WINDOW_HEIGHT//20 + 175), False)

    if planet:
        drawText(f"{planet}", text, "white", (graphSize + 3*WINDOW_WIDTH//20 + 140, 4*WINDOW_HEIGHT//20 + 30), False)
        drawText(f"{pDict.get(planet).mass:.2g} Kg", text, "white", (graphSize + 3*WINDOW_WIDTH//20 + 140, 4*WINDOW_HEIGHT//20 + 61), False)
        drawText(f"{pDict.get(planet).a*2:.2g} AU", text, "white", (graphSize + 3*WINDOW_WIDTH//20 + 140, 4*WINDOW_HEIGHT//20 + 92), False)
        drawText(f"{pDict.get(planet).b*2:.2g} AU", text, "white", (graphSize + 3*WINDOW_WIDTH//20 + 140, 4*WINDOW_HEIGHT//20 + 123), False)
        drawText(f"{pDict.get(planet).e:.2g}", text, "white", (graphSize + 3*WINDOW_WIDTH//20 + 140, 4*WINDOW_HEIGHT//20 + 154), False)
        drawText(f"[{pDict.get(planet).vel[0]:.2g}, {pDict.get(planet).vel[1]:.2g}]", text, "white", (graphSize + 3*WINDOW_WIDTH//20 + 140, 4*WINDOW_HEIGHT//20 + 185), False)

# Main --------------------------------------------------------------------------------
for i in planets: # largest semi major axis and semi minor axis
    largest = 0

    if (planets.get(i).b+planets.get(i).a**2)**(1/2)>largest:
        largest = (planets.get(i).b**2+planets.get(i).a**2)**(1/2)
        largestOrbitPLanet = i

# We want the largest orbit to cover 2/3 of the screen, AU in pixels is the radius,so 1/2 of 2/3 is 2/6.
# Here we are making related to both width and height by using pythag
auInPixels = (((WINDOW_WIDTH**2+WINDOW_HEIGHT**2)**(1/2))/5)/(2**(1/2))

while True:
    screen.fill("black")
    screen.blit(ellipseScreen, (0,0))
    screen.blit(infoScreen, (21*WINDOW_WIDTH//30,21*WINDOW_HEIGHT//30))
    infoScreen.fill("black")

    auInPixels = max(100, min(10000, auInPixels))
    size = max(-10, min(10, size))
    time += 100*dt

    # Screen Fading
    if 1.31 > time%2 > 1.2:
        ellipseScreen.blit(fadeScreen, (0, 0))

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        # Exit screen
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Zooming only do it if auInPx is larger than 100 when zoom is -ive
        elif event.type == pygame.MOUSEWHEEL and (10000 > auInPixels >= 100):
            if event.__dict__.get("y") < 0:
                if auInPixels > 100:
                    size += event.__dict__.get("y")/4
                    size = max(-10, min(10, size))
                    auInPixels = size*100 
                    ellipseScreen.fill("black")
            else:
                size += event.__dict__.get("y")/4
                size = max(-10, min(10, size))
                auInPixels = size*100 
                ellipseScreen.fill("black")

        # Clicking actions
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                planetToDisplayInfo = closestPlanet(pos, planets)

            # New planet generation
            elif (WINDOW_WIDTH//30)<(pos[0])<(WINDOW_WIDTH//30+graphSize) and ((WINDOW_HEIGHT-graphSize)/2)<(pos[1])<((WINDOW_HEIGHT+graphSize)/2) and event.button == 1:
            # gonna have to check this later. abs doesn't feel right. It works for now tho

                newPlanetA = max(abs((pos[0] - SUN[1][0])/auInPixels), abs(pos[1] - SUN[1][1])/auInPixels)
                newPlanetB = min(abs((pos[0] - SUN[1][0])/auInPixels), abs(pos[1] - SUN[1][1])/auInPixels)
                newPlanetE = (1-((newPlanetB**2)/(newPlanetA**2))**(1/2))
                newTheta = math.atan2(pos[1]-SUN[1][1], pos[0]-SUN[1][0]) # for rotation: angle bewteen sun x axis and point, then rotate to match intended pos.

                planets.update({str(len(planets)) : planet(1, newPlanetE, newPlanetA, colourRandom, newTheta)}) # creating planet object
                colourRandom = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            # Clear button pressed
            elif (15*WINDOW_WIDTH//20 < pos[0] < 18*WINDOW_WIDTH//20) and (3*WINDOW_HEIGHT//20 > pos[1] > 2*WINDOW_HEIGHT//20) and event.button == 1:
                clearButton.buttonPressed = True
                planetToDisplayInfo = None

            # Reset button pressed
            elif (11*WINDOW_WIDTH//20 < pos[0] < 14*WINDOW_WIDTH//20) and (3*WINDOW_HEIGHT//20 > pos[1] > 2*WINDOW_HEIGHT//20) and event.button == 1:
                resetButton.buttonPressed = True
                planetToDisplayInfo = None

        # Clicking actions button up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            # Clear button released
            if (15*WINDOW_WIDTH//20 < pos[0] < 18*WINDOW_WIDTH//20) and (3*WINDOW_HEIGHT//20 > pos[1] > 2*WINDOW_HEIGHT//20):
                clearButton.buttonPressed = False
                ellipseScreen.fill("black")
                planets = {}

            # Reset button released
            elif (11*WINDOW_WIDTH//20 < pos[0] < 14*WINDOW_WIDTH//20) and (3*WINDOW_HEIGHT//20 > pos[1] > 2*WINDOW_HEIGHT//20):
                ellipseScreen.fill("black")
                resetButton.buttonPressed = False
                time = 0
                reset(planets)


    # Drawing buttons ----------
    # Clear button
    pygame.draw.rect(screen, (60, 60, 60), pygame.rect.Rect(15*WINDOW_WIDTH//20-1, 2*WINDOW_HEIGHT//20, 3*WINDOW_WIDTH//20+2, WINDOW_HEIGHT//20),border_radius=3)
    if clearButton.buttonPressed:
        pygame.draw.rect(screen, (100, 100, 100), pygame.rect.Rect(15*WINDOW_WIDTH//20, 2*WINDOW_HEIGHT//20-2, 3*WINDOW_WIDTH//20, WINDOW_HEIGHT//20), border_radius=3)
        drawText("Clear", title, "white", (31*WINDOW_WIDTH//40, 2*WINDOW_HEIGHT//20-2), False)
    else:
        pygame.draw.rect(screen, "grey", pygame.rect.Rect(15*WINDOW_WIDTH//20, 2*WINDOW_HEIGHT//20-5, 3*WINDOW_WIDTH//20, WINDOW_HEIGHT//20), border_radius=3)
        drawText("Clear", title, "white", (31*WINDOW_WIDTH//40, 2*WINDOW_HEIGHT//20-5), False)
    
    # Reset Button
    pygame.draw.rect(screen, (60, 60, 60), pygame.rect.Rect(11*WINDOW_WIDTH//20-1, 2*WINDOW_HEIGHT//20, 3*WINDOW_WIDTH//20+2, WINDOW_HEIGHT//20),border_radius=3)
    if resetButton.buttonPressed:
        pygame.draw.rect(screen, (100, 100, 100), pygame.rect.Rect(11*WINDOW_WIDTH//20, 2*WINDOW_HEIGHT//20-2, 3*WINDOW_WIDTH//20, WINDOW_HEIGHT//20), border_radius=3)
        drawText("Reset", title, "white", (23*WINDOW_WIDTH//40, 2*WINDOW_HEIGHT//20-2), False)
    else:
        pygame.draw.rect(screen, "grey", pygame.rect.Rect(11*WINDOW_WIDTH//20, 2*WINDOW_HEIGHT//20-5, 3*WINDOW_WIDTH//20, WINDOW_HEIGHT//20), border_radius=3)
        drawText("Reset", title, "white", (23*WINDOW_WIDTH//40, 2*WINDOW_HEIGHT//20-5), False)
    # -------------------------


    # cursorPlanet
    if (WINDOW_WIDTH//30)<(pos[0])<(WINDOW_WIDTH//30+graphSize) and ((WINDOW_HEIGHT-graphSize)/2)<(pos[1])<((WINDOW_HEIGHT+graphSize)/2):
        pygame.draw.circle(screen, colourRandom, pygame.mouse.get_pos(), 5) # Only draw follow cursor when hoverin in graph

    # Sun
    pygame.draw.circle(screen, "red", (SUN[1][0], SUN[1][1]), auInPixels*0.1)

    # Planet drawings
    for i in planets:
        # every frame we increase the velocity in the direction of the sun by the force due to gravity multiplied by the mass of the planet (acceleration)
        # every frame we add said velocity to the planet's position vectors.
        planetToStarVector = - planets.get(i).pos
        r = planetToStarVector.length()
        rDirection = planetToStarVector.normalize()

        accelerationDirection = (((1000) / (r ** 2)) * rDirection)
        planets.get(i).vel += accelerationDirection * dt
        planets.get(i).pos += planets.get(i).vel * dt
        x = SUN[1][0] + planets.get(i).pos.x * auInPixels
        y = SUN[1][1] + planets.get(i).pos.y * auInPixels
        displayX = WINDOW_WIDTH//10 + (planets.get(i).pos.x * 60)
        displayY = WINDOW_HEIGHT//10 + (planets.get(i).pos.y * 60)

        if (WINDOW_WIDTH//30)<(x)<(WINDOW_WIDTH//30 + graphSize) and ((WINDOW_HEIGHT-graphSize)/2)<(y)<((WINDOW_HEIGHT+graphSize)/2):
            if i == planetToDisplayInfo:
                brighterColor = (min(planets.get(i).colour[0]+120, 255), min(planets.get(i).colour[1]+120, 255), min(planets.get(i).colour[2]+120, 255))
                pygame.draw.circle(infoScreen, planets.get(i).colour, (displayX, displayY), 5)
                pygame.draw.circle(screen, brighterColor, (x, y), 6)
                pygame.draw.circle(ellipseScreen, brighterColor, (x, y), 3)
            pygame.draw.circle(screen, planets.get(i).colour, (x, y), 5)
            pygame.draw.circle(ellipseScreen, planets.get(i).colour, (x, y), 1)
        
        # Here were gonna make it so a secondary orbit is created inside the info displayer


    # Graphing
    for i in range(0, int(graphSize/2), int(auInPixels/5)):
        pygame.draw.line(screen, "white", (i + SUN[1][0], (WINDOW_HEIGHT+graphSize)/2), (i + SUN[1][0], (WINDOW_HEIGHT+graphSize)/2+10), 1)
        pygame.draw.line(screen, "white", (SUN[1][0] - i, (WINDOW_HEIGHT+graphSize)/2), (SUN[1][0] - i, (WINDOW_HEIGHT+graphSize)/2+10), 1)
        pygame.draw.line(screen, "white", (WINDOW_WIDTH//30 + graphSize, i + SUN[1][1]), (WINDOW_WIDTH//30 + 10 + graphSize, i + SUN[1][1]), 1)
        pygame.draw.line(screen, "white", (WINDOW_WIDTH//30 + graphSize, SUN[1][1] - i), (WINDOW_WIDTH//30 + 10 + graphSize, SUN[1][1] - i), 1)
        drawText(str(f"{(i)/auInPixels:.2f} AU"), text, "white", (i + SUN[1][0] - 5, (WINDOW_HEIGHT+graphSize)/2 + 20), True)
        drawText(str(f"{(i)/auInPixels:.2f} AU"), text, "white", (SUN[1][0] - i - 5, (WINDOW_HEIGHT+graphSize)/2 + 20), True)
        drawText(str(f"{(i)/auInPixels:.2f} AU"), text, "white", (WINDOW_WIDTH//30 + 20 + graphSize, i + SUN[1][1] - 5), False)
        drawText(str(f"{(i)/auInPixels:.2f} AU"), text, "white", (WINDOW_WIDTH//30 + 20 + graphSize, SUN[1][1] - i - 5), False)

    # Displaying planet info
    pygame.draw.rect(screen, "white", pygame.rect.Rect(WINDOW_WIDTH//30, (WINDOW_HEIGHT-graphSize)/2, graphSize, graphSize), 1)
    drawText(str(f"{len(planets)} planets generated"), title, "white", (WINDOW_WIDTH//11, 2*WINDOW_HEIGHT//20), False)
    displayInfo(planetToDisplayInfo, planets)
    pygame.display.update()
    clock.tick(50)



# LATER ADDITIONS
#   • Axis and making the system fit on the screen dynamically
#   • Hovering over ellipses shows information about orbit in question



# REDESIGN -------------
#   • Create design logic, class NODE
#   • main runs the parent instance
#   • The parent instance handles children
#   • Each child recursively handles children and so on
#   • Shared states between nodes are passed through parents
#   • Each child is a class with different functions