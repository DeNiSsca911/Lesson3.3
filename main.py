import pygame
import random

pygame.init()

# Указываем ширину и высоту окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Называем игру
pygame.display.set_caption("Игра ТИР")

# Загружаем иконку
icon = pygame.image.load("img/i.jpg")
pygame.display.set_icon(icon)

# Загружаем изображение цели
target_img = pygame.image.load("img/target.png")
target_width = 80  # Ширина цели
target_height = 80  # Высота цели

# Начальные координаты цели
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

# Цвет фона (исправлено: добавлена закрывающая скобка)
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

running = True
while running:
    screen.fill(color)  # Заливаем экран цветом
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверяем событие закрытия окна
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Проверяем клик мыши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Проверяем, попал ли клик в цель
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                # Перемещаем цель в случайное место
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)

    # Отображаем цель на экране
    screen.blit(target_img, (target_x, target_y))
    pygame.display.update()  # Обновляем экран

pygame.quit()