
class Context:
    """
    Properties:
        W (int)
        H (int)
        AREA (int)
        HW (int): Half width
        HH (int): Half height
        SCREEN: Screen dimensions
        bullets (game.entities.bullet.BulletsGroup): Bullet group
        zombies (game.entities.zombie.ZombiesGroup): Zombies group
    """
    W = int()
    H = int()
    AREA = int()
    HW = int()
    HH = int()

    CLOCK = None
    FPS = int()
    SCREEN = None

    bullets = None
    shotTime = int()
    distance = int()

    playerx = int()
    playery = int()

    # Timers
    drop_timer = int()
    gen_zombie_timer = int()
    gen_weapon_timer = int()
    gen_ammo_timer = int()

    # Score
    time = int()
    kills = int()
    score = int()

    # Spawner
    zombies_spawners = list()
    ammo_spawners = list()
    weapon_spawners = list()
    player_spawners = list()

    # Other
    MAX_GUNS = int()
    hand = int()
    speed = int()
    scene = None
    zombies = None
    player_name = str()
