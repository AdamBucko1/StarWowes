import pygame
import os

class Projectile:
    def __init__(self,x,y):
        self.shot_image = pygame.image.load(
            os.path.join('Assets', 'basic_laser_shot.png'))
        self.shot_image = pygame.transform.scale(
            self.shot_image, (100, 10))
        self.shot_velocity=50

        self.x_position=x+10
        self.y_position=y+10