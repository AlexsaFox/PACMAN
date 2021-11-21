import pygame

from app import App


def main():
    clock = pygame.time.Clock()
    app = App()

    while app.running:
        clock.tick(app.FPS)

        # TODO: Clear this
        print('FPS:', clock.get_fps())

        for event in pygame.event.get():
            app.handle_event(event)

        app.update()
        app.draw()


if __name__ == "__main__":
    main()
