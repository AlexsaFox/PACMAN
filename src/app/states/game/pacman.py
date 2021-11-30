from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING
from app.states.game.moving_creature import MovingCreature
from utilities.direction import Direction, opposite

if TYPE_CHECKING:
    from app.states.game import Game


class Pacman(MovingCreature):
    SECONDS_PER_CELL = 0.5

    def __init__(self, game: Game):
        super().__init__(game=game, 
                         start_cell=game.maze.pacman_start,
                         sprite=choice(game.app.theme.player),
                         seconds_for_cell=Pacman.SECONDS_PER_CELL)
        self.hashed_direction = None
    
    def get_direction(self):
        cell = self.game.maze.grid[self.cell[1]][self.cell[0]]
        if (self.hashed_direction == Direction.N and cell.can_go_N) or \
            (self.hashed_direction == Direction.E and cell.can_go_E) or \
            (self.hashed_direction == Direction.S and cell.can_go_S) or \
            (self.hashed_direction == Direction.W and cell.can_go_W):
            return self.hashed_direction
        elif (self.move_direction == Direction.N and cell.can_go_N) or \
            (self.move_direction == Direction.E and cell.can_go_E) or \
            (self.move_direction == Direction.S and cell.can_go_S) or \
            (self.move_direction == Direction.W and cell.can_go_W):
            return self.move_direction
        else:
            return None

    def change_direction(self, new_direction: int):
        if self.move_direction is None or opposite(new_direction) != self.direction:
            self.hashed_direction = new_direction
        else:
            self.move_direction = self.direction = self.hashed_direction = new_direction
            self.movement_frame = self.frames_per_cell - self.movement_frame
            self.cell, self.goal = self.goal, self.cell

