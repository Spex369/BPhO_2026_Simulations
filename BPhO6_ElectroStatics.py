import pygame
import sys
import random
import math

pygame.init()

COULOMB = 8.99 # all charges are given in nano coulombs
WINDOW_DIMENS = 640

screen = pygame.display.set_mode((WINDOW_DIMENS, 2*WINDOW_DIMENS//3))
clock = pygame.time.Clock()

pressed = False
text = pygame.font.SysFont("arial", 10)

class pointCharge:
    def __init__(self, pos : tuple, charge : int): # all point charges will have radius of 0.
        self.pos = pos
        self.Q = charge

class simulate:
    def __init__(self, pos : tuple, dimensions : int, res : int):
        self.pos = pos
        self.dimens = dimensions
        self.res = res
        self.charges = []
        
    def run(self):
        self.fieldColorScale(self.res, self.dimens)
        mousePos = pygame.mouse.get_pos()
        for i in self.charges: # checks each charge
            if i.Q > 0:
                if (i.pos[0] + 2 >= mousePos[0] >= i.pos[0] - 2) and (i.pos[1] + 2 >= mousePos[1] >= i.pos[1] - 2):
                    self.forces(self.charges, i)
                    drawText(f"Charge = {i.Q} nC", text, "green", (10+self.pos[0], 10+self.pos[1])) # Draws text for charge in top left
                    pygame.draw.circle(screen, "black", i.pos, 7)
                color = "white"
            elif i.Q < 0:
                if (i.pos[0] + 2 >= mousePos[0] >= i.pos[0] - 2) and (i.pos[1] + 2 >= mousePos[1] >= i.pos[1] - 2):
                    self.forces(self.charges, i)
                    drawText(f"Charge = {i.Q} nC", text, "green", (10+self.pos[0], 10+self.pos[1])) # Draws text for charge in top left
                    pygame.draw.circle(screen, "white", i.pos, 5)
                color = "black"

            pygame.draw.circle(screen, color, i.pos, 4)

    def fieldStrength (self, pos : tuple, pCharges : list[pointCharge], maxDist): # checks every tile and calculates the electric field strength experienced by the tile at pos.
        totalE = 0
        for charge in pCharges:
            deltaX = (pos[0] - charge.pos[0])/250 #
            deltaY = (pos[1] - charge.pos[1])/250
            r_squared = deltaX**2 + deltaY**2

            distance = min(maxDist, r_squared)
            if distance == 0:
                break
            totalE += int((charge.Q/distance))
        return max(min(totalE, 99), -99)

    def forces(self, pCharges : list[pointCharge], thisCharge): # generates an arrow to all charges.
        for charge in pCharges:
            if charge != thisCharge: # avoiding division by zero and such by not checking current charge
                distance_sqrd = ((charge.pos[0] - thisCharge.pos[0]) ** 2) + ((charge.pos[1] - thisCharge.pos[1]) ** 2)
                force = (thisCharge.Q * charge.Q * COULOMB)/(distance_sqrd)
                midPoint = ((charge.pos[0] - thisCharge.pos[0])//2 + thisCharge.pos[0], (charge.pos[1] - thisCharge.pos[1])//2 + thisCharge.pos[1])

                pygame.draw.line(screen, (90, 90, 90), thisCharge.pos, charge.pos) # line to charge
                drawText(f"{force:.2e} N", text, "green", midPoint) # gets the midpoint of the line and draws the text for force there. +ive F means repulsion.
                self.drawArrow(midPoint, (90, 90, 90), math.atan2((thisCharge.pos[1] - charge.pos[1]), (thisCharge.pos[0] - charge.pos[0])), ((force**2)**(1/2))/force) # lineAngle : finds the angle of the line to the horizontal (-pi to pi radians), direct : sign of force decides if arrow points towards or away.

    def createCharge(self, pos : tuple, charge : int):
        chargesPos = [x.pos for x in self.charges]
        if (((self.pos[0] + self.dimens) >= pos[0] >= self.pos[0]) and (((self.pos[1] + self.dimens) >= pos[1] >= self.pos[1]))) and pos not in chargesPos: # generic  "in the desired simulation space" verification.
            self.charges.append(pointCharge(pos, charge))

    def drawArrow(self, pos : tuple, color, lineAngle : float, direct):
        angleFromLine = math.pi/9 # radians
        first_branch_end_pos = (direct * 30*math.cos(lineAngle + angleFromLine) + pos[0], direct * 30*math.sin(lineAngle + angleFromLine) + pos[1])
        second_branch_end_pos = (direct * 30*math.cos(lineAngle - angleFromLine) + pos[0], direct * 30*math.sin(lineAngle - angleFromLine) + pos[1])
        pygame.draw.line(screen, color, pos, first_branch_end_pos)
        pygame.draw.line(screen, color, pos, second_branch_end_pos)

    def fieldColorScale(self, res : int, dimensions): # seperates the screen in a series of tiles, according to the desired resolution of field and the size of the window. The center of each tile is the pixel whose electric field strength represents the tile's.
        tileSize = dimensions/(res**(1/2)) # res is the total num of tiles. The screen is a square, so res^1/2 = how many tiles per line. (Length of line)/(tiles per line) = length of one tile.
        electricFieldStrength = 0
            
        for line in range(int(res**(1/2))):
            for tile in range(int(res**(1/2))):

                centerPos = (tile*tileSize + tileSize//2 + self.pos[0], line*tileSize + tileSize//2 + self.pos[1]) # center pos = tileSize/2 + (number of tiles before it in the X or in the Y) + co-ord of leftmost or highest point.
                electricFieldStrength = self.fieldStrength(centerPos, self.charges, 5)


                #color = pygame.Color.lerp(pygame.Color(0, 0, 255, 20), pygame.Color(255, 0, 0, 20), tile/int(res**(1/2))) # interpolate between two colours, where the normal value (0 to 1) is (the tile number in the x * the length of one tile) divided by (the total length in the x).
                color = pygame.Color.lerp(pygame.Color(0, 0, 255), pygame.Color(255, 0, 0), max(min((electricFieldStrength+50), 99), 1)/100) # interpolate between two colours, where the normal value (0 to 1) is the electric potential divided by the scale maximum.
                tileRect = pygame.rect.Rect(tile*tileSize + self.pos[0], line*tileSize + self.pos[1], tileSize, tileSize)
                pygame.draw.rect(screen, color, tileRect)

class Scale:
    def __init__(self, pos, height, width):
        self.height = height
        self.pos = pos
        self.width = width

    def drawScale(self):
        for i in range(64): # constructing the electric field strength scale
            scaleRect = pygame.rect.Rect(self.pos[0], self.pos[1]+i*5, 30, 5)
            rectColor = 1-max(min(i//2, 31), 1)/32
            pygame.draw.rect(screen, pygame.Color.lerp(pygame.Color(0, 0, 255), pygame.Color(255, 0, 0), rectColor), scaleRect)

            if (i%8) == 0 and i > 0:
                pygame.draw.line(screen, "black", (self.pos[0], self.pos[1]+i*5 ), (self.pos[0] + 5, self.pos[1]+i*5), 1)
                pygame.draw.line(screen, "black", (self.pos[0] + 25, self.pos[1]+i*5 ), (self.pos[0] + 30, self.pos[1]+i*5), 1)
                drawText(f"{(rectColor * -100 + 50)*8.99:.1f}", text, "black", (self.pos[0] + 32, 24+i*5))
        
        pygame.draw.line(screen, "black", (self.pos[0], self.pos[1]-1), (self.pos[0] + 5, self.pos[1]-1), 2) # first graduation line left
        pygame.draw.line(screen, "black", (self.pos[0] + 25, self.pos[1]-1), (self.pos[0] + 30, self.pos[1]-1), 2) # first graduation line right
        pygame.draw.line(screen, "black", (self.pos[0], self.pos[1]+64*5), (self.pos[0] + 5, self.pos[1]+64*5), 2) # last graduation line left
        pygame.draw.line(screen, "black", (self.pos[0] + 25, self.pos[1]+64*5), (self.pos[0] + 30, self.pos[1]+64*5), 2) # last graduation line right

        pygame.draw.line(screen, "black", (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]+64*5), 2) # side of bar left
        pygame.draw.line(screen, "black", (self.pos[0] + 29, self.pos[1]), (self.pos[0] + 29, self.pos[1]+64*5), 2) # side of bar right
        drawText(f"{(rectColor * 100 - 50)*8.99:.1f}", text, "black", (self.pos[0] + 32, self.pos[1] - 6)) # first electric field strength reading
        drawText(f"{(rectColor * -100 + 50)*8.99:.1f}", text, "black", (self.pos[0] + 32, (self.pos[1] - 6)+64*5)) # last electric field strength reading
        drawText("Electric Field Strength (x10^-1 N/C)", text, "black", (self.pos[0] - 55, self.pos[1] - 20)) # last electric field strength reading

        self.colourSelect()

    def colourSelect(self):
        mousePos = pygame.mouse.get_pos()

        for i in range(64):
            if (self.pos[0]+self.width >= mousePos[0] >= self.pos[0]) and (self.pos[1]+(i+1)*5 >= mousePos[1] > self.pos[1]+i*5):
                scaleRectBorder = pygame.rect.Rect(self.pos[0]-3, self.pos[1]+i*5-3, 36, 11)
                scaleRect = pygame.rect.Rect(self.pos[0], self.pos[1]+i*5, 30, 5)
                rectColor = 1-max(min(i//2, 31), 1)/32

                pygame.draw.rect(screen, "white", scaleRectBorder, 3)
                pygame.draw.rect(screen, pygame.Color.lerp(pygame.Color(0, 0, 255), pygame.Color(255, 0, 0), rectColor), scaleRect)

                drawText(f"{(rectColor * 100 - 50)*8.99:.1f}", text, "black", (self.pos[0] - 50, self.pos[1]+i*5-3))

class Button:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height
        self.clicked = False
        self.buttonRect = pygame.Rect(pos[0], pos[1], width, height)

    def Click(self, mousePos):
        if (self.pos[0]+self.width >= mousePos[0] >= self.pos[0]) and (self.pos[1]+self.height >= mousePos[1] >= self.pos[1]):
            self.clicked = True

    def drawButton(self):
        if not self.clicked:
            pygame.draw.rect(screen, (210, 210, 210), self.buttonRect)
        else:
            pygame.draw.rect(screen, (160, 160, 160), self.buttonRect)
            simulation.charges = []
        drawText("Reset", text, "black", (self.pos[0]+5, self.pos[1]+3))

def drawText(text, font, colour, pos):
    screen.blit(font.render(text, True, colour), pos)

simulation = simulate((30,30), 320, 25600)
scale = Scale((WINDOW_DIMENS - 150, 30), 320, 30)
resetButton = Button((30, 2*WINDOW_DIMENS//3 - 50), 50, 20)

while True:
    screen.fill((90, 90, 90))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (not pressed): # generic "create only on frame where pressed" verfification.
            pressed = True
            mousePos = pygame.mouse.get_pos()
            simulation.createCharge(mousePos, int(random.choice([random.uniform(-10, -1),random.uniform(1, 10)])))
            resetButton.Click(mousePos)
        elif event.type == pygame.MOUSEBUTTONUP:
            resetButton.clicked = False
            pressed = False

    simulation.run()
    scale.drawScale()
    resetButton.drawButton()

    pygame.display.update()

    clock.tick(60)
