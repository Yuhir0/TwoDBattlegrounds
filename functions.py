#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pygame, math, sys
from pygame.locals import *
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print filename, "doesen't work"
        print "La imagen se fue a la puta"
        sys.exit()

    image = image.convert()

    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

def process_text(text, posx, posy, color=(255,255,255), size=25, font="DroidSans"):
    font = pygame.font.Font("graphics/fonts/" + font + ".ttf", size)
    res = pygame.font.Font.render(font, text, 1, color)
    res_rect = res.get_rect()
    res_rect.centerx = posx
    res_rect.centery = posy
    return res, res_rect

def degrees(radians):
    if (radians * 180) // math.pi < 0:
        return (radians * 180) // math.pi + 360
    else:
        return (radians * 180) // math.pi

def write_score(player_name, score, kills, time):
    score_file = open("score.txt", "r+")
    if len(score_file.read()) > 0:
        new_score = score_file.read() + "/" + player_name + ": " + str(score) + " pts, " + str(kills) + " kills, " + str(time / 60) + " seconds"
    else:
        new_score = player_name + ": " + str(score) + " pts, " + str(kills) + " kills, " + str(time / 60) + " seconds"
    score_file.write(new_score)
    score_file.close()

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    return
