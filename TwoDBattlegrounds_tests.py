#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import sys, random, math, pygame
from pygame.locals import *
from pygame.sprite import *
from load import *
from menu import home
from clases import *
from functions import *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Clases
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Player(Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.life = 100
        self.image = pygame.image.load("graphics/player_0_w0.png").convert()
        self.degrees = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.initial_posx = x
        self.initial_posy = y
        self.rect.centerx = x
        self.rect.centery = y
        self.walk = 0
        self.ammo = {"Light": 0, "Medium": 0, "Heavy": 0, "Cartridge": 0}
        self.guns = [Guns("Knife", None, "pistol", 50, 1, 1, 30, 0, 1, (0, 0))]

    def animation(self):
        if self.degrees < 45 or self.degrees >= 315:
            self.degrees = 0
        elif self.degrees < 135 and self.degrees >= 45:
            self.degrees = 90
        elif self.degrees < 225 and self.degrees >= 135:
            self.degrees = 180
        elif self.degrees < 315 and self.degrees >= 225:
            self.degrees = 270

        self.image = load_image("graphics/player_" + str(self.degrees) + "_w" + str(self.walk) + ".png", True)
        return

    def pickup_gun(self, gun):
        if len(self.guns) < 4:
            self.guns.append(Guns(gun[0], gun[1], gun[2], gun[3], gun[4], gun[5], gun[6], gun[7], gun[8], gun[9]))
            return True
        return False

    def pickup_ammo(self, ammo):
        self.ammo[ammo[0]] += ammo[1]

class Zombie(Sprite):
    def __init__(self, name, x, y, path):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.life = 100
        self.damage = 15
        self.path = path
        self.image = load_image(path + "_0.png", True)
        self.degrees = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.initial_posx = x
        self.initial_posy = y
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = 0
        self.dy = 0
        self.hitting_speed = 30
        self.hitting_time = 0

    def update(self):
        self.rect.centerx = self.initial_posx + playerx
        self.rect.centery = self.initial_posy + playery

    def animation(self, degrees):
        if self.degrees < 45 or self.degrees >= 315:
            self.degrees = 0
        elif self.degrees < 135 and self.degrees >= 45:
            self.degrees = 90
        elif self.degrees < 225 and self.degrees >= 135:
            self.degrees = 180
        elif self.degrees < 315 and self.degrees >= 225:
            self.degrees = 270

        self.image = load_image(self.path + "_" + str(self.degrees) + ".png", True)
        return

    def ai(self, player):
        radians = math.atan2(HH - self.rect.centery, HW - self.rect.centerx)
        self.animation(degrees(radians))
        self.dx = math.cos(radians)
        self.dy = math.sin(radians)

        self.initial_posx += self.dx
        self.update()
        if self.wall_collide():
            self.initial_posx -= self.dx

        self.initial_posy += self.dy
        self.update()
        if self.wall_collide():
            self.initial_posy -= self.dy

    def wall_collide(self):
        for object in spritecollide(self, map, False):
            if not object.name == "Spawn Wall" and "Wall" in object.name:
                return True
        return False

    def hitting(self, player):
        if collide_rect(player, self) and self.hitting_time == 0:
            player.life -= self.damage
            self.hitting_time = self.hitting_speed
        elif self.hitting_time > 0:
            self.hitting_time -= 1

class Zombies(Group):
    def update(self, player):
        for zombie in self:
            zombie.ai(player)
            zombie.hitting(player)
            SCREEN.blit(zombie.image, zombie.rect)

class Guns(Sprite):
    def __init__(self, name, ammo, shot_sound, damage, maxCharger, charger, shotingTime, reloadTime, distance, deviation):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.animation = ""#[pygame.image.load(image).convert(), 0]
        self.damage = damage
        self.ammo = ammo
        self.maxCharger = charger
        self.charger = charger
        self.shotingTime = shotingTime
        self.reloadTime = reloadTime
        self.reloading = 0
        self.distance = distance
        self.deviation = deviation
        self.shot_sound = shot_sound

    def shoting(self, radians):
        global shotTime, bullets
        MULTIPLIER = 40
        shotTime = self.shotingTime
        distance = self.distance
        if self.name == "Shotgun":
            dx = math.cos(radians) * MULTIPLIER  - math.sin(radians) * 8
            dy = math.sin(radians) * MULTIPLIER  + math.cos(radians) * 8
            bullets.add(Bullet(self.damage, distance, dx, dy))

            dx = math.cos(radians) * MULTIPLIER - self.accuarcy()
            dy = math.sin(radians) * MULTIPLIER
            bullets.add(Bullet(self.damage, distance, dx, dy))

            dx = math.cos(radians) * MULTIPLIER  + math.sin(radians) * 8
            dy = math.sin(radians) * MULTIPLIER  - math.cos(radians) * 8
            bullets.add(Bullet(self.damage, distance, dx, dy))
        else:
            if self.name == "Knife":
                dx = math.cos(radians) * MULTIPLIER - 10 - self.accuarcy()
                dy = math.sin(radians) * MULTIPLIER - 10
                bullets.add(Bullet(self.damage, distance, dx, dy))
            else:
                dx = math.cos(radians) * MULTIPLIER - self.accuarcy()
                dy = math.sin(radians) * MULTIPLIER
                bullets.add(Bullet(self.damage, distance, dx, dy))

        if self.name == "Knife":
            self.charger = 1
        else:
            self.charger -= 1

        pygame.mixer.Sound(self.shot_sound).play()
        return

    def accuarcy(self):
        return random.randint(self.deviation[0], self.deviation[1])

    def reload(self, player):
        if self.reloading == 1:
            if player.ammo[self.ammo] >= self.maxCharger - self.charger:
                player.ammo[self.ammo] += self.charger - self.maxCharger
                self.charger = self.maxCharger
            elif player.ammo[self.ammo] > 0:
                self.charger += player.ammo[self.ammo]
                player.ammo[self.ammo] = 0

        self.reloading -= 1
        return

class Bullet(Sprite):
    def __init__(self, damage, distance, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/bullet.png").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = HW
        self.rect.centery = HH
        self.distance = distance
        self.speedx = speedx
        self.speedy = speedy
        self.damage = damage

    def zombies_hited(self, _zombies):
        global kills
        for zombie in _zombies:
            zombie.life -= self.damage
            bullets.remove(self)
            if zombie.life <= 0:
                zombies.remove(zombie)
                kills += 1

    def wall_collide(self, walls):
        for object in walls:
            if not object.name in ("Wall Fence", "Spawn Wall") and "Wall" in object.name:
                bullets.remove(self)

class Bullets(Group):
    def update(self):
        global shotTime
        for bullet in self:
            if bullet.distance > 0:
                bullet.rect.centerx += int(bullet.speedx)
                bullet.rect.centery += int(bullet.speedy)
                bullet.distance -= 1
                pygame.draw.circle(SCREEN, YELLOW, (bullet.rect.centerx, bullet.rect.centery), 2, 0)
            else:
                bullets.remove(bullet)

            bullet.zombies_hited(spritecollide(bullet, zombies, False))
            bullet.wall_collide(spritecollide(bullet, map, False))

        if shotTime >= 1:
            shotTime -= 1
        return

class MapObjects(Sprite):
    def __init__(self, name, image_path, x, y, gun, ammo, transparent=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = load_image(image_path, transparent)
        self.rect = self.image.get_rect()
        self.initial_posx = x
        self.initial_posy = y
        self.rect.centerx = x
        self.rect.centery = y
        self.gun = gun
        self.ammo = ammo

    def update(self):
        self.rect.centerx = self.initial_posx + playerx
        self.rect.centery = self.initial_posy + playery
        return

class Map(Group):
    def draw(self):
        for object in self:
            object.update()
            SCREEN.blit(object.image, object.rect)
        return

    def collide(self, player):
        for object in self:
            object.update()
            if "Wall" in object.name and pygame.sprite.collide_rect(object, player):
                return True
            if object.name == "Weapon" and pygame.sprite.collide_rect(object, player):
                if player.pickup_gun(object.gun):
                    self.remove(object)
            if object.name == "Ammo" and pygame.sprite.collide_rect(object, player):
                player.pickup_ammo(object.ammo)
                self.remove(object)
        return False
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Game Functions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    return

def keyboard_interaction(keys, player):
    global show_inventory
    change_gun(keys, player)
    sprint(keys, player)
    move_control(keys, player)
    drop_weapon(keys, player)

    if keys[K_LALT]:
        show_inventory = True
    else:
        show_inventory = False

    if keys[K_r] and player.guns[hand].reloading == 0 and player.guns[hand].charger < player.guns[hand].maxCharger:
        player.guns[hand].reloading = player.guns[hand].reloadTime
        pygame.mixer.Sound("sounds/say_reload.wav").play()
    return

def change_gun(keys, player):
    global hand
    if keys[K_1]:
        hand = 0
    if keys[K_2] and len(player.guns) >= 2:
        hand = 1
    if keys[K_3] and len(player.guns) >= 3:
        hand = 2
    if keys[K_4] and len(player.guns) == 4:
        hand = 3
    return

def drop_weapon(keys, player):
    global hand, drop_timer
    if keys[K_g] and hand > 0 and drop_timer == 0:
        rnd = (50,-50)
        weapon = MapObjects("Weapon", weapon_image(search_weapon(player.guns[hand].name)), HW - playerx + rnd[random.randint(0,1)], HH - playery + rnd[random.randint(0,1)], (player.guns[hand].name, player.guns[hand].ammo,\
        player.guns[hand].shot_sound, player.guns[hand].damage, player.guns[hand].maxCharger, player.guns[hand].charger,\
        player.guns[hand].shotingTime, player.guns[hand].reloadTime, player.guns[hand].distance, player.guns[hand].deviation), None, True)
        player.guns.pop(hand)
        if hand > len(player.guns) - 1:
            hand = len(player.guns) - 1
        map.add(weapon)
        drop_timer = 10
    elif drop_timer > 0:
        drop_timer -= 1

def search_weapon(weapon_name):
    if weapon_name == "Pistol":
        return 0
    elif weapon_name == "Rifle":
        return 1
    elif weapon_name == "Shotgun":
        return 2
    elif weapon_name == "Sniper":
        return 3

def sprint(keys, player):
    global speed
    if keys[K_LSHIFT] and player.guns[hand].reloading == 0:
        speed = 4
    else:
        speed = 2
    return

def move_control(keys, player):
    if keys:
        if keys[K_w]:
            move_up(player)
        if keys[K_d]:
            move_right(player)
        if keys[K_s]:
            move_down(player)
        if keys[K_a]:
            move_left(player)

def walk_animation(player):
    if player.walk < 2:
        player.walk += 1
    else:
        player.walk = 0

def mouse_interaction(player, click, position, pmy, pmx):
    # Control position on the screen
    radians = math.atan2(position[1] - pmy, position[0] - pmx)
    player.degrees = degrees(radians)
    player.animation()

    # Shoot on click
    if click and player.guns[hand].charger > 0 and shotTime == 0:
        player.guns[hand].shoting(radians)
    return

def move_up(player):
    global playery
    playery += speed
    if map.collide(player):
        playery -= speed
    return

def move_right(player):
    global playerx
    playerx -= speed
    if map.collide(player):
        playerx += speed
    return

def move_down(player):
    global playery
    playery -= speed
    if map.collide(player):
        playery += speed
    return

def move_left(player):
    global playerx
    playerx += speed
    if map.collide(player):
         playerx -= speed
    return

def reload(player):
    reload, reload_rect = process_text("RELOADING", HW, HH - 30)
    if player.guns[hand].reloading and player.ammo[player.guns[hand].ammo]:
        SCREEN.blit(reload, reload_rect)
        player.guns[hand].reload(player)
    return

def inventory(player):
    ammo, ammo_rect = process_text("Light: " + str(player.ammo["Light"]) + " | Medium: "+ str(player.ammo["Medium"]) + " | Heavy: "+ str(player.ammo["Heavy"]) + " | Cartridge: " + str(player.ammo["Cartridge"]), W - 170, H - 80, WHITE, 15)

    SCREEN.blit(ammo, ammo_rect)

    position = 300
    for i in range(len(player.guns)):
        if i == hand:
            gun, gun_rect = process_text(player.guns[i].name, W - position, H - 25 , YELLOW, 18)
        else:
            gun, gun_rect = process_text(player.guns[i].name, W - position, H - 25 , WHITE, 15)
        SCREEN.blit(gun, gun_rect)
        position -= 70
    return

def player_life(player):
    if player.life > 30:
        life, life_rect = process_text(str(player.life), 70, H - 100, GREEN, 30)
    else:
        life, life_rect = process_text(str(player.life), 70, H - 100, RED, 30)

    SCREEN.blit(life, life_rect)

def game_over(player):
    gameover_text, gameover_text_rect = process_text("GAME OVER", HW, HH - 300, WHITE, 80)
    write_score(player.name, score, kills, time)

    for i in range(360):
        events()

        SCREEN.blit(player.image, player.rect)
        SCREEN.blit(gameover_text, gameover_text_rect)

        pygame.display.update()
        SCREEN.fill(BLACK)
        CLOCK.tick(FPS)
    return

def generate_zombies():
    global gen_zombie_timer, zombies, zombies_spawners

    if gen_zombie_timer >= 120 and len(zombies) < 30:
        max_spawners = len(zombies_spawners) - 1
        zombie_posx, zombie_posy = zombies_spawners[random.randint(0,max_spawners)]
        zombie = Zombie("Zombie", zombie_posx, zombie_posy, "graphics/basic_zombie")
        zombies.add(zombie)
        gen_zombie_timer = 0
    return

def generate_weapon():
    global gen_weapon_timer, map
    if gen_weapon_timer >= 3600:
        max_spawners = len(weapon_spawners) - 1
        weapon_posx, weapon_posy = weapon_spawners[random.randint(0,max_spawners)]
        if check_generation(weapon_posx, weapon_posy):
            pos = random.randint(0,3)
            weapon = MapObjects("Weapon", weapon_image(pos), weapon_posx, weapon_posy, load_weapon(pos), None, True)
            map.add(weapon)
            gen_weapon_timer = 0
    return


def generate_ammo():
    global gen_ammo_timer, map
    if gen_ammo_timer >= 1200:
        max_spawners = len(ammo_spawners) - 1
        ammo_posx, ammo_posy = ammo_spawners[random.randint(0,max_spawners)]
        if check_generation(ammo_posx, ammo_posy):
            pos = random.randint(0,3)
            ammo = MapObjects("Ammo", ammo_image(pos), ammo_posx, ammo_posy, None, load_ammo(pos), True)
            map.add(ammo)
            gen_ammo_timer = 0
    return

def check_generation(x, y):
    for object in map:
        if object.initial_posx == x and object.initial_posy == y:
            return False
    return True

def scoreboard():
    score = time / 60 + kills * 10
    scoreboard_text, scoreboard_text_rect = process_text(str(score), HW, 50, WHITE, 40)
    SCREEN.blit(scoreboard_text, scoreboard_text_rect)
    return score
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Main
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def main():
    global shotx, shoty, shotTime, distance, name, bullets, zombies, gen_zombie_timer, gen_weapon_timer, gen_ammo_timer, time, score

    stagex, stagey = load_map(MapObjects, map, zombies_spawners, ammo_spawners, weapon_spawners)

    player = Player(player_name, HW, HH)

    #background = load_image("graphics/map1.png")

    # Cursor
    pygame.mouse.set_visible(False)
    cursor = load_image("graphics/cursor.png", True)
    mouse = Mouse()

    name, name_rect = process_text(player.name, 70, H - 150, WHITE, 10, "m12")
    to_exit, to_exit_rect = process_text("Press ESCAPE to exit", HW, H - 20, WHITE, 40)

    while player.life > 0:
        events()

        keyboard_interaction(pygame.key.get_pressed(), player)

        mouse_interaction(player, mouse.pressed(), mouse.position(), HH, HW)

        generate_zombies()
        generate_weapon()
        generate_ammo()

        charger, charger_rect = process_text(str(player.guns[hand].charger), 70, H - 50, WHITE, 30)

        # Position on screen
        map.draw()
        SCREEN.blit(name, name_rect), player_life(player), SCREEN.blit(charger, charger_rect)
        SCREEN.blit(player.image, player.rect), reload(player)
        zombies.update(player)
        SCREEN.blit(to_exit, to_exit_rect)
        bullets.update()
        score = scoreboard()
        inventory(player)

        # Cursosr on screen
        SCREEN.blit(cursor, (mouse.posx - 15, mouse.posy - 15))

        pygame.display.update()
        SCREEN.fill(BLACK)
        CLOCK.tick(FPS)

        # Timers
        gen_zombie_timer += 1
        gen_weapon_timer += 1
        gen_ammo_timer += 1
        time += 1

    return game_over(player)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Global
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
pygame.init()

    # Colors
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (122, 122, 122)

    # Clock
CLOCK = pygame.time.Clock()
FPS = 60

    #Player position
playerx, playery = 0, 0

    # Shoot
bullets = Bullets()
shotTime = 0
distance = 0

    # Timers
drop_timer = 0
gen_zombie_timer = 0
gen_weapon_timer = 0
gen_ammo_timer = 0

    # Other
MAX_GUNS = 4
hand = 0
speed = 2
map = Map()
zombies = Zombies()
zombies_spawners = []
ammo_spawners = []
weapon_spawners =[]
show_inventory = False
time = 0
kills = 0
score = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

while True:
    player_name = home()

    # Screen
    W, H = 1280, 720
    HW, HH = W / 2, H / 2 # Half
    AREA = W * H
    try:
        SCREEN = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    except:
        SCREEN = pygame.display.set_mode((W, H))

    main()
