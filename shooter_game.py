#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
width = 700
height = 500
S =  5
lost = 0
score = 0
max_lost = 3
goal = 15
life = 3
num_fire = 0
rel_time = False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wei, hei):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(wei, hei))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < width - 65 :
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx-15, self.rect.top+40,-15,30,35)
        bullets.add(bullet)
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > width:
            self.rect.x = randint(65, width-65)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 or sprite.groupcollide(bullets, asteroids, True, False):
            self.kill()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(65, width-65), -65, randint(1,4), 65, 65)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(60, width-60), -60, randint(1,4), 60, 50)
    asteroids.add(asteroid)

player = Player('rocket.png', 300, 400, S, 65,65)    
window = display.set_mode((width,height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(width,height))
game = True

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font = font.SysFont('Arial', 36)
lose = font.render('YOU LOSER (press R to restart)', 1, (180,0,0))
win = font.render('YOU WIN',1, (0, 255, 127))
FPS = 60
clock = time.Clock()

finish = False


while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN and i.key == K_SPACE:
            if num_fire < 8 and rel_time == False:
                num_fire += 1
                fire_sound.play()
                player.fire()
            if num_fire >= 8 and rel_time == False:
                last_time = timer()
                rel_time = True
    if not finish:
        window.blit(background,(0,0))
        player.reset()
        player.move()
        monsters.update()
        bullets.update()
        asteroids.update()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font.render('Wait, reloading...', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(65, width-65), -65, randint(1,4), 65, 65)
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False) or lost >= max_lost:
            sprite.spritecollide(player,monsters, True)
            sprite.spritecollide(player,asteroids, True)
            life = life-1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (100,200))

        if score >= goal:
            finish = True
            window.blit(win, (270,250))
        text_lose = font.render('Пропущено:' + str(lost), 1, (255,255,255))
        text_score = font.render('Счет:' + str(score), 1, (255,255,255))
        text_life = font.render(str(life), 1, (0,255,0))
        window.blit(text_lose, (10, 50))
        window.blit(text_score, (10,20))
        window.blit(text_life, (650,10))
        display.update()
    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            finish = False
            score = 0
            lost = 0
            life = 3
            for b in bullets:
                b.kill()
            for m in monsters:
                m.kill()
            for z in asteroids:
                z.kill()
            time.delay(1000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(65, width-65), -65, randint(1,4), 65, 65)
            monsters.add(monster)

        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(60, width-60), -60, randint(1,4), 60, 50)
            asteroids.add(asteroid)
    clock.tick(FPS)
