import pygame


class AppWindow():
    WHITE = (255, 255, 255)
    FPS= 60


    def __init__(self, window_width, window_height):
        self.WIDTH = window_width
        self.HEIGHT = window_height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("First Game")
        self.main_loop(self.WIN)

    def main_loop(self, WIN):
        clock= pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw_window(WIN)
        pygame.quit()

    def draw_window(self, WIN):
        WIN.fill(self.WHITE)
        pygame.display.update()
