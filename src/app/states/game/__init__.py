from __future__ import annotations

import app
import pygame
from math import ceil
from typing import TYPE_CHECKING
from random import choice, randrange
from app.states import AppState
from app.states.menu.scoreboard import save_result
from app.states.game.ghost import Blinky, Clyde, GhostBase, Inky, Pinky
from app.states.game.maze import Maze, MazeCell
from app.states.game.pacman import Pacman
from utilities.direction import Direction

if TYPE_CHECKING:
    from app.states.game.moving_creature import MovingCreature


class Game(AppState):
    BASE_SCORE_FOR_GHOST_IN_SCARE_MODE = 100

    PAUSE_OVERLAY_BG = (0, 0, 0, 200)
    PAUSE_OVERLAY_FG = (240, 240, 240)
    PAUSE_OVERLAY_TEXT = "Game is paused"
    PAUSE_OVERLAY_FONT = pygame.font.SysFont('Comic Sans MS', 72)

    INFO_PANEL_WIDTH_OF_SCREEN = 0.5
    INFO_PANEL_HEIGHT_OF_SCREEN = 0.1
    INFO_PANEL_BORDER_RADIUS = 30
    INFO_PANEL_BORDER_WIDTH = 5
    INFO_PANEL_BG_COLOR = (0, 0, 0)
    INFO_PANEL_FG_COLOR = (240, 240, 240)
    INFO_PANEL_FONT = pygame.font.SysFont('Comic Sans MS', 48)

    LIFE_SPRITE_WIDTH = 60
    LIFE_SPRITE_PADDING = 20

    def __init__(self, app, score: int = 0, lives: int = 3):
        super().__init__(app)

        self.score = score
        self.lives = lives
        self.is_paused = False
        self.camera_center = 0, 0

        self.life_sprite = choice(self.app.theme.life)
        self.life_frame_idx = randrange(0, self.life_sprite.amount)
        
        self.maze = Maze.classic(self)
        self.pacman = Pacman(self)
        self.ghosts = [
            Blinky(self),
            Inky(self),
            Pinky(self),
            Clyde(self)
        ]
        self.scare_timer = 0
        self.scare_score_for_ghost = Game.BASE_SCORE_FOR_GHOST_IN_SCARE_MODE

    @property
    def blinky(self) -> Blinky:
        return self.ghosts[0]

    @property
    def inky(self) -> Inky:
        return self.ghosts[1]

    @property
    def pinky(self) -> Pinky:
        return self.ghosts[2]

    @property
    def clyde(self) -> Clyde:
        return self.ghosts[3]

    @property
    def creatures(self) -> list[MovingCreature]:
        return self.ghosts + [self.pacman]

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

        # Draw creatures in order
        creatures = sorted(self.creatures, 
                           key=lambda creature: creature.sc_coords[1])
        for creature in creatures:
            creature.draw()

        # Display pause overlay if game is paused
        if self.is_paused:
            overlay = pygame.Surface((sc_w, sc_h), pygame.SRCALPHA)
            overlay.fill(Game.PAUSE_OVERLAY_BG)
            self.app.screen.blit(overlay, (0, 0))

            pause_text = Game.PAUSE_OVERLAY_FONT.render(Game.PAUSE_OVERLAY_TEXT, True, Game.PAUSE_OVERLAY_FG)
            pos = pause_text.get_rect(center=(sc_w/2, sc_h/2))
            self.app.screen.blit(pause_text, pos)

        # Display score and lives
        pygame.draw.rect(
            self.app.screen, 
            Game.INFO_PANEL_BG_COLOR,
            (
                sc_w * (1 - Game.INFO_PANEL_WIDTH_OF_SCREEN)/2, sc_h * (1 - Game.INFO_PANEL_HEIGHT_OF_SCREEN),
                sc_w * Game.INFO_PANEL_WIDTH_OF_SCREEN,sc_h * Game.INFO_PANEL_HEIGHT_OF_SCREEN
            ),
            border_top_left_radius=Game.INFO_PANEL_BORDER_RADIUS,
            border_top_right_radius=Game.INFO_PANEL_BORDER_RADIUS
        )
        pygame.draw.rect(
            self.app.screen, 
            Game.INFO_PANEL_FG_COLOR,
            (
                sc_w * (1 - Game.INFO_PANEL_WIDTH_OF_SCREEN)/2, sc_h * (1 - Game.INFO_PANEL_HEIGHT_OF_SCREEN),
                sc_w * Game.INFO_PANEL_WIDTH_OF_SCREEN,sc_h * Game.INFO_PANEL_HEIGHT_OF_SCREEN + Game.INFO_PANEL_BORDER_WIDTH
            ),
            Game.INFO_PANEL_BORDER_WIDTH,
            border_top_left_radius=Game.INFO_PANEL_BORDER_RADIUS,
            border_top_right_radius=Game.INFO_PANEL_BORDER_RADIUS
        )

        score_text = self.INFO_PANEL_FONT.render(f'{self.score} PTS', True, Game.INFO_PANEL_FG_COLOR)
        pos = score_text.get_rect(center=(sc_w * (1 - Game.INFO_PANEL_WIDTH_OF_SCREEN/2)/2, sc_h * (1 - Game.INFO_PANEL_HEIGHT_OF_SCREEN/2)))
        self.app.screen.blit(score_text, pos)

        life_sprite_center = sc_w * (1 + Game.INFO_PANEL_WIDTH_OF_SCREEN/2)/2 - \
                             self.lives * (Game.LIFE_SPRITE_WIDTH + Game.LIFE_SPRITE_PADDING)/2
        life_frame = self.life_sprite.frame(self.life_frame_idx)
        self.life_frame_idx = (self.life_frame_idx + 1) % self.life_sprite.amount
        for _ in range(self.lives):
            pos = life_frame.get_rect(center=(life_sprite_center, sc_h * (1 - Game.INFO_PANEL_HEIGHT_OF_SCREEN/2)))
            life_sprite_center += Game.LIFE_SPRITE_WIDTH + Game.LIFE_SPRITE_PADDING
            self.app.screen.blit(life_frame, pos)
        
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused

            # Do not process pacman inputs if game is paused
            if not self.is_paused:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    self.pacman.change_direction(Direction.N)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.pacman.change_direction(Direction.E)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.pacman.change_direction(Direction.S)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.pacman.change_direction(Direction.W)
    
    def update(self):
        # Do not process events if game is paused
        if self.is_paused:
            return
            
        # Move pacman and camera to it's position
        self.pacman.move()
        sc_w, sc_h = self.app.screen.get_size()
        self.camera_center = (
            self.camera_center[0] - sc_w/2 + self.pacman.sc_coords[0],
            self.camera_center[1] - sc_h/2 + self.pacman.sc_coords[1]
        )

        # Move ghosts 
        for ghost in self.ghosts:
            ghost.move()

        # If in scare mode, process it's timer
        if self.scare_timer == 1:
            self.scare_timer = 0

            # If timer is over, convert all ghosts back to normal state
            for ghost in self.ghosts:
                ghost.scare_mode = False

            # Make sure all ghosts still exist
            for ghost_type in [Blinky, Inky, Pinky, Clyde]:
                if not any(isinstance(ghost, ghost_type) for ghost in self.ghosts):
                    self.ghosts += [ghost_type(self)]
            
        elif self.scare_timer > 0:
            self.scare_timer -= 1

        # Check collision of pacman with ghosts
        for ghost in self.ghosts:
            if self.pacman.check_collision(ghost):

                # In scare mode
                if self.scare_timer > 0:
                    self.ghosts.remove(ghost)
                    self.score += self.scare_score_for_ghost
                    self.scare_score_for_ghost *= 2

                # In regular mode
                else:
                    self.lives -= 1
                    if self.lives > 0:
                        self.pacman.respawn()
                        break
                    else:
                        self.game_over()

    def activate_scare(self):
        for ghost in self.ghosts:
            ghost.scare_mode = True

        self.scare_score_for_ghost = Game.BASE_SCORE_FOR_GHOST_IN_SCARE_MODE
        self.scare_timer = self.app.FPS * GhostBase.SECONDS_FOR_SCARE_MODE

    def next_level(self):
        self.app.state = Game(self.app, self.score, self.lives)

    def game_over(self):
        """ Is called when pacman loses all lives """
        save_result(self.app.username, self.score)
        self.app.state = app.states.menu.Menu(self.app)