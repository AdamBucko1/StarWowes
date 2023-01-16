import pygame
import os
from spaceship import *
from projectile import *
from spaceship_methods import *


class AppWindow():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BORDER_WIDTH = 10
    FPS = 60
    LEFT_ROTATION = -90
    RIGHT_ROTATION = 90
    # SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BORDER = pygame.Rect(WINDOW_WIDTH / 2 + BORDER_WIDTH / 2, 0, BORDER_WIDTH, WINDOW_HEIGHT)

    BACKROUND = pygame.image.load(
        os.path.join('Assets', 'backround1.png'))
    BACKROUND = pygame.transform.scale(
        BACKROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

    red_spaceship = Spaceship('red_venom_spaceship.png', LEFT_ROTATION)
    yellow_spaceship = Spaceship('yellow_venom_spaceship.png', RIGHT_ROTATION)

    def __init__(self):
        pygame.font.init()
        self.HEALTH_FONT = pygame.font.SysFont('comicssans', 40)
        pygame.display.set_caption("Orbiting Dark")
        self.red_projectiles = []
        self.yellow_projectiles = []

        self.main_loop(self.WIN)

    def main_loop(self, WIN):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            Spaceship_methods.handle_cannon_cooldown(self.red_spaceship, self.yellow_spaceship)
            keys_pressed = pygame.key.get_pressed()

            Spaceship_methods.yellow_ship_movement(keys_pressed, self.yellow_spaceship, self.BORDER, self.WINDOW_WIDTH,
                                                   self.WINDOW_HEIGHT)
            Spaceship_methods.red_ship_movement(keys_pressed, self.red_spaceship, self.BORDER, self.WINDOW_WIDTH,
                                                self.WINDOW_HEIGHT)

            Spaceship_methods.yellow_ship_shot(keys_pressed, self.yellow_spaceship, self.yellow_projectiles)
            Spaceship_methods.red_ship_shot(keys_pressed, self.red_spaceship, self.red_projectiles)

            Projectile.handle_projectile_movement(self.red_projectiles, "red")
            Projectile.handle_projectile_movement(self.yellow_projectiles, "yellow")

            Spaceship_methods.manage_hit_detection(self.yellow_spaceship, self.red_projectiles)
            Spaceship_methods.manage_hit_detection(self.red_spaceship, self.yellow_projectiles)

            self.draw_window(WIN)
        pygame.quit()

    def draw_window(self, WIN):
        self.display_arena(WIN)
        self.display_spaceships(WIN)
        self.display_healt(WIN)
        self.display_projectiles(WIN, self.yellow_projectiles)
        self.display_projectiles(WIN, self.red_projectiles)
        pygame.display.update()

    def display_healt(self, WIN):
        red_health_text = self.HEALTH_FONT.render("Health:" + str(self.red_spaceship.health), True, self.WHITE)
        yellow_health_text = self.HEALTH_FONT.render("Health:" + str(self.yellow_spaceship.health), True, self.WHITE)
        WIN.blit(red_health_text, (10, 10))
        WIN.blit(yellow_health_text, (self.WINDOW_WIDTH - red_health_text.get_width() - 50, 10))

    def display_arena(self, WIN):
        WIN.blit(self.BACKROUND, (0, 0))
        pygame.draw.rect(WIN, self.BLACK, self.red_spaceship.get_hitbox_indicator())
        pygame.draw.rect(WIN, self.BLACK, self.yellow_spaceship.get_hitbox_indicator())
        pygame.draw.rect(WIN, self.BLACK, self.BORDER)

    def display_spaceships(self, WIN):
        WIN.blit(self.yellow_spaceship.spaceship, (self.yellow_spaceship.hitbox.x, self.yellow_spaceship.hitbox.y))
        WIN.blit(self.red_spaceship.spaceship, (self.red_spaceship.hitbox.x, self.red_spaceship.hitbox.y))

    def display_projectiles(self, WIN, projectiles):
        for num_projectile in range(len(projectiles)):
            WIN.blit(projectiles[num_projectile].shot_image, (
                projectiles[num_projectile].x_position,
                projectiles[num_projectile].y_position))
