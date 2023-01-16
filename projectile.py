import pygame
import os


class Projectile:
    def __init__(self, x, y):
        self.shot_image = pygame.image.load(
            os.path.join('Assets', 'basic_laser_shot.png'))
        self.shot_image = pygame.transform.scale(
            self.shot_image, (100, 10))
        self.shot_velocity = 50

        self.x_position = x + 10
        self.y_position = y + 10

    def handle_projectile_movement(projectiles: list, color):
        if color == "red":
            for num_projectile in range(len(projectiles)):
                projectiles[num_projectile].x_position += projectiles[num_projectile].shot_velocity
            projectiles = [item for item in projectiles if item.x_position < 2000]
        else:
            for num_projectile in range(len(projectiles)):
                projectiles[num_projectile].x_position -= projectiles[num_projectile].shot_velocity
            projectiles = [item for item in projectiles if item.x_position > -100]

