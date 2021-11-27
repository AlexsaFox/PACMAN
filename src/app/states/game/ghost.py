from __future__ import annotations

import pygame
from abc import abstractmethod
from math import inf
from queue import Queue
from random import choice
from typing import TYPE_CHECKING
from app.states.game import pacman
from utilities.direction import *
from app.states.game.moving_creature import MovingCreature

if TYPE_CHECKING:
    from app.states.game import Game
    from app.themes.sprite import FourDirectionAnimatedSprite


class GhostMode:
    CHASE = 0
    SCATTER = 1
    SCATTER = 2


class GhostBase(MovingCreature):
    def __init__(self, game: Game, sprite: FourDirectionAnimatedSprite, 
                 start_cell: tuple[int, int], seconds_for_cell: float, 
                 seconds_for_chase_mode: float, seconds_for_scatter_mode: float,
                 scatter_goal: tuple[int, int]):
        super().__init__(game=game, 
                         start_cell=start_cell,
                         sprite=sprite,
                         seconds_for_cell=seconds_for_cell)
        self.scatter_goal = scatter_goal
        self.seconds_for_chase_mode = seconds_for_chase_mode
        self.seconds_for_scatter_mode = seconds_for_scatter_mode
        self.change_time = pygame.time.get_ticks()
        self.mode = GhostMode.CHASE

    @abstractmethod
    def get_goal_cell(self) -> tuple[int, int]:
        pass
    
    def check_switch_mode(self):
        current_time = pygame.time.get_ticks()
        time_since_change = (current_time - self.change_time) / 1000
        if self.mode == GhostMode.CHASE and time_since_change >= self.seconds_for_chase_mode:
            self.mode = GhostMode.SCATTER
            self.change_time = current_time
        elif (self.mode == GhostMode.SCATTER and time_since_change >= self.seconds_for_scatter_mode) or \
            self.cell == self.scatter_goal:
            self.mode = GhostMode.CHASE
            self.change_time = current_time

    def get_direction(self):
        self.check_switch_mode()
        goal = self.get_goal_cell()

        mz_w = self.game.maze.width_in_cells
        mz_h = self.game.maze.height_in_cells

        q = Queue()
        q.put(self.cell)
        path = [[(-1, -1)] * mz_w for _ in range(mz_h)]
        path[self.cell[1]][self.cell[0]] = self.cell
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while not q.empty():
            u = q.get()

            if u == goal:
                break

            for d in directions:
                v = u[0] + d[0], u[1] + d[1]
                if 0 <= v[0] < mz_w and 0 <= v[1] < mz_h and path[v[1]][v[0]] == (-1, -1) and \
                    not self.game.maze.grid[v[1]][v[0]].is_wall:
                    path[v[1]][v[0]] = u
                    q.put(v)

        direction = None
        bt_cell = goal
        print(goal)
        while bt_cell != path[bt_cell[1]][bt_cell[0]]:
            d = (
                bt_cell[0] - path[bt_cell[1]][bt_cell[0]][0],
                bt_cell[1] - path[bt_cell[1]][bt_cell[0]][1]
            )
            bt_cell = path[bt_cell[1]][bt_cell[0]]

            if d[0] == 1:
                direction = Direction.W
            elif d[0] == -1:
                direction = Direction.E
            elif d[1] == 1:
                direction = Direction.S
            elif d[1] == -1:
                direction = Direction.N

        return direction


class Blinky(GhostBase):
    SECONDS_FOR_CELL = 0.5
    SECONDS_FOR_CHASE_MODE = 10
    SECONDS_FOR_SCATTER_MODE = 5

    def __init__(self, game: Game):
        super().__init__(game=game,
                         sprite=game.app.theme.enemy[0],
                         start_cell=game.maze.blinky_start,
                         scatter_goal=game.maze.blinky_scatter_goal,
                         seconds_for_cell=Blinky.SECONDS_FOR_CELL,
                         seconds_for_chase_mode=Blinky.SECONDS_FOR_CHASE_MODE,
                         seconds_for_scatter_mode=Blinky.SECONDS_FOR_SCATTER_MODE)

    def get_goal_cell(self) -> tuple[int, int]:
        if self.mode == GhostMode.SCATTER:
            return self.game.maze.blinky_scatter_goal
        elif self.mode == GhostMode.CHASE:
            return self.game.pacman.cell


class Inky(GhostBase):
    SECONDS_FOR_CELL = 0.5
    SECONDS_FOR_CHASE_MODE = 10
    SECONDS_FOR_SCATTER_MODE = 5

    def __init__(self, game: Game):
        super().__init__(game=game,
                         sprite=game.app.theme.enemy[1],
                         start_cell=game.maze.inky_start,
                         scatter_goal=game.maze.inky_scatter_goal,
                         seconds_for_cell=Inky.SECONDS_FOR_CELL,
                         seconds_for_chase_mode=Inky.SECONDS_FOR_CHASE_MODE,
                         seconds_for_scatter_mode=Inky.SECONDS_FOR_SCATTER_MODE)

    def get_goal_cell(self) -> tuple[int, int]:
        if self.mode == GhostMode.SCATTER:
            return self.scatter_goal
        elif self.mode == GhostMode.CHASE:
            blinky_pos = self.game.blinky.cell
            pacman_pos = self.game.pacman.cell
            d = pacman_pos[0] - blinky_pos[0], pacman_pos[1] - blinky_pos[1]
            goal = pacman_pos[0] + d[0], pacman_pos[1] + d[1]

            mz_w, mz_h = self.game.maze.width_in_cells, self.game.maze.height_in_cells
            if 0 <= goal[1] < mz_h and 0 <= goal[0] < mz_w and \
                not self.game.maze.grid[goal[1]][goal[0]].is_wall:
                return goal
            
            min_dist = inf
            min_dist_cell = None
            for i, line in enumerate(self.game.maze.grid):
                for j, cell in enumerate(line):
                    if not cell.is_wall and (abs(goal[0] - i) + abs(goal[1] - j)) < min_dist:
                        min_dist = abs(goal[0] - i) + abs(goal[1] - j)
                        min_dist_cell = (j, i)

            return min_dist_cell


class Pinky(GhostBase):
    SECONDS_FOR_CELL = 0.5
    SECONDS_FOR_CHASE_MODE = 10
    SECONDS_FOR_SCATTER_MODE = 5

    def __init__(self, game: Game):
        super().__init__(game=game,
                         sprite=game.app.theme.enemy[2],
                         start_cell=game.maze.pinky_start,
                         scatter_goal=game.maze.pinky_scatter_goal,
                         seconds_for_cell=Pinky.SECONDS_FOR_CELL,
                         seconds_for_chase_mode=Pinky.SECONDS_FOR_CHASE_MODE,
                         seconds_for_scatter_mode=Pinky.SECONDS_FOR_SCATTER_MODE)

    def go_forward(self, cell, direction) -> tuple[tuple[int, int], int]:
        """ Returns [coords, direction], where:
        coords - coordinates of new cell
        direction - movement direction
        """
        neighbor = get_neighbor(cell, direction)
        if not self.game.maze.grid[neighbor[1]][neighbor[0]].is_wall:
            return neighbor, direction
        elif self.game.maze.grid[cell[1]][cell[0]].can_turn(left(direction)) and \
            self.game.maze.grid[cell[1]][cell[0]].can_turn(right(direction)):
            direction = choice((left(direction), right(direction)))
            return get_neighbor(cell, direction), direction
        elif self.game.maze.grid[cell[1]][cell[0]].can_turn(left(direction)):
            return get_neighbor(cell, left(direction)), direction
        elif self.game.maze.grid[cell[1]][cell[0]].can_turn(right(direction)):
            return get_neighbor(cell, right(direction)), direction
        else:
            return get_neighbor(cell, opposite(direction)), direction
        


    def get_goal_cell(self) -> tuple[int, int]:
        if self.mode == GhostMode.SCATTER:
            return self.scatter_goal
        elif self.mode == GhostMode.CHASE:
            cell, direction = self.game.pacman.cell, self.game.pacman.direction
            for _ in range(3):
                cell, direction = self.go_forward(cell, direction)
            return cell


class Clyde(GhostBase):
    SECONDS_FOR_CELL = 0.5
    SECONDS_FOR_CHASE_MODE = 15
    SECONDS_FOR_SCATTER_MODE = 5

    def __init__(self, game: Game):
        super().__init__(game=game,
                         sprite=game.app.theme.enemy[3],
                         start_cell=game.maze.clyde_start,
                         scatter_goal=game.maze.clyde_scatter_goal,
                         seconds_for_cell=Clyde.SECONDS_FOR_CELL,
                         seconds_for_chase_mode=Clyde.SECONDS_FOR_CHASE_MODE,
                         seconds_for_scatter_mode=Clyde.SECONDS_FOR_SCATTER_MODE)

    def get_goal_cell(self) -> tuple[int, int]:
        if self.mode == GhostMode.SCATTER:
            return self.scatter_goal
        else:
            pacman_pos = self.game.pacman.cell
            dist_to_pacman = abs(self.cell[0] - pacman_pos[0]) + abs(self.cell[1] - pacman_pos[1])

            if dist_to_pacman > 8:
                return pacman_pos
            else:
                return self.scatter_goal 
