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
SCREEN_NUM = 1
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
wall = pygame.transform.scale(wall, (WIDTH, HEIGHT)).convert()
door = pygame.image.load('door.png')
doorVert = pygame.transform.scale(door, (DOOR_WIDTH,DOOR_HEIGHT)).convert_alpha()
doorHori = pygame.transform.rotate(doorVert, 90).convert_alpha()
char_image = pygame.image.load('character.png').convert_alpha()
char_image = pygame.transform.scale(char_image, (CHAR_WIDTH, CHAR_HEIGHT)).convert_alpha()


#Audio
pygame.mixer.music.load('in_game.mp3')
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
        x = WIDTH-width-5
    if y <= 5:
        screenNum = screenChange(screenNum, x, y, width, height)
        y = HEIGHT-height-5
    if x >= WIDTH-width-1:
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
    if screenNum == 1:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        char1.move()
        char1.draw(screen)
        message_display('Use WASD or', 150, 60)
        message_display('arrow keys to', 150, 90)
        message_display('move', 150, 120)
    if screenNum == 2:
        screen.blit (wall, (0,0))
        screen.blit (floor, (BORDER_Y, BORDER_X))
        topDoor()
        botDoor()
        leftDoor()
        char1.move()
        char1.draw(screen)
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
        if y <= 5:
            screenNum = 3
        elif y >= HEIGHT - height-1:
            screenNum = 1
    elif screenNum == 3:
        if y >= HEIGHT - height-1:
            screenNum = 2
    elif screenNum == 4:
        pass
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