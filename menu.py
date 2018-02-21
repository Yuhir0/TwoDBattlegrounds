#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pygame, sys
from pygame.locals import *
from about import credits, score
from clases import Button, Input, Mouse
from functions import events, process_text, load_image
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Home menu
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def home():
    pygame.init()
    pygame.display.set_caption("TwoD Battlegrounds")

    # Screen
    W, H = 800, 600
    HW, HH = W / 2, H / 2 # Half
    AREA = W * H
    SCREEN = pygame.display.set_mode((W, H))

    # Colors
    RED = (255, 0, 0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GREY = (100,100,100)
    LIGHT_GREY = (170,170,170)

    # Clock
    CLOCK = pygame.time.Clock()
    FPS = 60

    name = ""

    background = load_image("graphics/twodbattlegrounds.png")

    title_font = "ice_pixel-7"
    title_size = 130
    TwoD, TwoD_rect = process_text("TwoD", HW, HH - 230, WHITE, title_size, title_font)
    Battlegrounds, Battlegrounds_rect = process_text("Battlegrounds", HW, HH - 130, WHITE, title_size, title_font)

    play_button = Button("graphics/play_button", HW, HH + 200)
    play_text, play_text_rect = process_text("PLAY", HW, HH + 200, WHITE, 50, "ABITE")

    credits_button = Button("graphics/generic_button", W - 80, H - 50)
    credits_text, credits_text_rect = process_text("Credits", W - 80, H - 50)

    score_button = Button("graphics/generic_button", 80, H - 50)
    score_text, score_text_rect = process_text("Score", 80, H - 50)


    input = Input()
    keys = pygame.key.get_pressed()

    # Mouse
    pygame.mouse.set_visible(True)
    mouse = Mouse()

    while not (((play_button.hover(mouse.position()) and mouse.pressed()) or keys[K_RETURN]) and len(name) > 0):
        keys = pygame.key.get_pressed()

        name = input.read()
        if len(name) == 0:
            nickname, nickname_rect = process_text("Type your nickname", HW, H - 230, LIGHT_GREY, 30)
        else:
            nickname, nickname_rect = process_text(name, HW, H - 230, GREY, 20, "m12")

        if credits_button.hover(mouse.position()) and mouse.pressed():
            credits(W, H)

        if score_button.hover(mouse.position()) and mouse.pressed():
            score(W, H)

        SCREEN.blit(background, (0, 0))
        pygame.draw.rect(SCREEN, WHITE, (HW - 150 , H - 260, 300, 60))
        SCREEN.blit(nickname, nickname_rect)
        SCREEN.blit(TwoD, TwoD_rect)
        SCREEN.blit(Battlegrounds, Battlegrounds_rect)
        SCREEN.blit(play_button.image, play_button.rect)
        SCREEN.blit(play_text, play_text_rect)
        SCREEN.blit(credits_button.image, credits_button.rect)
        SCREEN.blit(credits_text, credits_text_rect)
        SCREEN.blit(score_button.image, score_button.rect)
        SCREEN.blit(score_text, score_text_rect)

        pygame.display.update()
        CLOCK.tick(FPS)

    return name
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
