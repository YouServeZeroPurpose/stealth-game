import pygame
import time
from levels import *

pygame.init()

FPS = 60
clock = pygame.time.Clock()
window_width, window_height = 512, 512

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Don't get caught! (Demo)")

font = pygame.font.SysFont('Midnight Letters', 35)
big_font = pygame.font.SysFont('Midnight Letters', 60)

menu = pygame.image.load('floor_tile.png')
menu = pygame.transform.scale(menu, (window_width, window_height))

menu_lb = font.render("Don't get caught!", True, (0, 0, 0))
menu_lb_start = big_font.render('Start!', True, (0, 0, 0), (0, 200, 0))

with open('cur_level.txt', 'r') as file:
    try:
        cur_lvl = file.read()
    except:
        cur_lvl = 0

menu_lb_lvl = font.render(f'Current level: {cur_lvl}', True, (0, 0, 0))

pause_lb = big_font.render('Pause', True, (0, 0, 0))
menu_btn_lb = font.render('press space to go to menu', True, (0, 0, 0))

lose_lb = big_font.render('You died!', True, (255, 0, 0))

win_lb = big_font.render('You won!', True, (0, 255, 0))
next_lvl_lb = font.render('click to go to next lvl', True, (0, 0, 0))

end_lb = font.render('End of demo!', True, (0, 0, 0))
end_lb_thx = font.render('Thanks for playing :)', True, (0, 0, 0))
end_lb_reset = font.render('press space to reset', True, (0, 0, 0), (200, 0, 0))

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
        self.has_key = False
    
    def move(self, w, a, s, d):
        global vault_door
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

        colliding_walls = any(new_hitbox.colliderect(wall.hitbox) for wall in walls)
        
        if not self.has_key:
            colliding_door = new_hitbox.colliderect(vault_door.hitbox)
        else:
            colliding_door = new_hitbox.colliderect(key.hitbox)

        if not colliding_walls and not colliding_door:
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
        self.delay = 100
        self.state = 'off'
        self.image = self.images[self.anim_index]

    def animate(self):
        if self.anim_timer <= 0 and self.delay <= 0:
            if self.state == 'on':
                self.anim_index -= 1
                if self.anim_index <= 0: 
                    self.anim_index = 0
                    self.state = 'off'
                    self.delay = 100

            elif self.state == 'off':
                self.anim_index += 1
                if self.anim_index >= len(laser_images) - 1:
                    self.anim_index = len(laser_images) - 1
                    self.state = 'on'
                    self.delay = 100

            self.image = self.images[self.anim_index]
            self.anim_timer = 10
        else:
            self.anim_timer -= 1
            self.delay -= 1

def lineOfSight(enemy, player, walls):
    start = enemy.hitbox.center
    end = player.hitbox.center

    for w in walls:
        if w.hitbox.clipline(start, end):
            return False
    return True


player_images = [pygame.image.load('player_walk1.png'), pygame.image.load('player_stand.png'), pygame.image.load('player_walk2.png')]
enemy_images = [pygame.image.load('policeman_up.png'), pygame.image.load('policeman_right.png'), pygame.image.load('policeman_down.png'), pygame.image.load('policeman_left.png')] 

laser_images = [pygame.image.load('laser_off.png'), pygame.image.load('laser_on1.png'), pygame.image.load('laser_on2.png'), pygame.image.load('laser_on3.png'), pygame.image.load('laser_on4.png')]
side_laser_images = []

for _ in range(len(laser_images)):
    side_laser_images.append(pygame.transform.rotate(laser_images[(_)], 90))

floor_img = pygame.image.load('floor_tile.png')
floor_img = pygame.transform.scale(floor_img, (window_width, window_height))

wall_img = pygame.image.load('wall_tile.png')
key_img = pygame.image.load('key.png')
door_img = pygame.image.load('door.png')
money_img = pygame.image.load('money.png')

player_speed = 3
enemy_speed = 3

player_size = 30

door_w, door_h = 64, 20
money_size = 64

wall_size = 32
walls = []

enemy_w, enemy_h = 48, 92
enemies = []

laser_w, laser_h = 64, 16
lasers = []

x, y = 0, 0

player_x, player_y = 0, 0
key_x, key_y = 0, 0
door_x, door_y = 0, 0
money_x, money_y = 0, 0

game = True

start = False
win = False
finish = False
pause = False

def pauseGame():
    global pause
    if pause:
        pause = False
    else:
        pause = True

def returnToMenu():
    global start, win, finish, pause, player, level_start, x, y, enemies, lasers, walls, level_number, level_count

    x, y = 0, 0

    start = False
    win = False
    finish = False
    pause = False
    player.has_key = False
    level_start = True
    level_number = True
    level_count = True

    enemies.clear()
    lasers.clear()
    walls.clear()

    with open('cur_level.txt', 'w') as file:
        file.write(str(cur_lvl))

def nextLevel():
    global start, win, finish, pause, player, level_start, x, y, enemies, lasers, walls, level_number, level_count

    x, y = 0, 0

    start = True
    win = False
    finish = False
    pause = False
    player.has_key = False
    level_start = True
    level_number = True
    level_count = True

    enemies.clear()
    lasers.clear()
    walls.clear()

    with open('cur_level.txt', 'w') as file:
        file.write(str(cur_lvl))

def RESET():
    global start, win, finish, pause, player, level_start, x, y, enemies, lasers, walls, menu_lb_lvl, cur_lvl, level_number, level_count

    x, y = 0, 0

    start = False
    win = False
    finish = False
    pause = False
    player.has_key = False
    level_start = True
    level_number = True
    level_count = True

    enemies.clear()
    lasers.clear()
    walls.clear()

    with open('cur_level.txt', 'w') as file:
        file.write('1')

    cur_lvl = 1

level_start = True
level_count = True
level_number = True

cur_lvl = 0

with open('cur_level.txt', 'r') as file:
    try:
        cur_lvl = int(file.read())
    except:
        cur_lvl = 1

while game:
    if not start:
        window.blit(menu, (0, 0))
        window.blit(menu_lb, (80, 150))
        window.blit(menu_lb_start, (152, 250))

        if level_number:
            with open('cur_level.txt', 'r') as file:
                try:
                    cur_lvl = int(file.read())
                except:
                    cur_lvl = 1
                menu_lb_lvl = font.render(f'Current level: {cur_lvl}', True, (0, 0, 0))
            level_number = False
        window.blit(menu_lb_lvl, (100, 350))

    else:
        if not finish:
            if level_start:
                cur_lvl_name = 'lvl' + str(cur_lvl)

                for row in levels[cur_lvl_name]:
                    for p in str(row):
                        if p == '1':
                            walls.append(Sprite(x, y, wall_size, wall_size, wall_img))
                        elif p == '8':
                            player_x, player_y = x + 16, y + 16
                        elif p == '2':
                            enemies.append(Enemy((x + 8), (y - 45), enemy_w, enemy_h, enemy_images[0], enemy_speed, enemy_images))
                        elif p == '3':
                            lasers.append(Laser(x, (y + 8), laser_w, laser_h, laser_images[0], laser_images))
                        elif p == '4':
                            lasers.append(Laser((x + 8), y, laser_h, laser_w, side_laser_images[0], side_laser_images))
                        elif p == '5':
                            key_x, key_y = x, y
                        elif p == '6':
                            door_x, door_y = x, (y + 6)
                        elif p == '7':
                            money_x, money_y = x, y

                        x += wall_size
                    x = 0
                    y += wall_size 

                    
                player = Player(player_x, player_y, player_size, player_size, player_images[1], player_speed, player_images)

                key = Sprite(key_x, key_y, wall_size, wall_size, key_img)
                vault_door = Sprite(door_x, door_y, door_w, door_h, door_img)
                money = Sprite(money_x, money_y, money_size, money_size, money_img)

                level_start = False

            if not pause: 
                window.blit(floor_img, (0, 0))

                key.draw()
                vault_door.draw()
                money.draw()

                player.draw()
                player.move(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)
                player.animate()

                if player.hitbox.colliderect(key.hitbox):
                    player.has_key = True
                    key = Sprite(-100, -100, wall_size, wall_size, key_img)

                if player.hitbox.colliderect(vault_door.hitbox) and player.has_key:
                    player.has_key = False
                    vault_door = Sprite(-150, -150, door_w, door_h, door_img)

                if player.hitbox.colliderect(money.hitbox):
                    win = True
                    finish = True

                for e in enemies:
                    e.draw()
                    e.move()

                    if e.hitbox.colliderect(player.hitbox):
                        if lineOfSight(e, player, walls):
                            finish = True

                for l in lasers:
                    l.draw()
                    l.animate()

                    if player.hitbox.colliderect(l.hitbox) and l.image == l.images[4]:
                        finish = True

                for w in walls:
                    w.draw()
            
            else:
                window.blit(pause_lb, (155, 150))
                window.blit(menu_btn_lb, (0, 250))

    
        else:
            if win:
                if level_count:
                    cur_lvl += 1
                    if cur_lvl <= 4:
                        window.blit(win_lb, (118, 150))
                        window.blit(next_lvl_lb, (24, 250))

                    else:
                        window.blit(menu, (0, 0))
                        window.blit(end_lb, (154, 150))
                        window.blit(end_lb_thx, (48, 250))
                        window.blit(end_lb_reset, (50, 350))
                    
                    level_count = False

            else:
                window.blit(lose_lb, (102, 150))
                window.blit(menu_btn_lb, (0, 250))
                


    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and not start:
                start = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pauseGame()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and pause or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish and not win:
                returnToMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and win and cur_lvl <= 4:
                nextLevel()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and win and cur_lvl == 5:
                RESET()

                

    pygame.display.update()
    clock.tick(FPS)