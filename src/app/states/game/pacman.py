from __future__ import annotations

from app.states.game.moving_creature import MovingCreature
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.states.game import Game
    from app.themes.sprite import FourDirectionAnimatedSprite


class Pacman(MovingCreature):
    SECONDS_PER_CELL = 3

    def __init__(self, game: Game, sprite: FourDirectionAnimatedSprite,start_cell: tuple[int, int]):
        super().__init__(game=game, 
                         start_cell=start_cell,
                         sprite=sprite,
                         seconds_for_cell=Pacman.SECONDS_PER_CELL)
    
    def get_direction(self):
        ...

    def change_direction(self, new_direction: int):
        ...
                         