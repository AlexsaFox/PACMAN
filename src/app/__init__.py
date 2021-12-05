import pygame
import sys
import os

from app.states import AppState
from app.states.loading import Loading
from app.states.game import Game
from app.states.menu import Menu
from app.themes import Theme
from utilities.color import *


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class App:
    # Constants
    WINDOW_CAPTION = "Pac-man"
    ANIMATION_FPS = 15
    FPS = 60
    DEFAULT_SIZE = 1920, 1080

    # Default values for fields of App instance
    BG_COLOR = Color.BLACK

    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode(App.DEFAULT_SIZE, pygame.FULLSCREEN)
        pygame.display.set_caption(App.WINDOW_CAPTION)

        self.theme = Theme.load_theme(Theme.get_available()[1])
        self.state: AppState = Menu(self)
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
        else:
            self.state.handle_event(event)

    def update(self) -> None:
        self.state.update()