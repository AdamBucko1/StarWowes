import pygame
import os
from projectile import *
from spaceship import *


class Spaceship_methods:

    def __init__(self):
        pass

    @staticmethod
    def is_hit(target_hitbox, laser_projectiles: list):
        for projectile in laser_projectiles:
            if projectile.x_position > target_hitbox.x and projectile.x_position < target_hitbox.x + target_hitbox.width and projectile.y_position > target_hitbox.y and projectile.y_position < target_hitbox.y + target_hitbox.height:
                return True
        return False

    @staticmethod
    def is_vulnerable(spaceship: Spaceship):
        if spaceship.hit_invulnerability_duration == 0:
            return True
        else:
            return False

    @staticmethod
    def lowered_invulnerability_duration(spaceship_invunerability_time):
        return spaceship_invunerability_time - 1

    @staticmethod
    def yellow_ship_movement(keys_pressed , yellow_spaceship, border, window_width, window_height):
        if keys_pressed[
            pygame.K_LEFT] and yellow_spaceship.hitbox.x - yellow_spaceship.velocity > border.x + border.width:  # YELLOW LEFT\#
            yellow_spaceship.hitbox.x -= yellow_spaceship.velocity
        if keys_pressed[
            pygame.K_RIGHT] and yellow_spaceship.hitbox.x + yellow_spaceship.velocity + yellow_spaceship.hitbox.width < window_width:  # YELLOW RIGHT\
            yellow_spaceship.hitbox.x += yellow_spaceship.velocity
        if keys_pressed[
            pygame.K_UP] and yellow_spaceship.hitbox.y - yellow_spaceship.velocity > 0:  # YELLOW UP\
            yellow_spaceship.hitbox.y -= yellow_spaceship.velocity
        if keys_pressed[
            pygame.K_DOWN] and yellow_spaceship.hitbox.y + yellow_spaceship.velocity + yellow_spaceship.hitbox.height < window_height:  # YELLOW DOWN\
            yellow_spaceship.hitbox.y += yellow_spaceship.velocity

    @staticmethod
    def yellow_ship_shot(keys_pressed, yellow_spaceship: Spaceship, yellow_projectiles: list):
        if keys_pressed[pygame.K_KP0] and yellow_spaceship.cannon_cooldown == 0:
            yellow_projectiles.append(Projectile(yellow_spaceship.hitbox.x,
                                                 yellow_spaceship.hitbox.y + yellow_spaceship.cannon_iterator()))
            yellow_spaceship.cannon_cooldown = Spaceship.BASIC_CANNON_COOLDOWN

    @staticmethod
    def red_ship_movement(keys_pressed,red_spaceship, border, window_width, window_height):
        if keys_pressed[pygame.K_a] and red_spaceship.hitbox.x - red_spaceship.velocity > 0:  # RED LEFT\
            red_spaceship.hitbox.x -= red_spaceship.velocity
        if keys_pressed[
            pygame.K_d] and red_spaceship.hitbox.x + red_spaceship.velocity + red_spaceship.hitbox.width < border.x:  # RED RIGHT\
            red_spaceship.hitbox.x += red_spaceship.velocity
        if keys_pressed[pygame.K_w] and red_spaceship.hitbox.y - red_spaceship.velocity > 0:  # RED UP\
            red_spaceship.hitbox.y -= red_spaceship.velocity
        if keys_pressed[
            pygame.K_s] and red_spaceship.hitbox.y + red_spaceship.velocity + red_spaceship.hitbox.height < window_height:  # RED DOWN\
            red_spaceship.hitbox.y += red_spaceship.velocity

    @staticmethod
    def red_ship_shot(keys_pressed, red_spaceship: Spaceship, red_projectiles: list):
        if keys_pressed[pygame.K_LSHIFT] and red_spaceship.cannon_cooldown == 0:
            red_projectiles.append(Projectile(red_spaceship.hitbox.x,
                                                   red_spaceship.hitbox.y + red_spaceship.cannon_iterator()))
            red_spaceship.cannon_cooldown = Spaceship.BASIC_CANNON_COOLDOWN
    @staticmethod
    def handle_cannon_cooldown(red_spaceship:Spaceship,yellow_spaceship:Spaceship):
        if red_spaceship.cannon_cooldown > 0:
            red_spaceship.cannon_cooldown -= 1
        if yellow_spaceship.cannon_cooldown > 0:
            yellow_spaceship.cannon_cooldown -= 1
    @staticmethod
    def manage_hit_detection(spaceship,projectile):
        if not Spaceship_methods.is_vulnerable(spaceship):
            spaceship.hit_invulnerability_duration -= 1

        else:
            if Spaceship_methods.is_hit(spaceship.hitbox, projectile):
                spaceship.health -= 1
                spaceship.hit_invulnerability_duration = Spaceship.INVULNERABILITY_DURATION