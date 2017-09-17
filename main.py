import pygame as pg, pygame
import random
from settings import *
from sprites import *

#from os import path
#Art from Irina Mir (irmirx)(SKELETON),(ZOMBIE)
#Art from Killyoverdrive (Knight)
#Art from Kungfu4000 (fire)
#Music bu Tom Peter


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
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            # An exception to avoid crashing from no filename
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new_game(self):
        #things I want every time I start a new game.
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        self.boss = Boss(WIDTH + 300, HEIGHT - 50, 120, 250)
        self.player = Player(self)

        self.p1 = Platform(0, HEIGHT -40, WIDTH, 40)
        p2 = Platform(WIDTH /2 -200, HEIGHT *3/4, 100, 20)
        p3 = Platform(500, 400, 100, 20)
        mob1 = Mob(WIDTH - 15, HEIGHT - 100, 100, 40)
        mob2 = Mob(50, HEIGHT - 100, 100, 40)
        self.all_sprites.add(self.player, self.p1,p2,p3, mob1,mob2)
        self.platforms.add(self.p1, p2, p3)
        self.mobs.add(mob1, mob2)

        self.mob_timer = 0
        self.mob_swing = 0
        self.boss_counter = 0
        pg.mixer.music.load(path.join(snd_dir, 'bob1.ogg'))
        self.run()
        self.start_screen()

    def run(self):
        #game loop
        pg.mixer.music.play(loops=-1)
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
        now = pg.time.get_ticks()
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if self.player.vel.y > 1:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 1

        if self.boss_counter == 10:
            self.all_sprites.add(self.boss)
            self.mobs.add(self.boss)
            if self.boss.health <= 0:
                self.boss.kill()
                self.boss_counter = 0

        # Mobs walk on platforms
        for mob in self.mobs:
            if mob.rect.bottom > self.p1.rect.top:
                mob.rect.bottom = self.p1.rect.top
                mob.vel.y = 0

        # Mobs Attacking
        mob_now = pg.time.get_ticks()
        #if mob_now -
        mob_attacks = pg.sprite.spritecollide(self.player, self.mobs, False)
        for mob in mob_attacks:
            self.player.health -= 10
            if mob.vel.x < 0:
                mob.pos.x += 75
            if mob.vel.x > 0:
                mob.pos.x -= 75
            if self.player.health <= 0:
                self.player.hide()
                self.player.lives -=1
                self.player.health = PLAYER_HEALTH
                #self.player.pos = vec(WIDTH /4, HEIGHT - 50)


        #make more mobs
        Mob_list = [Mob(WIDTH + 150, HEIGHT - 100, 100, 40)]
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
                    self.boss_counter += 1
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

        if self.player.lives == 0:
            self.playing = False



    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_mob_health()
        self.player.draw_player_health(self.screen, 10, 10, self.player.health)
        self.player.draw_player_lives(self.screen, WIDTH - 150, 10, self.player.lives, self.player.player_mini_image)
        self.draw_text(str(self.player.score), 30, WHITE, WIDTH /2, 15)
        pg.display.flip()


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def start_screen(self):
        # game start screen
        pg.mixer.music.load(path.join(snd_dir, 'bob2.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, WIDTH /2, HEIGHT /4)
        self.draw_text("Arrows to move,   Space to jump", 22, WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Press any key to Start", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, 20)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def game_over(self):
        # game over screen
        if not self.running:
            return
        pg.mixer.music.load(path.join(snd_dir, 'lmc1.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLUE)
        self.draw_text("Game Over", 48, WHITE, WIDTH /2, HEIGHT /4)
        self.draw_text("SCORE: "+ str(self.player.score), 22, WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("To Play Again,  Press any Key", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
        #if self.player.score > self.highscore:
            #self.highscore = self.player.score
            #self.draw_text("!! NEW HIGH SCORE !!", 22, WHITE, WIDTH /2, HEIGHT /2 + 40)
            #with open(path.join(self.dir, HS_FILE), 'w') as f:
                #f.write(str(self.player.score))
        #else:
            #self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()


g = Game()
g.start_screen()
while g.running:
    g.new_game()
    g.game_over()

pygame.quit()
