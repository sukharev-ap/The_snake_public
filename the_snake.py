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

# Цвет текста
TEXT_COLOR = (255, 255, 255)

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
BOOST_GROW = 5

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Шрифт для отображения счета
SCORE_FONT = pygame.font.Font(None, 36)

# Константа для области отображения счета
SCORE_RECT = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 36)


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

    def rect_aaaa(self, surface, color):
        """Метод отриссовки яблока."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, color, rect, 1)


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
        # self.rect(surface, BORDER_COLOR)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            # self.rect(surface, BOARD_BACKGROUND_COLOR)
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Описания поведения яблока."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.position = self.randomize_position()
        self.sort_apple = self.choice_sort()

    @staticmethod
    def randomize_position():
        """Реализация слуйного появления яблока."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def choice_sort(self):
        """Описание видов яблок."""
        begin_num = 1
        end_num = 10
        self.sort_apple = randint(begin_num, end_num)
        if self.sort_apple == 1:
            self.body_color = SUPER_APPLE_COLOR
        elif self.sort_apple == 2:
            self.body_color = BAD_APPLE_COLOR
        else:
            self.body_color = APPLE_COLOR
        return self.sort_apple

    # Метод draw класса Apple
    def draw(self, surface):
        """Метод отриссовки яблока."""
        # self.rect(surface, BORDER_COLOR)
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )

        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Brick(Apple):
    """Класс описывающий кирпич, наследуется от Apple"""

    def __init__(self):
        super().__init__()
        self.body_color = BRICK_COLOR
        self.position = self.brick_out()

    def brick_out(self):
        """Метод для удаления кирпича"""
        brick_rect = pygame.Rect(self.position[0],
                                 self.position[1],
                                 GRID_SIZE, GRID_SIZE)
        screen.fill(BOARD_BACKGROUND_COLOR, brick_rect)
        return -GRID_SIZE, -GRID_SIZE


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


def draw_score(surface, score):
    """Функция для отображения счета на экране"""
    # Очистка области для отображения счета
    surface.fill(BOARD_BACKGROUND_COLOR, SCORE_RECT)
    score_text = SCORE_FONT.render(f"Score: {score}", True, TEXT_COLOR)
    score_rect = score_text.get_rect()
    score_rect.topright = (SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
    surface.blit(score_text, score_rect)


def not_in_snake(length, positions, func_position, reset_func):
    """Функция отрисовки объекта за пределами змейки"""
    if length < (GRID_HEIGHT * GRID_WIDTH):
        while True:
            new_apple_position = func_position
            if new_apple_position not in positions:
                new_position = new_apple_position
                return new_position
    else:
        reset_func()
        screen.fill(BOARD_BACKGROUND_COLOR)
        return func_position


def main():
    """Создаем экземпляры классов"""
    snake = Snake()
    apple = Apple()
    brick = Brick()
    is_created = False

    while True:

        clock.tick(SPEED + snake.length)
        draw_score(screen, snake.length)
        apple.draw(screen)
        brick.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)
        # Реакция на столкновение головы змейки с телом или кирпичем
        if (snake.get_head_position() in snake.positions[1:]
                or snake.get_head_position() == brick.position):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Реакция на поедание яблока
        if snake.get_head_position() == apple.position:
            # Если яблоко синее, +3 элемента
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
            # Отриссовка яблока за пределами змейки
            apple.position = (
                not_in_snake(snake.length, snake.positions,
                             apple.randomize_position(),
                             snake.reset
                             ))
            apple.choice_sort()
            apple.draw(screen)
        # Появление кирпича.
        if snake.length % BOOST_GROW == 0 and not is_created:
            brick.position = (
                not_in_snake(snake.length, snake.positions,
                             brick.randomize_position(),
                             snake.reset
                             ))
            is_created = True
        elif snake.length % BOOST_GROW > 0 and not is_created:
            brick.position = brick.brick_out()
            is_created = False
        pygame.display.update()


if __name__ == '__main__':
    main()
