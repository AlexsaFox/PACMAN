import sys, pygame
from math import cos, pi, sin, sqrt
from random import randint

width = 1600
height = 1200
class Button():
    def __init__(self, screen, self_x, self_y,name, number):
        self.screen = screen
        self.texture = pygame.image.load("xxx")
        self.width = width
        self.height = height
        self.x=self_x
        self.y=self_y
        self.number = number
    def draw(screen,self_x, self_y, text, number):
        pygame.font.init()
        myfont = pygame.font.SysFont(None, 112)  # use default system font, size 10
        pygame.draw.rect(screen, (255,255,255), (self_x, self_y, width/2, height/7.5))# отрисовка кнопки
        mytext = myfont.render(text, 1, (255, 100, 100))#мой текст
        place = mytext.get_rect(center=(self_x+(width/2)/2, self_y+(height/7.5)/2))# позиционирование центра отрисовки текста
        screen.blit(mytext, place)




