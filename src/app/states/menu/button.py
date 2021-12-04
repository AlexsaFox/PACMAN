import pygame
class Button():
    def __init__(self,screen, pos_x, pos_y, self_x, self_y, font_size, text):
        self.rect = pygame.Rect(pos_x, pos_y, self_x, self_y)
        self.font_size = font_size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.self_x = self_x
        self.self_y = self_y
        self.screen = screen
        self.text = text
        self.IS_SELECTED = False
    def draw(self):
        pygame.font.init()
        myfont = pygame.font.SysFont("Comic Sans MS", self.font_size)  # use default system font, size 10
        pygame.draw.rect(self.screen, (255,255,255), self.rect)# отрисовка кнопки
        mytext = myfont.render(self.text, 1, (255, 100, 100))#мой текст
        place = mytext.get_rect(center=(self.pos_x+self.self_x/2, self.pos_y+self.self_y/2 - 3))# позиционирование центра отрисовки текста
        self.screen.blit(mytext, place)
    def draw_selection(self):
        pygame.draw.rect(self.screen, (255, 100, 100), self.rect, 6)




