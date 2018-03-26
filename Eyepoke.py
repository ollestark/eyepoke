import pygame
import time
import random

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (250,200,165)
blue = (0,0,255)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Eyepoke!')

img = pygame.image.load("Snakehead.png")
appleimg = pygame.image.load("apple.png")

icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon)


clock = pygame.time.Clock()

AppleThickness = 30
block_size = 20
FPS = 15
direction = "right"

smallfont = pygame.font.SysFont("Verdanams", 25)
medfont = pygame.font.SysFont("Verdanams", 50)
largefont = pygame.font.SysFont("Verdanams", 80)

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

            gameDisplay.fill(black)
            message_to_screen("Paused",
                              white,
                              -100,
                              size="large")
            
            message_to_screen("Press C to continue or Q to quit",
                              white,
                              25)
            pygame.display.update()
            clock.tick(5)

def score(score):
    text = smallfont.render("Eyes poked: "+str(score), True, white)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0

    return randAppleX, randAppleY

def game_intro():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(black)
        message_to_screen("Eyepoke!",
                          green,
                          -100,
                          size="large")
        message_to_screen("Poke as many eyes as you can!",
                          red,
                          -30)
        message_to_screen("Watch yourself and the walls!",
                          red,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit",
                          red,
                          180)

        pygame.display.update()
        clock.tick(5)

def snake(block_size, snakelist):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)

    if direction == "left":
        head = pygame.transform.rotate(img, 90)

    if direction == "up":
        head = img

    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()
    

def message_to_screen(msg, color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)
    
def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX,randAppleY = randAppleGen()
    while not gameExit:

        while gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("Game over",
                              red,
                              y_displace=-50,
                              size="large")
            
            message_to_screen("Press C to play again or Q to quit",
                              white,
                              50,
                              size="medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0

                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
        

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        
        gameDisplay.fill(black)

        
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        snake(block_size, snakeList)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score(snakeLength-1)

        
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX+AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX+AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY+AppleThickness:

                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1
                
            elif lead_y + block_size >  randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1
            
            

        clock.tick(FPS)
        
    pygame.quit()
    quit()

game_intro()
gameLoop()

