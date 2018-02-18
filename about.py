#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pygame
from pygame.locals import *
from functions import process_text
from clases import Button, Mouse
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def events(max_scroll, H):
    global posy
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and posy < 30:
                posy += 15
            elif event.button == 5 and max_scroll > H:
                posy -= 15
    return True

def read_credits(SCREEN, HW):
    credits_file = open("credits.txt", "r")
    credits_text = credits_file.readlines()
    y = posy
    for line in credits_text:
        if line[0] == "*":
            text, text_rect = process_text(line[1:-1], HW, y, (255,255,255), 30)
            line_size = 300
            pygame.draw.line(SCREEN, (255,255,255), (HW - line_size, y + 15), (HW + line_size, y + 15))
        else:
            text, text_rect = process_text(line[:-1], HW, y, (255,255,255), 20)
        SCREEN.blit(text, text_rect)
        y += 30
    credits_file.close()
    return posy + len(credits_text) * 30

def read_score(SCREEN, HW, H):
    global posy
    score_file = open("score.txt", "r")
    score_text = score_file.read().split("/")
    score_text = sort_score(score_text)
    y = posy + 80
    if len(score_text) > 0:
        for i in range(len(score_text)):
            x = 100
            endline = len(score_text[i]) - 1
            split_score = score_text[i].split()
            text, text_rect = process_text(str(i + 1), x, y, (255,255,255), 20)
            SCREEN.blit(text, text_rect)
            for data in split_score:
                x += 150
                text, text_rect = process_text(data, x, y, (255,255,255), 20)
                SCREEN.blit(text, text_rect)
            y += 40
    else:
        text, text_rect = process_text("None Scores", HW, y, (255,255,255), 35)
        SCREEN.blit(text, text_rect)
    score_file.close()
    return posy + 80 + len(score_text) * 40

def sort_score(score_text):
    for j in range(len(score_text)):
        score = 0
        kills = 0
        for i in range(len(score_text)):
            split_score = score_text[i].split()
            if score > int(split_score[1]):
                score_text[i], score_text[i - 1] = score_text[i - 1], score_text[i]
            elif score == int(split_score[1]) and kills > int(split_score[2]):
                score_text[i], score_text[i - 1] = score_text[i - 1], score_text[i]
            else:
                score = int(split_score[1])
                kills = int(split_score[2])

    return score_text[::-1]

def header(SCREEN, x, y):
    head = "Position Name Score Kills Time".split()
    pygame.draw.rect(SCREEN, (0,0,0), (0, 0, x + (150 * len(head)), y + 30))
    pygame.draw.line(SCREEN, (255,255,255), (0, y + 30), (x + (150 * len(head)), y + 30))
    for text in head:
        text, text_rect = process_text(text, x, y, (255,255,255), 30)
        SCREEN.blit(text, text_rect)
        x += 150
    return

def credits(W, H):
    global posy
    pygame.init()

    # Screen
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

    # Clock
    CLOCK = pygame.time.Clock()
    FPS = 60

    mouse = Mouse()
    back_button = Button("graphics/back_button", 20, 20)

    max_scroll = H
    while events(max_scroll, H) and not (back_button.hover(mouse.position()) and mouse.pressed()):
        max_scroll = read_credits(SCREEN, HW)
        SCREEN.blit(back_button.image, back_button.rect)
        pygame.display.update()
        SCREEN.fill(BLACK)
        CLOCK.tick(FPS)
    posy = 30
    return


def score(W, H):
    global posy
    pygame.init()

    # Screen
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

    # Clock
    CLOCK = pygame.time.Clock()
    FPS = 60

    mouse = Mouse()
    back_button = Button("graphics/back_button", 20, 20)

    max_scroll = H
    while events(max_scroll, H) and not (back_button.hover(mouse.position()) and mouse.pressed()):
        max_scroll = read_score(SCREEN, HW, H)
        header(SCREEN, 100, 50)
        SCREEN.blit(back_button.image, back_button.rect)
        pygame.display.update()
        SCREEN.fill(BLACK)
        CLOCK.tick(FPS)
    posy = 30
    return

posy = 30
