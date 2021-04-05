import pygame
import random

win = pygame.display.set_mode((600,600))
pygame.display.set_caption("Snake")

class background():
    def draw(self, win):
        for i in range(0,15):
            for j in range(0,15):
                pygame.draw.rect(win, (255,255,255), (i * 40, j * 40, 40, 40), 1)
            
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
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    
    def draw(self,win):
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)
        pygame.draw.circle(win, (0, 255, 0), (self.x, self.y), 18)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class food():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, win):
        pygame.draw.circle(win, (0,225, 255), (self.x, self.y), 18)

def redrawGameWindow():
    win.fill((0,0,0))
    snake.draw(win)
    grid.draw(win)
    for tailPart in tail:
        tailPart.draw(win)
    snakeFood.draw(win)
    pygame.display.update()

snake = player(260, 300, 18, (0, 255, 0), 1, 0, 3)
grid = background()
tail = [part(220, 300), part(180, 300), part(140, 300)]
snakeFood = food(random.randint(0, 14) * 40 + 20, random.randint(0, 14) * 40 + 20)
hungry = False
run = True 

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not(snake.horizontalFacing == 1):
        snake.horizontalFacing = -1
        snake.verticalFacing = 0
    if keys[pygame.K_RIGHT] and not(snake.horizontalFacing == -1):
        snake.horizontalFacing = 1
        snake.verticalFacing = 0
    if keys[pygame.K_UP] and not(snake.verticalFacing == 1):
        snake.verticalFacing = -1
        snake.horizontalFacing = 0
    if keys[pygame.K_DOWN] and not(snake.verticalFacing == -1):
        snake.verticalFacing = 1
        snake.horizontalFacing = 0

    for tailPart in tail:
        if tailPart.x == snake.x:
            if tailPart.y == snake.y:
                snake.tailLength = 3
                for i in range(3, len(tail)):
                    tail.pop(3)

    if snake.tailLength > len(tail):
        tail.append(0)

    for i in range(snake.tailLength - 1, 0, -1):
        tail[i] = tail[i-1]
    tail[0] = part(snake.x, snake.y)
    
    snake.verticalVel = 40 * snake.verticalFacing
    snake.horizontalVel = 40 * snake.horizontalFacing
    if (tail[1].hitbox[0] < snake.x + snake.horizontalVel and tail[1].hitbox[0] + tail[1].hitbox[2] > snake.x + snake.horizontalVel and tail[1].hitbox[1] < snake.y + snake.verticalVel and tail[1].hitbox[1] + tail[1].hitbox[3] > snake.y + snake.verticalVel):
        snake.verticalFacing = -snake.verticalFacing
        snake.horizontalFacing = -snake.horizontalFacing
        snake.verticalVel = 40 * snake.verticalFacing
        snake.horizontalVel = 40 * snake.horizontalFacing
        print('fixed')

    if snake.x + snake.horizontalVel < 0:
        snake.x = 580
    elif snake.x + snake.horizontalVel > 600:
        snake.x = 20
    else:
        snake.x += snake.horizontalVel
    if snake.y + snake.verticalVel < 0:
        snake.y = 580
    elif snake.y + snake.verticalVel > 600:
        snake.y = 20
    else: 
        snake.y += snake.verticalVel

    if not(hungry):
        hungry = True
        checkFood = 0 
        while checkFood == 0:
            checkFood = 1
            snakeFood.x = random.randint(0, 14) * 40 + 20
            snakeFood.y = random.randint(0, 14) * 40 + 20
            for tailPart in tail:
                if (tailPart.hitbox[0] < snakeFood.x and tailPart.hitbox[0] + tailPart.hitbox[2] > snakeFood.x and tailPart.hitbox[1] < snakeFood.y and tailPart.hitbox[1] + tailPart.hitbox[3] > snakeFood.y) or (snakeFood.x == snake.x and snakeFood.y == snake.y) or (checkFood == 0):
                    checkFood = 0
                    #print('finding food...')
                
    else:
        if snakeFood.x == snake.x:
            if snakeFood.y == snake.y:
                hungry = False
                snake.tailLength += 1

    pygame.time.delay(100)
    redrawGameWindow()
pygame.quit()