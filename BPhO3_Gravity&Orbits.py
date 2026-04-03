import pygame
import sys
import math

pygame.init()
(WINDOW_WIDTH, WINDOW_HEIGHT) = 500, 500
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ellipseScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
ellipseScreen.set_alpha(150)

# Masses are given in 1*10^24 kg.

# Constants -------------------------------------------------------------------------
SUN = (1.989*(10**30), (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)) # Mass, pos.
G = 6.67*(10**-11) # Uni. Gravitational C. All is given in 1*10^24 so divided by 10^24.

# Classes ---------------------------------------------------------------------------
class planet:
    def __init__(self, m, epsilon, majorA, colour): # epsilon = eccentricity, majorA = semi major axis in AU.
        self.mass = m * (10**24)
        self.e = epsilon
        self.a = majorA
        self.colour = colour
        
    def r(self, theta):
        return (self.a * (1 - self.e**2)) / (1 - self.e*math.cos(theta))

# Variables ---------------------------------------------------------------------------
planets = {"Mercury" : planet(0.33, 0.206, 0.387, (162,211, 38)), "Venus" : planet(4.87, 0.0067, 0.723, (211,46,57)), "Earth" : planet(5.97, 0.0167, 1, (135,177,211))} # {"Name" : planetObject} # Three planets for the moment # later adding the ability to add planets maybe?? For the moment built-in planets
theta = 0

for i in planets: # largest semi major axis
    largest = 0
    largest = max(planets.get(i).a, largest)

# We want the largest orbit to cover 4/5 of the screen, AU in pixels is the radius, 1/2 of 4/5 is 2/5.
auInPixels = (2*WINDOW_WIDTH//5)/largest
    

# Ellipses -------------------------------------------------------------------------

for i in planets:
    colour = planets.get(i).colour
    for j in range(360):
        r = planets.get(i).r(math.radians(j)) * auInPixels
        nextR = planets.get(i).r(math.radians(j+1)) * auInPixels
        pygame.draw.line(ellipseScreen, colour, (SUN[1][0] - r*math.cos(math.radians(j)), SUN[1][1] - r*math.sin(math.radians(j))), (SUN[1][0] - r*math.cos(math.radians(j+1)), SUN[1][1] - r*math.sin(math.radians(j+1))), 1)
# Main --------------------------------------------------------------------------------

while True:
    screen.fill("black")
    screen.blit(ellipseScreen, (0,0))

    theta += 0.01
    
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.draw.circle(screen, "red", (SUN[1][0], SUN[1][1]), 10)

    for i in planets:
        r = planets.get(i).r(theta) * auInPixels
        pygame.draw.circle(screen, planets.get(i).colour, (SUN[1][0] - r*math.cos(theta), SUN[1][1] - r*math.sin(theta)), 5)

    pygame.display.update()
    clock.tick(50) # smooth and CPU friendly. DO NOT MODIFY.



# LATER ADDITIONS
#   • Add more planets/ customizeable planet addition
#   • Moving planets using orbital period rather than angle, so angular speed is relative
#   • Axis and making the system fit on the screen dynamically