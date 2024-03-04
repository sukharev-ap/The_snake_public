from random import choice, randint
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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10
speed = 10
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    # Инициализация базовых атрибутов, позиция и цвет
    def __init__(self, body_color = None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color
    
    
    
    # абстактный метод отрисовки объекта на экране    
    def draw (self, surface):
        pass


class Apple(GameObject):
    
    
    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = (255, 0, 0)
    
    
    @staticmethod
    def randomize_position():
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE, 
            randint(0, GRID_HEIGHT) * GRID_SIZE
                )
    
    
    # Метод draw класса Apple
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
    
    
class Snake(GameObject):

    
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None
        
        
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    # Описание движения питона
    def move(self):
        head = self.get_head_position()
        x_new = (self.direction[0] * GRID_SIZE + head[0]) % SCREEN_WIDTH
        y_new = (self.direction[1] * GRID_SIZE+ head[1]) % SCREEN_HEIGHT
        new_element = (x_new, y_new)
        # Добавляем новый элемент
        self.positions.insert(0, new_element)
        # Удаляем старый
        self.last = self.positions.pop() if self.length < len(self.positions) else None
        
        
    
    def get_head_position(self):
        return self.positions[0]
    
    
    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None
    
    
    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

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
 
    while True:
        clock.tick(SPEED + 1)
        apple.draw(screen)
        snake.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
 
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
 
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            apple.draw(screen)
            
 
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

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
