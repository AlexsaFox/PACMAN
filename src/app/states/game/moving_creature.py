from __future__ import annotations

from abc import ABC, abstractmethod
from math import isclose
from random import randrange
from typing import TYPE_CHECKING, Union
from utilities.direction import *
from app.states.game.maze import MazeCell

if TYPE_CHECKING:
    from app.states.game import Game
    from app.themes.sprite import FourDirectionAnimatedSprite


class Line:
    EPS = 1e-3

    def __init__(self, p1: tuple[float, float], p2: tuple[float, float]):
        x1, y1 = p1
        x2, y2 = p2

        # y = k * x + b
        self.k = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.k * x1

    def get_ordinate(self, x: float):
        return self.k * x + self.b

    def is_parallel_to(self, other: Line):
        return isclose(self.k, other.k, abs_tol=Line.EPS)

    def get_intersection_point(self, other: Line):
        if self.is_parallel_to(other):
            raise ValueError(f"{self} and {other} got no intersection points: they are parallel.")

        x = (other.b - self.b) / (self.k - other.k)
        y = self.get_ordinate(x)
        return x, y

    def __eq__(self, other: Line):
        return isclose(self.k, other.k, abs_tol=Line.EPS) and isclose(self.b, other.b, abs_tol=Line.EPS)

    def __str__(self):
        base = f"<Line: y = {self.k}x" 
        
        if self.b == 0:
            return base + ">"
        elif self.b > 0:
            return base + f" + {self.b}>"
        else:
            return base + f" - {-self.b}>"

class MovingCreature(ABC):
    SPRITE_WIDTH = 108
    BOTTOM_LINE_HEIGHT = 54

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
        self.move_direction = None
        self.goal = get_neighbor(self.cell, self.move_direction)
        self.goal = self.goal[0] % self.game.maze.width_in_cells, self.goal[1] % self.game.maze.height_in_cells

    @abstractmethod
    def get_direction(self) -> Union[int, None]:
        pass

    def bottom_line(self) -> tuple[tuple[float, float], tuple[float, float]]:
        if self.direction in [Direction.E, Direction.W]:
            p1 = (
                self.sc_coords[0] - MovingCreature.SPRITE_WIDTH/2,
                self.sc_coords[1] - MovingCreature.BOTTOM_LINE_HEIGHT/2
            )
            p2 = (
                self.sc_coords[0] + MovingCreature.SPRITE_WIDTH/2,
                self.sc_coords[1] + MovingCreature.BOTTOM_LINE_HEIGHT/2
            )
        else:
            p1 = (
                self.sc_coords[0] - MovingCreature.SPRITE_WIDTH/2,
                self.sc_coords[1] + MovingCreature.BOTTOM_LINE_HEIGHT/2
            )
            p2 = (
                self.sc_coords[0] + MovingCreature.SPRITE_WIDTH/2,
                self.sc_coords[1] - MovingCreature.BOTTOM_LINE_HEIGHT/2
            )
        return p1, p2


    def check_collision(self, other: MovingCreature) -> bool:
        self_1, self_2 = self.bottom_line()
        other_1, other_2 = other.bottom_line()
        
        self_min_x = min(self_1[0], self_2[0])
        self_max_x = max(self_1[0], self_2[0])
        other_min_x = min(other_1[0], other_2[0])
        other_max_x = max(other_1[0], other_2[0])

        self_line = Line(self_1, self_2)
        other_line =  Line(other_1, other_2)

        if self_line.is_parallel_to(other_line):
            return self_line == other_line and (
                self_min_x <= other_min_x <= self_max_x or \
                self_min_x <= other_max_x <= self_max_x
            )
            
        intersection = self_line.get_intersection_point(other_line)
        return self_min_x <= intersection[0] <= self_max_x and \
               other_min_x <= intersection[0] <= other_max_x


    def draw(self):
        game_frames_per_sprite_frame = self.game.app.FPS // self.game.app.ANIMATION_FPS

        frame = self.sprite.frame(self.frame_idx // game_frames_per_sprite_frame, self.direction)
        self.frame_idx = (self.frame_idx + 1) % (self.sprite.amount * game_frames_per_sprite_frame)

        pos = frame.get_rect(midbottom=self.sc_coords)
        self.game.app.screen.blit(frame, pos)
        
    def move(self):
        if self.movement_frame == 0:
            self.cell = (
                self.goal[0] % self.game.maze.width_in_cells,
                self.goal[1] % self.game.maze.height_in_cells
            )

            if self.game.maze.grid[self.cell[1]][self.cell[0]].turnable or self.move_direction is None:
                self.move_direction = self.get_direction()
                if self.move_direction is not None:
                    self.direction = self.move_direction

            self.goal = get_neighbor(self.cell, self.move_direction)
            self.goal = self.goal[0], self.goal[1]

        d = (
            self.goal[0] - self.cell[0],
            self.goal[1] - self.cell[1]
        )
        
        cell_coords = self.game.maze.get_cell_center(self.cell)
        self.sc_coords = (
            cell_coords[0] + MazeCell.CELL_WIDTH/2 * (d[0] - d[1]) * self.movement_frame / self.frames_per_cell,
            cell_coords[1] + MazeCell.CELL_HEIGHT/2 * (d[0] + d[1]) * self.movement_frame / self.frames_per_cell
        )

        if self.move_direction is not None:
            self.movement_frame = (self.movement_frame + 1) % self.frames_per_cell
