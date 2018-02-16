#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pygame
from pygame.locals import *
from pygame.sprite import *
from functions import *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Mouse(Sprite):
    def __init__(self):
        self.posx = 0
        self.posy = 0

    def position(self):
        self.posx, self.posy = pygame.mouse.get_pos()
        return self.posx, self.posy

    def pressed(self, button=0):
        res = pygame.mouse.get_pressed()
        return res[button]

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        self.image_path = image_path
        self.image = pygame.image.load(image_path + ".png").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def hover(self, mouse):
        if mouse[0] > self.rect[0] and mouse[1] > self.rect[1] and mouse[0] < self.rect[2] + self.rect[0] and mouse[1] < self.rect[3] + self.rect[1]:
            self.image = pygame.image.load(self.image_path + "_hover.png").convert()
            return True
        else:
            self.image = pygame.image.load(self.image_path + ".png").convert()
            return False

class Input:
    def __init__(self):
        self.characters = []

    def read(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE and len(self.characters) > 0:
                    self.characters = self.characters[0:-1]
                elif len(self.characters) <= 12 and event.key not in (K_BACKSPACE, K_RETURN):
                    self.characters += str(event.unicode)

        return self.write()

    def write(self):
        name = ""
        for i in self.characters:
            name += i
        return name
