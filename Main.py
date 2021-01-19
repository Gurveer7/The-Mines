#-------------------------------------------------------------------------------
# Name: Gurveer Grewal

#Purpose: The purpose of this code is to make a playable pygame mining tycoon

# Date: 2019-06-17

#-------------------------------------------------------------------------------

# Importing modules
import pygame
import spritesheetFunctions
import random
import time

GREEN = (0, 255, 0)
pygame.init() # Initialize python


# VARIABLES
#Bat spawn coordinates
batx = 150
baty = 175
batx2 = 750
baty2 = 175
batx3 = 540
baty3 = 300
#health bar size
healthx = 240
screenx = 1080
screeny = 720
#Variables for ores scores and total score
goldScore = 0
ironScore = 0
diamondScore = 0
global AmountOfIron
AmountOfIron = 0
global AmountOfGold
AmountOfGold = 0
global AmountOfDiamond
AmountOfDiamond = 0
global AmountOfTotalScore
AmountOfTotalScore = 0
#UFO Coordinates
ufox = 0
ufoy = 50

### Ore Spawns ###
goldtimes = random.randint(25000,50000)
irontimes = random.randint(10000,25000)
diamondtimes = random.randint(60000,100000)

# gold ore group to spawn different instances
goldOreSpawn = pygame.sprite.Group()
SPAWN_GOLD = pygame.USEREVENT+1
pygame.time.set_timer(SPAWN_GOLD, goldtimes)

#iron ore sprite group to spawn different instances
ironOreSpawn = pygame.sprite.Group()
SPAWN_IRON = pygame.USEREVENT+2
pygame.time.set_timer(SPAWN_IRON, irontimes)

#diamond ore sprite group to spawn different instances
diamondOreSpawn = pygame.sprite.Group()
SPAWN_DIAMOND = pygame.USEREVENT+3
pygame.time.set_timer(SPAWN_DIAMOND, diamondtimes)
### Ore Spawns ###

#Initialize screen and background
backGround = pygame.image.load("backgrounder.png")
global screen
# parameters for screen size

screen = pygame.display.set_mode((screenx,screeny))
pygame.display.set_caption("Gurveer's Culminating")
clock = pygame.time.Clock()

# Variables
global currentSpriteImage, spriteChangeTimer
currentSpriteImage = 0
spriteChangeTimer = 0.25

# Sprite Images
global minerWalkForward
global goldnugget
# Uses spritesheetFunctions to cut out images instead of having a lot of pictures
#https://grandmadebslittlebits.wordpress.com/2015/11/07/themo-monster-sprites/
minerSpriteSheet = spritesheetFunctions.SpriteSheet("spriteMapRed.png")
#https://opengameart.org/content/bat-sprite
batsprite = spritesheetFunctions.SpriteSheet("batsprite.png")
#https://pngtree.com/freepng/gold-stone-effect_2418224.html
goldnugget = spritesheetFunctions.SpriteSheet("goldNugget.png")
#https://satisfactory.gamepedia.com/Iron_Ore
ironnugget = spritesheetFunctions.SpriteSheet("ironores.png")
#https://imgbin.com/png/yJKzt30c/gemstone-bejeweled-diamond-computer-icons-png
diamondnugget = spritesheetFunctions.SpriteSheet("diamondoregreen.png")
#Coordinates for spritesheetfunctions (to animate)
minerWalkForward = [0, 32, 64, 32]
minerMining = [96, 128, 160, 128]
BatWalking = [0, 32, 64]

# Sprites
#Main miner will be the main sprite I will be using
MainMiner = pygame.sprite.Sprite()
MainMiner.image = minerSpriteSheet.getSprite(minerWalkForward[0], 0, 32, 32)
MainMiner.image.set_colorkey((255, 0, 0))
MainMiner.rect = MainMiner.image.get_rect() # Get rect
minerx = 500 # coordinates for x
minery = 400 # coordinates for y
MainMiner.rect.center = (minerx, minery) # spawn in miner


# Functions
def MinerAnimate(direction):
    global spriteChangeTimer, currentSpriteImage, minerWalkForward
    if (spriteChangeTimer <= 0):
        spriteChangeTimer = 0.001 # flips through images
        if (currentSpriteImage > 2):
            currentSpriteImage = 0
        else:
            currentSpriteImage += 1
#This function helps the miner become animated
        if (direction == "down"): #Changes sprite for down
            MainMiner.image = minerSpriteSheet.getSprite(minerWalkForward[currentSpriteImage], 0, 32, 32)
            MainMiner.image.set_colorkey((255, 0 ,0))
        if (direction == "left"): #Changes sprite for left
            MainMiner.image = minerSpriteSheet.getSprite(minerWalkForward[currentSpriteImage], 32, 32, 32)
            MainMiner.image.set_colorkey((255, 0 ,0))
        if (direction == "right"): #Changes sprite for  right
            MainMiner.image = minerSpriteSheet.getSprite(minerWalkForward[currentSpriteImage], 64, 32, 32)
            MainMiner.image.set_colorkey((255, 0 ,0))
        if (direction == "up"): #Changes sprite for up
            MainMiner.image = minerSpriteSheet.getSprite(minerWalkForward[currentSpriteImage], 96, 32, 32)
            MainMiner.image.set_colorkey((255, 0 ,0))
        if (direction == "space"): #Changes sprite for space
            MainMiner.image = minerSpriteSheet.getSprite(minerMining[currentSpriteImage], 0, 32, 32)
            MainMiner.image.set_colorkey((255, 0 ,0))

    else:
        spriteChangeTimer -= 0.1



def enemy(minerx, minery):
    global batx, baty, MainMiner, healthx
    #Initialize bat
    bat = pygame.sprite.Sprite()
    bat.image = pygame.image.load("batworko.png")
    bat.image.set_colorkey((0, 255 ,0))
    bat.rect = bat.image.get_rect()


    bat.rect.center = (batx, baty)
    screen.blit(bat.image, bat.rect)
    #To make the bat follow the miner
    if batx >= ((MainMiner.rect.x)):
        batx -= 1.5
    if batx <= ((MainMiner.rect.x)):
        batx += 1.5
    if baty >= ((MainMiner.rect.y)):
        baty -= 1.5
    if baty <= ((MainMiner.rect.y)):
        baty += 1.5
        #Health bar
    if healthx >= 0:
        pygame.draw.rect(screen, GREEN, (500,10,healthx,35))
    if pygame.sprite.collide_rect(MainMiner, bat):
        healthx-=10
        pygame.display.update()
    else:
        if healthx >=10 and healthx <= 240:
            healthx+=0.5
#boundaries so the miner cant run out of the map
def boundary():
# have to do +32 to account for half the miner as I am comparing CENTER
    if MainMiner.rect.x + 32 >= screenx:
        MainMiner.rect.x = screenx - 32
    if MainMiner.rect.x <= 0:
        MainMiner.rect.x = 0
    if MainMiner.rect.y <= 0:
        MainMiner.rect.y = 0
    if MainMiner.rect.y > 688:
        MainMiner.rect.y = 688


#Keeps track of mineral counters
def score():
    global ScoreGold, AmountOfTotalScore
    #Resource Header
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Resources:', False, (255, 255, 255))
    screen.blit(textsurface,(0,0))
    #Resource Header

    #Iron Score Counter
    ScoreIron = pygame.image.load("Iron_Ore_icon.png")
    screen.blit (ScoreIron,(190,10))
    IronScore = pygame.font.SysFont('Comic Sans MS', 25)
    IronScoreText = IronScore.render("{0}".format(AmountOfIron), False , (255,255,255))
    screen.blit(IronScoreText,(170,7))
    #Iron Score Counter

    #Gold Score Counter
    ScoreGold = pygame.image.load("coin_single_gold.png")
    screen.blit (ScoreGold,(270,10))
    GoldScore = pygame.font.SysFont('Comic Sans MS', 25)
    GoldScoreText = GoldScore.render("{0}".format(AmountOfGold), False, (255,255,255))
    screen.blit(GoldScoreText,(250,7))
    #Gold Score Counter

    #Diamond Score Counter
    ScoreDiamond = pygame.image.load("diascore.png")
    screen.blit (ScoreDiamond,(350,10))
    DiamondScore = pygame.font.SysFont('Comic Sans MS', 25)
    DiamondScoreText = DiamondScore.render("{0}".format(AmountOfDiamond), False, (255,255,255))
    screen.blit(DiamondScoreText,(330,7))

    Healthy = pygame.font.SysFont('Comic Sans MS', 25)
    HealthText = Healthy.render("HP", False , (0,0,255))
    screen.blit(HealthText,(460,10))
    #Diamond Score Counter

# allows miner to sell ores for score
def store():
    global AmountOfGold, AmountOfIron, AmountOfDiamond, AmountOfTotalScore
    TotalScorelbl = pygame.font.SysFont('Comic Sans MS', 25)
    TotalScoreTextlbl = TotalScorelbl.render("Total Score:  " + str(AmountOfTotalScore), False , (255,255,255))
    screen.blit(TotalScoreTextlbl,(825,7))
    # detects collision of user to shop
    if MainMiner.rect.x >=824 and MainMiner.rect.x <=924 and MainMiner.rect.y >= 194 and MainMiner.rect.y <=294:
        AmountOfTotalScore += (AmountOfIron * 20) + (AmountOfGold * 50) + (AmountOfDiamond * 100)
        AmountOfIron = 0
        AmountOfGold = 0
        AmountOfDiamond = 0

#Prizes depending on amount of score reached and difficulties
def prize():
    global AmountOfTotalScore, ufox, ufoy
#Spawns stephen curry
    if AmountOfTotalScore >= 100:
        lights = pygame.image.load("curryprize.png")
        screen.blit(lights,(1015,660))
        #spawns the larry OB trophy
    if AmountOfTotalScore >= 250:
        #https://dlpng.com/tag/Trophy
        LarryOB = pygame.image.load("trophy.png")
        screen.blit(LarryOB,(800,230))
        #allows a ufo to fly across the screen
    if AmountOfTotalScore >= 500:
        Ufo = pygame.sprite.Sprite()
        #https://picsart.com/i/sticker-ufo-pixelart-pixelated-freetouse-255914449008212
        Ufo.image = pygame.image.load("ufoo.png")
        Ufo.rect = Ufo.image.get_rect()
        Ufo.rect.center = (ufox, ufoy)
        screen.blit(Ufo.image, Ufo.rect)
        if ufox <1200:
            ufox += 5

#Spawns another bat SECOND ONE (harder difficulty)
    if AmountOfTotalScore >= 1000:
        global batx2, baty2, healthx
        bat2 = pygame.sprite.Sprite()
        bat2.image = pygame.image.load("batworko.png")
        bat2.image.set_colorkey((0, 255 ,0))
        bat2.rect = bat2.image.get_rect()
        bat2.rect.center = (batx2, baty2)
        screen.blit(bat2.image, bat2.rect)
        # makes bat follow miner
        if batx2 >= ((MainMiner.rect.x)):
            batx2 -= 1.5
        if batx2 <= ((MainMiner.rect.x)):
            batx2 += 1.5
        if baty2 >= ((MainMiner.rect.y)):
            baty2 -= 1.5
        if baty2 <= ((MainMiner.rect.y)):
            baty2 += 1.5
        if healthx >= 0:
            pygame.draw.rect(screen, GREEN, (500,10,healthx,35))
            #health bar goes down
        if pygame.sprite.collide_rect(MainMiner, bat2):
            healthx-=10
            pygame.display.update()


#Spawns another bat THIRD ONE (harder difficulty)
    if AmountOfTotalScore >= 2500:
        global batx3, baty3, healthx
        bat3 = pygame.sprite.Sprite()
        bat3.image = pygame.image.load("batworko.png")
        bat3.image.set_colorkey((0, 255 ,0))
        bat3.rect = bat3.image.get_rect()
        bat3.rect.center = (batx3, baty3)
        screen.blit(bat3.image, bat3.rect)
        # makes bat follow miner
        if batx3 >= ((MainMiner.rect.x)):
            batx3 -= 1.5
        if batx3 <= ((MainMiner.rect.x)):
            batx3 += 1.5
        if baty3 >= ((MainMiner.rect.y)):
            baty3 -= 1.5
        if baty3 <= ((MainMiner.rect.y)):
            baty3 += 1.5
        if healthx >= 0:
            pygame.draw.rect(screen, GREEN, (500,10,healthx,35))
            #health bar goes down
        if pygame.sprite.collide_rect(MainMiner, bat3):
            healthx-=10
            pygame.display.update()




#Animates the miner (main character)
spaceTimer = 0
def MinerMove(key):
    upImage = 0
    global spaceTimer, AmountOfIron, AmountOfGold, AmountOfDiamond
    if (key[pygame.K_DOWN]): # allows miner to go down
        MainMiner.rect.y += 5
        MinerAnimate("down")
    elif (key[pygame.K_LEFT]): # allows miner to go left
        MainMiner.rect.x -= 5
        MinerAnimate("left")
    elif (key[pygame.K_RIGHT]): # allows miner to go right
        MainMiner.rect.x += 5
        MinerAnimate("right")
    elif (key[pygame.K_UP]): # allows miner to go up
        MainMiner.rect.y -= 5
        MinerAnimate("up")
    if (key[pygame.K_SPACE]): # allows miner to mine ore
        spaceTimer+=1
        MinerAnimate("space")
#Holding down spacebar allows for the timer to go higher
        if spaceTimer >= 80 and pygame.sprite.spritecollide(MainMiner, diamondOreSpawn, True):
            AmountOfDiamond += 1

        if spaceTimer >= 55 and pygame.sprite.spritecollide(MainMiner, goldOreSpawn, True):
            AmountOfGold += 1

        if spaceTimer >= 30 and pygame.sprite.spritecollide(MainMiner, ironOreSpawn, True):
            AmountOfIron +=1
#Reset timer if not clicker
    else:
        spaceTimer = 0



#draws ores onto the screen
def draw():
    # Clear Sceen
    screen.blit(backGround,(0,0)) # blits background

    # Draw Sprites
    goldOreSpawn.draw(screen) # spawns gold
    ironOreSpawn.draw(screen) # spawns ore
    diamondOreSpawn.draw(screen) # spawns diamond
    screen.blit(MainMiner.image, (MainMiner.rect.x, MainMiner.rect.y))



#Main loop parameter only runs if True
run = False
#MAIN LOOP
start = True
while start == True:

    menu = pygame.image.load("startscreen.png")
    screen.blit(menu,(0,0))
    pygame.display.update()
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()
    if (event.type == pygame.MOUSEBUTTONDOWN):
        position = pygame.mouse.get_pos()
        if (position[0]>= 120) and (position[0]<=414) and (position[1]>=214) and (position[1]<=403):
            start = False
            run = True
    if event.type == pygame.QUIT: # If user clicked close
        run = False # Flag that we are done so we exit this loop
        start = False

#Main loop (only runs when true)
while run == True:
    clock.tick(30)

#If user dies
    if healthx <= 0:
        Deathy = pygame.font.SysFont('Comic Sans MS', 25) # variabal for font
        DeathText = Deathy.render("You have DIED. Your final Score is: " + str(AmountOfTotalScore), False, (255,0,0)) #dictates whats going to be said
        screen.blit(DeathText,(290,350)) #blits onto screen
        pygame.display.update()
        time.sleep(2)
        run = False


#Call all functions here
    draw()
    store()
    MinerMove(pygame.key.get_pressed())
    score()
    boundary()
    enemy(minerx, minery)
    prize()



    for event in pygame.event.get(): # User did something


#All ores spawning (randomly given their parameters of time and location)
        if event.type == SPAWN_GOLD:
            goldx = random.randint(150,900)
            goldy = random.randint(150,600)
            gold = pygame.sprite.Sprite()
            gold.image = goldnugget.getSprite(100, 483 ,64, 64)
            gold.image.set_colorkey((255, 0, 0))
            gold.rect = gold.image.get_rect()
            gold.rect.center = (goldx, goldy)
            goldOreSpawn.add(gold)

        if event.type == SPAWN_IRON:
            ironx = random.randint(150,900)
            irony = random.randint(200,600)
            iron = pygame.sprite.Sprite()
            iron.image = ironnugget.getSprite(0, 0, 100, 150)
            iron.image.set_colorkey((255, 0, 0))
            iron.rect = iron.image.get_rect()
            iron.rect.center = (ironx , irony)
            ironOreSpawn.add(iron)

        if event.type == SPAWN_DIAMOND:
            diax = random.randint(150,900)
            diay = random.randint(150,600)
            diamond = pygame.sprite.Sprite()
            diamond.image = diamondnugget.getSprite(0, 0 ,32, 32)
            diamond.image.set_colorkey((0, 255, 0))
            diamond.rect = diamond.image.get_rect()
            diamond.rect.center = (diax, diay)
            diamondOreSpawn.add(diamond)

        if event.type == pygame.QUIT: # If user clicked close
            run = False # Flag that we are done so we exit this loop





    pygame.display.update()
    clock.tick(60)

#MAIN LOOP
