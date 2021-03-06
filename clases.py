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
    def __init__(self, image_path, x, y, transparent=False):
        self.image_path = image_path
        self.image = load_image(image_path + ".png", transparent)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.transparent = transparent

    def hover(self, mouse):
        if mouse[0] > self.rect[0] and mouse[1] > self.rect[1] and mouse[0] < self.rect[2] + self.rect[0] and mouse[1] < self.rect[3] + self.rect[1]:
            self.image = load_image(self.image_path + "_hover.png", self.transparent)
            return True
        else:
            self.image = load_image(self.image_path + ".png", self.transparent)
            return False

class Input:
    def __init__(self):
        self.characters = []
        self.error_time = 0
        self.error = "Incorrect character"

    def read(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE and len(self.characters) > 0:
                    self.characters = self.characters[0:-1]
                elif len(self.characters) <= 12 and event.key not in (K_BACKSPACE, K_RETURN, K_SPACE):
                    try:
                        self.characters += str(event.unicode)
                    except:
                        self.error_time = 90

        return self.write()

    def write(self):
        name = ""
        for i in self.characters:
            name += i
        return name

    def show_errors(self, SCREEN, posx, posy, color):
        if self.error_time > 0:
            error, error_rect = process_text(self.error, posx, posy, color, 30)
            SCREEN.blit(error, error_rect)
            self.error_time -= 1
