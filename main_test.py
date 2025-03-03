import pygame
import random
import sys
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting Range Pro")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Загрузка ресурсов
try:
    target_img = pygame.image.load("img/target.png").convert_alpha()
except Exception as e:
    print(f"Ошибка загрузки ресурсов: {e}")
    sys.exit()


class Target:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.reset()

    def reset(self):
        # Размер и скорость в зависимости от сложности
        self.size = 80 - (self.difficulty * 2)
        base_speed = 3 + self.difficulty // 2

        # Начальная позиция с учетом размера
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = random.randint(0, SCREEN_HEIGHT - self.size)

        # Случайное направление движения
        self.speed_x = random.choice([-base_speed, base_speed])
        self.speed_y = random.choice([-base_speed, base_speed])

        self.active = True

    def move(self):
        if self.active:
            # Обновляем позицию
            self.x += self.speed_x
            self.y += self.speed_y

            # Корректировка при выходе за границы
            # Горизонтальные границы
            if self.x <= 0:
                self.x = 0
                self.speed_x = abs(self.speed_x)
            elif self.x >= SCREEN_WIDTH - self.size:
                self.x = SCREEN_WIDTH - self.size
                self.speed_x = -abs(self.speed_x)

            # Вертикальные границы
            if self.y <= 0:
                self.y = 0
                self.speed_y = abs(self.speed_y)
            elif self.y >= SCREEN_HEIGHT - self.size:
                self.y = SCREEN_HEIGHT - self.size
                self.speed_y = -abs(self.speed_y)


class Game:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.time_left = 30
        self.difficulty = 1
        self.targets = [Target(self.difficulty) for _ in range(3)]
        self.start_time = pygame.time.get_ticks()

    def reset(self):
        self.score = 0
        self.time_left = 30
        self.difficulty = 1
        self.targets = [Target(self.difficulty) for _ in range(3)]
        self.start_time = pygame.time.get_ticks()


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        draw_text("SHOOTING RANGE", big_font, WHITE, SCREEN_WIDTH // 2 - 200, 100)
        draw_text("1. Начать игру", font, WHITE, SCREEN_WIDTH // 2 - 80, 300)
        draw_text("2. Выход", font, WHITE, SCREEN_WIDTH // 2 - 60, 350)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    menu = False
                if event.key == K_2:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def game_loop():
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for target in game.targets:
                    if (target.x < mouse_x < target.x + target.size and
                            target.y < mouse_y < target.y + target.size and
                            target.active):
                        game.score += 10 * game.difficulty
                        # Пересоздаем мишень с новыми параметрами
                        game.targets.remove(target)
                        game.targets.append(Target(game.difficulty))

        # Обновление времени
        elapsed = (pygame.time.get_ticks() - game.start_time) // 1000
        game.time_left = 30 - elapsed

        if game.time_left <= 0:
            running = False

        # Увеличение сложности
        game.difficulty = 1 + game.score // 100

        # Обновление мишеней
        for target in game.targets:
            # Обновляем параметры для существующих мишеней
            base_speed = 3 + game.difficulty // 2
            target.difficulty = game.difficulty
            target.speed_x = base_speed if target.speed_x > 0 else -base_speed
            target.speed_y = base_speed if target.speed_y > 0 else -base_speed
            target.size = 80 - (game.difficulty * 2)
            target.move()

        # Отрисовка
        screen.fill(BLACK)

        # Рисуем мишени
        for target in game.targets:
            if target.active:
                scaled_target = pygame.transform.scale(target_img, (target.size, target.size))
                screen.blit(scaled_target, (target.x, target.y))

        # Интерфейс
        draw_text(f"Очки: {game.score}", font, WHITE, 10, 10)
        draw_text(f"Время: {game.time_left}", font, WHITE, SCREEN_WIDTH - 150, 10)
        draw_text(f"Уровень: {game.difficulty}", font, WHITE, SCREEN_WIDTH // 2 - 50, 10)

        pygame.display.update()
        clock.tick(FPS)

    game_over(game.score)


def game_over(score):
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0

    if score > high_score:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
        high_score = score

    while True:
        screen.fill(BLACK)
        draw_text("ИГРА ОКОНЧЕНА", big_font, WHITE, SCREEN_WIDTH // 2 - 200, 100)
        draw_text(f"Ваш счет: {score}", font, WHITE, SCREEN_WIDTH // 2 - 80, 200)
        draw_text(f"Рекорд: {high_score}", font, WHITE, SCREEN_WIDTH // 2 - 80, 250)
        draw_text("1. Новая игра", font, WHITE, SCREEN_WIDTH // 2 - 90, 350)
        draw_text("2. Выход", font, WHITE, SCREEN_WIDTH // 2 - 60, 400)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    main_menu()
                    game_loop()
                    return
                if event.key == K_2:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
    game_loop()