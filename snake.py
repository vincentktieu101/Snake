import pygame
import random

pygame.init()
win = pygame.display.set_mode((449,500))

pygame.display.set_caption("Snake")

#music = pygame.mixer.music.load('Snek_Song_Extended.wav')
#pygame.mixer.music.play(-1)

class background():
    def draw(self, win):
        for i in range(0,15):
            for j in range(0,15):
                if (i+j)%2 == 0:
                    pygame.draw.rect(win, (255,255,255), (i * 30-1, j * 30-1, 31, 31), 1)
            
class player():
    def __init__(self, x, y, radius, color, horizontalFacing, verticalFacing, tailLength):
        self.x = x 
        self.y = y
        self.radius = radius
        self.color = color
        self.verticalFacing = verticalFacing
        self.horizontalFacing = horizontalFacing
        self.tailLength = tailLength

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class part():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self,win):
        pygame.draw.circle(win, (0, 255, 0), (self.x, self.y), 14)

class food():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, win):
        pygame.draw.circle(win, (0,225, 255), (self.x, self.y), 14)

def redrawGameWindow():
    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 255, 255), (0, 450, 450, 50))
    textScore = font.render('Score: ' + str(snake.tailLength + 1), 1, (0,0,0))
    win.blit(textScore, (0, 455))
    putBackground.draw(win)
    snake.draw(win)
    for tailPart in tail:
        tailPart.draw(win)
    snakeFood.draw(win)
    pygame.display.update()

font = pygame.font.SysFont('comicsans', 30, True)
putBackground = background()
snake = player(225, 225, 14, (0, 255, 0), 1, 0, 3)
tail = [part(195, 225), part(165, 225), part(135, 255)]
snakeFood = food(random.randint(0, 14) * 30 + 15, random.randint(0, 14) * 30 + 15)
run = True
hungry = True

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    turn = False

    if keys[pygame.K_LEFT] and not(snake.horizontalFacing == 1):
        snake.horizontalFacing = -1
        snake.verticalFacing = 0
    elif keys[pygame.K_RIGHT]and not(snake.horizontalFacing == -1):
        snake.horizontalFacing = 1
        snake.verticalFacing = 0
    if keys[pygame.K_UP] and not(snake.verticalFacing == 1):
        snake.verticalFacing = -1
        snake.horizontalFacing = 0
    elif keys[pygame.K_DOWN] and not(snake.verticalFacing == -1):
        snake.verticalFacing = 1
        snake.horizontalFacing = 0

    if snake.tailLength > len(tail):
        tail.append(0)

    for i in range(snake.tailLength - 1, 0, -1):
        tail[i] = tail[i-1]
    tail[0] = part(snake.x, snake.y)

    snake.verticalVel = 30 * snake.verticalFacing
    snake.horizontalVel = 30 * snake.horizontalFacing
    if (tail[1].x == snake.x and tail[1].y == snake.y):
        snake.verticalFacing = -snake.verticalFacing
        snake.horizontalFacing = -snake.horizontalFacing
        snake.verticalVel = 40 * snake.verticalFacing
        snake.horizontalVel = 40 * snake.horizontalFacing
        print('fixed')
    
    if snake.x + snake.horizontalVel < 0:
        snake.x = 435
    elif snake.x + snake.horizontalVel > 450:
        snake.x = 15
    elif snake.y + snake.verticalVel < 0:
        snake.y = 435
    elif snake.y + snake.verticalVel > 450:
        snake.y = 15
    else:
        snake.x += snake.horizontalVel
        snake.y += snake.verticalVel
    
    for tailPart in tail:
        if tailPart.x == snake.x:
            if tailPart.y == snake.y:
                snake.tailLength = 3
                for i in range(3, len(tail)):
                    tail.pop(3)

    if not(hungry):
        hungry = True
        checkFood = 0
        while checkFood == 0:
            checkFood = 1
            snakeFood.x = random.randint(0, 14) * 30 + 15
            snakeFood.y = random.randint(0, 14) * 30 + 15
            for tailPart in tail:
                if (tailPart.x == snakeFood.x and tailPart.y == snakeFood.y) and (checkFood == 1):
                    checkFood = 0
                    print('finding food...')
                
    else:
        if snakeFood.x == snake.x:
            if snakeFood.y == snake.y:
                hungry = False
                snake.tailLength += 1
    
    pygame.time.delay(100)
    redrawGameWindow()
pygame.quit()