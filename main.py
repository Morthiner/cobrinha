import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
FPS = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = RIGHT

    def move(self, food):
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * GRID_SIZE, head[1] + self.direction[1] * GRID_SIZE)

        new_head = ((new_head[0] + WIDTH) % WIDTH, (new_head[1] + HEIGHT) % HEIGHT)

        if new_head in self.body[1:]:
            show_game_over_screen()
            return False

        self.body.insert(0, new_head)

        if new_head == food.position:
            food.spawn(self.body)
        else:
            self.body.pop()

        return True

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, WHITE, (*segment, GRID_SIZE, GRID_SIZE))


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn([])

    def spawn(self, snake_body):
        while True:
            self.position = (random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                             random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
            if self.position not in snake_body:
                break

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*self.position, GRID_SIZE, GRID_SIZE))


def game_over():
    pygame.quit()
    sys.exit()

def show_game_over_screen():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    restart_text = font.render("Pressione R para reiniciar ou Q para sair", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(game_over_text, text_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  
                elif event.key == pygame.K_q:
                    game_over()  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo da Cobrinha')

snake = Snake()
food = Food()

clock = pygame.time.Clock()


game_over_state = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_state = True  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)

    if game_over_state:
        if show_game_over_screen():
          
            snake = Snake()
            food = Food()
            game_over_state = False  

    if not game_over_state:
        if not snake.move(food):
            game_over_state = True  

    screen.fill((0, 0, 0))
    snake.draw(screen)
    food.draw(screen)
    pygame.display.flip()

    # Controla o FPS
    clock.tick(FPS)
