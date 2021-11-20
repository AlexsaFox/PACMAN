import pygame
import os
import app

from abc import ABC, abstractmethod
from utilities.direction import Direction


class AnimatedSprite(ABC):
    FRAMES_CHANGED_PER_SECOND = 12

    def __init__(self):
        self._since_last_frame_change = 0
        self.amount = 0

    @staticmethod
    def _load(sprite_path) -> list[pygame.Surface]:
        if not os.path.exists(sprite_path):
            raise FileNotFoundError(f"Path {sprite_path} doesn't exist")

        frames = []
        i = 0
        frame_path = os.path.join(sprite_path, f"{i}.png")
        while os.path.exists(frame_path):
            img = pygame.image.load(frame_path).convert_alpha()
            frames.append(img)
            
            i += 1
            frame_path = os.path.join(sprite_path, f"{i}.png")

        if len(frames) == 0:
            raise FileNotFoundError(
                f"No _frames were found inside {sprite_path}"
            )

        return frames

    @abstractmethod
    def frame(self, idx) -> pygame.Surface:
        pass

    @classmethod
    @abstractmethod
    def load(cls, sprite_path) -> None:
        pass


class SingleDirectionAnimatedSprite(AnimatedSprite):
    """ Represents game sprite """

    def __init__(self, frames: list[pygame.Surface]):
        super().__init__()
        self._frames = frames
        self.amount = len(frames)

    def frame(self, idx: int) -> pygame.Surface:
        """Returns current frame of sprite

        Args:
            idx (int): Index of sprite frame

        Returns:
            pygame.Surface: surface containing current frame image
        """

        return self._frames[idx]

    @classmethod
    def load(cls, sprite_path) -> "SingleDirectionAnimatedSprite":
        frames = cls._load(sprite_path)
        return cls(frames)


class TwoDirectionAnimatedSprite(AnimatedSprite):
    def __init__(self, frames: list[pygame.Surface]):
        super().__init__()

        self._frames = frames
        self._rev_frames = [pygame.transform.flip(img, True, False)
                            for img in frames]

        self.amount = len(frames)

    def frame(self, 
              idx: int, 
              reversed_: bool = False) -> pygame.Surface:
        """Returns current frame of sprite

        Args:
            idx (int): Index of sprite frame
            reversed (bool, optional): If True, returns inverted 
            horizontally frame. Defaults to False.

        Returns:
            pygame.Surface: surface containing current frame image
        """

        return self._frames[idx] if not reversed_ else self._rev_frames[idx]

    @classmethod
    def load(cls, sprite_path) -> 'TwoDirectionAnimatedSprite':
        frames = cls._load(sprite_path)
        return cls(frames)


class FourDirectionAnimatedSprite(AnimatedSprite):
    def __init__(self, 
                 fwd_frames: list[pygame.Surface], 
                 bwd_frames: list[pygame.Surface]):
        super().__init__()

        if (len(fwd_frames) != len(bwd_frames)):
            raise ValueError("Amount of forward and backward frames doesn't match")
        
        self._W_frames = fwd_frames
        self._S_frames = [pygame.transform.flip(img, True, False) 
                              for img in fwd_frames]
        self._N_frames = bwd_frames
        self._E_frames = [pygame.transform.flip(img, True, False) 
                              for img in bwd_frames]

        self.amount = len(fwd_frames)

    def frame(self, 
              idx: int,
              direction: int) -> pygame.Surface:
        """Returns current frame of sprite

        Args:
            idx (int): Index of sprite frame
            direction(int): Orientation of sprite

        Returns:
            pygame.Surface: surface containing current frame image
        """

        current_frame = None
        if direction == Direction.N:
            current_frame = self._N_frames[idx]
        elif direction == Direction.E:
            current_frame = self._E_frames[idx]
        elif direction == Direction.S:
            current_frame = self._S_frames[idx]
        elif direction == Direction.W:
            current_frame = self._W_frames[idx]
        else:
            raise ValueError(f'Invalid direction value: {direction}')

        return current_frame

    @classmethod
    def load(cls, sprite_path) -> 'FourDirectionAnimatedSprite':
        fwd_path = os.path.join(sprite_path, 'forward')
        fwd_frames = cls._load(fwd_path)

        bwd_path = os.path.join(sprite_path, 'backward')
        bwd_frames = cls._load(bwd_path)

        return cls(fwd_frames, bwd_frames)
