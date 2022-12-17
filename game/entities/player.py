import pygame
from pygame.sprite import Sprite

from game.entities.weapon import Weapon
from functions import load_image


class Player(Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.life = 100
        self.image = load_image("graphics/player_0_w0.png", True)
        self.degrees = 0
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.walk = 0
        self.walk_time = 0
        self.ammo = {"Light": 0, "Medium": 0, "Heavy": 0, "Shells": 0}
        self.guns = [
            Weapon("Knife", "hand_knife", None, "pistol", 50, 1, 1, 30, 0, 1, None, 20)]

    def animation(self):
        if self.degrees < 45 or self.degrees >= 315:
            self.degrees = 0
        elif 135 > self.degrees >= 45:
            self.degrees = 90
        elif 225 > self.degrees >= 135:
            self.degrees = 180
        elif 315 > self.degrees >= 225:
            self.degrees = 270

        self.image = load_image(
            "graphics/player_" + str(self.degrees) + "_w" + str(self.walk) + ".png", True)

    def pickup_gun(self, gun):
        if len(self.guns) < 4:
            self.guns.append(
                Weapon(gun[0], gun[1], gun[2], gun[3], gun[4], gun[5], gun[6], gun[7],
                       gun[8], gun[9], gun[10], gun[11]))
            return True
        return False

    def pickup_ammo(self, ammo):
        self.ammo[ammo[0]] += ammo[1]