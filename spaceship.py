import pygame
import os

class SpaceShip:
    def __init__(self, imageName, rotation):
        self.spaceship_width, self.spaceship_height = 55*3, 40*3
        self.spaceship = pygame.image.load(
            os.path.join('Assets', imageName))
        self.spaceship = pygame.transform.rotate(pygame.transform.scale(
            self.spaceship, (self.spaceship_width, self.spaceship_height)), rotation)
        self.velocity = 10
        self.hit_invurnability_duration=0
        self.cannon_in_use=0
        if self.is_red(rotation):
            self.hitbox = pygame.Rect(100, 300, self.spaceship_width-40, self.spaceship_height+40)
        else:
            self.hitbox = pygame.Rect(1800, 300, self.spaceship_width-40, self.spaceship_height+40)

        # self.hitbox_indicator=pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)

    def is_red(self,rotation):
        if rotation == -90:
            return True
        else:
            return False
    def get_hitbox_indicator(self):
        hitbox_indicator = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)
        return hitbox_indicator
    def cannon_iterator(self):
        self.cannon_in_use+=1
        if self.cannon_in_use>1:
            self.cannon_in_use=0
        return self.cannon_in_use