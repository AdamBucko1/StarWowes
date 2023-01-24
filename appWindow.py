import pygame
import os
from spaceship import *
from projectile import *
import spaceship_methods
from enum import Enum
from pygame import mixer



class GameState(Enum):
    RUNNING = 1
    PAUSED = 2
    WINNER = 3


class AppWindow():
    WHITE = (255, 255, 255)
    YELLOW= (255,255,0)
    RED =(255,0,0)
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
        #pygame.mixer.pre_init(44100,-16,4, 1024)
        pygame.mixer.init()
        pygame.mixer_music.load(os.path.join('Assets', 'Soundtrack.ogg'))
        pygame.mixer_music.play(-1)
        pygame.mixer_music.set_volume(0.3)
        self.HEALTH_FONT = pygame.font.SysFont('comicssans', 50)
        self.WINNER_FONT = pygame.font.SysFont('comicssans', 100)
        self.RESTART_FONT=pygame.font.SysFont('comicssans', 70)
        self.PAUSE_FONT = pygame.font.SysFont('comicssans', 100)
        self.PAUSE_INFO_FONT = pygame.font.SysFont('comicssans', 30)

        self.HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Hit_Sound.mp3'))
        self.HIT_SOUND.set_volume(1)
        self.SHOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Laser_shot.mp3'))
        self.SHOT_SOUND.set_volume(0.15)
        pygame.display.set_caption("Orbiting Dark")

        self.red_projectiles = []
        self.yellow_projectiles = []

        self.red_spaceship = Spaceship('red_venom_spaceship.png', self.LEFT_ROTATION)
        self.yellow_spaceship = Spaceship('yellow_venom_spaceship.png', self.RIGHT_ROTATION)
        self.game_state = GameState.RUNNING


        self.main_loop(self.WIN)

    def main_loop(self, WIN):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.game_state == GameState.RUNNING:
                            self.game_state = GameState.PAUSED
                            pygame.mixer_music.pause()
                        else:
                            self.game_state = GameState.RUNNING
                            pygame.mixer_music.unpause()
                    if event.key==pygame.K_r and self.game_state== GameState.WINNER:
                        self.restart_game()
                        self.game_state = GameState.RUNNING
                if event.type == pygame.QUIT:
                    run = False

            if self.red_spaceship.health < 1 or self.yellow_spaceship.health < 1:
                self.game_state = GameState.WINNER

            if self.game_state == GameState.RUNNING:
                spaceship_methods.handle_cannon_cooldown(self.red_spaceship, self.yellow_spaceship)
                keys_pressed = pygame.key.get_pressed()

                spaceship_methods.yellow_ship_movement(keys_pressed, self.yellow_spaceship, self.BORDER,
                                                       self.WINDOW_WIDTH,
                                                       self.WINDOW_HEIGHT)
                spaceship_methods.red_ship_movement(keys_pressed, self.red_spaceship, self.BORDER, self.WINDOW_WIDTH,
                                                    self.WINDOW_HEIGHT)

                if spaceship_methods.yellow_ship_shot(keys_pressed, self.yellow_spaceship, self.yellow_projectiles):
                    self.SHOT_SOUND.play()
                if spaceship_methods.red_ship_shot(keys_pressed, self.red_spaceship, self.red_projectiles):
                    self.SHOT_SOUND.play()
                for projectile in self.red_projectiles:
                    projectile.projectile_movement()
                    if projectile.projectile_out_of_bounds():
                        self.red_projectiles.remove(projectile)

                for projectile in self.yellow_projectiles:
                    projectile.projectile_movement()
                    if projectile.projectile_out_of_bounds():
                        self.yellow_projectiles.remove(projectile)

                if spaceship_methods.manage_hit_detection(self.yellow_spaceship, self.red_projectiles):
                    self.HIT_SOUND.play()
                if spaceship_methods.manage_hit_detection(self.red_spaceship, self.yellow_projectiles):
                    self.HIT_SOUND.play()

            self.draw_window(WIN)
        pygame.quit()

    def draw_window(self, WIN):
        self.display_arena(WIN)
        self.display_spaceships(WIN)
        self.display_healt(WIN)
        self.display_projectiles(WIN, self.yellow_projectiles)
        self.display_projectiles(WIN, self.red_projectiles)
        if self.game_state == GameState.WINNER:
            self.display_winner(WIN)
        if self.game_state == GameState.PAUSED:
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
            restart_text = self.RESTART_FONT.render(f"PRESS \"R\" TO RESTART", True, self.YELLOW)
        else:
            winner = "RED"
            restart_text = self.RESTART_FONT.render(f"PRESS \"R\" TO RESTART", True, self.RED)
        winner_text = self.WINNER_FONT.render(f"WINNER IS {winner}", True, self.WHITE)
        WIN.blit(winner_text, (self.WINDOW_WIDTH / 2 - 175 - len(winner) * 25, self.WINDOW_HEIGHT / 2 - 50))
        WIN.blit(restart_text, (self.WINDOW_WIDTH / 2 - 270, self.WINDOW_HEIGHT / 2 + 50))
    def restart_game(self):
        self.red_spaceship=Spaceship('red_venom_spaceship.png', self.LEFT_ROTATION)
        self.yellow_spaceship = Spaceship('yellow_venom_spaceship.png', self.RIGHT_ROTATION)
        self.red_projectiles = []
        self.yellow_projectiles = []
