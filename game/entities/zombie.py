import math
import random

import pygame
from pygame.sprite import Sprite, spritecollide, collide_rect, Group

from functions import load_image, degrees
from utils.helper import Context


class Zombie(Sprite):
    def __init__(self, name, path, x, y, life, damage, speed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.life = life
        self.damage = damage
        self.image_path = path
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
        self.speed = speed
        self.hitting_speed = 30
        self.hitting_time = 0

    def update(self):
        self.rect.centerx = self.initial_posx + Context.playerx
        self.rect.centery = self.initial_posy + Context.playery
        return

    def animation(self, degrees):
        if degrees < 45 or degrees >= 315:
            self.degrees = 0
        elif 135 > degrees >= 45:
            self.degrees = 90
        elif 225 > degrees >= 135:
            self.degrees = 180
        elif 315 > degrees >= 225:
            self.degrees = 270

        self.image = load_image(self.image_path + "_" + str(self.degrees) + ".png", True)

    def ai(self, player):
        radians = math.atan2(Context.HH - self.rect.centery, Context.HW - self.rect.centerx)
        self.animation(degrees(radians))
        self.dx = math.cos(radians)
        self.dy = math.sin(radians)
        self.initial_posx += self.dx * self.speed
        self.update()
        if self.wall_collide():
            self.initial_posx -= self.dx * self.speed

        self.initial_posy += self.dy * self.speed
        self.update()
        if self.wall_collide():
            self.initial_posy -= self.dy * self.speed
        return

    def wall_collide(self):
        for element in spritecollide(self, Context.scene, False):
            if not element.name == "Spawn Wall" and "Wall" in element.name:
                return True
        return False

    def hitting(self, player):
        if collide_rect(player, self) and self.hitting_time == 0:
            pygame.mixer.Sound("sounds/hit" + str(random.randint(1, 4)) + ".wav").play()
            player.life -= self.damage
            self.hitting_time = self.hitting_speed
        elif self.hitting_time > 0:
            self.hitting_time -= 1
        return


class ZombiesGroup(Group):

    def __init__(self, *sprites: Zombie) -> None:
        super().__init__(*sprites)

    def update(self: list[Zombie], player):
        for zombie in self:
            zombie.ai(player)
            zombie.hitting(player)
            Context.SCREEN.blit(zombie.image, zombie.rect)
