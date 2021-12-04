from app.states import AppState
from app.states.menu.button import Button
import pygame

class Menu(AppState):
    def __init__(self,app):
       super().__init__(app)
       self.width,self.height = app.screen.get_size()
       self.screen = app.screen
       self.Game_Button = Button(self.screen, self.width//20, self.height//20, self.width//4, self.height//10, self.height//23, "Play")
    def draw(self):
        #Background


        #Play Button
        self.Game_Button.draw()
        #Records Button
        Records_Button = Button(self.screen, self.width//20, self.height//5, self.width//4, self.height//10, self.height//23, "Records")
        Records_Button.draw()
        #Quit Button
        Quit_Button = Button(self.screen, self.width//20, self.height//2.9, self.width//4, self.height//10, self.height//23, "Quit")
        Quit_Button.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION and self.Game_Button.rect.collidepoint(event.pos):
            self.Game_Button.draw_selection()
        else:
            self.Game_Button.draw()
            
    def update(self):
        ...
