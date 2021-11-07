import pygame

from math import ceil

from app.states import AppState
from app.states.game.maze import Maze, MazeCell


class Game(AppState):
    def __init__(self, app):
        super().__init__(app)
        self.maze = Maze.classic(self)
        
        # Camera center. Cemter of cell in
        # northeast corner of maze is taken as (0, 0)
        self.camera_center = 0, self.maze.height/2 - MazeCell.CELL_HEIGHT/2     # Placeholder, center of maze
                                                                                # Should be pacman start location

    def draw(self):
        # Get cells in corners of screen
        # Calculate top left corner first
        ne_sc_x, ne_sc_y = self.maze.ne_corner
        top_left_mz_y = ne_sc_x/MazeCell.CELL_WIDTH - ne_sc_y/MazeCell.CELL_HEIGHT
        top_left_mz_x = -ne_sc_x/MazeCell.CELL_WIDTH - ne_sc_y/MazeCell.CELL_HEIGHT
        top_left_cell = int(top_left_mz_x), int(top_left_mz_y) 
        
        # Calculate screen width and height in maze cells;
        sc_w, sc_h = self.app.screen.get_size()
        screen_mz_w = ceil(sc_w / MazeCell.CELL_WIDTH)
        screen_mz_h = ceil(sc_h / MazeCell.CELL_HEIGHT)

        # Calculate cells for other corners
        bottom_left_cell = (
            top_left_cell[0] + screen_mz_h, 
            top_left_cell[1] + screen_mz_h
        )
        top_right_cell = (
            top_left_cell[0] + screen_mz_w, 
            top_left_cell[1] - screen_mz_w
        )
        bottom_right_cell = (
            top_left_cell[0] + screen_mz_w + screen_mz_h, 
            top_left_cell[1] - screen_mz_w + screen_mz_h
        ) 

        # Padding to make sure there's no blank space 
        # left on screen
        padding = 3
        top_left_cell = top_left_cell[0] - padding, top_left_cell[1]
        top_right_cell = top_right_cell[0], top_right_cell[1] - padding
        bottom_left_cell = bottom_left_cell[0], bottom_left_cell[1] + padding
        bottom_right_cell = bottom_right_cell[0] + padding, bottom_right_cell[1]
        
        # Helper variables and functions
        x, y = start_x, start_y = top_left_cell
        from_top_border = True
        to_bottom_border = False

        def continue_drawing() -> bool:
            return not (not from_top_border and to_bottom_border and start_y > bottom_right_cell[1])

        def not_end_of_line() -> bool:
            if to_bottom_border:
                return x + y != bottom_left_cell[0] + bottom_left_cell[1]
            else:
                return x - y != bottom_left_cell[0] - bottom_left_cell[1]

        def change_state():
            nonlocal x, y, start_x, start_y, from_top_border, to_bottom_border

            if from_top_border and not to_bottom_border:
                if start_x >= bottom_left_cell[0]:
                    to_bottom_border = True
                elif start_x >= top_right_cell[0]:
                    from_top_border = False
            
            if from_top_border and to_bottom_border and start_x >= top_right_cell[0]:
                    from_top_border = False

            if not from_top_border and not to_bottom_border and start_x >= bottom_left_cell[0]:
                    to_bottom_border = True

            if from_top_border:
                start_x, start_y = start_x + 1, start_y - 1
            else:
                start_x, start_y = start_x + 1, start_y + 1
            x, y = start_x, start_y
        
        # Draw cells
        while continue_drawing():
            # Draw next line from north to south
            while not_end_of_line():
                self.maze.draw_cell((x, y))
                y += 1

            # Change the cell from which the drawing starts;
            # Also change boolean values that are checked if needed
            change_state()

    def handle_event(self, event):
        pressed = pygame.key.get_pressed()

        mult = 20 if pressed[pygame.K_LSHIFT] else 2

        x, y = self.camera_center
        dx = mult   * (pressed[pygame.K_d] - pressed[pygame.K_a])
        dy = mult/2 * (pressed[pygame.K_s] - pressed[pygame.K_w])

        self.camera_center = x + dx, y + dy
