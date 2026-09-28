import pygame
import sys
import random
import math

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

charges = []
pressed = False
COULOMB = 8.99 # all charges are given in nano coulombs
text = pygame.font.SysFont("arial", 10)

class pointCharge:
    def __init__(self, pos : tuple, charge : int): # all point charges will have radius of 0.
        self.pos = pos
        self.Q = charge

def forces(pCharges : list[pointCharge], thisCharge): # generates an arrow to all charges.
    for charge in pCharges:
        if charge != thisCharge: # avoiding division by zero and such by not checking current charge
            distance_sqrd = ((charge.pos[0] - thisCharge.pos[0]) ** 2) + ((charge.pos[1] - thisCharge.pos[1]) ** 2)
            force = (thisCharge.Q * charge.Q * COULOMB)/(distance_sqrd)
            midPoint = ((charge.pos[0] - thisCharge.pos[0])//2 + thisCharge.pos[0], (charge.pos[1] - thisCharge.pos[1])//2 + thisCharge.pos[1])

            pygame.draw.line(screen, (90, 90, 90), thisCharge.pos, charge.pos) # line to charge
            drawText(f"{force:.2e} N", text, "green", midPoint) # gets the midpoint of the line and draws the text for force there. +ive F means repulsion.

def createCharge(pos : tuple, charge : int):
    charges.append(pointCharge(pos, charge))

def drawText(text, font, colour, pos):
    screen.blit(font.render(text, True, colour), pos)

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

    for i in charges: # checks each charge
        if i.Q > 0:
            color = "red"
        elif i.Q < 0:
            color = "blue"

        if (i.pos[0] + 2 >= pygame.mouse.get_pos()[0] >= i.pos[0] - 2) and (i.pos[1] + 2 >= pygame.mouse.get_pos()[1] >= i.pos[1] - 2):
            forces(charges, i)
            drawText(f"Charge = {i.Q} nC", text, "green", (10, 10)) # Draws text for charge in top left
            pygame.draw.circle(screen, "white", i.pos, 5)

        pygame.draw.circle(screen, color, i.pos, 4)



    pygame.display.update()
    clock.tick(60)


# Right now, nothing stops the user from creating two charges with the same pos, which can create a ZeroDivisionError at the subprogrogram force, where the distance_sqrd between 2 charges is 0.