import pygame
import time
import random
import math


### SOUNDS FROM https://www.classicgaming.cc/classics/space-invaders/sounds


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
        self.grey = (64,64,64)
        self.dark_grey = (32,32,32)
        self.dark_transparent_black = (0,0,0,175)
        self.light_transparent_black = (0,0,0,50)
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
                ship.score += 10
                break
            i += 1
    def draw(self):
        if not self.dead:
            self.rect = (self.x,self.y,self.w,self.h)
            screen.blit(self.img, (self.x,self.y))
            if random.randint(1,1000) == 2:
                bullets.append(Bullet(is_enemy=True, enemy_id=self.id))
    def move(self):
        if not self.dead:
            if self.moving_right:
                self.x += Enemy.speed
            if self.moving_left:
                self.x -= Enemy.speed
     
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
    def collision_enemy(self):
        if self.y <= 0:
            self.delete()
        else:
            for Enemy in enemies:
                if self.rect.colliderect(Enemy.rect):
                    if not Enemy.dead:
                        Enemy.delete()
                        self.delete()
    def collision_player(self):
        if self.y >= HEIGHT:
            self.delete()
        else:
            if self.rect.colliderect(ship.rect):
                ship.health -= 1
                self.delete()
                
    def delete(self):
        i = 0
        for Bullet in bullets:
            if Bullet.id == self.id:
                del bullets[i]
                break
            i += 1



def lose():
    font = pygame.font.Font(None, 128)
    ship_death_sound.play()
    screen.fill(color.grey)
    display_text("You Lose", color.red, 200, 230, font)
    outline_effect()
    apply_crt_effect(screen)
    screen_real.blit(screen, (0,0))
    pygame.display.flip()
    time.sleep(2)
    quit()

def win():
    print("win")

def load_enemies(amount=40, spacing=20):
    list = []
    y = 100
    x = 1
    for i in range(amount):
        x += 1
        if x*50+(x*spacing) >= WIDTH-160:
            y += 60
            x = 2
        list.append(Enemy(scaled_enemy, x*50+(x*spacing), y))
    return list

def display_text(text, color, x, y, font):
    new_text = font.render(text, False, color)
    screen.blit(new_text, (x,y))

def refresh_display():
    ship.score_txt = f"Score: {ship.score}"
    screen.fill(color.dark_grey)
    ship.draw()
    for Bullet in bullets:
        Bullet.fly()
    for Enemy in enemies:
        Enemy.draw() 
    outline_effect()
    display_text(ship.score_txt, color.white, 30, 20, font)
    apply_crt_effect(screen, intensity="medium", pixelation="minimum")
    screen_real.blit(screen, (0,0))
    pygame.display.flip()

def ship_movement():
    if key.a:
        ship.x -= SPEED_BASE*ship.speed
    if key.d:
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
                    enemies[i].y += 60
                break
            if enemies[i].x <= 30:
                for e in range(len(enemies)-i):
                    enemies[e+i].x += Enemy.speed
                enemies[i].x += Enemy.speed
                for i in range(len(enemies)):
                    enemies[i].moving_right = True
                    enemies[i].moving_left = False
                    enemies[i].y += 60
                break
        Enemy.movement_cooldown = ENEMY_MOVEMENT_DELAY

def cooldown():
    if Bullet.cooldown > 0:
        Bullet.cooldown -= 1/(FPS*BULLET_COOLDOWN)
    if Enemy.movement_cooldown > 0:
        Enemy.movement_cooldown -= 1/(FPS*ENEMY_MOVEMENT_DELAY)

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
                if event.key == pygame.K_F10:
                    lose()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key.a = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key.d = False
                if event.key == pygame.K_SPACE:
                    key.space = False
                    if Bullet.cooldown <= 0:
                        bullets.append(Bullet()) 
                        bullet_sound.play()
                        Bullet.cooldown = BULLET_COOLDOWN
    if ship.health <= 0:
        lose()
    elif enemies == []:
        win()

def main():
    running = True
    while running:
        event_checker()
        ship_movement()
        enemy_movement()
        cooldown()
        refresh_display()
        clock.tick(FPS)

def outline_effect():
    pygame.draw.rect(outline, color.light_transparent_black, (0,0,WIDTH,HEIGHT), 10, 70)
    pygame.draw.rect(outline, color.dark_transparent_black, (0,0,WIDTH,HEIGHT), 10, 50)
    pygame.draw.rect(outline, color.black, (0,0,WIDTH,HEIGHT), 10, 30)
    pygame.draw.rect(outline, color.black, (0,0,WIDTH,HEIGHT), 10)


    screen.blit(outline, (0,0))

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
ENEMY_MOVEMENT_DELAY = 1



### SOUND FX AND MUSIC
bullet_sound = pygame.mixer.Sound("Invaders_Media/shoot.wav")
enemy_death_sound = pygame.mixer.Sound("Invaders_Media/invaderkilled.wav")
ship_death_sound = pygame.mixer.Sound("Invaders_Media/explosion.wav")
music = pygame.mixer.Sound("Invaders_Media/music.mp3")

### ADJUST VOLUME
bullet_sound.set_volume(SOUND_VOLUME/100)
enemy_death_sound.set_volume(SOUND_VOLUME/100)
ship_death_sound.set_volume(SOUND_VOLUME/100)
music.set_volume(SOUND_VOLUME/100)

### LOAD IMAGES
ship_image = pygame.image.load("Invaders_Media/ship.png")
enemy_image = pygame.image.load("Invaders_Media/enemy.png")

### TRANSFORM IMAGES
scaled_ship = pygame.transform.scale(ship_image, (50,50))
scaled_enemy = pygame.transform.scale(enemy_image, (50,50))
icon_image = scaled_ship
ship = Ship(scaled_ship)

## OBJECT LISTS
bullets = []
enemies = load_enemies(amount=32)

## Screen and objects
font = pygame.font.Font(None, 32)
pygame.display.set_icon(icon_image)
screen_real = pygame.display.set_mode((WIDTH,HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Galaxy Conquerors")


outline = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
color = Color()
key = Key()
clock = pygame.time.Clock()

music.play()
main()
