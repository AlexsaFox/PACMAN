import sys, pygame
from math import cos, pi, sin, sqrt
from random import randint

width=1600
height = 800  # Размеры экрана
black = 0, 0, 0  # rgb черного цвета
size=[width, height]
red = (255, 0, 0)
pygame.init()
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
clock = pygame.time.Clock()
fps = 60
bg = [255, 255, 255]
window = pygame.display.set_mode((800, 800))
myfont = pygame.font.SysFont(None,112) # use default system font, size 10
mytext = myfont.render('Menu', 1, (255, 100, 100))
class Button():
    def __init__(self, screen, self_x, self_y,name, number):
        self.screen = screen
        self.texture = pygame.image.load("xxx")
        self.width = width
        self.height = height
        self.x=self_x
        self.y=self_y
        self.rec = pygame.rect((self_x, self_y, width / 2, height / 7.5))
        self.cord=[self_x,self_y]
        self.number = number
    def draw(screen,self_x, self_y, text, number):
        pygame.draw.rect(screen, (255,255,255), (self_x, self_y, width/2, height/7.5))# отрисовка кнопки
        mytext = myfont.render(text, 1, (255, 100, 100))#мой текст
        place = mytext.get_rect(center=(self_x+(width/2)/2, self_y+(height/7.5)/2))# позиционирование центра отрисовки текста
        screen.blit(mytext, place)




def main():
    global size, width, height
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # pygame.RESIZABLE - позволяет окну изменять размер
    gameover = False

    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('This is the end of the game')
                gameover = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)


        screen.fill(black)
        Button.draw(screen, 50, 50, 'Menu', 1)
        Button.draw(screen, 50,200, 'Settings', 2)
        Button.draw(screen, 50, 350, 'records', 3)

        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


main()