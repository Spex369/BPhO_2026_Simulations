import pygame
import sys
import random
import math

pygame.init()

COULOMB = 8.99 # all charges are given in nano coulombs
WINDOW_DIMENS = 640

screen = pygame.display.set_mode((WINDOW_DIMENS, WINDOW_DIMENS))
clock = pygame.time.Clock()

charges = []
pressed = False
text = pygame.font.SysFont("arial", 10)

class pointCharge:
    def __init__(self, pos : tuple, charge : int): # all point charges will have radius of 0.
        self.pos = pos
        self.Q = charge

def fieldStrength (pos : tuple, pCharges : list[pointCharge], maxDist): # checks every tile and calculates the electric field strength experienced by the tile at pos.
    totalE = 0
    for charge in pCharges:
        deltaX = (pos[0] - charge.pos[0])/250 #
        deltaY = (pos[1] - charge.pos[1])/250
        r_squared = deltaX**2 + deltaY**2

        distance = min(maxDist, r_squared) 
        totalE += int((charge.Q/distance))
    return max(min(totalE, 99), -99)

def forces(pCharges : list[pointCharge], thisCharge): # generates an arrow to all charges.
    for charge in pCharges:
        if charge != thisCharge: # avoiding division by zero and such by not checking current charge
            distance_sqrd = ((charge.pos[0] - thisCharge.pos[0]) ** 2) + ((charge.pos[1] - thisCharge.pos[1]) ** 2)
            force = (thisCharge.Q * charge.Q * COULOMB)/(distance_sqrd)
            midPoint = ((charge.pos[0] - thisCharge.pos[0])//2 + thisCharge.pos[0], (charge.pos[1] - thisCharge.pos[1])//2 + thisCharge.pos[1])

            pygame.draw.line(screen, (90, 90, 90), thisCharge.pos, charge.pos) # line to charge
            drawText(f"{force:.2e} N", text, "green", midPoint) # gets the midpoint of the line and draws the text for force there. +ive F means repulsion.
            drawArrow(midPoint, (90, 90, 90), math.atan2((thisCharge.pos[1] - charge.pos[1]), (thisCharge.pos[0] - charge.pos[0])), ((force**2)**(1/2))/force) # lineAngle : finds the angle of the line to the horizontal (-pi to pi radians), direct : sign of force decides if arrow points towards or away.

def createCharge(pos : tuple, charge : int):
    charges.append(pointCharge(pos, charge))

def drawText(text, font, colour, pos):
    screen.blit(font.render(text, True, colour), pos)

def drawArrow(pos : tuple, color, lineAngle : float, direct):
    angleFromLine = math.pi/9 # radians
    first_branch_end_pos = (direct * 30*math.cos(lineAngle + angleFromLine) + pos[0], direct * 30*math.sin(lineAngle + angleFromLine) + pos[1])
    second_branch_end_pos = (direct * 30*math.cos(lineAngle - angleFromLine) + pos[0], direct * 30*math.sin(lineAngle - angleFromLine) + pos[1])
    pygame.draw.line(screen, color, pos, first_branch_end_pos)
    pygame.draw.line(screen, color, pos, second_branch_end_pos)

def fieldColorScale(res : int, dimensions): # seperates the screen in a series of tiles, according to the desired resolution of field and the size of the window. The center of each tile is the pixel whose electric field strength represents the tile's.
    tileSize = dimensions/(res**(1/2)) # res is the total num of tiles. The screen is a square, so res^1/2 = how many tiles per line. (Length of line)/(tiles per line) = length of one tile.
    electricFieldStrength = 0
        
    for line in range(int(res**(1/2))):
        for tile in range(int(res**(1/2))):

            centerPos = (tile*tileSize + tileSize//2, line*tileSize + tileSize//2) # center pos = tileSize/2 + (number of tiles before it in the X or in the Y)
            electricFieldStrength = fieldStrength(centerPos, charges, 5)


            #color = pygame.Color.lerp(pygame.Color(0, 0, 255, 20), pygame.Color(255, 0, 0, 20), tile/int(res**(1/2))) # interpolate between two colours, where the normal value (0 to 1) is (the tile number in the x * the length of one tile) divided by (the total length in the x).
            color = pygame.Color.lerp(pygame.Color(0, 0, 255), pygame.Color(255, 0, 0), max(min((electricFieldStrength+50), 99), 1)/100) # interpolate between two colours, where the normal value (0 to 1) is the electric potential divided by the scale maximum.
            tileRect = pygame.rect.Rect(tile*tileSize, line*tileSize, tileSize, tileSize)
            pygame.draw.rect(screen, color, tileRect)

while True:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not pressed: # generic "create only on frame where pressed".
            pressed = True
            createCharge(pygame.mouse.get_pos(), int(random.choice([random.uniform(-10, -1),random.uniform(1, 10)])))
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = False

    fieldColorScale(25600, WINDOW_DIMENS)

    for i in charges: # checks each charge
        if i.Q > 0:
            if (i.pos[0] + 2 >= pygame.mouse.get_pos()[0] >= i.pos[0] - 2) and (i.pos[1] + 2 >= pygame.mouse.get_pos()[1] >= i.pos[1] - 2):
                forces(charges, i)
                drawText(f"Charge = {i.Q} nC", text, "green", (10, 10)) # Draws text for charge in top left
                pygame.draw.circle(screen, "black", i.pos, 7)
            color = "white"
        elif i.Q < 0:
            if (i.pos[0] + 2 >= pygame.mouse.get_pos()[0] >= i.pos[0] - 2) and (i.pos[1] + 2 >= pygame.mouse.get_pos()[1] >= i.pos[1] - 2):
                forces(charges, i)
                drawText(f"Charge = {i.Q} nC", text, "green", (10, 10)) # Draws text for charge in top left
                pygame.draw.circle(screen, "white", i.pos, 5)
            color = "black"


        pygame.draw.circle(screen, color, i.pos, 4)


    pygame.display.update()
    clock.tick(60)


# Right now, nothing stops the user from creating two charges with the same pos, which can create a ZeroDivisionError at the subprogrogram force, where the distance_sqrd between 2 charges is 0.
