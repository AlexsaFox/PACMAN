import os

from main import resource_path

class Theme:
    PATH = "themes"

    def __init__():
        ...

    def load_from_file():
        ...

    @staticmethod
    def get_available() -> list[str]:
        """ Returns list of themes from /themes folder """
        return os.listdir(resource_path(Theme.PATH))