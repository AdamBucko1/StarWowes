import pygame
import os


class Projectile:
    def __init__(self, x, y, color):
        if color=="red":
            self.shot_image = pygame.image.load(
                os.path.join('Assets', 'basic_laser_shot.png'))
        else:
            self.shot_image = pygame.image.load(
                os.path.join('Assets', 'basic_laser_shot_yellow.png'))
        self.shot_image = pygame.transform.scale(
            self.shot_image, (100, 10))
        self.shot_velocity = 50

        self.x_position = x + 10
        self.y_position = y + 10
        self.color=color

    def projectile_movement(self):
        if self.color == "red":
            self.x_position += self.shot_velocity
        else:
            self.x_position -= self.shot_velocity

    def projectile_out_of_bounds(self):
        if -100 > self.x_position or  2000 < self.x_position:
            return True
        return False

