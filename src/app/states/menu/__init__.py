from app.states import AppState
from app.states.menu.button import Button


class Menu(AppState):
    def __init__(self,app):
       super().__init__(app)
       self.width,self.height = app.screen.get_size()
       self.screen = app.screen
    def draw(self):
        #Background
        

        #Buttons
        Button.draw(self.screen, self.width//20, self.height//20, self.width//4, self.height//10, self.height//23, "Play")
        Button.draw(self.screen, self.width//20, self.height//5, self.width//4, self.height//10, self.height//23, "Records")
        Button.draw(self.screen, self.width//20, self.height//2.9, self.width//4, self.height//10, self.height//23, "Quit")
    def handle_event(self, event):
        ...
    def update(self):
        ...
