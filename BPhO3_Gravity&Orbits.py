import pygame
import sys
import math
import random

pygame.init()
(WINDOW_WIDTH, WINDOW_HEIGHT) = 600, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ellipseScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
fadeScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
ellipseScreen.set_alpha(180)
fadeScreen.set_alpha(20)

# Masses are given in 1*10^24 kg.

# Constants -------------------------------------------------------------------------
graphSize = ((WINDOW_WIDTH**2+WINDOW_HEIGHT**2)**(1/2))/3
SUN = (1000, (WINDOW_WIDTH//30+graphSize/2, WINDOW_HEIGHT//2)) # Mass, pos.
sunVectorPos = pygame.Vector2(SUN[1])
G = 1 # Uni. Gravitational C.

# Classes ---------------------------------------------------------------------------
class planet:
    def __init__(self, m, epsilon, majorA, colour, theta): # We'll start at aphelion, so r(pixels) = semi major axis(AU) * auInPixels.
        self.mass = m * (10**24)
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
        k = (1 - epsilon)**(1/2)
        self.vel = pygame.Vector2(0, -k * v_circular)
        self.colour = colour


# Variables ---------------------------------------------------------------------------
planets = {"Mercury" : planet(0.33, 0.206, 0.387, (162, 211, 38), 2*math.pi), "Venus" : planet(4.87, 0.0067, 0.723, (211,46,57), 2*math.pi), "Earth" : planet(5.97, 0.167, 1, (135,177,211), 0)} # {"Name" : planetObject} # Three planets for the moment # later adding the ability to add planets maybe?? For the moment built-in planets
time = 0
dt = 0.001
colourRandom = (230, 87, 76)
largestOrbitPLanet = ""
auInPixels = 0
text = pygame.font.SysFont("arial", 11)
title = pygame.font.SysFont("arial", 21)
newPlanetE = 0
newPlanetA = 0
size = 1

# Subprograms -------------------------------------------------------------------------
def drawText(text, font, colour, pos, rotate):
    if not rotate:
        screen.blit(font.render(text, True, colour), pos)
    else:
        screen.blit(pygame.transform.rotate(font.render(text, True, colour), 90), pos)

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

    auInPixels = max(100, min(10000, auInPixels))
    size = max(-10, min(10, size))
    time += 100*dt

    # Screen Fading
    if 1.31 > time%2 > 1.2:
        ellipseScreen.blit(fadeScreen, (0, 0))

    
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Zooming
        elif event.type == pygame.MOUSEWHEEL:
            size += event.__dict__.get("y")/4
            size = max(-10, min(10, size))
            if size == 0:
                size = 1
            auInPixels = size*100 
            ellipseScreen.fill("black")

        # New planet generation
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1  and (WINDOW_WIDTH//30)<(pos[0])<(WINDOW_WIDTH//30+graphSize) and ((WINDOW_HEIGHT-graphSize)/2)<(pos[1])<((WINDOW_HEIGHT+graphSize)/2):
            # gonna have to check this later. abs doesn't feel right. It works for now tho

            newPlanetA = max(abs((pos[0] - SUN[1][0])/auInPixels), abs(pos[1] - SUN[1][1])/auInPixels)
            newPlanetB = min(abs((pos[0] - SUN[1][0])/auInPixels), abs(pos[1] - SUN[1][1])/auInPixels)
            newTheta = math.atan2(pos[1]-SUN[1][1], pos[0]-SUN[1][0]) # for rotation: angle bewteen sun x axis and point, then rotate to match intended pos.

            planets.update({str(len(planets)) : planet(1, newPlanetE, newPlanetA, colourRandom, newTheta)}) # creating planet object
            colourRandom = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    if (WINDOW_WIDTH//30)<(pos[0])<(WINDOW_WIDTH//30+graphSize) and ((WINDOW_HEIGHT-graphSize)/2)<(pos[1])<((WINDOW_HEIGHT+graphSize)/2):
        pygame.draw.circle(screen, colourRandom, pygame.mouse.get_pos(), 5) # Only draw follow cursor when hoverin in graph

    pygame.draw.circle(screen, "red", (SUN[1][0], SUN[1][1]), 1*size*5) # SUN

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

        if (WINDOW_WIDTH//30)<(x)<(WINDOW_WIDTH//30+graphSize) and ((WINDOW_HEIGHT-graphSize)/2)<(y)<((WINDOW_HEIGHT+graphSize)/2):
            pygame.draw.circle(screen, planets.get(i).colour, (x, y), 5)
            pygame.draw.circle(ellipseScreen, planets.get(i).colour, (x, y), 1)

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

    drawText(str(f"{len(planets)} planets generated"), title, "white", (WINDOW_WIDTH//11, WINDOW_HEIGHT//11), False)
    pygame.draw.rect(screen, "white", pygame.rect.Rect(WINDOW_WIDTH//30, (WINDOW_HEIGHT-graphSize)/2, graphSize, graphSize), 1) # graph size is in AU.
    pygame.display.update()
    clock.tick(50)



# LATER ADDITIONS
#   • Add more planets/ customizeable planet addition
#   • Axis and making the system fit on the screen dynamically
#   • Hovering over ellipses shows information about orbit in question
