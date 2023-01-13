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
    HEALTH_FONT = pygame.font.SysFont('comicssans', 40)

    BACKROUND = pygame.image.load(
        os.path.join('Assets', 'backround1.png'))
    BACKROUND = pygame.transform.scale(
        BACKROUND, (WINDOW_WIDTH, WINDOW_HEIGHT))

    red_spaceship = SpaceShip('red_venom_spaceship.png', LEFT_ROTATION)
    yellow_spaceship = SpaceShip('yellow_venom_spaceship.png', RIGHT_ROTATION)

    def __init__(self):
        pygame.display.set_caption("Star Wowes")
        self.red_projectile=Projectile(2000,0)
        self.yellow_projectile = Projectile(-200, 0)

        self.main_loop(self.WIN)
    def main_loop(self, WIN):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys_pressed = pygame.key.get_pressed()
            self.yellow_ship_movement(keys_pressed)
            self.red_ship_movement(keys_pressed)
            self.red_projectile.x_position += self.red_projectile.shot_velocity
            self.yellow_projectile.x_position -= self.yellow_projectile.shot_velocity

            if self.yellow_hit_detection():
                print("yellow hit")
            if self.red_hit_detection():
                print("red hit")
            self.draw_window(WIN)
        pygame.quit()

    def draw_window(self, WIN):
        WIN.blit(self.BACKROUND, (0, 0))
       # pygame.draw.rect(WIN, self.BLACK, self.red_spaceship.get_hitbox_indicator())
       # pygame.draw.rect(WIN, self.BLACK, self.yellow_spaceship.get_hitbox_indicator())
        pygame.draw.rect(WIN, self.BLACK, self.BORDER)
        WIN.blit(self.yellow_spaceship.spaceship, (self.yellow_spaceship.hitbox.x, self.yellow_spaceship.hitbox.y))
        WIN.blit(self.red_spaceship.spaceship, (self.red_spaceship.hitbox.x, self.red_spaceship.hitbox.y))

        red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)

        try:
            WIN.blit(self.red_projectile.shot_image, (self.red_projectile.x_position, self.red_projectile.y_position))
        except:
            pass
        try:
            WIN.blit(self.yellow_projectile.shot_image, (self.yellow_projectile.x_position, self.yellow_projectile.y_position))
        except:
            pass
        pygame.display.update()

    def yellow_ship_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.yellow_spaceship.hitbox.x - self.yellow_spaceship.velocity > self.BORDER.x + self.BORDER.width:  # YELLOW LEFT\#
            self.yellow_spaceship.hitbox.x -= self.yellow_spaceship.velocity
        if keys_pressed[pygame.K_RIGHT] and self.yellow_spaceship.hitbox.x + self.yellow_spaceship.velocity + self.yellow_spaceship.hitbox.width < self.WINDOW_WIDTH:  # YELLOW RIGHT\
            self.yellow_spaceship.hitbox.x += self.yellow_spaceship.velocity
        if keys_pressed[pygame.K_UP] and self.yellow_spaceship.hitbox.y - self.yellow_spaceship.velocity > 0:  # YELLOW UP\
            self.yellow_spaceship.hitbox.y -= self.yellow_spaceship.velocity
        if keys_pressed[pygame.K_DOWN] and self.yellow_spaceship.hitbox.y + self.yellow_spaceship.velocity + self.yellow_spaceship.hitbox.height < self.WINDOW_HEIGHT:  # YELLOW DOWN\
            self.yellow_spaceship.hitbox.y += self.yellow_spaceship.velocity
        if keys_pressed[pygame.K_KP0] and self.yellow_projectile.x_position<0:
            self.yellow_projectile=Projectile(self.yellow_spaceship.hitbox.x,self.yellow_spaceship.hitbox.y+self.yellow_spaceship.cannon_iterator()*80)

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
        if keys_pressed[pygame.K_LSHIFT] and self.red_projectile.x_position>self.WINDOW_WIDTH:
            self.red_projectile=Projectile(self.red_spaceship.hitbox.x,self.red_spaceship.hitbox.y+self.red_spaceship.cannon_iterator()*80)

    def yellow_hit_detection(self):
        if self.yellow_spaceship.hit_invurnability_duration != 0:
            self.yellow_spaceship.hit_invurnability_duration -= 1
            return False
        if self.yellow_spaceship.hit_invurnability_duration == 0:
            if self.red_projectile.x_position>self.yellow_spaceship.hitbox.x and  self.red_projectile.x_position<self.yellow_spaceship.hitbox.x+self.yellow_spaceship.hitbox.width:
                if self.red_projectile.y_position>self.yellow_spaceship.hitbox.y and  self.red_projectile.y_position<self.yellow_spaceship.hitbox.y+self.yellow_spaceship.hitbox.height:
                    self.yellow_spaceship.hit_invurnability_duration=10
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def red_hit_detection(self):
        if self.red_spaceship.hit_invurnability_duration != 0:
            self.red_spaceship.hit_invurnability_duration -= 1
            return False
        if self.red_spaceship.hit_invurnability_duration == 0:
            if self.yellow_projectile.x_position<self.red_spaceship.hitbox.x+self.red_spaceship.hitbox.width and  self.yellow_projectile.x_position>self.red_spaceship.hitbox.x:
                if self.yellow_projectile.y_position>self.red_spaceship.hitbox.y and  self.yellow_projectile.y_position<self.red_spaceship.hitbox.y+self.red_spaceship.hitbox.height:
                    self.red_spaceship.hit_invurnability_duration=10
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False