import pygame
from pygame.sprite import Sprite, Group, spritecollide

from utils.constants import Colors
from utils.helper import Context


class Bullet(Sprite):
    def __init__(self, damage, distance, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("graphics/bullet.png").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = Context.HW
        self.rect.centery = Context.HH
        self.distance = distance
        self.speedx = speedx
        self.speedy = speedy
        self.damage = damage

    def zombies_hited(self, zombies_):
        for zombie in zombies_:
            zombie.life -= self.damage
            Context.bullets.remove(self)
            if zombie.life <= 0:
                Context.zombies.remove(zombie)
                Context.kills += 1

    def wall_collide(self, walls):
        for wall in walls:
            if (not ("Fence" in wall.name or "Spawn" in wall.name)
                    and "Wall" in wall.name):
                Context.bullets.remove(self)


class BulletsGroup(Group):

    def __init__(self, *sprites: Bullet) -> None:
        super().__init__(*sprites)

    def update(self: list[Bullet]):
        for bullet in self:
            if bullet.distance > 0:
                bullet.rect.centerx += int(bullet.speedx)
                bullet.rect.centery += int(bullet.speedy)
                bullet.distance -= 1
                pygame.draw.circle(Context.SCREEN, Colors.YELLOW,
                                   (bullet.rect.centerx, bullet.rect.centery), 2, 0)
            else:
                Context.bullets.remove(bullet)

            bullet.zombies_hited(spritecollide(bullet, Context.zombies, False))
            bullet.wall_collide(spritecollide(bullet, Context.scene, False))

        if Context.shotTime >= 1:
            Context.shotTime -= 1
