from __future__ import annotations

import csv
import os

from itertools import combinations
from random import choice, randrange
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
        self.floor_frame_idx = randrange(0, self.floor_sprite.amount)

        if self.is_wall:
            self.wall_sprite = choice(theme.wall)
            self.wall_sprite_idx = randrange(0, self.wall_sprite.amount)

        if self.has_dot:
            self.dot_sprite = choice(theme.dot)
            self.dot_frame_idx = randrange(0, self.dot_sprite.amount)

        if self.has_energizer:
            self.energizer_sprite = choice(theme.energizer)
            self.energizer_frame_idx = randrange(0, self.energizer_sprite.amount)

        if self.is_ghost_box_exit:
            self.ghost_box_exit = choice(theme.ghost_box_exit)
            self.ghost_box_frame_idx = randrange(0, self.ghost_box_exit.amount)

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
    def draw(self, mz_coords: tuple[int, int], screen_coords: tuple[int, int]):
        """ Displays cell to screen in specified coordinates

        Args:
            abs_coords (tuple[int, int]): Coordinates of the cell in maze grid
            screen_coords (tuple[int, int]): Coordinates of the cell center on screen surface
        """        

        screen = self.maze.game.app.screen
        mz_x, mz_y = mz_coords
        sc_x, sc_y = screen_coords
        
        # Display floor 
        floor_frame = self.floor_sprite.frame(self.floor_frame_idx)
        self.floor_frame_idx = (self.floor_frame_idx + 1) % self.floor_sprite.amount
        pos = floor_frame.get_rect(center=screen_coords)
        screen.blit(floor_frame, pos)

        # Display wall according to surroundings
        if self.is_wall:
            # Check each corner if it needs wall
            nw = mz_x == 0 or \
                 mz_y == 0 or \
                 (self.maze.grid[mz_y - 1][mz_x].is_wall and \
                  self.maze.grid[mz_y][mz_x - 1].is_wall and \
                  self.maze.grid[mz_y - 1][mz_x - 1].is_wall)

            sw = mz_x == 0 or \
                 mz_y == self.maze.height_in_cells - 1 or \
                 (self.maze.grid[mz_y + 1][mz_x].is_wall and \
                  self.maze.grid[mz_y][mz_x - 1].is_wall and \
                  self.maze.grid[mz_y + 1][mz_x - 1].is_wall)

            se = mz_x == self.maze.width_in_cells - 1 or \
                 mz_y == self.maze.height_in_cells - 1 or \
                 (self.maze.grid[mz_y + 1][mz_x].is_wall and \
                  self.maze.grid[mz_y][mz_x + 1].is_wall and \
                  self.maze.grid[mz_y + 1][mz_x + 1].is_wall)

            ne = mz_x == self.maze.width_in_cells - 1 or \
                 mz_y == 0 or \
                 (self.maze.grid[mz_y - 1][mz_x].is_wall and \
                  self.maze.grid[mz_y][mz_x + 1].is_wall and \
                  self.maze.grid[mz_y - 1][mz_x + 1].is_wall)

            # Draw walls in order
            wall_frame = self.wall_sprite.frame(self.wall_sprite_idx)
            self.wall_sprite_idx = (self.wall_sprite_idx + 1) % self.wall_sprite.amount
            if nw:
                pos = wall_frame.get_rect(midbottom=(sc_x, sc_y))
                screen.blit(wall_frame, pos)
            if ne:
                pos = wall_frame.get_rect(midbottom=(sc_x + MazeCell.CELL_WIDTH/4, 
                                                     sc_y + MazeCell.CELL_HEIGHT/4))
                screen.blit(wall_frame, pos)
            if sw:
                pos = wall_frame.get_rect(midbottom=(sc_x - MazeCell.CELL_WIDTH/4, 
                                                     sc_y + MazeCell.CELL_HEIGHT/4))
                screen.blit(wall_frame, pos)
            if se:
                pos = wall_frame.get_rect(midbottom=(sc_x, 
                                                     sc_y + MazeCell.CELL_HEIGHT/2))
                screen.blit(wall_frame, pos)

        # Display dot
        if self.has_dot:
            dot_frame = self.dot_sprite.frame(self.dot_frame_idx)
            self.dot_frame_idx = (self.dot_frame_idx + 1) % self.dot_sprite.amount
            pos = dot_frame.get_rect(center=screen_coords)
            screen.blit(dot_frame, pos)
            
        # Display energizer
        if self.has_energizer:
            energizer_frame = self.energizer_sprite.frame(self.energizer_frame_idx)
            self.energizer_frame_idx = (self.energizer_frame_idx + 1) % self.energizer_sprite.amount
            pos = energizer_frame.get_rect(center=screen_coords)
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
        """ Position on the screen of the cell center
        in north-east corner of the maze 
        """

        sc_w, sc_h = self.game.app.screen.get_size()
        cam_x, cam_y = self.game.camera_center

        return sc_w/2 - cam_x, sc_h/2 - cam_y

    # Drawing cells to screen
    def _get_cell_center(self, mz_coords: tuple[int, int]) -> tuple[int, int]:
        sc_x, sc_y = self.ne_corner
        mz_x, mz_y = mz_coords

        sc_x += MazeCell.CELL_WIDTH/2 * (mz_x - mz_y)
        sc_y += MazeCell.CELL_HEIGHT/2 * (mz_x + mz_y)

        return sc_x, sc_y

    def draw_cell(self, mz_coords: tuple[int, int]) -> None:
        """ Draws specified maze cell """
        mz_x, mz_y = mz_coords

        if mz_x < 0 or mz_x >= self.width_in_cells or \
            mz_y < 0 or mz_y >= self.height_in_cells:
            return

        on_screen_coords = self._get_cell_center(mz_coords)
        self.grid[mz_y][mz_x].draw(mz_coords, on_screen_coords)

    # Loading existing mazes from files
    @staticmethod
    def _load_level_csv(level_name) -> list[list[int]]:
        path = os.path.join(Maze.LEVEL_PATH, level_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Level file at {path} doesn't exist")

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
