from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from app import App


class AppState(ABC):
    def __init__(self, app: App):
        self.app = app

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def handle_event(self, event) -> None:
        pass
