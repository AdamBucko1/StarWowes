import pygame
import os
from spaceship import *
from projectile import *
import spaceship_methods


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
    GAME_ENDED = False
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BORDER = pygame.Rect(WINDOW_WIDTH / 2 + BORDER_WIDTH / 2, 0, BORDER_WIDTH, WINDOW_HEIGHT)
    BACKROUND_IMAGE = 'backround1.png'

    BACKROUND = pygame.image.load(
        os.path.join('Assets', BACKROUND_IMAGE))
    BACKROUND = pygame.transform.scale(
        BACKROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))
    game_paused = False

    def __init__(self):
        pygame.font.init()
        self.HEALTH_FONT = pygame.font.SysFont('comicssans', 50)
        self.WINNER_FONT = pygame.font.SysFont('comicssans', 100)
        self.PAUSE_FONT = pygame.font.SysFont('comicssans', 100)
        self.PAUSE_INFO_FONT = pygame.font.SysFont('comicssans', 30)
        pygame.display.set_caption("Orbiting Dark")

        self.red_projectiles = []
        self.yellow_projectiles = []

        self.red_spaceship = Spaceship('red_venom_spaceship.png', self.LEFT_ROTATION)
        self.yellow_spaceship = Spaceship('yellow_venom_spaceship.png', self.RIGHT_ROTATION)
        self.main_loop(self.WIN)

    def main_loop(self, WIN):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game_paused = not self.game_paused
                if event.type == pygame.QUIT:
                    run = False
            if self.red_spaceship.health < 1 or self.yellow_spaceship.health < 1:
                self.GAME_ENDED = True
                self.draw_window(WIN)

            elif self.game_paused == True:
                self.draw_window(WIN)
            else:
                spaceship_methods.handle_cannon_cooldown(self.red_spaceship, self.yellow_spaceship)
                keys_pressed = pygame.key.get_pressed()

                spaceship_methods.yellow_ship_movement(keys_pressed, self.yellow_spaceship, self.BORDER,
                                                       self.WINDOW_WIDTH,
                                                       self.WINDOW_HEIGHT)
                spaceship_methods.red_ship_movement(keys_pressed, self.red_spaceship, self.BORDER, self.WINDOW_WIDTH,
                                                    self.WINDOW_HEIGHT)

                spaceship_methods.yellow_ship_shot(keys_pressed, self.yellow_spaceship, self.yellow_projectiles)
                spaceship_methods.red_ship_shot(keys_pressed, self.red_spaceship, self.red_projectiles)

                for projectile in self.red_projectiles:
                    projectile.projectile_movement()
                    if projectile.projectile_out_of_bounds():
                        self.red_projectiles.remove(projectile)

                for projectile in self.yellow_projectiles:
                    projectile.projectile_movement()
                    if projectile.projectile_out_of_bounds():
                        self.yellow_projectiles.remove(projectile)

                spaceship_methods.manage_hit_detection(self.yellow_spaceship, self.red_projectiles)
                spaceship_methods.manage_hit_detection(self.red_spaceship, self.yellow_projectiles)

                self.draw_window(WIN)
        pygame.quit()

    def draw_window(self, WIN):
        self.display_arena(WIN)
        self.display_spaceships(WIN)
        self.display_healt(WIN)
        self.display_projectiles(WIN, self.yellow_projectiles)
        self.display_projectiles(WIN, self.red_projectiles)
        if self.GAME_ENDED == True:
            self.display_winner(WIN)
        if self.game_paused == True:
            self.display_pause(WIN)
        self.display_pause_info(WIN)
        pygame.display.update()

    def display_healt(self, WIN):
        red_health_text = self.HEALTH_FONT.render("Health:" + str(self.red_spaceship.health), True, self.WHITE)
        yellow_health_text = self.HEALTH_FONT.render("Health:" + str(self.yellow_spaceship.health), True, self.WHITE)
        WIN.blit(red_health_text, (10, 10))
        WIN.blit(yellow_health_text, (self.WINDOW_WIDTH - red_health_text.get_width() - 50, 10))

    def display_pause(self, WIN):
        pause_text = self.PAUSE_FONT.render("PAUSED", True, self.WHITE)
        WIN.blit(pause_text, (self.WINDOW_WIDTH / 2 - 120, self.WINDOW_HEIGHT / 2 - 50))

    def display_pause_info(self, WIN):
        if self.game_paused == True:
            display_pause_info = self.PAUSE_INFO_FONT.render("Press P to unpause", True, self.WHITE)
        else:
            display_pause_info = self.PAUSE_INFO_FONT.render("Press P to pause", True, self.WHITE)
        WIN.blit(display_pause_info, (self.WINDOW_WIDTH - 200, self.WINDOW_HEIGHT - 25))

    def display_arena(self, WIN):
        WIN.blit(self.BACKROUND, (0, 0))
        pygame.draw.rect(WIN, self.BLACK, self.BORDER)

    def display_spaceships(self, WIN):
        WIN.blit(self.yellow_spaceship.spaceship, (self.yellow_spaceship.hitbox.x, self.yellow_spaceship.hitbox.y))
        WIN.blit(self.red_spaceship.spaceship, (self.red_spaceship.hitbox.x, self.red_spaceship.hitbox.y))

    def display_projectiles(self, WIN, projectiles):
        for num_projectile in range(len(projectiles)):
            WIN.blit(projectiles[num_projectile].shot_image, (
                projectiles[num_projectile].x_position,
                projectiles[num_projectile].y_position))

    def display_winner(self, WIN):
        if self.red_spaceship.health < self.yellow_spaceship.health:
            winner = "YELLLOW"
        else:
            winner = "RED"
        winner_text = self.WINNER_FONT.render(f"WINNER IS {winner}", True, self.WHITE)
        WIN.blit(winner_text, (self.WINDOW_WIDTH / 2 - 175 - len(winner) * 25, self.WINDOW_HEIGHT / 2 - 50))
