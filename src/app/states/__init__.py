from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App


class AppState(ABC):
    def __init__(self, app: App):
        self.app = app

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
