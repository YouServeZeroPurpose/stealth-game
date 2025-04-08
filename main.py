import pygame
import time
from levels import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()
window_width, window_height = 512, 512

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Don't get caught! (Demo)")

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.hitbox = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.hitbox.x, self.hitbox.y))
        # pygame.draw.rect(window, (100, 0, 200), self.hitbox, 3)

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed, images):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.images = []
        for img in images:
            img = pygame.transform.scale(img, (w, h))
            self.images.append(img)
        self.state = 'standing'
        self.img_num = 0
        self.anim_timer = 1
        self.direction = 'up'
        self.prev_walk = 2
    
    def move(self, w, a, s, d):
        keys = pygame.key.get_pressed()

        new_x, new_y = self.hitbox.x, self.hitbox.y

        if keys[w]:
            new_y -= self.speed
            self.direction = 'up'
        if keys[a]:
            new_x -= self.speed
            self.direction = 'left'
        if keys[s]:
            new_y += self.speed
            self.direction = 'down'
        if keys[d]:
            new_x += self.speed
            self.direction = 'right'

        new_hitbox = pygame.Rect(new_x, new_y, self.hitbox.width, self.hitbox.height)

        colliding = any(new_hitbox.colliderect(wall.hitbox) for wall in walls)

        if not colliding:
            self.hitbox.x, self.hitbox.y = new_x, new_y

        if keys[w] or keys[a] or keys[s] or keys[d]:
            self.state = 'walking'
        else:
            self.state = 'standing'

    def animate(self):
        if self.anim_timer == 0:
            if self.state == 'walking':
                if self.img_num == 0:
                    self.img_num = 1
                    self.prev_walk = 0
                elif self.img_num == 2:
                    self.img_num = 1
                    self.prev_walk = 2
                elif self.img_num == 1:
                    if self.prev_walk == 0:
                        self.img_num = 2 
                    elif self.prev_walk == 2:
                        self.img_num = 0
            else:
                self.img_num = 1
            current_frame = self.images[self.img_num]

            if self.direction == 'down':
                current_frame = pygame.transform.flip(current_frame, False, True)

            elif self.direction == 'right':
                current_frame = pygame.transform.rotate(current_frame, 270)

            elif self.direction == 'left':
                current_frame = pygame.transform.rotate(current_frame, 90)

            self.image = current_frame
            self.anim_timer = 6
        else:
            self.anim_timer -= 1



class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed, images):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.direction = 0
        self.steps = 0
        self.images = []
        self.images.append(pygame.transform.scale(images[0], (w, h)))
        self.images.append(pygame.transform.scale(images[1], (h, w)))
        self.images.append(pygame.transform.scale(images[2], (w, h)))
        self.images.append(pygame.transform.scale(images[3], (h, w)))

        self.og_h, self.og_w = w, h
        self.og_x = self.hitbox.x

        self.image = self.images[0]
    
    def move(self):
        if self.direction == 0:
            self.hitbox.y -= self.speed
            self.image = self.images[0]
            self.hitbox.update(self.og_x, self.hitbox.y, self.og_h, self.og_w)

        elif self.direction == 1: 
            self.hitbox.x += self.speed
            self.image = self.images[1]
            self.hitbox.update(self.hitbox.x, self.hitbox.y, self.og_w, self.og_h)

        elif self.direction == 2:
            self.hitbox.y += self.speed
            self.image = self.images[2]
            self.hitbox.update(self.hitbox.x, self.hitbox.y, self.og_h, self.og_w)

        elif self.direction == 3: 
            self.hitbox.x -= self.speed
            self.image = self.images[3]
            self.hitbox.update(self.hitbox.x, self.hitbox.y, self.og_w, self.og_h)
        
        self.steps += self.speed

        if self.steps >= 160:
            self.steps = 0

            if self.direction == 0:
                self.hitbox.y += 53
                self.hitbox.x += 8

            elif self.direction == 1:
                self.hitbox.x -= 8
                self.hitbox.y += 8

            elif self.direction == 2:
                self.hitbox.x -= 53
                self.hitbox.y -= 8

            elif self.direction == 3:
                self.hitbox.y -= 53

            self.direction = (self.direction + 1) % 4

class Laser(Sprite):
    def __init__(self, x, y, w, h, image, images):
        super().__init__(x, y, w, h, image)
        self.images = []
        for img in images:
            img = pygame.transform.scale(img, (w, h))
            self.images.append(img)
        self.anim_index = 0
        self.anim_timer = 0
        self.delay = 250
        self.state = 'off'
        self.image = self.images[self.anim_index]

    def animate(self):
        if self.anim_timer <= 0 and self.delay <= 0:
            if self.state == 'on':
                self.anim_index -= 1
                if self.anim_index <= 0: 
                    self.anim_index = 0
                    self.state = 'off'
                    self.delay = 250

            elif self.state == 'off':
                self.anim_index += 1
                if self.anim_index >= len(laser_images) - 1:
                    self.anim_index = len(laser_images) - 1
                    self.state = 'on'
                    self.delay = 250

            self.image = self.images[self.anim_index]
            self.anim_timer = 10
        else:
            self.anim_timer -= 1
            self.delay -= 1




player_images = [pygame.image.load('player_walk1.png'), pygame.image.load('player_stand.png'), pygame.image.load('player_walk2.png')]
laser_images = [pygame.image.load('laser_off.png'), pygame.image.load('laser_on1.png'), pygame.image.load('laser_on2.png'), pygame.image.load('laser_on3.png'), pygame.image.load('laser_on4.png')]
enemy_images = [pygame.image.load('policeman_up.png'), pygame.image.load('policeman_right.png'), pygame.image.load('policeman_down.png'), pygame.image.load('policeman_left.png')] 

floor_img = pygame.image.load('floor_tile.png')
floor_img = pygame.transform.scale(floor_img, (window_width, window_height))

wall_img = pygame.image.load('wall_tile.png')
key_img = pygame.image.load('key.png')
door_img = pygame.image.load('door.png')

player_speed = 3
enemy_speed = 3

player_size = 30

wall_size = 32
walls = []

enemy_w, enemy_h = 48, 92
enemies = []

laser_w, laser_h = 64, 16
lasers = []

x, y = 0, 0

player_x, player_y = 0, 0

for row in lvl1:
    for p in str(row):
        if p == '1':
            walls.append(Sprite(x, y, wall_size, wall_size, wall_img))
        elif p == '9':
            player_x, player_y = x + 16, y + 16
        elif p == '2':
            enemies.append(Enemy((x + 8), (y - 45), enemy_w, enemy_h, enemy_images[0], enemy_speed, enemy_images))
        elif p == '3':
            lasers.append(Laser(x, (y + 8), laser_w, laser_h, laser_images[0], laser_images))

        x += wall_size
    x = 0
    y += wall_size

game = True

start = False
win = False
death = False

player = Player(player_x, player_y, player_size, player_size, player_images[1], player_speed, player_images)

while game:   
    window.blit(floor_img, (0, 0))

    player.draw()
    player.move(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)
    player.animate()

    for e in enemies:
        e.draw()
        e.move()

        if player.hitbox.colliderect(e.hitbox):
            print('touching enemy')

    for l in lasers:
        l.draw()
        l.animate()

        if player.hitbox.colliderect(l.hitbox) and l.image == l.images[4]:
            print('touching laser')

    for w in walls:
        w.draw()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

    pygame.display.update()
    clock.tick(FPS)