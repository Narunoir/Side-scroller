import pygame as pg, pygame
from settings import *
vec = pygame.math.Vector2
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self):
            pg.sprite.Sprite.__init__(self)
            self.player_img = pygame.image.load(path.join(img_dir, "knight1.png")).convert()
            self.image = pygame.transform.scale(self.player_img, (80, 100))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH /2, HEIGHT /2)
            self.pos = vec(WIDTH /2, HEIGHT /2)
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.health = PLAYER_HEALTH
            self.image_l = pg.transform.flip(self.image, True, False)
            self.image_l.set_colorkey(WHITE)
            self.face_left = False
    def jump(self):
        self.vel.y = -15


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.image = self.image_l
            self.face_left = True
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.image = pygame.transform.scale(self.player_img, (80, 100))
            self.image.set_colorkey(WHITE)
            self.face_left = False

        #apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #wrap around
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos
        #if self.health <= 0:
            #self.kill()
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Mob(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        mob_img = pygame.image.load(path.join(img_dir, "go_1.png")).convert()
        self.image = pygame.transform.scale(mob_img, (50, 80))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH -10, HEIGHT - 100)
        self.rect.x = x
        self.rect.y = y
        self.pos  = vec(x, y)
        self.vel  = vec(-3, 4)
        self.health = MOB_HEALTH
        #if self.health <= 0:
            #self.kill()


    def draw_health(self):
        if self.health > MOB_HEALTH * 0.6:
            col = GREEN
        elif self.health > MOB_HEALTH * 0.3:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
    def update(self):
        self.pos += self.vel
        self.rect.midbottom = self.pos
        if self.pos.x < 25:
            if self.vel.x < 0:
                self.vel.x *= -1
        if self.pos.x > WIDTH - 25:
            if self.vel.x > 0:
                self.vel.x *= -1

    def load_images(self):
        img_dir = path.join(path.dirname(__file__), "img")
        snd_dir = path.join(path.dirname(__file__), "sound")
        mob_img = pygame.image.load(path.join(img_dir, "go_1.png")).convert()

        #self.standing_frames = [self.game.spritesheet.get_image(0, 0, 33, 65)]
                                #self.game.spritesheet.get_image(31, 0, 33, 65),
                                #self.game.spritesheet.get_image(65, 0, 33, 65),
                                #self.game.spritesheet.get_image(99, 0, 33, 65),
                                #self.game.spritesheet.get_image(133, 0, 33, 65),
                                #self.game.spritesheet.get_image(99, 0, 33, 65)]
        #for frame in self.standing_frames:
            #frame.set_colorkey(BLACK)
