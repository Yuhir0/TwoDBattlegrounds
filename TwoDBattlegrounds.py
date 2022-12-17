from clases import *
from functions import *
from game.entities.bullet import BulletsGroup
from game.entities.player import Player
from game.entities.scene import SceneElements, Scene
from game.entities.zombie import Zombie, ZombiesGroup
from load import *
from menu import home
from utils.constants import Colors
from utils.helper import Context


def keyboard_interaction(keys, player):
    change_gun(keys, player)
    sprint(keys, player)
    move_control(keys, player)
    drop_weapon(keys, player)

    if keys[K_r] and player.guns[Context.hand].reloading == 0 and player.guns[Context.hand].charger < \
            player.guns[Context.hand].maxCharger and player.ammo[player.guns[Context.hand].ammo] > 0:
        player.guns[Context.hand].reloading = player.guns[Context.hand].reloadTime
        pygame.mixer.Sound("sounds/say_reload.wav").play()


def change_gun(keys, player):
    if keys[K_1] and Context.hand != 0:
        player.guns[Context.hand].reloading = 0
        Context.hand = 0
    if keys[K_2] and len(player.guns) >= 2 and Context.hand != 1:
        player.guns[Context.hand].reloading = 0
        Context.hand = 1
    if keys[K_3] and len(player.guns) >= 3 and Context.hand != 2:
        player.guns[Context.hand].reloading = 0
        Context.hand = 2
    if keys[K_4] and len(player.guns) == 4 and Context.hand != 3:
        player.guns[Context.hand].reloading = 0
        Context.hand = 3


def drop_weapon(keys, player):
    if keys[K_g] and Context.hand > 0 and Context.drop_timer == 0:
        pygame.mixer.Sound("sounds/drop.wav").play()
        rnd = (50, -50)
        weapon = SceneElements("Weapon",
                               weapon_image(search_weapon(player.guns[Context.hand].name)),
                               Context.HW - Context.playerx + rnd[random.randint(0, 1)],
                               Context.HH - Context.playery + rnd[random.randint(0, 1)], (
                                   player.guns[Context.hand].name, player.guns[Context.hand].image_path,
                                   player.guns[Context.hand].ammo,
                                   player.guns[Context.hand].shot_sound, player.guns[Context.hand].damage,
                                   player.guns[Context.hand].maxCharger,
                                   player.guns[Context.hand].charger,
                                   player.guns[Context.hand].shotingTime,
                                   player.guns[Context.hand].reloadTime,
                                   player.guns[Context.hand].distance,
                                   player.guns[Context.hand].deviation,
                                   player.guns[Context.hand].hand_distance), None, True)
        player.guns.pop(Context.hand)
        if Context.hand > len(player.guns) - 1:
            Context.hand = len(player.guns) - 1
        Context.scene.add(weapon)
        Context.drop_timer = 10
    elif Context.drop_timer > 0:
        Context.drop_timer -= 1


def search_weapon(weapon_name):
    weapons = {"Pistol": 0, "Rifle": 1, "Shotgun": 2, "Sniper": 3}
    return weapons[weapon_name]


def sprint(keys, player):
    if keys[K_LSHIFT] and player.guns[Context.hand].reloading == 0:
        Context.speed = 4
    else:
        Context.speed = 2


def move_control(keys, player):
    if keys[K_w] or keys[K_d] or keys[K_s] or keys[K_a]:
        walk_animation(player)

        if keys[K_w]:  # 'W' pressed, Move Up
            set_move(player, 0, +Context.speed)
        if keys[K_d]:  # 'D' pressed, Move Right
            set_move(player, -Context.speed, 0)
        if keys[K_s]:  # 'S' pressed, Move Down
            set_move(player, 0, -Context.speed)
        if keys[K_a]:  # 'A' pressed, Move Left
            set_move(player, Context.speed, 0)
    else:
        player.walk = 0
        player.walk_time = 0


def walk_animation(player):
    if player.walk_time == 0 or player.walk_time >= 30:
        pygame.mixer.Sound("sounds/walk.wav").play()
        player.walk += 1 if player.walk < 2 else -1
        player.walk_time = 0

    if Context.speed == 2:
        player.walk_time += 1
    else:
        player.walk_time += 2


def mouse_interaction(player, click, position):
    # Calculate radians of the mouse on the screen
    radians = math.atan2(position[1] - Context.HH, position[0] - Context.HW)
    player.degrees = degrees(radians)
    player.animation()
    player.guns[Context.hand].animation(player)

    # Shoot on click mouse left button
    if click and player.guns[Context.hand].charger > 0 and Context.shotTime == 0 and player.guns[
        Context.hand].reloading == 0:
        player.guns[Context.hand].shoting(radians)


def set_move(player, x, y):
    Context.playerx += x
    if Context.scene.collide(player) and x:
        Context.playerx -= x
    Context.playery += y
    if Context.scene.collide(player) and y:
        Context.playery -= y


def reload(player):
    reload, reload_rect = process_text("RELOADING", Context.HW, Context.HH - 30)
    if player.guns[Context.hand].reloading and player.ammo[player.guns[Context.hand].ammo]:
        Context.SCREEN.blit(reload, reload_rect)
        player.guns[Context.hand].reload(player)


def inventory(player):
    ammo, ammo_rect = process_text(
        "Light: " + str(player.ammo["Light"]) + " | Medium: " + str(
            player.ammo["Medium"]) + " | Heavy: " + str(
            player.ammo["Heavy"]) + " | Shells: " + str(player.ammo["Shells"]), Context.W - 170,
        Context.H - 80, Colors.WHITE, 15)

    Context.SCREEN.blit(ammo, ammo_rect)

    position = 300
    for i in range(len(player.guns)):
        if i == Context.hand:
            gun, gun_rect = process_text(player.guns[i].name, Context.W - position, Context.H - 25,
                                         Colors.YELLOW, 18)
        else:
            gun, gun_rect = process_text(player.guns[i].name, Context.W - position, Context.H - 25,
                                         Colors.WHITE, 15)
        Context.SCREEN.blit(gun, gun_rect)
        position -= 70


def player_life(player):
    if player.life > 30:
        life, life_rect = process_text(str(player.life), 70, Context.H - 100, Colors.GREEN, 30)
    else:
        life, life_rect = process_text(str(player.life), 70, Context.H - 100, Colors.RED, 30)

    Context.SCREEN.blit(life, life_rect)


def game_over(player):
    gameover_text, gameover_text_rect = process_text("GAME OVER", Context.HW, Context.HH - 300,
                                                     Colors.WHITE, 80)
    write_score(player.name, Context.score, Context.kills, Context.time)
    pygame.mixer.Sound("sounds/gameover.wav").play()
    score_text, score_rect = process_text("Your score is [" + str(Context.score) + "]", Context.HW,
                                          Context.H - 300, Colors.WHITE, 50)

    for i in range(240):
        events()

        Context.SCREEN.blit(player.image, player.rect)
        Context.SCREEN.blit(gameover_text, gameover_text_rect)
        Context.SCREEN.blit(score_text, score_rect)
        pygame.display.update()
        Context.SCREEN.fill(Colors.BLACK)
        Context.CLOCK.tick(Context.FPS)


def load_zombie(position, x, y):
    zombies = (Zombie("Basic Zombie", "graphics/basic_zombie", x, y, 100, 15, 1.5),
               Zombie("Tanky Zombie", "graphics/tanky_zombie", x, y, 300, 20, 1),
               Zombie("Fast Zombie", "graphics/fast_zombie", x, y, 70, 10, 3))
    return zombies[random.randint(0, position)]


def generate_zombies():
    if Context.gen_zombie_timer >= 300:  # and len(zombies) < 30:
        max_spawners = len(Context.zombies_spawners) - 1
        zombie_posx, zombie_posy = Context.zombies_spawners[random.randint(0, max_spawners)]
        zombie = load_zombie(random.randint(0, 2), zombie_posx, zombie_posy)
        Context.zombies.add(zombie)
        Context.gen_zombie_timer = 0


def generate_weapon():
    if Context.gen_weapon_timer >= 3600:
        max_spawners = len(Context.weapon_spawners) - 1
        weapon_posx, weapon_posy = Context.weapon_spawners[random.randint(0, max_spawners)]
        if check_generation(weapon_posx, weapon_posy):
            pos = random.randint(0, 3)
            weapon = SceneElements("Weapon", weapon_image(pos), weapon_posx, weapon_posy,
                                   load_weapon(pos), None, True)
            Context.scene.add(weapon)
            Context.gen_weapon_timer = 0


def generate_ammo():
    if Context.gen_ammo_timer >= 1200:
        max_spawners = len(Context.ammo_spawners) - 1
        ammo_posx, ammo_posy = Context.ammo_spawners[random.randint(0, max_spawners)]
        if check_generation(ammo_posx, ammo_posy):
            pos = random.randint(0, 3)
            ammo = SceneElements("Ammo", ammo_image(pos), ammo_posx, ammo_posy, None,
                                 load_ammo(pos), True)
            Context.scene.add(ammo)
            Context.gen_ammo_timer = 0


def check_generation(x, y):
    for element in Context.scene:
        if element.initial_posx == x and element.initial_posy == y:
            return False


def scoreboard():
    Context.score = Context.time / 60 + Context.kills * 10
    scoreboard_text, scoreboard_text_rect = process_text(
        str(Context.score), Context.HW, 50, Colors.WHITE, 40)
    Context.SCREEN.blit(scoreboard_text, scoreboard_text_rect)
    return Context.score


def start_position():
    Context.playerx, Context.playery = Context.player_spawners[
        random.randint(0, len(Context.player_spawners) - 1)]
    Context.playerx += Context.HW
    Context.playery += Context.HH


def draw_cursor(mouse, cursor):
    cursor_rect = cursor.get_rect()
    cursor_rect.centerx = mouse.posx
    cursor_rect.centery = mouse.posy
    Context.SCREEN.blit(cursor, cursor_rect)


def main():
    stage_background, stagex, stagey = load_map(
        SceneElements, Context.scene, Context.zombies_spawners,
        Context.ammo_spawners, Context.weapon_spawners,
        Context.player_spawners
    )
    background = load_image(stage_background)

    start_position()

    player = Player(Context.player_name, Context.HW, Context.HH)

    # Cursor
    pygame.mouse.set_visible(False)
    cursor = load_image("graphics/cursor.png", True)
    mouse = Mouse()

    name, name_rect = process_text(player.name, 70, Context.H - 150, Colors.WHITE, 10, "m12")
    to_exit, to_exit_rect = process_text(
        "Press ESCAPE to exit", Context.HW, Context.H - 20, Colors.WHITE, 40)

    while player.life > 0:
        events()

        keyboard_interaction(pygame.key.get_pressed(), player)

        mouse_interaction(player, mouse.pressed(), mouse.position())

        generate_zombies()
        generate_weapon()
        generate_ammo()

        charger, charger_rect = process_text(str(player.guns[Context.hand].charger), 70, Context.H - 50,
                                             Colors.WHITE, 30)

        # Position on screen
        Context.SCREEN.blit(background, (Context.playerx, Context.playery))
        Context.bullets.update()
        Context.scene.draw()
        Context.SCREEN.blit(name, name_rect), player_life(player), Context.SCREEN.blit(charger,
                                                                       charger_rect)
        Context.SCREEN.blit(player.image, player.rect)
        Context.SCREEN.blit(player.guns[Context.hand].image, player.guns[Context.hand].rect)
        reload(player)
        Context.zombies.update(player)
        Context.SCREEN.blit(to_exit, to_exit_rect)
        Context.score = scoreboard()
        inventory(player)
        player.guns[Context.hand].out_of_ammo()

        # Cursosr on screen
        draw_cursor(mouse, cursor)

        pygame.display.update()
        Context.SCREEN.fill(Colors.BLACK)
        Context.CLOCK.tick(Context.FPS)

        # Timers
        Context.gen_zombie_timer += 1
        Context.gen_weapon_timer += 1
        Context.gen_ammo_timer += 1
        Context.time += 1

    return game_over(player)


if __name__ == '__main__':
    pygame.init()
    while True:
        Context.player_name = home()
        pygame.display.set_caption("TwoD Battlegrounds")

        # Screen
        Context.W, Context.H = 1280, 720
        Context.HW = Context.W / 2
        Context.HH = Context.H / 2
        Context.AREA = Context.W * Context.H

        Context.SCREEN = pygame.display.set_mode((Context.W, Context.H))

        # Clock
        Context.CLOCK = pygame.time.Clock()
        Context.FPS = 60

        # Shoot
        Context.bullets = BulletsGroup()

        # Other
        Context.MAX_GUNS = 4
        Context.speed = 2
        Context.scene = Scene()
        Context.zombies = ZombiesGroup()

        main()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
