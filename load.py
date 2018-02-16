#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from time import sleep

"""
Walls
    W: Solid Wall
    w: Wood
    S: Stone
    B: Brick
    I: Iron Fence Vertical
    i: Iron Fence Horizontal
    F: Wood Fence Vertical
    f: Wood Fence Horizontal

Interaction
    A: Ammo
    G: Gun/Weapon
"""

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
        print elements, names, images
    return elements, names, images

def stage2():
    map_tuple = ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWVWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                 "W              S                          I                                                                   SSSSSSSSSSW",
                 "W              S                          I                                                                   SSSSSSSSSSW",
                 "W    AG        S                    wwwwwwwwwwww                                                              SSSSSSSSSSW",
                 "W              S                    w          w                                                              SSSSSSSSSSW",
                 "W              S                         A                iiiiiiiiiiii   iiiiiiiiiiiii                        SSSSSSSSSSW",
                 "V              S                          G               I                          I                         SSSSSSSSSW",
                 "W        AG    S                    w          w          I                          I                         VSSSSSSSSW",
                 "W              S                    wwwwwwwwwwww          I  Ffffffffff ffffffffffF  I                           SSSSSSSW",
                 "W                                         I               I  F                    F  I                                  W",
                 "W                                         I               I  F    A          A    F  I                                  W",
                 "W                                         I                  F                    F                                     W",
                 "WSSSSSSSSSSSSSSS                          I                            V                                                W",
                 "W                                         I                  F    A          A    F                                     W",
                 "W                                         I               I  F                    F  I                                  W",
                 "W                                         I               I  Ffffffffff ffffffffffF  I                                  W",
                 "W                                         I               I                          I                                  W",
                 "W          BBBBBBBBBBBBBBBBBBB   BBBBBBBBBB               I                          I                                  W",
                 "W          B           w                  B               iiiiiiiiiiii   iiiiiiiiiiiii                                  W",
                 "W          B           w                  B                                                                             W",
                 "W          B           w                  B                                                                             W",
                 "W          B    A      w                  B                                                                             W",
                 "W          B    G      w         AG       B                                                                             W",
                 "W          B           w                  B                                                                             W",
                 "W          B                              B                                                                             W",
                 "W          B           w                  B                                                                             W",
                 "W          B           w                  B                                                                             W",
                 "W          Bwwwwwwwwwwww      wwwww wwwwwwB                     BBBBBBBBBBBBBBBBBBBBBBBB   BBBBBBBBBBBBBBB              W",
                 "W          B                  w           B                     B               w             w          B              W",
                 "W          B                  w           B                     B               w             w          B              W",
                 "W          B     A            w     A     B                     B               w             w          B              W",
                 "W          B       G          w           B                     B    AG                       w          B              W",
                 "W          B                  w           B                     B               w             w          B              W",
                 "W          BBBBBBBBBBBB  BBBBBBBBBBBBBBBBBB                     B               w                        B              W",
                 "W          I                                                    Bwwwwwwwwwwwwwwww             w  AG      B              W",
                 "W          I                                                    B                             w          B              W",
                 "W          I                                                    B                     A       w          B              W",
                 "W          I                                                    B      AG                     w          B              W",
                 "W          I                     G                              B                         wwwwwwwwwwwwwwwB              W",
                 "W          I                                                    B                         w              B              W",
                 "W          I                                   S                Bwwwwwwwwwwwww            w              B              W",
                 "W          SSSSSSS  SSSSSSS                    S                B            w                           B              W",
                 "W          S              S                    S                B            w            w   A          B              W",
                 "W          S              S                    S                        A    w            w    G         B              W",
                 "W          S    A         S                    S                                          w              B              W",
                 "W          S    G         S                A   S                             w            w              B              W",
                 "W          S            A S                    S                B            w            w              B              W",
                 "W          S              S      ffffffffffffffS                B            w            w              B              W",
                 "W          SSSSSSSSSSSSSSSS                    S                Bwwwwwwwwwwwwwwwwwwwwwwwwwwwww           B              W",
                 "W                                       GA     SiiiiiiiiiiiiiiiiB                            w           B              W",
                 "W                                              S                B  AG                    A   w       A   B              W",
                 "W                                              S                B                            w           B              W",
                 "W                 F                            S                BBBBBBBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB              W",
                 "W                 F                                                                                                     W",
                 "W                 F                                                                                                     W",
                 "W                 F                                                                                                     W",
                 "W                 F                                                                                                     W",
                 "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    return map_tuple

def load_weapon(position):
    weapon = (("Pistol", "Light", "sounds/pistol.wav", 30, 12, 12, 30, 120, 30, (-2, 2)),
              ("Rifle", "Medium", "sounds/rifle1.wav", 30, 30, 30, 8, 150, 40, (-1, 1)),
              ("Shotgun", "Cartridge", "sounds/shotgun.wav", 35, 5, 5, 50, 180, 10, (-1, 1)),
              ("Sniper", "Heavy", "sounds/sniper.wav", 100, 5, 5, 90, 200, 100, (0, 0)))
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

def load_map(MapObjects, map, zombies_spawners, ammo_spawners, weapon_spawners):
    map_name = "the_old"
    elements, names, images = stage_config(map_name)
    #rndx, rndy = random.randint(-1600,1600), random.randint(-800,800)
    y = -10
    for row in stage(map_name):
        x = 0
        for col in row:
            """if col == "W":
                map.add(MapObjects("Wall", "graphics/wall.png", x, y, None, None))
            elif col == "w":
                map.add(MapObjects("Wall", "graphics/wood.png", x, y, None, None))
            elif col == "S":
                map.add(MapObjects("Wall", "graphics/stone.png", x, y, None, None))
            elif col == "B":
                map.add(MapObjects("Wall", "graphics/brick.png", x, y, None, None))
            elif col == "I":
                map.add(MapObjects("Wall Fence", "graphics/iron_fence_v.png", x, y, None, None))
            elif col == "i":
                map.add(MapObjects("Wall Fence", "graphics/iron_fence_h.png", x, y, None, None))
            elif col == "F":
                map.add(MapObjects("Wall Fence", "graphics/wood_fence_v.png", x, y, None, None))
            elif col == "f":
                map.add(MapObjects("Wall Fence", "graphics/wood_fence_h.png", x, y, None, None))"""
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
