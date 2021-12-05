import pygame
import sys
import app as app_module
from app.states import AppState
from app.states.menu import Menu 
from app.states.game import Game
import os



dark_blue = [15, 22, 70]
white= [0, 0, 0]
myfont = pygame.font.SysFont('Comic Sans MS', 32)
myfontForTopics = pygame.font.SysFont('Comic Sans MS', 45)
myfontSmall= pygame.font.SysFont('Comic Sans MS', 25)

class Loading(AppState):
    def __init__(self, app, text=''):
        super().__init__(app)
        path=app_module.resource_path(os.path.join('images','logo.png' ))
        self.image = pygame.image.load(path)
        width, height = self.app.screen.get_size()
        self.progress=0
        self.rect = pygame.Rect(width/1.75, height/3.5, width/2.5, height/13)
        self.active = False
        self.text = text
        self.color=(90, 98, 148)
        self.txt_surface=myfont.render(text, True, self.color)
        self.COLOR_INACTIVE=(90, 98, 148)
        self.COLOR_ACTIVE=(164, 173, 224)
        self.x_op=width/2
        self.y_op = height / 7

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = myfont.render(self.text, True, self.color) 
        if self.progress>100:     
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.app.state=Game(self.app)
        pass

    def draw(self):
        self.app.screen.fill(dark_blue)
        self.image_rect = self.image.get_rect(center=(self.x_op, self.y_op))
        self.app.screen.blit(self.image, self.image_rect)
        if self.progress<=100:
            s = 'Loading'
            time_count=400
            width, height = self.app.screen.get_size()
            text_progress = myfontForTopics.render('{} %'.format(self.progress), False, (255, 255, 255))
            text_rect=text_progress.get_rect(center=(width/2, height/2.5))
            self.app.screen.blit(text_progress, text_rect)
            text_title = myfontSmall.render('Developers: Team Сripples', False, (255, 255, 255))
            text_rect2 = text_title.get_rect(center=(width / 2, height / 1.25))
            self.app.screen.blit(text_title, text_rect2)
            self.progress += 20
            for i in range (3):
                spots = myfontForTopics.render(s, False, (255, 255, 255))
                self.app.screen.blit(spots, (width/2.35, height / 2.2))
                pygame.time.wait(time_count)
                s = s + '.'
                time_count-=100
                pygame.display.update()
            pygame.display.update()
        else:
            self.progress+=1
            self.app.screen.fill(dark_blue)
            width, height = self.app.screen.get_size()
            text_surface = myfontForTopics.render('Press Enter to Continue >>', False, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width / 2, height/1.75 ))
            self.app.screen.blit(text_surface, text_rect)
            text_surface = myfont.render('Enter your name', False, (255, 255, 255))
            self.app.screen.blit(text_surface, (width / 7, height / 3.5))
            self.app.screen.blit(self.txt_surface, (self.rect.x+width/200, self.rect.y-height/150))
            pygame.draw.rect(self.app.screen, self.color, self.rect, 2)
            pygame.display.update()
        pass
    
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
