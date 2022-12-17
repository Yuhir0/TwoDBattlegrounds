import math
import random

import pygame
from pygame.sprite import Sprite

from functions import load_image, process_text
from game.entities.bullet import Bullet
from utils.constants import Colors
from utils.helper import Context


class Weapon(Sprite):
    def __init__(self, name, image, ammo, shot_sound, damage, maxCharger, charger,
                 shotingTime, reloadTime, distance, deviation, hand_distance):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image_path = image
        self.image = load_image("graphics/" + image + "_0.png", True)
        self.hand_distance = hand_distance
        self.rect = self.image.get_rect()
        self.rect.centerx = Context.HW
        self.rect.centery = Context.HH
        self.damage = damage
        self.ammo = ammo
        self.maxCharger = maxCharger
        self.charger = charger
        self.shotingTime = shotingTime
        self.reloadTime = reloadTime
        self.reloading = 0
        self.distance = distance
        self.deviation = deviation
        self.shot_sound = shot_sound

    def shoting(self, radians):
        MULTIPLIER = 40
        Context.shotTime = self.shotingTime
        distance = self.distance
        if self.name == "Shotgun":
            direction = 10
            for i in range(5):
                dx = math.cos(radians) * MULTIPLIER - math.sin(radians) * direction
                dy = math.sin(radians) * MULTIPLIER + math.cos(radians) * direction
                Context.bullets.add(Bullet(self.damage, distance, dx, dy))
                direction -= 5
        else:
            if self.name == "Knife":
                dx = math.cos(radians) * (MULTIPLIER - 5)
                dy = math.sin(radians) * (MULTIPLIER - 5)
            else:
                dx = math.cos(radians) * MULTIPLIER - self.accuarcy()
                dy = math.sin(radians) * MULTIPLIER
            Context.bullets.add(Bullet(self.damage, distance, dx, dy))

        if self.name == "Knife":
            self.charger = 1
        else:
            self.charger -= 1

        pygame.mixer.Sound(self.shot_sound).play()

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

    def animation(self, player):
        self.image = load_image(
            "graphics/" + self.image_path + "_" + str(player.degrees) + ".png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = Context.HW
        self.rect.centery = Context.HH

    def out_of_ammo(self):
        if self.charger == 0 and self.reloading == 0:
            text, text_rect = process_text("OUT OF AMMO", Context.HW, Context.HH - 30, Colors.RED)
            Context.SCREEN.blit(text, text_rect)