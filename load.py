#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from time import sleep
from os import listdir

def stage(map_name):
    return open("graphics/maps/" + map_name + "/map.gen").readlines()

def stage_config(map_name):
    elements = []
    names = []
    images = []
    config = open("graphics/maps/" + map_name + "/map.conf").readlines()
    for c in config:
        elements.append(c.split('"')[0][:-1])
        names.append(c.split('"')[1])
        images.append(c.split('"')[2][1:-2])
    return elements, names, images

def load_weapon(position):
    weapon = (("Pistol", "hand_gun", "Light", "sounds/pistol.wav", 30, 12, 12, 30, 120, 30, (-2, 2)),
              ("Rifle", "hand_gun", "Medium", "sounds/rifle1.wav", 30, 30, 30, 8, 150, 40, (-1, 1)),
              ("Shotgun", "hand_gun", "Cartridge", "sounds/shotgun.wav", 35, 5, 5, 50, 180, 10, (-1, 1)),
              ("Sniper", "hand_gun", "Heavy", "sounds/sniper.wav", 100, 5, 5, 90, 200, 100, (0, 0)))
    return weapon[position]

def weapon_image(position):
    image = ("pistol.png",
             "rifle.png",
             "shotgun.png",
             "sniper.png")
    return "graphics/" + image[position]

def load_ammo(position):
    ammo = (("Light", 10),
            ("Medium", 20),
            ("Heavy", 3),
            ("Cartridge", 5))
    return ammo[position]

def ammo_image(position):
    image = ("light_ammo.png",
             "light_ammo.png",
             "light_ammo.png",
             "light_ammo.png")
    return "graphics/" + image[position]

def choose_map():
    maps = listdir("./graphics/maps/")
    rnd = random.randint(0, len(maps) - 1)
    return maps[rnd]

def load_map(MapObjects, map, zombies_spawners, ammo_spawners, weapon_spawners):
    map_name = choose_map()
    elements, names, images = stage_config(map_name)
    #rndx, rndy = random.randint(-1600,1600), random.randint(-800,800)
    y = -10
    for row in stage(map_name):
        x = 0
        for col in row:
            if col in elements:
                pos = elements.index(col)
                map.add(MapObjects(names[pos], "graphics/maps/" + map_name + "/" + images[pos], x, y, None, None))
            elif col == "G" and random.randint(0,1):
                weapon_spawners.append((x, y))
                pos = random.randint(0,3)
                map.add(MapObjects("Weapon", weapon_image(pos), x, y, load_weapon(pos), None, True))
            elif col == "A" and random.randint(0,1):
                ammo_spawners.append((x, y))
                pos = random.randint(0,3)
                map.add(MapObjects("Ammo", ammo_image(pos), x, y, None, load_ammo(pos), True))
            elif col == "V":
                zombies_spawners.append((x, y))
                map.add(MapObjects("Spawn Wall", "graphics/spawner.png", x, y, None, None,))
            x += 50
        y += 50
    print x, y
    return x, y
