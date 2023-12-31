from __future__ import annotations

import csv
import os
import app
from itertools import combinations
from random import choice, randrange
from typing import TYPE_CHECKING
from utilities.direction import Direction

if TYPE_CHECKING:
    from app.states.game import Game


class InvalidMazeLayoutError(ValueError):
    def __init__(self, msg="Bad maze layout"):
        super().__init__(msg)


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
        self.is_blinky_scatter_goal = kwargs.get('is_blinky_scatter_goal', False)
        self.is_pinky_scatter_goal = kwargs.get('is_pinky_scatter_goal', False)
        self.is_inky_scatter_goal = kwargs.get('is_inky_scatter_goal', False)
        self.is_clyde_scatter_goal = kwargs.get('is_clyde_scatter_goal', False)
        self.has_fruit = kwargs.get('has_fruit', False)

        # Set other properties to default values
        self.turnable = False
        self.can_go_N = False
        self.can_go_E = False
        self.can_go_W = False
        self.can_go_S = False

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

        if self.has_fruit:
            self.fruit_sprite = choice(theme.fruit)
            self.fruit_frame_idx = randrange(self.fruit_sprite.amount)
    
    def can_turn(self, direction: int) -> bool:
        if direction == Direction.N:
            return self.can_go_N
        if direction == Direction.E:
            return self.can_go_E
        if direction == Direction.W:
            return self.can_go_W
        if direction == Direction.S:
            return self.can_go_S
        raise ValueError(f'Invalid direction: {direction}')

    @property
    def has_collectible(self):
        return self.has_dot or self.has_energizer or self.has_fruit

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
            is_pacman_spawnpoint = bool(n & (1 << 5)),
            is_blinky_scatter_goal = bool(n & (1 << 6)),
            is_pinky_scatter_goal = bool(n & (1 << 7)),
            is_inky_scatter_goal = bool(n & (1 << 8)),
            is_clyde_scatter_goal = bool(n & (1 << 9)),
            has_fruit = bool(n & (1 << 10))
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
            raise InvalidMazeLayoutError('Invalid maze cell')

    # Displaying cell on screen
    def draw(self, mz_coords: tuple[int, int], screen_coords: tuple[int, int]):
        """ Displays cell to screen in specified coordinates

        Args:
            mz_coords (tuple[int, int]): Coordinates of the cell in maze grid
            screen_coords (tuple[int, int]): Coordinates of the cell center on screen surface
        """        
        game_frames_per_sprite_frame = self.maze.game.app.FPS // self.maze.game.app.ANIMATION_FPS

        screen = self.maze.game.app.screen
        mz_x, mz_y = mz_coords
        sc_x, sc_y = screen_coords
        
        # Display floor 
        floor_frame = self.floor_sprite.frame(self.floor_frame_idx // game_frames_per_sprite_frame)
        self.floor_frame_idx = (self.floor_frame_idx + 1) % (self.floor_sprite.amount * game_frames_per_sprite_frame)
        pos = floor_frame.get_rect(center=screen_coords)
        screen.blit(floor_frame, pos)

        # Display wall according to surroundings
        if self.is_wall:
            # Check each corner if it needs wall
            w, h = self.maze.width_in_cells, self.maze.height_in_cells

            nw = (mz_y <= 0 or self.maze.grid[mz_y - 1][mz_x].is_wall) and \
                 (mz_x <= 0 or self.maze.grid[mz_y][mz_x - 1].is_wall) and \
                 (mz_x <= 0 or mz_y <= 0 or self.maze.grid[mz_y - 1][mz_x - 1].is_wall)

            sw = (mz_y >= h - 1 or self.maze.grid[mz_y + 1][mz_x].is_wall) and \
                 (mz_x <= 0 or self.maze.grid[mz_y][mz_x - 1].is_wall) and \
                 (mz_x <= 0 or mz_y >= h - 1 or self.maze.grid[mz_y + 1][mz_x - 1].is_wall)

            se = (mz_y >= h - 1 or self.maze.grid[mz_y + 1][mz_x].is_wall) and \
                 (mz_x >= w - 1 or self.maze.grid[mz_y][mz_x + 1].is_wall) and \
                 (mz_x >= w - 1 or mz_y >= h - 1 or self.maze.grid[mz_y + 1][mz_x + 1].is_wall)

            ne = (mz_y <= 0 or self.maze.grid[mz_y - 1][mz_x].is_wall) and \
                 (mz_x >= w - 1 or self.maze.grid[mz_y][mz_x + 1].is_wall) and \
                 (mz_x >= w - 1 or mz_y <= 0 or self.maze.grid[mz_y - 1][mz_x + 1].is_wall)

            # Draw walls in order
            wall_frame = self.wall_sprite.frame(self.wall_sprite_idx // game_frames_per_sprite_frame)
            self.wall_sprite_idx = (self.wall_sprite_idx + 1) % (self.wall_sprite.amount * game_frames_per_sprite_frame)
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
            dot_frame = self.dot_sprite.frame(self.dot_frame_idx // game_frames_per_sprite_frame)
            self.dot_frame_idx = (self.dot_frame_idx + 1) % (self.dot_sprite.amount * game_frames_per_sprite_frame)
            pos = dot_frame.get_rect(center=screen_coords)
            screen.blit(dot_frame, pos)
            
        # Display energizer
        if self.has_energizer:
            energizer_frame = self.energizer_sprite.frame(self.energizer_frame_idx // game_frames_per_sprite_frame)
            self.energizer_frame_idx = (self.energizer_frame_idx + 1) % (self.energizer_sprite.amount * game_frames_per_sprite_frame)
            pos = energizer_frame.get_rect(center=screen_coords)
            screen.blit(energizer_frame, pos)

        if self.has_fruit:
            fruit_frame = self.fruit_sprite.frame(self.fruit_frame_idx // game_frames_per_sprite_frame)
            self.fruit_frame_idx = (self.fruit_frame_idx + 1) % (self.fruit_sprite.amount * game_frames_per_sprite_frame)
            pos = fruit_frame.get_rect(center=screen_coords)
            screen.blit(fruit_frame, pos)


class Maze:
    LEVEL_PATH = 'levels'

    def __init__(self, game: Game, grid_nums: list[list[int]]):
        """ Creates maze from grid of numbers

        Args:
            game (Game): Game object that created this maze
            grid_nums (list[list[int]]): Matrix containing numeric description
            of maze layout
        """

        self.game = game
        self.grid = [[MazeCell.from_number(self, n) for n in line] 
                    for line in grid_nums]
        self.collectibles_amount = 0

        self._validate()

    def _validate(self):
        # Get pacman and ghost spawnpoints and make sure 
        # there is at least one of them for each character
        self._pacman_spawnpoints = []
        self._blinky_spawnpoints = []
        ghost_box_counter = 0
        self._pinky_spawnpoints = []
        self._inky_spawnpoints = []
        self._clyde_spawnpoints = []
        self.blinky_scatter_goal = None
        self.pinky_scatter_goal = None
        self.inky_scatter_goal = None
        self.clyde_scatter_goal = None
        for i, line in enumerate(self.grid):
            for j, cell in enumerate(line):
                if cell.is_pacman_spawnpoint:
                    self._pacman_spawnpoints.append((j, i))

                if cell.is_ghost_box_exit:
                    self._blinky_spawnpoints.append((j, i))

                if cell.is_ghost_box:
                    if ghost_box_counter == 0:
                        self._pinky_spawnpoints.append((j, i))
                    if ghost_box_counter == 1:
                        self._inky_spawnpoints.append((j, i))
                    if ghost_box_counter == 2:
                        self._clyde_spawnpoints.append((j, i))
                    ghost_box_counter = (ghost_box_counter + 1) % 3

                if cell.is_blinky_scatter_goal:
                    if self.blinky_scatter_goal is None:
                        self.blinky_scatter_goal = (j, i)
                    else:
                        raise InvalidMazeLayoutError(f'Multiple Blinky scatter goals found: at {self.blinky_scatter_goal} and {(j, i)}')

                if cell.is_pinky_scatter_goal:
                    if self.pinky_scatter_goal is None:
                        self.pinky_scatter_goal = (j, i)
                    else:
                        raise InvalidMazeLayoutError(f'Multiple Pinky scatter goals found: at {self.pinky_scatter_goal} and {(j, i)}')

                if cell.is_inky_scatter_goal:
                    if self.inky_scatter_goal is None:
                        self.inky_scatter_goal = (j, i)
                    else:
                        raise InvalidMazeLayoutError(f'Multiple Inky scatter goals found: at {self.inky_scatter_goal} and {(j, i)}')

                if cell.is_clyde_scatter_goal:
                    if self.clyde_scatter_goal is None:
                        self.clyde_scatter_goal = (j, i)
                    else:
                        raise InvalidMazeLayoutError(f'Multiple Clyde scatter goals found: at {self.clyde_scatter_goal} and {(j, i)}')
        
        if not self._pacman_spawnpoints:
            raise InvalidMazeLayoutError('No Pacman spawnpoint found')
        if not self._blinky_spawnpoints:
            raise InvalidMazeLayoutError('No Blinky spawnpoint found')
        if not self._pinky_spawnpoints:
            raise InvalidMazeLayoutError('No Pinky spawnpoint found')
        if not self._inky_spawnpoints:
            raise InvalidMazeLayoutError('No Inky spawnpoint found')
        if not self._clyde_spawnpoints:
            raise InvalidMazeLayoutError('No Clyde spawnpoint found')
        if self.blinky_scatter_goal is None:
            raise InvalidMazeLayoutError('No Blinky scatter goal found')
        if self.pinky_scatter_goal is None:
            raise InvalidMazeLayoutError('No Pinky scatter goal found')
        if self.inky_scatter_goal is None:
            raise InvalidMazeLayoutError('No Inky scatter goal found')
        if self.clyde_scatter_goal is None:
            raise InvalidMazeLayoutError('No Clyde scatter goal found')

        # Find all turnable cells
        for i, line in enumerate(self.grid):
            for j, cell in enumerate(line):
                if not cell.is_wall:
                    if i + 1 < len(self.grid) and not self.grid[i + 1][j].is_wall and \
                        not (self.grid[i][j].is_ghost_box_exit and self.grid[i + 1][j].is_ghost_box):
                        cell.can_go_S = True 
                    if 0 <= i - 1 and not self.grid[i - 1][j].is_wall and \
                        not (self.grid[i][j].is_ghost_box_exit and self.grid[i - 1][j].is_ghost_box):
                        cell.can_go_N = True 
                    if j + 1 < len(line) and not self.grid[i][j + 1].is_wall and \
                        not (self.grid[i][j].is_ghost_box_exit and self.grid[i][j + 1].is_ghost_box):
                        cell.can_go_W = True 
                    if 0 <= j - 1 <= len(line) and not self.grid[i][j - 1].is_wall and \
                        not (self.grid[i][j].is_ghost_box_exit and self.grid[i][j - 1].is_ghost_box):
                        cell.can_go_E = True

                    if cell.is_ghost_box_exit or \
                        (cell.can_go_N and cell.can_go_E) or \
                        (cell.can_go_E and cell.can_go_S) or \
                        (cell.can_go_S and cell.can_go_W) or \
                        (cell.can_go_W and cell.can_go_N):
                        cell.turnable = True

        # Count collectibles
        for line in self.grid:
            for cell in line:
                if cell.has_collectible:
                    self.collectibles_amount += 1
                    

    # Readonly properties of maze 
    @property
    def width_in_cells(self):
        return len(self.grid[0])

    @property
    def height_in_cells(self):
        return len(self.grid)

    @property
    def width(self):
        return MazeCell.CELL_WIDTH * max(self.width_in_cells, self.height_in_cells)

    @property
    def height(self):
        return MazeCell.CELL_HEIGHT * max(self.width_in_cells, self.height_in_cells)

    @property
    def ne_corner(self) -> tuple[int, int]:
        """ Position on the screen of the center of the 
        cell in the north-east corner of the maze 
        """

        sc_w, sc_h = self.game.app.screen.get_size()
        cam_abs_x, cam_abs_y = self.game.camera_center

        return sc_w/2 - cam_abs_x, sc_h/2 - cam_abs_y

    @property
    def pacman_start(self):
        return choice(self._pacman_spawnpoints)

    @property
    def blinky_start(self):
        return choice(self._blinky_spawnpoints)

    @property
    def pinky_start(self):
        return choice(self._pinky_spawnpoints)
        
    @property
    def inky_start(self):
        return choice(self._inky_spawnpoints)
        
    @property
    def clyde_start(self):
        return choice(self._clyde_spawnpoints)

    # Drawing cells to screen
    def get_cell_center(self, mz_coords: tuple[int, int]) -> tuple[int, int]:
        sc_x, sc_y = self.ne_corner
        mz_x, mz_y = mz_coords

        sc_x += MazeCell.CELL_WIDTH/2 * (mz_x - mz_y)
        sc_y += MazeCell.CELL_HEIGHT/2 * (mz_x + mz_y)

        return sc_x, sc_y

    def draw_cell(self, mz_coords: tuple[int, int]) -> None:
        """ Draws specified maze cell """
        mz_x, mz_y = mz_coords

        if 0 <= mz_x < self.width_in_cells and \
           0 <= mz_y < self.height_in_cells:
            on_screen_coords = self.get_cell_center(mz_coords)
            self.grid[mz_y][mz_x].draw(mz_coords, on_screen_coords)

    # Loading existing mazes from files
    @staticmethod
    def _load_level_csv(level_name) -> list[list[int]]:
        path = app.resource_path(os.path.join(Maze.LEVEL_PATH, level_name))
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
    def classic(cls, game: Game) -> Maze:
        grid = cls._load_level_csv('classic.csv')
        return Maze(game, grid)
