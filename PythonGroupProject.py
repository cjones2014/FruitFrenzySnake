import pygame
import random
import os

# add Pygame
pygame.init()

# Game Size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
FPS = 10
FONT = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Frenzy Snake")

# Sounds
EAT_SOUND = pygame.mixer.Sound("eat.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("gameover.wav")

# File paths
HIGH_SCORE_FILE = "highscore.txt"
FRUIT_FILE = "fruits.txt"

# Helper functions
def load_fruits():
    # Might not need this is we persist the fruits.txt file
    if not os.path.exists(FRUIT_FILE):
        with open(FRUIT_FILE, 'w') as f:
            f.write("apple\nbanana\nwatermelon\ngrapes\n")
    with open(FRUIT_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write("0")
    with open(HIGH_SCORE_FILE, 'r') as f:
        return int(f.read())

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

# Snake class
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (20, 0)

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, PURPLE, (*segment, CELL_SIZE, CELL_SIZE))

# Fruit class
class Fruit:
    def __init__(self, fruit_list):
        self.fruit_list = fruit_list
        self.image = pygame.transform.scale(
            pygame.image.load("orange.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)
        )
        self.position = self.random_position()

    def random_position(self):
        x = random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        return (x, y)

    def draw(self):
        screen.blit(self.image, self.position)


# Main Game Loop
def main():
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    fruit_names = load_fruits()
    fruit = Fruit(fruit_names)
    score = 0
    high_score = load_high_score()
    paused = False

    running = True
    while running:
        clock.tick(FPS)
    
        # Always process events first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    main()  # Restart game
                    return
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused  # Toggle pause
                elif not paused:  # Only allow movement keys if not paused
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -CELL_SIZE))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, CELL_SIZE))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-CELL_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((CELL_SIZE, 0))
    
        # Game updates only if not paused
        if not paused:
            snake.move()
    
            # Check collisions
            if snake.body[0] == fruit.position:
                snake.grow()
                fruit = Fruit(fruit_names)
                score += 1
                EAT_SOUND.play()
    
            head_x, head_y = snake.body[0]
            if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT or snake.body[0] in snake.body[1:]:
                GAME_OVER_SOUND.play()
                if score > high_score:
                    save_high_score(score)
    
                # Draw Game Over screen
                game_over_text = FONT.render("Game Over! Press R to Restart or Q to Quit", True, RED)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
                pygame.display.flip()
    
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            waiting = False
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                waiting = False
                                running = False
                            elif event.key == pygame.K_r:
                                waiting = False
                                main()
                                return
                break
            
        # Drawing happens always
        screen.blit(background, (0, 0))
        snake.draw()
        fruit.draw()
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        high_score_text = FONT.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))
    
        if paused:
            paused_text = FONT.render("PAUSED", True, YELLOW)
            screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
        pygame.display.flip()


    pygame.quit()

if __name__ == '__main__':
    main()
