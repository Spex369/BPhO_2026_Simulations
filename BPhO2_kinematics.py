import pygame
import sys

pygame.init()
(WINDOW_WIDTH, WINDOW_HEIGHT) = 900, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
trackingScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

p = WINDOW_HEIGHT//5
a = 1
v = 0
C = 0.3
T = 2 * (((2 * (250))/a) ** (1/2))*(1/(1-C + 0.00001) - 0.5) # Expected time until no bounces. 2 * (2 * times OG height over g) * (1 over 1-C -0.5) infinit series for Time, giving total bounce time

bounce = 1
time = 0
dt = 1 # once per millisecond, 1000 times per second approximately
BoxHeight = 8*WINDOW_HEIGHT//12
BoxStart = WINDOW_HEIGHT//6
PosOverTimeLeft = WINDOW_WIDTH//2
PosOverTimeBottom = BoxHeight + BoxStart


font = pygame.font.SysFont("arial", 14)

def drawText(text, font, pos, rotate : bool):
    if not rotate:
        screen.blit(font.render(text, True, "white"), pos)
    else:
        screen.blit(pygame.transform.rotate(font.render(text, True, "white"), 90))


while True:
    screen.fill("black")
    screen.blit(trackingScreen, (0, 0))
    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Operations (calculate current pos, current velocity and time since start)
    p = p + (v ** dt) + (0.5 * a * (dt ** 2))
    v = v + a * dt
    time += dt
    
    # Boucning
    if p > 4*WINDOW_HEIGHT//5 and v > 0:
        bounce += 1 # current bounce
        v = -C * v # applying coeficient of restitution to velocity after bounce

        if T < time: # fixing the ball to the desired bounce height and forcing velocity to zero after final bounce.
            p = 4*WINDOW_HEIGHT//5 + 2
            v = 0
    
    nextPos = p + (v ** dt) + (0.5 * a * (dt ** 2)) # next pos used to draw lines on the position over time graph
    
    if WINDOW_WIDTH//2 - 2*(time+50) > 0: # if WINDOW_WIDTH//2 - 2*time is 0 or less, the pos over time line will exceed the boundaries of the screen. -100 for good measure, so -2(time+50) = -2*time - 100.
        pygame.draw.line(trackingScreen, "white", (PosOverTimeLeft + 2*time , p + 15), (PosOverTimeLeft + 2*(time+1), nextPos + 15), 3)
        xTracker = PosOverTimeLeft + 2*(time+1)
    pygame.draw.line(screen, "white", (xTracker, WINDOW_HEIGHT//30), (xTracker, WINDOW_HEIGHT//30 + 10), 3)
    drawText(str(xTracker), font, ((xTracker), 2*WINDOW_HEIGHT//30), False)
    drawText(str(time), font, ((xTracker), 3*WINDOW_HEIGHT//30), False)
    

    for i in range(BoxHeight//50 + 1):
        drawText(str(BoxStart + i*50), font, (WINDOW_WIDTH//4 - 65, BoxStart+ i*50 - 7), False)
        drawText(str(BoxStart + i*50), font, (PosOverTimeLeft - 50, BoxStart+ i*50 - 7), False)
        pygame.draw.line(screen, (90, 90, 90), (WINDOW_WIDTH//4 - 35, BoxStart + i*50), (WINDOW_WIDTH//4 + 30, BoxStart + i*50))
        pygame.draw.line(screen, (90, 90, 90), (PosOverTimeLeft - 20, BoxStart + i*50), (PosOverTimeLeft - 10, BoxStart + i*50))


    pygame.draw.line(screen, (90, 90, 90), (PosOverTimeLeft - 10, BoxStart), (PosOverTimeLeft - 10, PosOverTimeBottom))
    pygame.draw.line(screen, (90, 90, 90), (PosOverTimeLeft - 10, PosOverTimeBottom), (PosOverTimeLeft + WINDOW_WIDTH//2 - 80, PosOverTimeBottom)) # end position of line in the x is PosOverTimeLeft + 2*(time) - 20 (-20 for tolerance), where time = WINDOW_WIDTH//4-50 is rearranged from -WINDOW_WIDTH//2 + 2*(time+50) = 0. 
    pygame.draw.rect(screen, "white", pygame.rect.Rect(WINDOW_WIDTH//4 - 30, BoxStart , 60, BoxHeight), 1)
    pygame.draw.circle(screen, "white", (WINDOW_WIDTH//4, p), 15)
    
    pygame.display.update()
    clock.tick(50) # smooth and CPU friendly. DO NOT MODIFY.

