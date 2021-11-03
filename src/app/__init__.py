import pygame

from app.states import AppState
from app.states.loading import Loading
from utilities.color import *


class App:
    # Constants
    WINDOW_CAPTION = "Pac-man"
    FPS = 60
    DEFAULT_SIZE = 800, 600

    # Default values for fields of App instance
    BG_COLOR = Color.BLACK

    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode(App.DEFAULT_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption(App.WINDOW_CAPTION)

        self.state: AppState = Loading()
        self.bg_color = App.BG_COLOR

    @property
    def state(self) -> AppState:
        return self._state

    @state.setter
    def state(self, new_state: AppState) -> None:
        self._state = new_state
        self._state.app = self

    def draw(self) -> None:
        self.screen.fill(self.bg_color)
        self.state.draw()
        pygame.display.flip()

    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.VIDEORESIZE:
            size = event.w, event.h
            self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            self.state.handle_event(event)

        self.state.update()
