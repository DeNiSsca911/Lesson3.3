from turtledemo.nim import SCREENWIDTH

import pygame
import random

pygame.init()#

SCREEN_WIDTH = 800# указываем ширину окна
SCREEN_HEIGHT = 600# указываем высоту окна
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))#создаем окно с параметрами

pygame.display.set_caption("Игра ТИР") #называем игру
icon = pygame.image.load("img/i.jpg")#прописываем путь к картинке
pygame.display.set_icon(icon)#присваиваем игре логотип

target_img = pygame.image.load("img/target.png")#цель и путь к цели
target_widht = 50#ширина цели
target_hight = 50# высота цели

target_x = random.randint(0,SCREEN_WIDTH - target_widht)
target_y = random.randint(0,SCREEN_HEIGHT - target_hight)

color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


running = True
while running:
    pass

pygame.quit()