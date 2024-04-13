from pygame import *
from random import randint 
from time import time as timer

window = display.set_mode((700,500))
display.set_caption("Niger_game)))")
bg = "galaxy.jpg"
hero = "rocket.png"
enemy = "ufo.png"
rocket = "bullet.png"

lost = 0
score = 0


#mixer.init()
#mixer.music.load("music.mp3")
#mixer.music.play()

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

win = font1.render("VICTORY", True, (0,255,0))
lose = font1.render("GAME OVER", True, (180,0,0))


class Game(sprite.Sprite):
    def __init__(self,player_img, px,py,size_x, size_y,ps):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_img), (size_x,size_y))
        self.speed = ps
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Play(Game):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed


        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(rocket, self.rect.centerx, self.rect.top, 15,20,-15)
        bullets.add(bullet)

class Bullet(Game):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
bullets = sprite.Group()
class Enemy(Game):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1
ship = Play(hero, 5,400,80,100,10)
monsters = sprite.Group()
for i in range(1,6):
    m = Enemy(enemy, randint(80,620), -40,80,50,randint(1,5))
    monsters.add(m)
finish = False
run = True
background = transform.scale(image.load(bg), (700,500))
num_fire = 0
real_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and real_time == False:
                    num_fire = num_fire+1
                    ship.fire()

                if num_fire >= 5 and real_time == False :
                    last_time = timer()
                    real_time = True
                    
    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Score:"+ str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text2 = font2.render("Lost:"+ str(lost), 1, (255,255,255))
        window.blit(text2, (10,50))        



        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()

        monsters.draw(window)
        bullets.draw(window)

        if real_time ==True:
            now_time = timer()

            if now_time - last_time <  1:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260,460))
            else: 
                num_fire = 0
                real_time = False

        if sprite.spritecollide(ship, monsters, False) or lost >=10:
            finish = True
            window.blit(lose, (200,200))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            m = Enemy(enemy, randint(80,620), -40,80,50,randint(1,5))
            monsters.add(m)

        if score >=  10:
            finish = True
            window.blit (win,(200,200))


        display.update()
    time.delay(20)