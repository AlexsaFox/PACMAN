from __future__ import annotations

from typing import TYPE_CHECKING
from app.states.game.moving_creature import MovingCreature
from utilities.direction import Direction, opposite

if TYPE_CHECKING:
    from app.states.game import Game
    from app.themes.sprite import FourDirectionAnimatedSprite


class Pacman(MovingCreature):
    SECONDS_PER_CELL = 1

    def __init__(self, game: Game, sprite: FourDirectionAnimatedSprite,start_cell: tuple[int, int]):
        super().__init__(game=game, 
                         start_cell=start_cell,
                         sprite=sprite,
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
        if opposite(new_direction) != self.direction:
            self.hashed_direction = new_direction
