import pygame
import sys

pygame.init()
(WINDOW_WIDTH, WINDOW_HEIGHT) = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
trackingScreen = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
p = WINDOW_HEIGHT//5
a = 1
v = 0
C = 0.7
T = 2 * (((2 * (250))/a) ** (1/2))*(1/(1-C) - 0.5) # 2 * (2 * times OG height over g) * (1 over 1-C -0.5) infinit series for Time, giving total bounce time
bounce = 1
time = 0
dt = 1 # once per millisecond, 1000 times per second approximately (get delta time after flight)
BoxHeight = WINDOW_HEIGHT - 150
BoxStart = WINDOW_HEIGHT//6-15


font = pygame.font.SysFont("arial", 14)

def drawText(text, font, pos):
    screen.blit(font.render(text, True, "white"), pos)


while True:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    p = p + (v ** dt) + (0.5 * a * (dt ** 2))
    v = v + a * dt
    time += dt
    
    if p > 4*WINDOW_HEIGHT//5 and v > 0:
        bounce += 1
        v = -C * v
        if T < time:
            p = 4*WINDOW_HEIGHT//5
            v = 0

    nextPos = p + (v ** dt) + (0.5 * a * (dt ** 2))
    screen.fill("black")
    
    
    if time % 1 == 0 and -WINDOW_WIDTH//2 + 2*(time+50) < 0:
        pygame.draw.line(trackingScreen, "white", (WINDOW_WIDTH//2 + 2*time , p + 15), (WINDOW_WIDTH//2 + 2*(time+1), nextPos + 15), 3)

    screen.blit(trackingScreen, (0, 0))
    pygame.draw.rect(screen, "grey", pygame.rect.Rect(WINDOW_WIDTH//4 - 30, BoxStart , 60, BoxHeight), 1)

    for i in range(12):
        drawText(str(BoxStart + i*40), font, (WINDOW_WIDTH//4 - 65, BoxStart+ i*40 - 7))
        pygame.draw.line(screen, (90, 90, 90), (WINDOW_WIDTH//4 - 35, BoxStart + i*40), (WINDOW_WIDTH//4 + 30, BoxStart + i*40))
    pygame.draw.circle(screen, "white", (WINDOW_WIDTH//4, p), 15)
    
    pygame.display.update()
    clock.tick(50) # smooth and CPU friendly. DO NOT MODIFY.