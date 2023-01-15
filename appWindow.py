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
        self.red_projectiles=[]
        self.yellow_projectiles=[]
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

            if not self.is_vulnerable(self.yellow_spaceship):
                self.yellow_spaceship.hit_invurnability_duration-=1

            else:
                if self.is_hit(self.yellow_spaceship.hitbox,self.red_projectile):
                    self.yellow_spaceship.health-=1
                    self.yellow_spaceship.hit_invurnability_duration=10

            if not self.is_vulnerable(self.red_spaceship):
                self.red_spaceship.hit_invurnability_duration -= 1

            else:
                if self.is_hit(self.red_spaceship.hitbox, self.yellow_projectile):
                    self.red_spaceship.health -= 1
                    self.red_spaceship.hit_invurnability_duration = 10


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
        WIN.blit(red_health_text,(10,10))
        WIN.blit(yellow_health_text, (self.WINDOW_WIDTH - red_health_text.get_width() - 10, 10))
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
        if keys_pressed[pygame.K_d] and self.red_spaceship.hitbox.x + self.red_spaceship.velocity + self.red_spaceship.hitbox.width < self.BORDER.x:  # RED RIGHT\
            self.red_spaceship.hitbox.x += self.red_spaceship.velocity
        if keys_pressed[pygame.K_w] and self.red_spaceship.hitbox.y - self.red_spaceship.velocity > 0:  # RED UP\
            self.red_spaceship.hitbox.y -= self.red_spaceship.velocity
        if keys_pressed[pygame.K_s] and self.red_spaceship.hitbox.y + self.red_spaceship.velocity + self.red_spaceship.hitbox.height < self.WINDOW_HEIGHT:  # RED DOWN\
            self.red_spaceship.hitbox.y += self.red_spaceship.velocity
        if keys_pressed[pygame.K_LSHIFT] and self.red_projectile.x_position>self.WINDOW_WIDTH:
            self.red_projectile=Projectile(self.red_spaceship.hitbox.x,self.red_spaceship.hitbox.y+self.red_spaceship.cannon_iterator()*80)

    def is_hit(self,target_hitbox,point_damage):

        if point_damage.x_position>target_hitbox.x and point_damage.x_position<target_hitbox.x+target_hitbox.width and point_damage.y_position>target_hitbox.y and point_damage.y_position<target_hitbox.y+target_hitbox.height:
            return True
        else:
            return False
    def is_vulnerable(self,spaceship):
        if spaceship.hit_invurnability_duration == 0:
            return True
        else:
            return False
    def lowered_invulnerability_duration(self,spaceship_invunerability_time):
        return spaceship_invunerability_time-1