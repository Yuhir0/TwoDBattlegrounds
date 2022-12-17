import random
from os import listdir, name


def stage(map_name):
    return open("graphics/maps/" + map_name + "/map.gen").readlines()


def stage_config(map_name):
    if name != "nt":
        limit = 1
    else:
        limit = 2
    elements = []
    names = []
    images = []
    transparent = []
    config = open("graphics/maps/" + map_name + "/map.conf").readlines()
    for c in config[:-1]:
        print(c)
        elements.append(c.split('"')[0][:-1])
        names.append(c.split('"')[1])
        if c.split()[len(c.split()) - 1:][0] == "T" and not ".png" in c.split()[
                                                                      len(c.split()) - 1:]:
            images.append(c.split()[len(c.split()) - 2:len(c.split()) - 1][0])
            transparent.append(1)
        else:
            transparent.append(0)
            images.append(c.split('"')[2][1:-limit])
    background = config[len(config) - 1:][0]
    return elements, names, images, transparent, background.split()[1:][0]


def load_weapon(position):
    weapon = (("Pistol", "hand_pistol", "Light", "sounds/pistol.wav", 35, 12, 12, 30, 90,
               30, (-2, 2), 10),
              ("Rifle", "hand_rifle", "Medium", "sounds/rifle1.wav", 30, 30, 30, 8, 120,
               40, (-1, 1), 10),
              ("Shotgun", "hand_shotgun", "Shells", "sounds/shotgun.wav", 25, 5, 5, 50,
               180, 10, (-1, 1), 10),
              ("Sniper", "hand_sniper", "Heavy", "sounds/sniper.wav", 100, 5, 5, 90, 200,
               120, (0, 0), 10))
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
            ("Shells", 5),
            ("Heavy", 3))
    return ammo[position]


def ammo_image(position):
    image = ("light_ammo.png",
             "medium_ammo.png",
             "shells_ammo.png",
             "heavy_ammo.png")
    return "graphics/" + image[position]


def choose_map():
    maps = listdir("./graphics/maps/")
    rnd = random.randint(0, len(maps) - 1)
    return maps[rnd]


def load_map(MapObjects, map, zombies_spawners, ammo_spawners, weapon_spawners,
             player_spawners):
    map_name = choose_map()
    map_name = "the_old"

    elements, names, images, transparent, background = stage_config(map_name)
    print(elements, names, images, transparent, background, sep='\n')

    y = 0
    x = 0
    for row in stage(map_name):
        x = 0
        for col in row:
            if col in elements:
                pos = elements.index(col)
                map.add(MapObjects(names[pos],
                                   "graphics/maps/" + map_name + "/" + images[pos], x, y,
                                   None, None, transparent[pos]))
            elif col == "G" and random.randint(0, 1):
                weapon_spawners.append((x, y))
                pos = random.randint(0, 3)
                map.add(
                    MapObjects("Weapon", weapon_image(pos), x, y, load_weapon(pos), None,
                               True))
            elif col == "A" and random.randint(0, 1):
                ammo_spawners.append((x, y))
                pos = random.randint(0, 3)
                map.add(
                    MapObjects("Ammo", ammo_image(pos), x, y, None, load_ammo(pos), True))
            elif col == "V":
                zombies_spawners.append((x, y))
                map.add(
                    MapObjects("Spawn Wall", "graphics/spawner.png", x, y, None, None, ))
            elif col == " ":
                player_spawners.append((-x, -y))
            x += 50
        y += 50
    return "graphics/maps/" + map_name + "/" + background, x, y
