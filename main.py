from time import time as timer
from pygame import *
from random import randint
import pygame_menu

init()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, speed, w, h, picture):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 1080:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullets(self.rect.centerx, self.rect.top, -15, 5, 30, 'bullet1.png')
        bullets_group.add(bullet)

    def super_fire(self):
        super_bullets = Bullets(self.rect.centerx, self.rect.top, -10, 10, 35, 'bulletboss1.png')
        super_bullets_group.add(super_bullets)
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 800:
            self.rect.y = 0
            self.rect.x = randint(20, 1180)
            lost = lost + 1


class Bullets(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.rect.y = 0
            self.rect.x = randint(20, 1180)

class LifeBar(sprite.Sprite):
    def __init__(self, color, lifebar_x, lifebar_y, lifebar_width, lifebar_height):
        super().__init__()
        self.color = color
        self.width = lifebar_width
        self.height = lifebar_height
        self.image = Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = lifebar_x
        self.rect.y = lifebar_y
    def draw_life(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        

font.init()
font2 = font.SysFont('Verdana', 30)


window = display.set_mode((1200, 800))
display.set_caption('Shooter')
background = transform.scale(image.load('background2.png'), (1200, 800))


mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()

bullets_group = sprite.Group()
super_bullets_group = sprite.Group()


def main():
    monsters1 = sprite.Group()
    for _ in range(1):
        monster1 = Enemy(randint(80, 750), 0, randint(5, 10), 100, 100, 'enemy1.png')
        monsters1.add(monster1)

    monsters2 = sprite.Group()
    for _ in range(1):
        monster2 = Enemy(randint(80, 750), 0, randint(5, 10), 100, 100, 'enemy2.png')
        monsters2.add(monster2)

    monsters3 = sprite.Group()
    for _ in range(1):
        monster3 = Enemy(randint(80, 750), 0, randint(5, 10), 100, 100, 'enemy3.png')
        monsters3.add(monster3)

    boss_group = sprite.Group()
    for _ in range(1):
        boss = Enemy(randint(80, 750), 0, randint(7, 13), 150, 150, 'boss.png')
        boss_group.add(boss)

    meteor_group = sprite.Group()
    for _ in range(1):
        meteor = Meteor(randint(80, 750), 0, randint(7, 13), 80, 80, 'meteor2.png')
        meteor_group.add(meteor)

    finish = False

    

    player = Player(600, 650, 30, 100, 100, 'player.png')
    life_bar = LifeBar((0, 0, 0), 900, 40, 200, 20)
    life_bar_green = LifeBar((18, 166, 5), 900, 40, 200, 20)
    life_bar_yellow = LifeBar((255, 229, 0), 900, 40, 125, 20)
    life_bar_red = LifeBar((255, 0, 0), 900, 40, 50, 20)

    reload_bar = LifeBar((0, 0, 0), 10, 130, 210, 20)
    reload_bar_green = LifeBar((18, 166, 5), 10, 130, 210, 20)
    reload_bar_yellow = LifeBar((255, 229, 0), 10, 130, 140, 20)
    reload_bar_red = LifeBar((255, 0, 0), 10, 130, 70, 20)

    life = 3

    num_fire = 0
    rel_time = False

    super_num_fire = 0
    boss_rel_time = False

    win = 0
    while True:
        window.blit(background,(0, 0))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_win = font2.render('Убито:' + str(win), 1, (255, 255, 255))
        text_reload = font2.render('Перезарядка:', 1, (255, 255, 255))
        win_text = font2.render('YOU WIN!', 1, (71, 194, 41))
        lose_text = font2.render('YOU LOSE!', 1, (255, 0, 0))
        window.blit(text_lose, (10, 10))
        window.blit(text_win, (10, 45))
        window.blit(text_reload, (10, 80))
        for e in event.get():
            if e.type == QUIT:
                return
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1

                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start_time = timer()

            if e.type == MOUSEBUTTONDOWN and e.button == 3:
                if super_num_fire < 2 and boss_rel_time == False:
                    super_num_fire += 1

                    player.super_fire()
                if super_num_fire >= 2 and boss_rel_time == False:
                    boss_rel_time = True
                    boss_start_time = timer()


        if not finish:

            player.reset()
            player.update()
            monsters1.draw(window)
            monsters2.draw(window)
            monsters3.draw(window)
            boss_group.draw(window)
            bullets_group.draw(window)
            super_bullets_group.draw(window)
            meteor_group.draw(window)
            monsters1.update()
            monsters2.update()
            monsters3.update()
            boss_group.update()
            bullets_group.update()
            super_bullets_group.update()
            meteor_group.update()

            if rel_time == True:
                reload_bar_green.draw_life()
                end_time = timer()
                if end_time - start_time < 3:
                    reload_bar.draw_life()
                    reload_bar_green.draw_life()
                    if end_time - start_time <= 2:
                        reload_bar.draw_life()
                        reload_bar_yellow.draw_life()
                        if end_time - start_time <= 1:
                            reload_bar.draw_life()
                            reload_bar_red.draw_life()
                
                else:
                    rel_time = False
                    num_fire = 0

            if boss_rel_time == True:
                end_time = timer()
                reload_bar_green.draw_life()
                if end_time - boss_start_time < 3:
                    reload_bar.draw_life()
                    reload_bar_green.draw_life()
                    if end_time - boss_start_time <= 2:
                        reload_bar.draw_life()
                        reload_bar_yellow.draw_life()
                        if end_time - boss_start_time <= 1:
                            reload_bar.draw_life()
                            reload_bar_red.draw_life()
                
                else:
                    boss_rel_time = False
                    super_num_fire = 0




            sprite_list1 = sprite.groupcollide(monsters1, bullets_group, True, True) or sprite.groupcollide(monsters1, super_bullets_group, True, True)
            sprite_list2 = sprite.groupcollide(monsters2, bullets_group, True, True) or sprite.groupcollide(monsters2, super_bullets_group, True, True)
            sprite_list3 = sprite.groupcollide(monsters3, bullets_group, True, True) or sprite.groupcollide(monsters3, super_bullets_group, True, True)
            sprite_list4 = sprite.groupcollide(boss_group, super_bullets_group, True, True)

            for _ in sprite_list1:
                win += 1
                monster1 = Enemy(randint(80, 900), 0, randint(5, 10), 100, 100, 'enemy1.png')
                monsters1.add(monster1)

            for _ in sprite_list2:
                win += 1
                monster2 = Enemy(randint(80, 900), 0, randint(5, 10), 100, 100, 'enemy2.png')
                monsters2.add(monster2)

            for _ in sprite_list3:
                win += 1 
                monster3 = Enemy(randint(80, 900), 0, randint(5, 10), 100, 100, 'enemy3.png')
                monsters3.add(monster3)

            for _ in sprite_list4:
                win += 1 
                boss = Enemy(randint(80, 900), 0, randint(7, 13), 150, 150, 'boss.png')
                boss_group.add(boss)

            if win == 10:
                finish = True
                window.blit(win_text, (550, 300))
            if sprite.spritecollide(player, monsters1, True) or sprite.spritecollide(player, monsters2, True) or sprite.spritecollide(player, monsters3, True) or sprite.spritecollide(player, boss_group, True) or sprite.spritecollide(player, meteor_group, True):
                life -= 1
            if life == 0 or lost >= 5:
                finish = True
                window.blit(lose_text, (550, 300))

            if life == 3:
                life_bar.draw_life()
                life_bar_green.draw_life()
            if life == 2:
                life_bar.draw_life()
                life_bar_yellow.draw_life()
            if life == 1:
                life_bar.draw_life()
                life_bar_red.draw_life()
            if life == 0:
                life_bar.draw_life()




            display.update()
        time.delay(60)


def start_menu():
    menu = pygame_menu.Menu('Шутер', 1200, 800, theme = pygame_menu.themes.THEME_BLUE)
    menu.add.button('Начать', main)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    menu.mainloop(window)

start_menu()
