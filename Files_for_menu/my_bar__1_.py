# Импорты лучше писать каждый с новой строки, соблюдение pep8
import sys
import pygame
from pygame.locals import Rect

# Размеры
width = 800
height = 600
size = [width, height]

# Цвета
red_color = pygame.Color(255, 0, 0)
black_color = pygame.Color(0, 0, 0)

# Инициализация pygame
pygame.init()


class Bar:
    def __init__(self, screen):
        self.screen = screen
        self.move = False
        self.width = 10
        self.height = 90

    def draw(self, i_x: int, i_y: int):
        pygame.draw.rect(self.screen, black_color, Rect(0, 0, width, height))
        pygame.draw.rect(self.screen, red_color, Rect(i_x, i_y, self.width, self.height))
        pygame.display.update(pygame.Rect(0, 0, width, height))


def main():
    global size
    pygame.init()
    game_over = False
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    bar = Bar(screen)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('This is the end of the game')
                game_over = True
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bar.move = True
                    bar.draw(event.pos[0], 5)
            elif event.type == pygame.MOUSEBUTTONUP:
                bar.move = False
            elif event.type == pygame.MOUSEMOTION and bar.move:
                bar.draw(event.pos[0], 5)

        pygame.display.flip()
        pygame.time.wait(10)

    sys.exit()


if __name__ == "__main__":
    main()
