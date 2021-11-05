from __future__ import annotations

import csv
import os

from itertools import combinations
from random import choice
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from app.states.game import Game


class MazeCell:
    CELL_WIDTH = 192
    CELL_HEIGHT = 96

    def __init__(self, maze: Maze, **kwargs):
        # Reference to maze with this cell
        self.maze = maze

        # Get properties
        self.is_wall = kwargs.get('is_wall', False)
        self.has_dot = kwargs.get('has_dot', False)
        self.has_energizer = kwargs.get('has_energizer', False)
        self.is_ghost_box = kwargs.get('is_ghost_box', False)
        self.is_ghost_box_exit = kwargs.get('is_ghost_box_exit', False)
        self.is_pacman_spawnpoint = kwargs.get('is_pacman_spawnpoint', False)

        # Validate properties
        self._validate()

        # Get sprites
        theme = self.maze.game.app.theme
        self.floor_sprite = choice(theme.floor)
        self.wall_sprite = choice(theme.wall)
        self.corner_sprite = choice(theme.top_corner)
        self.dot_sprite = choice(theme.dot)
        self.energizer_sprite = choice(theme.energizer)
        self.ghost_box_exit = choice(theme.ghost_box_exit)

    # Creating and validating cell
    @classmethod
    def from_number(self, maze: Maze, n: int) -> MazeCell:
        return MazeCell(
            maze = maze,
            is_wall = bool(n & (1 << 0)),
            has_dot = bool(n & (1 << 1)),
            has_energizer = bool(n & (1 << 2)),
            is_ghost_box = bool(n & (1 << 3)),
            is_ghost_box_exit = bool(n & (1 << 4)),
            is_pacman_spawnpoint = bool(n & (1 << 5))
        )

    def _validate(self):
        """ Checks if this cell has any conflicting
        properties

        Raises:
            ValueError: conflicting properties exist
        """     
           
        attributes = [
            self.is_wall,
            self.has_dot,
            self.has_energizer,
            self.is_ghost_box,
            self.is_ghost_box_exit,
            self.is_pacman_spawnpoint,
        ]

        if any(a and b for a, b in combinations(attributes, r=2)):
            raise ValueError('Invalid maze cell')

    # Displaying cell on screen
    def draw(self, rel_coords: tuple[int, int], abs_coords: tuple[int, int]):
        """ Displays cell to screen in specified coordinates

        Args:
            abs_coords (tuple[int, int]): Coordinates of the cell in maze grid
            abs_coords (tuple[int, int]): Coordinates of the cell center
        """        

        screen = self.maze.game.app.screen
        rel_y, rel_x = rel_coords
        abs_x, abs_y = abs_coords
        
        # Display floor 
        floor_frame = self.floor_sprite.frame()
        pos = floor_frame.get_rect(center=abs_coords)
        screen.blit(floor_frame, pos)

        # Display wall according to surroundings
        if self.is_wall:
            # Check each corner if it needs wall
            nw = rel_x == 0 or \
                 rel_y == 0 or \
                 (self.maze.grid[rel_y - 1][rel_x].is_wall and \
                  self.maze.grid[rel_y][rel_x - 1].is_wall and \
                  self.maze.grid[rel_y - 1][rel_x - 1].is_wall)

            sw = rel_x == 0 or \
                 rel_y == self.maze.height_in_cells - 1 or \
                 (self.maze.grid[rel_y + 1][rel_x].is_wall and \
                  self.maze.grid[rel_y][rel_x - 1].is_wall and \
                  self.maze.grid[rel_y + 1][rel_x - 1].is_wall)

            se = rel_x == self.maze.width_in_cells - 1 or \
                 rel_y == self.maze.height_in_cells - 1 or \
                 (self.maze.grid[rel_y + 1][rel_x].is_wall and \
                  self.maze.grid[rel_y][rel_x + 1].is_wall and \
                  self.maze.grid[rel_y + 1][rel_x + 1].is_wall)

            ne = rel_x == self.maze.width_in_cells - 1 or \
                 rel_y == 0 or \
                 (self.maze.grid[rel_y - 1][rel_x].is_wall and \
                  self.maze.grid[rel_y][rel_x + 1].is_wall and \
                  self.maze.grid[rel_y - 1][rel_x + 1].is_wall)

            # Draw walls in order
            if nw:
                nw = False
                corner_frame = self.corner_sprite.frame()
                pos = corner_frame.get_rect(midbottom=(abs_x, abs_y))
                screen.blit(corner_frame, pos)

            if ne:
                nw = False
                corner_frame = self.corner_sprite.frame()
                pos = corner_frame.get_rect(midbottom=(abs_x + MazeCell.CELL_WIDTH/4, 
                                                       abs_y + MazeCell.CELL_HEIGHT/4))
                screen.blit(corner_frame, pos)

            if sw:
                nw = False
                corner_frame = self.corner_sprite.frame()
                pos = corner_frame.get_rect(midbottom=(abs_x - MazeCell.CELL_WIDTH/4, 
                                                       abs_y + MazeCell.CELL_HEIGHT/4))
                screen.blit(corner_frame, pos)

            if se:
                corner_frame = self.corner_sprite.frame()
                pos = corner_frame.get_rect(midbottom=(abs_x, 
                                                       abs_y + MazeCell.CELL_HEIGHT/2))
                screen.blit(corner_frame, pos)

        # Display dot
        if self.has_dot:
            dot_frame = self.dot_sprite.frame()
            pos = dot_frame.get_rect(center=abs_coords)
            screen.blit(dot_frame, pos)
            
        # Display energizer
        if self.has_energizer:
            energizer_frame = self.energizer_sprite.frame()
            pos = energizer_frame.get_rect(center=abs_coords)
            screen.blit(energizer_frame, pos)


class Maze:
    LEVEL_PATH = 'levels'

    def __init__(self):
        """ Creates empty maze. Avoid using this
        unless you know what you're doing. 

        Use these instead:
            Maze.from_int_grid(cls, game, grid_nums)
            Maze.classic(cls, game)
        """
        self.grid: list[list[MazeCell]] = []
        self.game: Union[Game, None] = None
        pass

    def _validate(self):
        ...

    # Readonly properties of maze 
    @property
    def width_in_cells(self):
        return len(self.grid)

    @property
    def height_in_cells(self):
        return len(self.grid[0])

    @property
    def width(self):
        return MazeCell.CELL_WIDTH * max(self.width_in_cells, self.height_in_cells)

    @property
    def height(self):
        return MazeCell.CELL_HEIGHT * max(self.width_in_cells, self.height_in_cells)

    @property
    def ne_corner(self) -> tuple[int, int]:
        x, y = self.game.screen_center
        return x, y - self.height/2

    # Drawing cells to screen
    def _get_cell_center(self, rel_coords: tuple[int, int]) -> tuple[int, int]:
        x, y = self.ne_corner
        rel_y, rel_x = rel_coords

        x += MazeCell.CELL_WIDTH/2 * (rel_x - rel_y)
        y += MazeCell.CELL_HEIGHT/2 * (rel_x + rel_y)

        return (x, y)

    def draw_cell(self, rel_coords: tuple[int, int]) -> None:
        y, x = rel_coords
        abs_coords = self._get_cell_center(rel_coords)
        self.grid[y][x].draw(rel_coords, abs_coords)

    # Loading existing mazes from files  
    @staticmethod
    def _load_level_csv(level_name) -> list[list[int]]:
        path = os.path.join(Maze.LEVEL_PATH, level_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} doesn't exist")

        grid = []
        with open(path, 'r') as f:
            csvreader = csv.reader(f)
            for line in csvreader:
                try:
                    grid.append(list(map(int, line)))
                except ValueError:
                    raise ValueError(f"Found non-integer value in {path}")

        return grid

    @classmethod
    def from_int_grid(cls, game: Game, grid_nums: list[list[int]]) -> Maze:
        """ Creates maze from grid of numbers

        Args:
            game (Game): Game object that created this maze
            grid_nums (list[list[int]]): Matrix containing numeric description
            of maze layout

        Returns:
            Maze: Fully functionable Maze instance
        """        

        maze = cls()
        maze.game = game
        maze.grid = [[MazeCell.from_number(maze, n) for n in line] 
                    for line in grid_nums]
        maze._validate()
        return maze

    @classmethod
    def classic(cls, game: Game) -> Maze:
        grid = cls._load_level_csv('classic.csv')
        return cls.from_int_grid(game, grid)
