########################################################################
########################################################################
###                          _                     _                 ###
###                          (_)                   | |               ###
###  ___ _ __   __ _  ___ ___ _ _ ____   ____ _  __| | ___ _ __ ___  ###
### / __| '_ \ / _` |/ __/ _ \ | '_ \ \ / / _` |/ _` |/ _ \ '__/ __| ###
### \__ \ |_) | (_| | (_|  __/ | | | \ V / (_| | (_| |  __/ |  \__ \ ###   MADE BY: MAGUIRE HOUSE
### |___/ .__/ \__,_|\___\___|_|_| |_|\_/ \__,_|\__,_|\___|_|  |___/ ###
###     | |                                                          ###
###     |_|                                                          ###
########################################################################
########################################################################


#                            ##      ##        
#                          ##############
#                        ####  ######  ####
#                      ######################
#                      ##  ##############  ##     
#                      ##  ##          ##  ##
#                            ####  ####


import pygame
import time
import random
import math


### SOUNDS FROM https://www.classicgaming.cc/classics/space-invaders/sounds

class Star(object):
    def __init__(self, w):
        self.w = w
        self.x = random.randint(20,WIDTH-20)
        self.y = 0
    def draw(self, screen_param):
        self.y += 2
        pygame.draw.circle(screen_param, color.white, (self.x, self.y), self.w)

class Button(object):
    def __init__(self,x,y,w,h,c,text):
        self.rect = pygame.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = c
        self.txt = font.render(text, True, color.white)
        self.txt_center_pad = (w//2)-(len(text)*5)
        self.iterator = random.randint(0,100)
    def draw(self, screen_param):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (self.x+10, self.y+10, self.width-20, self.height-20))
        pygame.draw.rect(surface, self.color, self.rect, 20, 15)
        self.iterator += 3
        surface.blit(self.txt, (self.x+self.txt_center_pad,self.y+15))
        surface = pygame.transform.rotate(surface, math.sin(math.radians(self.iterator)))
        screen_param.blit(surface, (0,0))

class Color(object):
    """
    Shortcuts for basic RGB (r,g,b) values.
    """
    def __init__(self):
        self.red = (255,0,0)
        self.orange = (255,128,0)
        self.yellow = (255,255,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.purple = (153,0,153)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.light_black = (10,10,10)
        self.grey = (64,64,64)
        self.dark_grey = (32,32,32)
        self.dark_transparent_black = (64,64,64,175)
        self.light_transparent_black = (64,64,64,50)
        self.transparent_purple = (147,112,219,10)

class Ship(object):
    def __init__(self, img, health=3, damage=1, speed=1, bullet_count=1):
        self.health = health
        self.dmg = damage
        self.speed = speed
        self.bullets = bullet_count
        self.img = img
        self.score = 0
        self.x = WIDTH//2 - 50//2   # Finds the x-point at which the image will be centered on the screen
        self.y = HEIGHT-100
        self.rect = (self.x,self.y,50,50)
        self.bullets_shot = 0
        self.bullets_hit = 0
    def draw(self):
        self.rect = (self.x,self.y,50,50)
        screen.blit(self.img, (self.x,self.y))

class Key(object):
    def __init__(self):
        self.a = False
        self.d = False
        self.space = False

class Enemy(object):
    id = 0
    speed = 10
    movement_cooldown = 1
    delay = 1
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.img = img
        self.id = Enemy.id
        Enemy.id += 1
        self.rect = (self.x,self.y,self.w,self.h)
        self.moving_right = True
        self.moving_left = False
        self.dead = False
    def delete(self):
        i = 0
        for Enemy in enemies:
            if Enemy.id == self.id:
                self.dead = True
                enemy_death_sound.play()
                ship.score += 10 if self.id >= 8 else 20
                break
            i += 1
    def draw(self):
        if not self.dead:
            self.rect = (self.x,self.y,self.w,self.h)
            screen.blit(self.img, (self.x,self.y))
            if random.randint(1,5000) == 2:
                bullets.append(Bullet(is_enemy=True, enemy_id=self.id))
    def move(self):
        if not self.dead:
            if self.moving_right:
                self.x += Enemy.speed
            if self.moving_left:
                self.x -= Enemy.speed
            if self.y >= HEIGHT-200:
                results("You Lose")

class UFO(object):
    ufo_cooldown = 1
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.dead = True
        self.w = 100
        self.img = img
        self.h = 50
    def move(self):
        if not self.dead:
            self.x += 5
            if self.x >= WIDTH-20:
                self.dead = True
    def draw(self):
        self.rect = (self.x,self.y,self.w,self.h)
        if not self.dead:
            self.rect = (self.x,self.y,self.w,self.h)
            screen.blit(self.img, (self.x,self.y))

class Bullet(object):
    id = 0
    cooldown = 0
    def __init__(self, is_enemy=False, enemy_id=None):
        ## To get around the weird "not defined" thing
        if Bullet.id == 0:
            Bullet.cooldown = BULLET_COOLDOWN
        ##
        self.speed = BULLET_SPEED
        if not is_enemy:
            self.x = ship.x+25
            self.y = ship.y
            self.color = color.white
        elif is_enemy:
            self.x = enemies[enemy_id].x+25
            self.y = enemies[enemy_id].y+30
            self.color = color.green
        self.enemy = is_enemy
        self.flying = True
        self.id = Bullet.id
        Bullet.id += 1
        self.rect = pygame.Rect(self.x,self.y,10,10)
    def fly(self):
        if self.flying:
            self.rect = pygame.Rect(self.x,self.y,2,10)
            pygame.draw.rect(screen, self.color, self.rect)
            if not self.enemy:
                self.y -= self.speed
                self.collision_enemy()
            elif self.enemy:
                self.y += self.speed
                self.collision_player()
            self.collision_bunker()
            self.collision_ufo()
    def collision_enemy(self):
        if self.y <= 0:
            self.delete()
        else:
            for Enemy in enemies:
                if self.rect.colliderect(Enemy.rect):
                    if not Enemy.dead:
                        ship.bullets_hit += 1
                        Enemy.delete()
                        self.delete()
    def collision_player(self):
        if self.y >= HEIGHT:
            self.delete()
        else:
            if self.rect.colliderect(ship.rect):
                ship.health -= 1
                self.delete()
    def collision_bunker(self):
        for Bunker in bunkers:
            if self.rect.colliderect(Bunker.rect):
                if not Bunker.dead:
                    Bunker.health -= 1
                    self.delete()
    def collision_ufo(self):
        if not ufo.dead:
            if self.rect.colliderect(ufo.rect):
                ufo.dead = True
                ship.score += random.randint(50,200)
                enemy_death_sound.play()
                self.delete()
    def delete(self):
        i = 0
        for Bullet in bullets:
            if Bullet.id == self.id:
                del bullets[i]
                break
            i += 1

class Bunker(object):
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img_list = [scaled_bunker5,scaled_bunker4,scaled_bunker3,scaled_bunker2,scaled_bunker]
        self.img = self.img_list[0]
        self.health = 5
        self.rect = (self.x+63,self.y+81,79,50)
        self.dead = False
    def draw(self):
        if not self.dead:
            screen.blit(self.img, (self.x,self.y))
            self.img = self.img_list[self.health-1]
            if self.health <= 0:
                self.dead = True



def results(result):
    menu_music.stop() # Just in case
    music.stop()
    menu_music.play()
    win_screen = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    quit_button = Button(310, 350, 150, 60, color.black, "< Quit >")
    big_font = pygame.font.Font(None, 64)
    running = True
    while running:
        win_screen.fill(color.black)
        outline_effect(win_screen)
        display_text(result, color.white, 300, 100, big_font, win_screen)
        display_text(f"Score: {ship.score}", color.white, 350, 200, font, win_screen)
        display_text(f"Bullets Shot: {ship.bullets_shot}", color.white, 325, 230, font, win_screen)
        display_text(f"Bullet Accuracy: {round(ship.bullets_hit/ship.bullets_shot*100, 1)}%", color.white, 285, 260, font, win_screen)
        quit_button.draw(win_screen)
        stars(win_screen, stars_list)
        apply_crt_effect(win_screen)
        screen_real.blit(win_screen, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
        clock.tick(FPS)

def load_enemies(amount=40, spacing=20):
    list = []
    y = 100
    x = 1
    for i in range(amount):
        x += 1
        if x*50+(x*spacing) >= WIDTH-160:
            y += 60
            x = 2
        if y > 100:
            list.append(Enemy(scaled_enemy2, x*50+(x*spacing), y))
        else:
            list.append(Enemy(scaled_enemy1, x*50+(x*spacing), y))
    return list

def display_text(text, color, x, y, font, screen_param):
    new_text = font.render(text, False, color)
    screen_param.blit(new_text, (x,y))

def refresh_display():
    ship.score_txt = f"Score: {ship.score}                        Health: {ship.health}"
    screen.fill(color.black)
    stars(screen, stars_list)
    ship.draw()
    ufo.draw()
    ufo.move()
    for Bullet in bullets:
        Bullet.fly()
    for Enemy in enemies:
        Enemy.draw() 
    for Bunker in bunkers:
        Bunker.draw()
    outline_effect(screen)
    display_text(ship.score_txt, color.white, 30, 20, font, screen)
    apply_crt_effect(screen, intensity="medium", pixelation="minimum")
    screen_real.blit(screen, (0,0))
    pygame.display.flip()

def ship_movement():
    if key.a and ship.x >= 20:
        ship.x -= SPEED_BASE*ship.speed
    if key.d and ship.x <= WIDTH-70:
        ship.x += SPEED_BASE*ship.speed

def enemy_movement():
    if Enemy.movement_cooldown <= 0:
        for i in range(len(enemies)):
            enemies[i].move()
            if enemies[i].x >= WIDTH-80:
                for e in range(i):
                    enemies[e].x -= Enemy.speed
                enemies[i].x -= Enemy.speed
                for i in range(len(enemies)):
                    enemies[i].moving_right = False
                    enemies[i].moving_left = True
                    enemies[i].y += 10
                break
            if enemies[i].x <= 30:
                for e in range(len(enemies)-i):
                    enemies[e+i].x += Enemy.speed
                enemies[i].x += Enemy.speed
                for i in range(len(enemies)):
                    enemies[i].moving_right = True
                    enemies[i].moving_left = False
                    enemies[i].y += 10
                break
        Enemy.movement_cooldown = enemies[0].delay
    if ship.bullets_hit >= 30:
        Enemy.delay = 0.1
    elif ship.bullets_hit >= 25:
        Enemy.delay = 0.2
    elif ship.bullets_hit >= 20:
        Enemy.delay = 0.4
    elif ship.bullets_hit >= 15:
        Enemy.delay = 0.6
    elif ship.bullets_hit >= 10:
        Enemy.delay = 0.8

def cooldown():
    if Bullet.cooldown > 0:
        Bullet.cooldown -= 1/(FPS*BULLET_COOLDOWN)
    if Enemy.movement_cooldown > 0:
        Enemy.movement_cooldown -= 1/(FPS*Enemy.delay)
    
    ## UFO spawns every {UFO_COOLDOWN} seconds
    UFO.ufo_cooldown -= 1/(FPS*UFO_COOLDOWN)
    if UFO.ufo_cooldown <= 0 and UFO.ufo_cooldown >= -0.1:
        ufo.dead = False

def event_checker():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key.a = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key.d = True
                if event.key == pygame.K_SPACE:
                    key.space = True
                if event.key == pygame.K_F10 or event.key == pygame.K_BACKSLASH:
                    results("You Lose")
                if event.key == pygame.K_F11 or event.key == pygame.K_BACKSPACE:
                    results("You Win!")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key.a = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key.d = False
                if event.key == pygame.K_SPACE:
                    key.space = False
                    if Bullet.cooldown <= 0:
                        bullets.append(Bullet())
                        ship.bullets_shot += 1
                        bullet_sound.play()
                        Bullet.cooldown = BULLET_COOLDOWN
    if ship.health <= 0:
        results("You Lose")
    elif ship.bullets_hit > 31 or (ship.bullets_hit == 31 and ship.score == 400):
        results("You Win!")

def main():
    running = True
    while running:
        event_checker()
        ship_movement()
        enemy_movement()
        cooldown()
        refresh_display()
        clock.tick(FPS)

def stars(screen_param, stars):
    for e in range(random.randint(0,10)):
        if random.randint(1,50) == 2:
            stars.append(Star(1))
    for i in range(len(stars)):
        stars[i].draw(screen_param)

def outline_effect(screen_param):
    pygame.draw.rect(outline, color.light_transparent_black, (0,0,WIDTH,HEIGHT), 10, 70)
    pygame.draw.rect(outline, color.dark_transparent_black, (0,0,WIDTH,HEIGHT), 10, 50)
    pygame.draw.rect(outline, color.dark_grey, (0,0,WIDTH,HEIGHT), 10, 30)
    pygame.draw.rect(outline, color.dark_grey, (0,0,WIDTH,HEIGHT), 10)
    screen_param.blit(outline, (0,0))

def start_screen(stars_param):
    start_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    start_button = Button(300, 425, 200, 50, color.black, "< Start >")
    quit_button = Button(300, 475, 200, 50, color.black, "< Quit >")
    difficulty_left = Button(300, 525, 50, 50, color.black, "<<" )
    difficulty_right = Button(440, 525, 50, 50, color.black, ">>" )
    difficulty_txt = ["   Easy", "Normal", "   Hard"]
    difficulty = 2
    running = True
    while running:
        start_screen.fill(color.black)
        start_button.draw(start_screen)
        quit_button.draw(start_screen)
        display_text(difficulty_txt[difficulty-1], color.white, 360, 545, font, start_screen)
        difficulty_left.draw(start_screen)
        difficulty_right.draw(start_screen)
        outline_effect(start_screen)
        stars(start_screen, stars_param)
        start_screen.blit(scaled_logo, (200,50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    if difficulty == 1:
                        ship.health = 3
                    elif difficulty == 2:
                        ship.health = 2
                    else:
                        ship.health = 1
                    return
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if difficulty_right.rect.collidepoint(event.pos):
                    difficulty += 1
                    if difficulty > 3:
                        difficulty = 0
                if difficulty_left.rect.collidepoint(event.pos):
                    difficulty -= 1
                    if difficulty < 1:
                        difficulty = 3
        apply_crt_effect(start_screen, intensity="medium", pixelation="minimum")
        screen_real.blit(start_screen, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

def load_bunkers():
    bunkers = []
    for i in range(4):
        bunkers.append(Bunker(i*(200), HEIGHT-250, scaled_bunker))
    return bunkers




### Copied CRT effect from Chris Greening: 
##### https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1
def apply_crt_effect(screen, intensity="medium", pixelation="minimum"):
    apply_scanlines(screen)
    apply_pixelation(screen, pixelation)
    if Bullet.cooldown >= -.9:
        apply_flicker(screen)
    apply_glow(screen)
    add_glitch_effect(HEIGHT,WIDTH,screen,intensity)
    add_color_separation(screen, screen, intensity)

def apply_scanlines(screen):
    width, height = screen.get_size()
    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(0, height, 4):
        pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))

    screen.blit(scanline_surface, (0, 0))

def apply_pixelation(screen, pixelation):
    pixelation = {"minimum": 2, "medium": 4, "maximum": 6}.get(pixelation, 2)
    width, height = screen.get_size()
    small_surf = pygame.transform.scale(screen, (width // pixelation, height // pixelation))
    screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))

def apply_flicker(screen):
    if random.randint(0, 20) == 0:
        flicker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        flicker_surface.fill((255, 255, 255, 5))
        screen.blit(flicker_surface, (0, 0))

def apply_glow(screen):
    width, height = screen.get_size()
    glow_surf = pygame.transform.smoothscale(screen, (width // 2, height // 2))
    glow_surf = pygame.transform.smoothscale(glow_surf, (width, height))
    glow_surf.set_alpha(100)
    screen.blit(glow_surf, (0, 0))

def add_glitch_effect(height, width, glitch_surface, intensity):
    shift_amount = {"minimum": 10, "medium": 20, "maximum": 40}.get(intensity, 20)
    if random.random() < 0.1:
        y_start = random.randint(0, height - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = pygame.Rect(0, y_start, width, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))

def add_color_separation(screen, glitch_surface, intensity):
    color_shift = {"minimum": 2, "medium": 6, "maximum": 10}.get(intensity, 4)
    if random.random() < 0.001:
        for i in range(3):
            x_offset = random.randint(-color_shift, color_shift)
            y_offset = random.randint(-color_shift, color_shift)
            color_shift_surface = glitch_surface.copy()
            color_shift_surface.fill((0, 0, 0))
            color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
            screen.blit(color_shift_surface, (0, 0), special_flags=pygame.BLEND_ADD)


pygame.init()
pygame.mixer.init()

SPEED_BASE = 5
WIDTH = 800
HEIGHT = 600
FPS = 60
BULLET_SPEED = 10
BULLET_COOLDOWN = 0.5
SOUND_VOLUME = 25
UFO_COOLDOWN = random.randint(10,20)

media_path = "games/"

### SOUND FX AND MUSIC
bullet_sound = pygame.mixer.Sound(f"{media_path}Invaders_Media/shoot.wav")
enemy_death_sound = pygame.mixer.Sound(f"{media_path}Invaders_Media/invaderkilled.wav")
ship_death_sound = pygame.mixer.Sound(f"{media_path}Invaders_Media/explosion.wav")
music = pygame.mixer.Sound(f"{media_path}Invaders_Media/music.mp3")
menu_music = pygame.mixer.Sound(f"{media_path}Invaders_Media/menu.mp3")

### ADJUST VOLUME
bullet_sound.set_volume(SOUND_VOLUME/100)
enemy_death_sound.set_volume(SOUND_VOLUME/100)
ship_death_sound.set_volume(SOUND_VOLUME/100)
music.set_volume(SOUND_VOLUME/100)
menu_music.set_volume(SOUND_VOLUME/50)

### LOAD IMAGES
ship_image = pygame.image.load(f"{media_path}Invaders_Media/ship.png")
enemy1_image = pygame.image.load(f"{media_path}Invaders_Media/enemy1.png")
enemy2_image = pygame.image.load(f"{media_path}Invaders_Media/enemy2.png")
ufo_image = pygame.image.load(f"{media_path}Invaders_Media/ufo.png")
logo_image = pygame.image.load(f"{media_path}Invaders_Media/logo.png")
bunker_image = pygame.image.load(f"{media_path}Invaders_Media/bunker.png")
bunker_slight_dmg_image = pygame.image.load(f"{media_path}Invaders_Media/bunker1.png")
bunker_damaged_image = pygame.image.load(f"{media_path}Invaders_Media/bunker2.png")
bunker_heavy_damage_image = pygame.image.load(f"{media_path}Invaders_Media/bunker3.png")
bunker_near_death_image = pygame.image.load(f"{media_path}Invaders_Media/bunker4.png")

### TRANSFORM IMAGES
scaled_ship = pygame.transform.scale(ship_image, (50,50))
scaled_enemy1 = pygame.transform.scale(enemy1_image, (50,50))
scaled_enemy2 = pygame.transform.scale(enemy2_image, (50,50))
scaled_ufo = pygame.transform.scale(ufo_image, (100,50))
scaled_logo = pygame.transform.scale(logo_image, (400,200))
scaled_bunker = pygame.transform.scale(bunker_image, (200,200))
scaled_bunker2 = pygame.transform.scale(bunker_slight_dmg_image, (200,200))
scaled_bunker3 = pygame.transform.scale(bunker_damaged_image, (200,200))
scaled_bunker4 = pygame.transform.scale(bunker_heavy_damage_image, (200,200))
scaled_bunker5 = pygame.transform.scale(bunker_near_death_image, (200,200))
icon_image = scaled_ship

## OBJECT LISTS
bullets = []
stars_list = []
bunkers = load_bunkers()
enemies = load_enemies(amount=32)

## Screen and objects
font = pygame.font.Font(None, 32)
pygame.display.set_icon(icon_image)
screen_real = pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Space Invaders")



ship = Ship(scaled_ship)
outline = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
color = Color()
key = Key()
clock = pygame.time.Clock()
ufo = UFO(scaled_ufo, -20, 30)



menu_music.play()
start_screen(stars_list)
menu_music.stop()
music.play()

if __name__ == "__main__":
    main()
