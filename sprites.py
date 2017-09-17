import pygame as pg, pygame
from settings import *
vec = pygame.math.Vector2
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self, game):
            pg.sprite.Sprite.__init__(self)
            self.slash_sound = pygame.mixer.Sound(path.join(snd_dir, "Explosion3.wav"))
            self.player_img = pygame.image.load(path.join(img_dir, "knight1.png")).convert()
            self.slash_img = pygame.image.load(path.join(img_dir, "knight_slash.png")).convert()
            self.image = pygame.transform.scale(self.player_img, (80, 100))
            self.player_mini_image = pygame.transform.scale(self.player_img, (40, 45))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH /2, HEIGHT /2)
            self.game = game
            self.pos = vec(WIDTH /2, HEIGHT /2)
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.health = PLAYER_HEALTH
            self.lives  = 4
            self.hidden = False
            self.hide_timer = pg.time.get_ticks()
            self.hide_delay = 5000
            self.image_l = pg.transform.flip(self.image, True, False)
            self.image_l.set_colorkey(BLACK)
            self.face_left = False
            self.slashing = False
            self.last_slash = 0
            self.slash_delay = 350
            self.current_frame = 0
            self.last_update = 0
            self.score = 0
            self.slash_sound.set_volume(.2)


    def draw_player_health(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        fill = (pct / PLAYER_HEALTH) * PLAYER_HEALTH
        outline_rect = pg.Rect(x, y, PLAYER_HEALTH, PH_BAR_HEIGHT)
        fill_rect    = pg.Rect(x, y, fill, PH_BAR_HEIGHT)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)


    def draw_player_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 35 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.pos = vec(50, HEIGHT +400)

    def jump(self):
        self.vel.y = -15

    def slash(self):
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        sword_r = Sword(self.rect.midright, self.rect.centery)
        sword_l = Sword(self.rect.midleft, self.rect.centery)
        slash_l = pg.sprite.spritecollide(sword_l, self.game.mobs, False)
        slash_r = pg.sprite.spritecollide(sword_r, self.game.mobs, False)
        if now - self.last_slash > self.slash_delay:
            self.last_slash = now
            self.slash_sound.play()
            if keys[pg.K_j]:
                self.game.all_sprites.add(sword_l)
                slash_l
                if slash_l:
                    for mob in slash_l:
                        mob.pos.x  -= 75
                        mob.health -= 25
                        if mob.health <= 0:
                            mob.kill()
                            self.score += 50
            elif keys[pg.K_l]:
                self.game.all_sprites.add(sword_r)
                slash_r
                if slash_r:
                    for mob in slash_r:
                        mob.pos.x  += 75
                        mob.health -= 25
                        if mob.health <= 0:
                            mob.kill()
                            self.score += 50

    def animate(self):
        pass

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.pos = vec(100, HEIGHT - 50)
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            self.image = self.image_l
            self.face_left = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.image = pygame.transform.scale(self.player_img, (80, 100))
            self.image.set_colorkey(BLACK)
            self.face_left = False
        if keys[pg.K_j] or keys[pg.K_l]:
            self.slash()
            self.animate()

        #apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #wrap around
        #if self.pos.x > WIDTH:
            #self.pos.x = 0
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


    def draw_mob_health(self):
        if self.health > MOB_HEALTH * 60/100:
            col = GREEN
        elif self.health > MOB_HEALTH * 30/100:
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


    def mob_walk(self):
        mob_walk_animation = []
        for i in range(1, 7):
            filename = 'go_{}.png'.format(i)
            self.image = pygame.image.load(path.join(img_dir, filename)).convert()
            self.image = pg.transform.scale(self.image, (50, 80))
            self.image.set_colorkey(WHITE)
            mob_walk_animation.append(self.image)


    def load_images(self):
        pass
        #self.standing_frames = [self.game.spritesheet.get_image(0, 0, 33, 65)]
                                #self.game.spritesheet.get_image(31, 0, 33, 65),
                                #self.game.spritesheet.get_image(65, 0, 33, 65),
                                #self.game.spritesheet.get_image(99, 0, 33, 65),
                                #self.game.spritesheet.get_image(133, 0, 33, 65),
                                #self.game.spritesheet.get_image(99, 0, 33, 65)]
        #for frame in self.standing_frames:
            #frame.set_colorkey(BLACK)
class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pg.Surface((120, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center  = x
        self.rect.y  = y
        self.slash_dist = 15
        self.total_move = 0

    def update(self):
        self.rect.centerx += self.slash_dist
        self.total_move += 75
        if self.total_move > 200:
            self.kill()

class Boss(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        mob_img = pygame.image.load(path.join(img_dir, "go_1.png")).convert()
        self.image = pygame.transform.scale(mob_img, (120, 250))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH -10, HEIGHT - 100)
        self.rect.x = x
        self.rect.y = y
        self.pos  = vec(x, y)
        self.vel  = vec(-3, 2)
        self.health = BOSS_HEALTH

    def update(self):
        self.pos += self.vel
        self.rect.midbottom = self.pos
        if self.pos.x < WIDTH /2:
            if self.vel.x < 0:
                self.vel.x *= -1
        if self.pos.x > WIDTH - 25:
            if self.vel.x > 0:
                self.vel.x *= -1

    def draw_boss_health(self):
        if self.health > BOSS_HEALTH * 60/100:
            col = GREEN
        elif self.health > BOSS_HEALTH * 30/100:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / BOSS_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < 1500:
            pg.draw.rect(self.image, RED, self.health_bar)
