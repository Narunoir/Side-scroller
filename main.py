import pygame as pg, pygame
import random
from settings import *
from sprites import *

#from os import path
#Art from Irina Mir (irmirx)(SKELETON),(ZOMBIE)
#Art from Killyoverdrive (Knight)

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        pass

    def new_game(self):
        #things I want every time I start a new game.
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        self.player = Player(self)

        self.p1 = Platform(0, HEIGHT -40, WIDTH, 40)
        p2 = Platform(WIDTH /2 -200, HEIGHT *3/4, 100, 20)
        p3 = Platform(500, 400, 100, 20)
        mob1 = Mob(WIDTH - 15, HEIGHT - 100, 100, 40)
        mob2 = Mob(50, HEIGHT - 100, 100, 40)
        self.all_sprites.add(self.player, self.p1, p2,p3, mob1,mob2)
        self.platforms.add(self.p1, p2, p3)
        self.mobs.add(mob1, mob2)

        self.mob_timer = 0
        self.run()
        self.start_screen()

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        #Game Loop - events
        for event in pg.event.get():
        #check for window close
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            #if event.type == pg.KEYUP:w
                #if event.key == pg.K_SPACE:
                    #self.player.jump_cut()


    def update(self):
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if self.player.vel.y > 1:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 1


        # Mobs walk on platforms
        for mob in self.mobs:
            if mob.rect.bottom > self.p1.rect.top:
                mob.rect.bottom = self.p1.rect.top
                mob.vel.y = 0

        # Mobs Attacking
        mob_attacks = pg.sprite.spritecollide(self.player, self.mobs, False)
        for mob in mob_attacks:
            pass
            #mob.health -= 25
            #if mob.health <= 0:
                #mob.kill()
            #if self.player.face_left == False:
                #if mob.vel.x < 0:
                    #mob.pos.x += 200
                #if mob.vel.x > 0:
                    #mob.pos.x -= 200
            #elif self.player.face_left == True:
                #if mob.vel.x > 0:
                    #mob.pos.x -= 200
                #if mob.vel.x < 0:
                    #mob.pos.x += 200




        #make more mobs
        Mob_list = [Mob(WIDTH + 150, HEIGHT - 100, 100, 40)]
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([ 0,100, 2000, 5500, 9000]):
            self.mob_timer = now
            if len(self.mobs) < 3:
                for mob in Mob_list:
                    self.all_sprites.add(mob)
                    self.mobs.add(mob)


        #scroll the screen
        if self.player.rect.right >= WIDTH * 3/4:
            self.player.pos.x -= max(abs(self.player.vel.x), 3)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.x), 2)
                if plat.rect.x <= 0 - 400:
                    plat.kill()
            for mob in self.mobs:
                mob.pos.x -= max(abs(self.player.vel.x), 3)
                if mob.pos.x < 0 -1000:
                    mob.kill()
            if self.p1.rect.x < WIDTH:
                self.p1.rect.x = 0
        #Make more platforms
        Platform_list =[Platform(random.randrange(WIDTH +1, WIDTH + 800),
                                 random.randrange(150, HEIGHT -100),
                                 random.randrange(65, 150), 20)]
        if len(self.platforms) < 4:
            for plat in Platform_list:
                self.all_sprites.add(plat)
                self.platforms.add(plat)

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
        pg.display.flip()
    def start_screen(self):
        pass

    def game_over(self):
        pass

g = Game()
g.start_screen()
while g.running:
    g.new_game()
    g.game_over()

pygame.quit()
