import pygame
import sys
import math

pygame.init()
(WINDOW_WIDTH, WINDOW_HEIGHT) = 600, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ellipseScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
ellipseScreen.set_alpha(100)

# Masses are given in 1*10^24 kg.

# Constants -------------------------------------------------------------------------
SUN = (1000, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)) # Mass, pos.
sunVectorPos = pygame.Vector2(SUN[1])
G = 1 # Uni. Gravitational C.

# Classes ---------------------------------------------------------------------------
class planet:
    def __init__(self, m, epsilon, majorA, colour): # We'll start at aphelion, so r(pixels) = semi major axis(AU) * auInPixels.
        self.mass = m * (10**24)
        self.e = epsilon
        self.a = majorA
        self.pos = pygame.Vector2(self.a, 0) # testing with AU and then drawing in pixels

        # force = (G*m*M)/r^2
        # force * distance(r) / mass(m) = velocity
        # velocity = (G*M)/r
        # controlled using eccentricity using coefficient, k
        # k = (1-e)**(1/2)
        v_circular = math.sqrt(G * SUN[0] / self.a)
        k = math.sqrt(1 - epsilon)
        self.vel = pygame.Vector2(0, -k * v_circular)
        self.colour = colour

# Variables ---------------------------------------------------------------------------
planets = {"Mercury" : planet(0.33, 0.206, 0.387, (162, 211, 38)), "Venus" : planet(4.87, 0.67, 0.723, (211,46,57)), "Earth" : planet(5.97, 0.0167, 1, (135,177,211))} # {"Name" : planetObject} # Three planets for the moment # later adding the ability to add planets maybe?? For the moment built-in planets
time = 0
dt = 0.001

# Have to fix this later, because now we use force of gravity to find position
font = pygame.font.SysFont("arial", 14)

for i in planets: # largest semi major axis and semi minor axis
    b_squared = (1 - (planets.get(i).e**2))*(planets.get(i).a**2)
    largest = 0

    if (b_squared+planets.get(i).a**2)**(1/2)>largest:
        largest = (b_squared+planets.get(i).a**2)**(1/2)
        largestOrbitPLanet = i

# We want the largest orbit to cover 2/3 of the screen, AU in pixels is the radius,so 1/2 of 2/3 is 2/6.
# Here we are making related to both width and height by using pythag
auInPixels = (((WINDOW_WIDTH**2+WINDOW_HEIGHT**2)**(1/2))/3)/(largest)
graphSize = (planets.get(largestOrbitPLanet).a*2, b_squared**(1/2)*2) # length and width of graph is 2a and 2b respectively. Staying consistent even if not multiplying is a shortcut.

# Ellipses ----------------------------------------------------------------------------

#for i in planets: # drawing ellipses once
#    colour = planets.get(i).colour
#    for j in range(360):
#        r = planets.get(i).r(math.radians(j)) * auInPixels
#        nextR = planets.get(i).r(math.radians(j+1)) * auInPixels
#        pygame.draw.line(ellipseScreen, colour, (SUN[1][0] - r*math.cos(math.radians(j)), SUN[1][1] - r*math.sin(math.radians(j))), (SUN[1][0] - r*math.cos(math.radians(j+1)), SUN[1][1] - r*math.sin(math.radians(j+1))), 3)

# Subprograms -------------------------------------------------------------------------
def drawText(text, font, colour, pos):
    screen.blit(font.render(text, True, colour), pos)

# Main --------------------------------------------------------------------------------

while True:
    screen.fill("black")
    screen.blit(ellipseScreen, (0,0))

    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.draw.circle(screen, "red", (SUN[1][0], SUN[1][1]), 10)

    print(planets.get("Mercury").a)
    print(planets.get("Venus").a)
    print(planets.get("Earth").a)
    print("1 au = ", f"{auInPixels:.2f}", " pixels")
    for i in planets:
        print("true pos = ", planets.get(i).pos)
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

        pygame.draw.circle(screen, planets.get(i).colour, (x, y), 5)
        pygame.draw.circle(ellipseScreen, planets.get(i).colour, (x, y), 1)

    pygame.draw.rect(screen, "white", pygame.rect.Rect(SUN[1][0]-graphSize[0]*auInPixels//2, SUN[1][1]-graphSize[1]*auInPixels//2, graphSize[0]*auInPixels, graphSize[1]*auInPixels), 1) # graph size is in AU.
    pygame.display.update()
    clock.tick(50)



# LATER ADDITIONS
#   • Add more planets/ customizeable planet addition
#   • Axis and making the system fit on the screen dynamically
#   • Hovering over ellipses shows information about orbit in question


# I didn't know whether to use Force or dA/dT, so I'm going to do both in time as practice for intuition.
# This one is going to be Force. I had to use Ai for this, but no vibe coding. Just questions asked in order to understand the physics behind it all.

# I learned how to use pygame vectors today!! Thanks GPT, sir!
# No longer using polar coords, because the position no longer needs to be related to the sun. Now the position changes in relation to the sun using vectors, so no worries about that.
# I even get apsidal precession!!