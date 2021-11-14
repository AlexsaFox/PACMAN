from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHEKCING
from utilities.direction import *

if TYPE_CHEKCING:
    from app.states.game import Game


class MoveController(ABC):
    @abstractmethod
    def get_direction(self) -> int:
        ...


class MovingCreature(ABC):
    def __init__(self, game: Game, controller: MoveController, start_cell: tuple[int, int], seconds_for_cell: int):
        """ Creates movable object

        Args:
            game (Game): Game object that created this creature
            controller (MoveController): Inherited from MoveController object
            that provides directions for moves
            start_cell (tuple[int, int]): Starting point of creature in maze
            seconds_for_cell (int): Speed of creature; Determines how many seconds
            passes while creature is moving from cell to it's neighbor
        """  

        self.game = game
        self.controller = controller
        self.cell = start_cell
        self.abs_coords = self.game.maze._get_cell_center(self.cell)
        self.frames_per_cell = self.game.app.FPS * seconds_for_cell
        self.movement_frame = 0
        self.direction = None
        
    def move(self):
        if self.movement_frame == 0:
            self.direction = self.controller.get_direction()

        if self.direction is not None:
            ...
