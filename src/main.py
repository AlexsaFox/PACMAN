import pygame
import sys
import os

from app import App


def main():
    clock = pygame.time.Clock()
    app = App()

    while app.running:
        clock.tick(app.FPS)
        for event in pygame.event.get():
            app.handle_event(event)
        app.draw()


if __name__ == "__main__":
    main()
