import pygame, time

# Set presets and initialize
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.init()


#Basic screen setup
WIDTH = 640
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quest")

#Character starting stats
CHAR_X = WIDTH/2
CHAR_Y = HEIGHT/2
CHAR_WIDTH = 60
CHAR_HEIGHT = 60
CHAR_VEL = 1

#Monster Stuff
MONS_X = 50
MONS_Y = 50
MONS_VEL = 1
MONS_WIDTH = 40
MONS_HEIGHT = 40
MOVE_1 = True

#Door Stuff
DOOR_WIDTH = 200
DOOR_HEIGHT = 160
DOOR_MIDX = WIDTH/2-90
DOOR_MIDY = HEIGHT/2-90
DOOR_RIGHTX = WIDTH-100
DOOR_LEFTX = -60
DOOR_TOPY = -60
DOOR_BOTY = HEIGHT-100

TOP_DOOR = (DOOR_MIDX, DOOR_TOPY)
BOT_DOOR = (DOOR_MIDX, DOOR_BOTY)
LEFT_DOOR = (DOOR_LEFTX, DOOR_MIDY)
RIGHT_DOOR = (DOOR_RIGHTX, DOOR_MIDY)


#Text
def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def message_display(text, centerx, centery):
    displayText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, displayText)
    TextRect.center = (centerx,centery)
    screen.blit(TextSurf, TextRect)

#Other Variables
SCREEN_NUM = 0
BORDER_X = 40
BORDER_Y = 40

#Colors
BLACK = (0,0,0,255)
GREY = (100,100,100,255)
WHITE = (255,255,255,255)
BORDER_COLOR1 = (46,46,46,255)
BORDER_COLOR2 = (74,74,74,255)
BORDER_COLOR3 = (107,107,107,255)
RED = (160, 20, 20, 2)

#Pictures
floor = pygame.image.load('dungeon_floor.jpg')
floor = pygame.transform.scale(floor, (WIDTH-BORDER_X*2, HEIGHT-BORDER_Y*2)).convert()
wall = pygame.image.load('dungeon_wall.png')
pillar = pygame.transform.scale(wall, (75, 75)).convert_alpha()
wall = pygame.transform.scale(wall, (WIDTH, HEIGHT)).convert()
door = pygame.image.load('door.png')
doorVert = pygame.transform.scale(door, (DOOR_WIDTH,DOOR_HEIGHT)).convert_alpha()
doorHori = pygame.transform.rotate(doorVert, 90).convert_alpha()
char_image = pygame.image.load('character.png').convert_alpha()
char_image = pygame.transform.scale(char_image, (CHAR_WIDTH, CHAR_HEIGHT)).convert_alpha()
mother = pygame.image.load('mother.png').convert_alpha()
mother = pygame.transform.scale(mother, (300, 300)).convert_alpha()
mons_image = pygame.image.load('octopus.png')
mons_image = pygame.transform.scale(mons_image, (MONS_WIDTH, MONS_HEIGHT)).convert_alpha()


#Audio
IN_GAME = False
pygame.mixer.music.load('intro_music.mp3')
pygame.mixer.music.play(loops=-1, start=0.0)

#Motion functions
def left(x, vel):
    x -= vel
    return x

def right(x, vel):
    x += vel
    return x
    
def up(y, vel):
    y -= vel
    return y

def down(y, vel):
    y += vel
    return y

def keyMoveY(x,y,width,height,vel, color1, color2 = None, color3 = None, image = None, currentRot = None):
    keys = pygame.key.get_pressed()
    rotation = 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y = up(y, vel)
        if detectCollide(x,y,width,height,color1, color2, color3):
            y = down(y,vel)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y = down(y, vel)
        if image != None:
            rotation += 180
        if detectCollide(x,y,width,height,color1, color2, color3):
            y = up(y,vel)
            
    return y, rotation
    

def keyMoveX(x,y,width,height,vel,color1, color2 = None, color3 = None, image = None, currentRot = None):
    keys = pygame.key.get_pressed()
    rotation = 0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x = right(x, vel)
        if image != None:
            rotation -= 90
        
        if detectCollide(x,y,width,height,color1, color2, color3):
            x = left(x,vel)
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x = left(x, vel)
        if image != None:
            rotation += 90
        
        if detectCollide(x,y,width,height,color1, color2, color3):
            x = right(x, vel)
    return x, rotation


def detectCollide(x, y, width, height, color1, color2 = None, color3 = None):
    if tuple(screen.get_at((x, y))) == color1 or tuple(screen.get_at((x+width, y+height))) == color1 or tuple(screen.get_at((x+width, y))) == color1 or tuple(screen.get_at((x, y+height))) == color1 or tuple(screen.get_at((x+width/2, y))) == color1 or tuple(screen.get_at((x, y+height/2))) == color1 or tuple(screen.get_at((x + width, y+height/2))) == color1 or tuple(screen.get_at((x+width/2, y+height))) == color1 or tuple(screen.get_at((x, y))) == color2 or tuple(screen.get_at((x+width, y+height))) == color2 or tuple(screen.get_at((x+width, y))) == color2 or tuple(screen.get_at((x, y+height))) == color2 or tuple(screen.get_at((x+width/2, y))) == color2 or tuple(screen.get_at((x, y+height/2))) == color2 or tuple(screen.get_at((x + width, y+height/2))) == color2 or tuple(screen.get_at((x+width/2, y+height))) == color2 or tuple(screen.get_at((x, y))) == color3 or tuple(screen.get_at((x+width, y+height))) == color3 or tuple(screen.get_at((x+width, y))) == color3 or tuple(screen.get_at((x, y+height))) == color3 or tuple(screen.get_at((x+width/2, y))) == color3 or tuple(screen.get_at((x, y+height/2))) == color3 or tuple(screen.get_at((x + width, y+height/2))) == color3 or tuple(screen.get_at((x+width/2, y+height))) == color3:
        return True
    else:
        return False


def screenWrap(screenNum, x, y, width, height):
    if x <= 5:
        screenNum = screenChange(screenNum, x, y, width, height)
        x = WIDTH-width-5
    if y <= 5:
        screenNum = screenChange(screenNum, x, y, width, height)
        y = HEIGHT-height-5
    if x >= WIDTH-width-1:
        screenNum = screenChange(screenNum, x, y, width, height)
        x = 10
    if y >= HEIGHT - height-1:
        screenNum = screenChange(screenNum, x, y, width, height)
        y = 10
        
    return x, y, screenNum

#Player Stuff
class Character(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, vel, image):
        super(Character, self).__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vel = vel
        self.image = image
        self.rot = 0
        self.rot2 = 0
        self.image1 = image
    def draw(self, screen):
        screen.blit(self.image1, (self.x, self.y))
        
    def move(self):
        self.x, self.rot = keyMoveX(self.x, self.y, self.width, self.height, self.vel, BORDER_COLOR1,BORDER_COLOR2,BORDER_COLOR3, self.image, self.rot)
        self.y, self.rot2 = keyMoveY(self.x, self.y, self.width, self.height, self.vel, BORDER_COLOR1,BORDER_COLOR2,BORDER_COLOR3,self.image, self.rot)
        if self.rot2 == 180:
            self.rot = self.rot2
        self.image1 = pygame.transform.rotate(self.image, self.rot)
        global SCREEN_NUM
        self.x, self.y, SCREEN_NUM = screenWrap(SCREEN_NUM, self.x, self.y, self.width, self.height)
        time.sleep(0.002)

char1 = Character(CHAR_WIDTH, CHAR_HEIGHT, CHAR_X, CHAR_Y, CHAR_VEL, char_image)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vel, image):
        super(Monster, self).__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vel = vel
        self.image = image
        self.alive = True
    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))
    def move(self):
        global MOVE_1
        if MOVE_1 == True:
            if self.x < char1.x:
                self.x = right(self.x, self.vel)
                if detectCollide(self.x,self.y,self.width,self.height,BORDER_COLOR1,BORDER_COLOR2,BORDER_COLOR3):
                    self.x = left(self.x,self.vel)
            else:
                self.x = left(self.x, self.vel)
                if detectCollide(self.x,self.y,self.width,self.height,BORDER_COLOR1,BORDER_COLOR2,BORDER_COLOR3):
                    self.x = right(self.x,self.vel)
            if self.y < char1.y:
                self.y = down(self.y, self.vel)
                if detectCollide(self.x,self.y,self.width,self.height,BORDER_COLOR1,BORDER_COLOR2,BORDER_COLOR3):
                    self.x = up(self.x,self.vel)
            else:
                self.y = up(self.y, self.vel)
                if detectCollide(self.x,self.y,self.width,self.height,BORDER_COLOR1,BORDER_COLOR2,BORDER_COLOR3):
                    self.x = down(self.x,self.vel)
            MOVE_1 = False
        else:
            MOVE_1 = True
            
mons1 = Monster(MONS_X, MONS_Y, MONS_WIDTH, MONS_HEIGHT, MONS_VEL, mons_image)

#Door Stuff
def topDoor():
    screen.blit(doorVert, TOP_DOOR)

def botDoor():
    screen.blit(doorVert, BOT_DOOR)

def leftDoor():
    screen.blit(doorHori, LEFT_DOOR)

def rightDoor():
    screen.blit(doorHori, RIGHT_DOOR)

#Screen Display Stuff
def displayScreen(screenNum):
    if screenNum == 0:
        screen.blit(mother, (150, 300))
        message_display('Your mother has fallen grievously ill.', WIDTH/2, 30)
        message_display('Everything the doctors do does not help.', WIDTH/2, 80)
        message_display('You have tried everything: natural healing,', WIDTH/2, 130)
        message_display('chemical therapy, and even superstition.', WIDTH/2, 180)
        message_display('Nothing helps...', WIDTH/2, 230)
        message_display('Press space to continue.', WIDTH/2, 280)
        keys = pygame.key.get_pressed()
        global SCREEN_NUM
        if keys[pygame.K_SPACE]:
            SCREEN_NUM = 1
    if screenNum == 1:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        char1.move()
        char1.draw(screen)
        message_display('Use WASD or', 150, 60)
        message_display('arrow keys to', 150, 90)
        message_display('move', 150, 120)
        global IN_GAME
        if IN_GAME == False:
            IN_GAME = True
            pygame.mixer.music.load('in_game.mp3')
            pygame.mixer.music.play(loops=-1, start=0.0)
    if screenNum == 2:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        botDoor()
        leftDoor()
        char1.move()
        mons1.move()
        char1.draw(screen)
        mons1.draw(screen)
        
    if screenNum == 3:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 4:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 5:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        topDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 6:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 7:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 8:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        rightDoor()
        topDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 9:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 10:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 11:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 12:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        leftDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 13:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        rightDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 14:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 15:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 16:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        leftDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 17:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        rightDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 18:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        rightDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 19:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 20:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 21:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        topDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 22:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 23:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        leftDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 24:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 25:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        rightDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 26:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        leftDoor()
        rightDoor()
        char1.move()
        char1.draw(screen)
    if screenNum == 27:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        botDoor()
        topDoor()
        char1.move()
        char1.draw(screen)
        
def screenChange(screenNum, x, y, width, height):
    if screenNum == 1:
        screenNum = 2
    elif screenNum == 2:
        if x <= 5:
            screenNum = 16
        if y <= 5:
            screenNum = 3
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            screenNum = 1
    elif screenNum == 3:
        if x <= 5:
            pass
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 17
        if y >= HEIGHT - height-1:
            screenNum = 2
    elif screenNum == 4:
        if x <= 5:
            pass
        if y <= 5:
            screenNum = 5
        if x >= WIDTH-width-1:
            screenNum = 16
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 5:
        if x <= 5:
            pass
        if y <= 5:
            screenNum = 6
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            screenNum = 4
    elif screenNum == 6:
        if x <= 5:
            pass
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 7
        if y >= HEIGHT - height-1:
            screenNum = 5
    elif screenNum == 7:
        if x <= 5:
            screenNum = 6
        if y <= 5:
            screenNum = 8
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 8:
        if x <= 5:
            pass
        if y <= 5:
            screenNum = 9
        if x >= WIDTH-width-1:
            screenNum = 26
        if y >= HEIGHT - height-1:
            screenNum = 7
    elif screenNum == 9:
        if x <= 5:
            screenNum = 10
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            screenNum = 8
    elif screenNum == 10:
        if x <= 5:
            pass
        if y <= 5:
            screenNum = 11
        if x >= WIDTH-width-1:
            screenNum = 9
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 11:
        if x <= 5:
            pass
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 12
        if y >= HEIGHT - height-1:
            screenNum = 10
    elif screenNum == 12:
        if x <= 5:
            screenNum = 11
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 13
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 13:
        if x <= 5:
            screenNum = 12
        if y <= 5:
            screenNum = 15
        if x >= WIDTH-width-1:
            screenNum = 14
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 14:
        screenNum = 13
    elif screenNum == 15:
        screenNum = 13
    elif screenNum == 16:
        if x <= 5:
            screenNum = 4
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 2
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 17:
        if x <= 5:
            screenNum = 3
        if y <= 5:
            screenNum = 27
        if x >= WIDTH-width-1:
            screenNum = 18
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 18:
        if x <= 5:
            screenNum = 17
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 20
        if y >= HEIGHT - height-1:
            screenNum = 19
    elif screenNum == 19:
        screenNum = 18
    elif screenNum == 20:
        if x <= 5:
            screenNum = 18
        if y <= 5:
            screenNum = 21
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 21:
        if x <= 5:
            pass
        if y <= 5:
            screenNum = 22
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            screenNum = 20
    elif screenNum == 22:
        if x <= 5:
            screenNum = 23
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            screenNum = 21
    elif screenNum == 23:
        if x <= 5:
            screenNum = 25
        if y <= 5:
            screenNum = 24
        if x >= WIDTH-width-1:
            screenNum = 22
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 24:
        screenNum = 23
    elif screenNum == 25:
        if x <= 5:
            screenNum = 26
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 23
        if y >= HEIGHT - height-1:
            screenNum = 27
    elif screenNum == 26:
        if x <= 5:
            screenNum = 8
        if y <= 5:
            pass
        if x >= WIDTH-width-1:
            screenNum = 25
        if y >= HEIGHT - height-1:
            pass
    elif screenNum == 27:
        if x <= 5:
            pass
        if y <= 5:
            screenNum = 25
        if x >= WIDTH-width-1:
            pass
        if y >= HEIGHT - height-1:
            screenNum = 17
    return screenNum




#Animation Loop Stuff
def main():
    displayScreen(SCREEN_NUM)
    
    pygame.display.update()
    
inPlay = True
print "Hit ESC to end the program."
while inPlay:
    pygame.event.get()
    keys = pygame.key.get_pressed()
    main()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
        
pygame.quit()
