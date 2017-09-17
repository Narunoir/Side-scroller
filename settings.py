from os import path

WIDTH  = 1200
HEIGHT = 650
FPS    = 60
FONT_NAME = 'Arial'
TITLE     = "Hacks n Slash"
HS_FILE   = "highscore.txt"



WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)


# Image/snd dirs
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "sound")
#Player Porperties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_HEALTH = 250
ATTACH_DAMAGE = 10
PH_BAR_HEIGHT = 20
#Mob Properties
MOB_HEALTH = 100
BOSS_HEALTH = 1500
