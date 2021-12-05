import pygame
import os
import app as app_module
from app.states import AppState

class Menu(AppState):
    BUTTON_SURFACE_COLOR = (0, 0, 0, 200)

    BUTTON_FONT_INACTIVE = pygame.font.SysFont("Comic Sans MS", 72)
    BUTTON_FG_INACTIVE = (240, 240, 240)
    BUTTON_FONT_ACTIVE = pygame.font.SysFont("Comic Sans MS", 84)
    BUTTON_FG_ACTIVE = (165, 36, 61)
    BUTTON_PADDING = 30

    def __init__(self, app):
        super().__init__(app)

        bg_path = app_module.resource_path(os.path.join('images', 'background.png'))
        self.bg_image = pygame.image.load(bg_path)

        self.buttons = [
            "PLAY", 
            "SCOREBOARD", 
            "EXIT"
        ]
        self.selection = 0

        self.mx_button_width = 0
        for i, button in enumerate(self.buttons):
            text = Menu.BUTTON_FONT_ACTIVE.render(button, True, Menu.BUTTON_FG_ACTIVE)
            self.mx_button_width = max(self.mx_button_width, text.get_width())
        self.mx_button_width += 2 * Menu.BUTTON_PADDING

    def draw(self):
        # Draw background
        sc_w, sc_h = self.app.screen.get_size()
        pos = self.bg_image.get_rect(center=(sc_w/2, sc_h/2))
        self.app.screen.blit(self.bg_image, pos)

        # Draw buttons
        button_surface_height = (len(self.buttons) - 1) * Menu.BUTTON_FONT_INACTIVE.get_height() + \
                                Menu.BUTTON_FONT_ACTIVE.get_height() + \
                                (len(self.buttons) + 1) * Menu.BUTTON_PADDING
        button_surface = pygame.Surface(
            (
                self.mx_button_width, 
                button_surface_height
            ),
            pygame.SRCALPHA
        )
        button_surface.fill(Menu.BUTTON_SURFACE_COLOR)
        pos = button_surface.get_rect(center=(sc_w/2, sc_h/2))
        self.app.screen.blit(button_surface, pos)
    
        # Draw buttons
        height = (sc_h - button_surface_height) / 2 + Menu.BUTTON_PADDING
        for i, button in enumerate(self.buttons):
            if i == self.selection:
                text = Menu.BUTTON_FONT_ACTIVE.render(
                    button, True, Menu.BUTTON_FG_ACTIVE
                )
                height += text.get_height()
            else:
                text = Menu.BUTTON_FONT_INACTIVE.render(
                    button, True, Menu.BUTTON_FG_INACTIVE
                )
                height += text.get_height()

            pos = text.get_rect(midbottom=(sc_w/2, height))
            self.app.screen.blit(text, pos)
            height += Menu.BUTTON_PADDING
            

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.selection = (self.selection - 1) % len(self.buttons)
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.selection = (self.selection + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.handle_enter_press()

    def handle_enter_press(self):
        if self.selection == 0:
            self.app.state = app_module.states.game.Game(self.app)
        elif self.selection == 1:
            ...
        elif self.selection == 2:
            exit(0)


    def update(self):
        ...
