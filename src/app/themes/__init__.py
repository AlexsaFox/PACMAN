import os

from app.themes.sprite import *
import app

class Theme:
    PATH = "themes"
    SPRITE_TYPES = {
        "dot": SingleDirectionAnimatedSprite,
        "enemy": FourDirectionAnimatedSprite,
        "enemy_scare": FourDirectionAnimatedSprite,
        "energizer": SingleDirectionAnimatedSprite,
        "floor": SingleDirectionAnimatedSprite,
        "fruit": SingleDirectionAnimatedSprite,
        "ghost_box_exit": TwoDirectionAnimatedSprite,
        "life": SingleDirectionAnimatedSprite,
        "player": FourDirectionAnimatedSprite,
        "wall": SingleDirectionAnimatedSprite,
    }

    def __init__(self, sprites: dict[str, list[AnimatedSprite]]):
        self._sprites = sprites

    @classmethod
    def _load_sprite_variations(cls, sprite_path, sprite_type) -> list[AnimatedSprite]:
        variations = []

        i = 0
        variation_path = os.path.join(sprite_path, str(i))
        while os.path.exists(variation_path):
            variations.append(sprite_type.load(variation_path))

            i += 1
            variation_path = os.path.join(sprite_path, str(i))

        if len(variations) == 0:
            raise FileNotFoundError(
                f"No variations of sprite were found inside {sprite_path}"
            )

        return variations

    @classmethod
    def load_theme(cls, theme_name: str) -> "Theme":
        """Creates new theme object

        Args:
            theme_name (str): Theme name. List of available themes can be get
            from Theme.get_available
        """

        theme_root = app.resource_path(os.path.join(Theme.PATH, theme_name))
        if not os.path.exists(theme_root):
            raise FileNotFoundError(f'Theme "{theme_name}" cannot be found')

        sprites = {}
        for sprite_type in Theme.SPRITE_TYPES:
            sprite_path = os.path.join(theme_root, sprite_type)
            if not os.path.exists(sprite_path):
                raise FileNotFoundError(
                    f'Sprite "{sprite_type}" doesn\'t exist in theme "{theme_name}"'
                )

            variations = Theme._load_sprite_variations(sprite_path, 
                                                       Theme.SPRITE_TYPES[sprite_type])
            sprites[sprite_type] = variations

        return cls(sprites)

    @staticmethod
    def get_available() -> list[str]:
        """Returns list of themes from /themes folder"""

        return os.listdir(app.resource_path(Theme.PATH))

    @property
    def dot(self) -> list[SingleDirectionAnimatedSprite]:
        return self._sprites.get("dot")

    @property
    def enemy(self) -> list[FourDirectionAnimatedSprite]:
        return self._sprites.get("enemy")

    @property
    def enemy_scare(self) -> list[FourDirectionAnimatedSprite]:
        return self._sprites.get("enemy_scare")

    @property
    def energizer(self) -> list[SingleDirectionAnimatedSprite]:
        return self._sprites.get("energizer")

    @property
    def floor(self) -> list[SingleDirectionAnimatedSprite]:
        return self._sprites.get("floor")

    @property
    def fruit(self) -> list[SingleDirectionAnimatedSprite]:
        return self._sprites.get("fruit")

    @property
    def ghost_box_exit(self) -> list[TwoDirectionAnimatedSprite]:
        return self._sprites.get("ghost_box_exit")

    @property
    def player(self) -> list[FourDirectionAnimatedSprite]:
        return self._sprites.get("player")

    @property
    def wall(self) -> list[SingleDirectionAnimatedSprite]:
        return self._sprites.get("wall")

    @property
    def life(self) -> list[SingleDirectionAnimatedSprite]:
        return self._sprites.get("life")