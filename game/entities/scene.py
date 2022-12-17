import pygame
from pygame.sprite import Sprite, Group

from functions import load_image
from utils.helper import Context


class SceneElements(Sprite):
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
        self.rect.centerx = self.initial_posx + Context.playerx
        self.rect.centery = self.initial_posy + Context.playery


class Scene(Group):
    def draw(self: list[SceneElements], **kwargs):
        for element in self:
            element.update()
            Context.SCREEN.blit(element.image, element.rect)

    def collide(self: list[SceneElements], player):
        for element in self:
            element.update()
            if "Wall" in element.name and pygame.sprite.collide_rect(element, player):
                if element.name == "Spawn Wall":
                    pygame.mixer.Sound("sounds/thewae2.wav").play()
                return True
            if element.name == "Weapon" and pygame.sprite.collide_rect(element, player):
                if player.pickup_gun(element.gun):
                    pygame.mixer.Sound("sounds/say_pick2.wav").play()
                    self.remove(element)
            if element.name == "Ammo" and pygame.sprite.collide_rect(element, player):
                player.pickup_ammo(element.ammo)
                pygame.mixer.Sound("sounds/say_pick2.wav").play()
                self.remove(element)
        return False
