import pygame

from app.states import AppState
from app.states.game.maze import Maze


class Game(AppState):
    def __init__(self, app):
        super().__init__(app)
        self.maze = Maze.classic(self)

        w, h = self.app.screen.get_size()
        self.screen_center = (w/2, h/2)

    def _draw_maze_cell(self, coords: tuple[int, int]):
        screen = self.app.screen
        screen_size = screen.get_size()

        floor = self.app.theme.floor[0].frame()
        wall = self.app.theme.wall[0].frame()

        screen.blit(floor, self.maze.get_cell_center((coords[0], coords[1]), screen_size))
        if self.maze.grid[coords[0]][coords[1]].is_wall:
            screen.blit(wall, self.maze.get_cell_center((coords[0], coords[1]), screen_size))

    def draw(self):
        min_side = min(self.maze.width_in_cells, self.maze.height_in_cells)
        
        # TODO Draw only nesseccary cells

        for i in range(min_side):
            for j in range(i):
                self.maze.draw_cell((i, j))
                self.maze.draw_cell((j, i))
            self.maze.draw_cell((i, i))


    def handle_event(self, event):
        pressed = pygame.key.get_pressed()

        x, y = self.screen_center
        dx = 25 * (pressed[pygame.K_a] - pressed[pygame.K_d])
        dy = 25 * (pressed[pygame.K_w] - pressed[pygame.K_s])

        self.screen_center = (x + dx, y + dy)
