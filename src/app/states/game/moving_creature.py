from __future__ import annotations

from abc import ABC, abstractmethod
from random import randrange
from typing import TYPE_CHECKING
from utilities.direction import *

if TYPE_CHECKING:
    from app.states.game import Game
    from app.themes.sprite import FourDirectionAnimatedSprite



class MovingCreature(ABC):
    def __init__(self, game: Game, sprite: FourDirectionAnimatedSprite, 
                 start_cell: tuple[int, int], seconds_for_cell: int):
        """ Creates movable object

        Args:
            game (Game): Game object that created this creature
            start_cell (tuple[int, int]): Starting point of creature in maze
            seconds_for_cell (int): Speed of creature; Determines how many seconds
            passes while creature is moving from cell to it's neighbor
        """  

        self.game = game

        self.sprite = sprite
        self.frame_idx = randrange(0, self.sprite.amount)

        self.cell = start_cell
        self.sc_coords = self.game.maze.get_cell_center(self.cell)

        self.frames_per_cell = self.game.app.FPS * seconds_for_cell
        self.movement_frame = 0
        self.direction = None
        self.goal = get_neighbor(self.cell, self.direction)

    @abstractmethod
    def get_direction(self):
        pass

    def draw(self):
        game_frames_per_sprite_frame = self.game.app.FPS // self.game.app.ANIMATION_FPS

        frame = self.sprite.frame(self.frame_idx // game_frames_per_sprite_frame, 
                                  self.direction if self.direction else Direction.N)
        self.frame_idx = (self.frame_idx + 1) % (self.sprite.amount * game_frames_per_sprite_frame)

        pos = frame.get_rect(midbottom=self.sc_coords)
        self.game.app.screen.blit(frame, pos)
        
    def move(self):
        if self.movement_frame == 0:
            ...
            # self.direction = self.get_direction()

        if self.direction is not None:
            ...
            
