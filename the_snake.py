from random import randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
SUPER_APPLE_COLOR = (0, 0, 255)
BAD_APPLE_COLOR = (200, 20, 240)

# Типы яблок
SUPER_APPLE = 1
BAD_APPPLE = 2

# Цвет кирпича
BRICK_COLOR = (160, 54, 35)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
FIVE_EATEN = 5

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс"""

    # Инициализация базовых атрибутов, позиция и цвет
    def __init__(self, body_color=BORDER_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    # Абстактный метод отрисовки объекта на экране.
    def draw(self, surface):
        """Метод для отрисовки, по умолчанию pass."""
        pass


class Apple(GameObject):
    """Описания поведения яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()
        self.sort_apple = self.choice_sort()

    @staticmethod
    def randomize_position():
        """Реализация слуйного появления яблока."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def choice_sort(self):
        """Описание видов яблок."""
        self.sort_apple = randint(1, 10)
        if self.sort_apple == 1:
            self.body_color = SUPER_APPLE_COLOR
        elif self.sort_apple == 2:
            self.body_color = BAD_APPLE_COLOR
        else:
            self.body_color = (255, 0, 0)
        return self.sort_apple

    # Метод draw класса Apple
    def draw(self, surface):
        """Метод отриссовки яблока."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Brick(Apple):
    """Класс описывающий кирпич, наследуется от Apple"""

    def __init__(self, body_color=BRICK_COLOR):
        super().__init__(body_color)
        self.body_color = BRICK_COLOR

    def brick_out(self):
        """Метод убирающий кирпич с поля"""
        return (SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1)


class Snake(GameObject):
    """Клас для описания поведения змейки"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Описание движения питона
    def move(self):
        """Физика движения змейки"""
        head = self.get_head_position()
        x_new = (self.direction[0] * GRID_SIZE + head[0]) % SCREEN_WIDTH
        y_new = (self.direction[1] * GRID_SIZE + head[1]) % SCREEN_HEIGHT
        # Добавляем новый элемент
        self.positions.insert(0, (x_new, y_new))
        # Удаляем старый
        self.last = (
            self.positions.pop() if self.length < len(self.positions) else None
        )

    def get_head_position(self):
        """Метод для определения головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод возвращения к исходному состоянию"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def draw(self, surface):
        """Отрисовка змейки"""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция обработки действий пользователя."""
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
    """Создаем экземпляры классов"""
    apple = Apple()
    snake = Snake()
    brick = Brick()

    while True:
        clock.tick(SPEED + snake.length)
        apple.draw(screen)
        snake.draw(screen)
        brick.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Реакция на столкновение головы змейки с телом или кирпичем.
        if (snake.get_head_position() in snake.positions[1:]
                or snake.get_head_position() == brick.position):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Реакция на поедание яблока.
        if snake.get_head_position() == apple.position:
            # Если яблоко синее, +3 элемента.
            if apple.sort_apple == SUPER_APPLE:
                snake.length += 3
            # Если яблоко фиалетовое, разбиваем кирпич, уменьшаем змейку
            elif apple.sort_apple == BAD_APPPLE and snake.length > 1:
                snake.length -= 1
                snake.positions.pop()
                screen.fill(BOARD_BACKGROUND_COLOR)
            # Если яблоко красное, увеличиваем на один элемент
            else:
                snake.length += 1
            apple.position = apple.randomize_position()
            apple.choice_sort()
            apple.draw(screen)
        # Появление кирпича.
        if snake.length % FIVE_EATEN == 0:
            brick.brick_out()
#        else:
#            brick.position = brick.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
