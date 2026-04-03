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
        self.Period = ((4*(math.pi**2)*(self.a**3))/(G*(self.mass+SUN[0])))**1/2 # Years?
        self.angularV = (2*math.pi)/self.Period
        
    def r(self, theta):
        return (self.a * (1 - self.e**2)) / (1 - self.e*math.cos(theta))

# Variables ---------------------------------------------------------------------------
planets = {"Mercury" : planet(0.33, 0.206, 0.387, (162,211, 38)), "Venus" : planet(4.87, 0.0067, 0.723, (211,46,57)), "Earth" : planet(5.97, 0.0167, 1, (135,177,211))} # {"Name" : planetObject} # Three planets for the moment # later adding the ability to add planets maybe?? For the moment built-in planets
time = 0
dt = 1
# 1 year = time for earth to perform 1 orbit.
# What is theta for 1 frame?- angularV.
# Number of orbits in 1 frame? angularV/(2*pi).
# How many frames for 1 orbit? 1 frame/(angularV/(2*pi))
# Hence (2*pi)/angularV = interval of 1 year.
# Frames after 1 year = (2*pi)/(4.2229121604103004e+19)
framesAfterYear = (2*math.pi)/(4.2229121604103004e+19)
dt = framesAfterYear/1000

for i in planets: # largest semi major axis
    largest = 0
    largest = max(planets.get(i).a, largest)

# We want the largest orbit to cover 4/8 of the screen, AU in pixels is the radius, 1/2 of 4/8 is 2/8.
auInPixels = (2*WINDOW_WIDTH//8)/largest
    

# Ellipses -------------------------------------------------------------------------

for i in planets:
    colour = planets.get(i).colour
    for j in range(360):
        r = planets.get(i).r(math.radians(j)) * auInPixels
        nextR = planets.get(i).r(math.radians(j+1)) * auInPixels
        pygame.draw.line(ellipseScreen, colour, (SUN[1][0] - r*math.cos(math.radians(j)), SUN[1][1] - r*math.sin(math.radians(j))), (SUN[1][0] - r*math.cos(math.radians(j+1)), SUN[1][1] - r*math.sin(math.radians(j+1))), 3)
# Main --------------------------------------------------------------------------------

while True:
    screen.fill("black")
    screen.blit(ellipseScreen, (0,0))
    time += dt

    print("t = " + str(time/(1000*dt)) + " Years")
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.circle(screen, "red", (SUN[1][0], SUN[1][1]), 10)

    for i in planets:
        theta = planets.get(i).angularV * time
        r = planets.get(i).r(theta) * auInPixels
        pygame.draw.circle(screen, planets.get(i).colour, (SUN[1][0] - r*math.cos(theta), SUN[1][1] - r*math.sin(theta)), 5)

    pygame.display.update()
    clock.tick(50) # smooth and CPU friendly. DO NOT MODIFY.



# LATER ADDITIONS
#   • Add more planets/ customizeable planet addition
#   • Axis and making the system fit on the screen dynamically