import pygame
class Button():
    def draw(screen, pos_x, pos_y, self_x, self_y, font_size, text):
        pygame.font.init()
        myfont = pygame.font.SysFont("Comic Sans MS", font_size)  # use default system font, size 10
        pygame.draw.rect(screen, (255,255,255), (pos_x, pos_y, self_x, self_y))# отрисовка кнопки
        mytext = myfont.render(text, 1, (255, 100, 100))#мой текст
        place = mytext.get_rect(center=(pos_x+self_x/2, pos_y+self_y/2 - 3))# позиционирование центра отрисовки текста
        screen.blit(mytext, place)
        




