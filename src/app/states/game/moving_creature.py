from __future__ import annotations

from abc import ABC, abstractmethod
from random import randrange
from typing import TYPE_CHECKING, Union
from utilities.direction import *
from app.states.game.maze import MazeCell

if TYPE_CHECKING:
    from app.states.game import Game
    from app.themes.sprite import FourDirectionAnimatedSprite


class MovingCreature(ABC):
    def __init__(self, game: Game, sprite: FourDirectionAnimatedSprite, 
                 start_cell: tuple[int, int], seconds_for_cell: float):
        """ Creates movable object

        Args:
            game (Game): Game object that created this creature
            start_cell (tuple[int, int]): Starting point of creature in maze
            seconds_for_cell (float): Speed of creature; Determines how many seconds
            passes while creature is moving from cell to it's neighbor
        """  

        self.game = game

        self.sprite = sprite
        self.frame_idx = randrange(0, self.sprite.amount)
        self.direction = Direction.W

        self.cell = start_cell
        self.sc_coords = self.game.maze.get_cell_center(self.cell)

        self.frames_per_cell = self.game.app.FPS * seconds_for_cell
        self.movement_frame = 0
        self.move_direction = Direction.W
        self.goal = get_neighbor(self.cell, self.move_direction)
        self.goal = self.goal[0] % self.game.maze.width_in_cells, self.goal[1] % self.game.maze.height_in_cells

    @abstractmethod
    def get_direction(self) -> Union[int, None]:
        pass

    def draw(self):
        game_frames_per_sprite_frame = self.game.app.FPS // self.game.app.ANIMATION_FPS

        frame = self.sprite.frame(self.frame_idx // game_frames_per_sprite_frame, self.direction)
        self.frame_idx = (self.frame_idx + 1) % (self.sprite.amount * game_frames_per_sprite_frame)

        pos = frame.get_rect(midbottom=self.sc_coords)
        self.game.app.screen.blit(frame, pos)
        
    def move(self):
        if self.movement_frame == 0:
            self.cell = self.goal

            if self.game.maze.grid[self.cell[1]][self.cell[0]].turnable:
                self.move_direction = self.get_direction()
                if self.move_direction is not None:
                    self.direction = self.move_direction
             
            self.goal = get_neighbor(self.cell, self.move_direction)
            self.goal = self.goal[0] % self.game.maze.width_in_cells, self.goal[1] % self.game.maze.height_in_cells
        
        d = self.goal[0] - self.cell[0], self.goal[1] - self.cell[1]
        cell_coords = self.game.maze.get_cell_center(self.cell)
        self.sc_coords = (
            cell_coords[0] + MazeCell.CELL_WIDTH/2 * (d[0] - d[1]) * self.movement_frame / self.frames_per_cell,
            cell_coords[1] + MazeCell.CELL_HEIGHT/2 * (d[0] + d[1]) * self.movement_frame / self.frames_per_cell
        )

        if self.move_direction is not None:
            self.movement_frame = (self.movement_frame + 1) % self.frames_per_cell
