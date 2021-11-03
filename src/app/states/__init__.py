import app

from abc import ABC, abstractmethod
from typing import Union


class AppState(ABC):
    def __init__(self):
        self.app: Union[app.App, None] = None

    @abstractmethod
    def draw(self) -> None:
        pass

    def move(self) -> None:
        pass

    def update(self) -> None:
        self.move()
        self.draw()

    @abstractmethod
    def handle_event(self, event) -> None:
        pass
