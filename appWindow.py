import pygame
import os
from spaceship import *
from projectile import *


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

    red_spaceship = SpaceShip('red_venom_spaceship.png', LEFT_ROTATION)
    yellow_spaceship = SpaceShip('yellow_venom_spaceship.png', RIGHT_ROTATION)

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
            if self.red_spaceship.cannon_cooldown>0:
                self.red_spaceship.cannon_cooldown-=1
            if self.yellow_spaceship.cannon_cooldown>0:
                self.yellow_spaceship.cannon_cooldown-=1

            keys_pressed = pygame.key.get_pressed()
            self.yellow_ship_movement(keys_pressed)
            self.red_ship_movement(keys_pressed)

            self.red_projectiles = self.handle_projectile_movement(self.red_projectiles, "red")
            self.yellow_projectiles = self.handle_projectile_movement(self.yellow_projectiles, "yellow")

            if not self.is_vulnerable(self.yellow_spaceship):
                self.yellow_spaceship.hit_invulnerability_duration -= 1

            else:
                if self.is_hit(self.yellow_spaceship.hitbox, self.red_projectiles):
                    self.yellow_spaceship.health -= 1
                    self.yellow_spaceship.hit_invulnerability_duration = SpaceShip.INVULNERABILITY_DURATION

            if not self.is_vulnerable(self.red_spaceship):
                self.red_spaceship.hit_invulnerability_duration -= 1

            else:
                if self.is_hit(self.red_spaceship.hitbox, self.yellow_projectiles):
                    self.red_spaceship.health -= 1
                    self.red_spaceship.hit_invulnerability_duration = SpaceShip.INVULNERABILITY_DURATION

            self.draw_window(WIN)
        pygame.quit()

    def draw_window(self, WIN):
        WIN.blit(self.BACKROUND, (0, 0))
        pygame.draw.rect(WIN, self.BLACK, self.red_spaceship.get_hitbox_indicator())
        pygame.draw.rect(WIN, self.BLACK, self.yellow_spaceship.get_hitbox_indicator())
        pygame.draw.rect(WIN, self.BLACK, self.BORDER)
        WIN.blit(self.yellow_spaceship.spaceship, (self.yellow_spaceship.hitbox.x, self.yellow_spaceship.hitbox.y))
        WIN.blit(self.red_spaceship.spaceship, (self.red_spaceship.hitbox.x, self.red_spaceship.hitbox.y))

        red_health_text = self.HEALTH_FONT.render("Health:" + str(self.red_spaceship.health), True, self.WHITE)
        yellow_health_text = self.HEALTH_FONT.render("Health:" + str(self.yellow_spaceship.health), True, self.WHITE)
        WIN.blit(red_health_text, (10, 10))
        WIN.blit(yellow_health_text, (self.WINDOW_WIDTH - red_health_text.get_width() - 50, 10))

        for num_red_projectile in range(len(self.red_projectiles)):
            WIN.blit(self.red_projectiles[num_red_projectile].shot_image, (
            self.red_projectiles[num_red_projectile].x_position,
            self.red_projectiles[num_red_projectile].y_position))

        for num_yellow_projectile in range(len(self.yellow_projectiles)):
            WIN.blit(self.yellow_projectiles[num_yellow_projectile].shot_image, (
            self.yellow_projectiles[num_yellow_projectile].x_position,
            self.yellow_projectiles[num_yellow_projectile].y_position))

        pygame.display.update()

    def yellow_ship_movement(self, keys_pressed):
        if keys_pressed[
            pygame.K_LEFT] and self.yellow_spaceship.hitbox.x - self.yellow_spaceship.velocity > self.BORDER.x + self.BORDER.width:  # YELLOW LEFT\#
            self.yellow_spaceship.hitbox.x -= self.yellow_spaceship.velocity
        if keys_pressed[
            pygame.K_RIGHT] and self.yellow_spaceship.hitbox.x + self.yellow_spaceship.velocity + self.yellow_spaceship.hitbox.width < self.WINDOW_WIDTH:  # YELLOW RIGHT\
            self.yellow_spaceship.hitbox.x += self.yellow_spaceship.velocity
        if keys_pressed[
            pygame.K_UP] and self.yellow_spaceship.hitbox.y - self.yellow_spaceship.velocity > 0:  # YELLOW UP\
            self.yellow_spaceship.hitbox.y -= self.yellow_spaceship.velocity
        if keys_pressed[
            pygame.K_DOWN] and self.yellow_spaceship.hitbox.y + self.yellow_spaceship.velocity + self.yellow_spaceship.hitbox.height < self.WINDOW_HEIGHT:  # YELLOW DOWN\
            self.yellow_spaceship.hitbox.y += self.yellow_spaceship.velocity
        if keys_pressed[pygame.K_KP0] and self.yellow_spaceship.cannon_cooldown==0:
            self.yellow_projectiles.append(Projectile(self.yellow_spaceship.hitbox.x,
                                                      self.yellow_spaceship.hitbox.y + self.yellow_spaceship.cannon_iterator()))
            self.yellow_spaceship.cannon_cooldown = SpaceShip.BASIC_CANNON_COOLDOWN
    def red_ship_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.red_spaceship.hitbox.x - self.red_spaceship.velocity > 0:  # RED LEFT\
            self.red_spaceship.hitbox.x -= self.red_spaceship.velocity
        if keys_pressed[
            pygame.K_d] and self.red_spaceship.hitbox.x + self.red_spaceship.velocity + self.red_spaceship.hitbox.width < self.BORDER.x:  # RED RIGHT\
            self.red_spaceship.hitbox.x += self.red_spaceship.velocity
        if keys_pressed[pygame.K_w] and self.red_spaceship.hitbox.y - self.red_spaceship.velocity > 0:  # RED UP\
            self.red_spaceship.hitbox.y -= self.red_spaceship.velocity
        if keys_pressed[
            pygame.K_s] and self.red_spaceship.hitbox.y + self.red_spaceship.velocity + self.red_spaceship.hitbox.height < self.WINDOW_HEIGHT:  # RED DOWN\
            self.red_spaceship.hitbox.y += self.red_spaceship.velocity
        if keys_pressed[pygame.K_LSHIFT] and self.red_spaceship.cannon_cooldown==0:
            self.red_projectiles.append(Projectile(self.red_spaceship.hitbox.x,
                                                   self.red_spaceship.hitbox.y + self.red_spaceship.cannon_iterator()))
            self.red_spaceship.cannon_cooldown=SpaceShip.BASIC_CANNON_COOLDOWN

    def is_hit(self, target_hitbox, laser_projectiles):
        for projectile in laser_projectiles:
            if projectile.x_position > target_hitbox.x and projectile.x_position < target_hitbox.x + target_hitbox.width and projectile.y_position > target_hitbox.y and projectile.y_position < target_hitbox.y + target_hitbox.height:
                return True
        return False

    def is_vulnerable(self, spaceship):
        if spaceship.hit_invulnerability_duration == 0:
            return True
        else:
            return False

    def lowered_invulnerability_duration(self, spaceship_invunerability_time):
        return spaceship_invunerability_time - 1

    def handle_projectile_movement(self, projectiles, color):
        if color == "red":
            for num_projectile in range(len(projectiles)):
                projectiles[num_projectile].x_position += projectiles[num_projectile].shot_velocity
            projectiles = [item for item in projectiles if item.x_position < 2000]
        else:
            for num_projectile in range(len(projectiles)):
                projectiles[num_projectile].x_position -= projectiles[num_projectile].shot_velocity
            projectiles = [item for item in projectiles if item.x_position > -100]
        return projectiles
