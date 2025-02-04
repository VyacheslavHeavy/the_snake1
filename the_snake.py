"""
Модуль для реализации игры "Змейка" с использованием библиотеки Pygame.

Этот модуль содержит классы и функции для создания игрового поля, управления змейкой,
генерации яблок и обработки пользовательского ввода. Игра работает в окне с фиксированным
размером, а змейка управляется с помощью клавиш стрелок.

Основные классы:
- GameObject: Базовый класс для всех игровых объектов.
- Apple: Класс для яблока, которое змейка должна съесть.
- Snake: Класс для змейки, которая управляется игроком.

Основные функции:
- handle_keys: Обрабатывает нажатия клавиш для управления змейкой.
- main: Основная функция игры, запускающая игровой цикл.
"""
from random import randint
import pygame
"""Импортируем необходимые модули"""


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTR_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Изначальная позиция:
SNAKE_START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Этот класс предоставляет общие свойства и методы, которые используются всеми объектами
    на игровом поле. Каждый объект имеет позицию на поле и цвет, которые могут быть
    использованы для отрисовки.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле в формате (x, y).
        body_color (tuple): Цвет объекта в формате RGB. По умолчанию None.
    """

    def __init__(self) -> None:
        """
        Инициализация объекта с начальной позицией и цветом.

        Позиция устанавливается в центр игрового поля, а цвет остается неопределенным
        до переопределения в дочерних классах.
        """
        self.position = SNAKE_START_POSITION
        self.body_color = None

    def draw(self):
        """
        Метод для отрисовки объекта.

        Этот метод должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс для яблока, которое змейка должна съесть.

    Яблоко имеет случайную позицию на игровом поле и отрисовывается в виде красного квадрата.
    При съедании змейкой яблоко перемещается на новую случайную позицию.

    Атрибуты:
        body_color (tuple): Цвет яблока в формате RGB. По умолчанию красный (255, 0, 0).
    """

    def __init__(self):
        """Инициализация яблока со случайной позицией и цветом."""
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self, taked_positions=[SNAKE_START_POSITION]):
        """
        Устанавливает случайную позицию для яблока, исключая занятые позиции.

            taked_positions (list, optional): Список занятых позиций. По умолчанию None.
        """
        while self.position in taked_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает яблоко на новую случайную позицию."""
        self.cell_delete(self.position, BOARD_BACKGROUND_COLOR)
        self.randomize_position()


class Snake(GameObject):
    """
    Класс для змейки, которая управляется игроком.

    Змейка состоит из сегментов, каждый из которых занимает одну клетку на игровом поле.
    Змейка может двигаться в четырех направлениях и увеличиваться в длину при съедании яблок.

    Атрибуты:
        length (int): Текущая длина змейки.
        body_color (tuple): Цвет змейки в формате RGB. По умолчанию зеленый (0, 255, 0).
        positions (list): Список позиций сегментов змейки.
        direction (tuple): Текущее направление движения змейки.
        next_direction (tuple): Следующее направление движения (изменяется при нажатии клавиш).
        last (tuple): Последний удаленный сегмент (для затирания).
    """

    def __init__(self):
        """Инициализация змейки с начальной длиной, цветом и направлением."""
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки на основе следующего направления."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """
        Перемещает змейку в текущем направлении.

        Если змейка съела яблоко, длина увеличивается, и последний сегмент не удаляется.
        """
        head_snake = self.get_head_position()
        new_head = (
            (head_snake[0] + self.direction[0] * GRID_SIZE),
            (head_snake[1] + self.direction[1] * GRID_SIZE))

        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Return:
            tuple: Координаты головы змейки в формате (x, y).
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления змейкой.

    В данном случае управляемый объект змейка.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, запускающая игровой цикл."""
    # Инициализация PyGame.
    pygame.init()
    # Создание экземпляров класса.
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)  # Ограничение FPS
        handle_keys(snake)  # Обработка нажатия клавиш
        snake.update_direction()  # Обновление направления змейки
        # snake.move()

        # Проверка, съела ли змейка яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличение длины змейки.
            apple.randomize_position(snake.positions)  # Рандомное перемещение яблока.

        snake.move()  # Перемещение змейки.

        # Проверка на столкновение змейки со свои телом.
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()  # Сброс змейки в начальное состояние.

        # Отрисовка.
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
