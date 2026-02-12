import pygame, sys, random

pygame.init()

# Set up initial window size
window_width = 800
window_height = 600
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

# Set the window title
pygame.display.set_caption("Snake Game")

# Variables to track full-screen and running state
is_fullscreen = False
running = True

# Set up fonts
pygame.font.init()
font = pygame.font.Font("Minecraft.ttf", 74)  # Using Minecraft font
small_font = pygame.font.Font("Minecraft.ttf", 36)

# Setting up the size of each block
block_size = 60

# Game loop
clock = pygame.time.Clock()

paused = False

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRID_COLOR = (100, 149, 237)
PAUSE_COLOR = (148, 14, 48)
GAME_OVER_COLOR = (255, 0, 0)

# Load the snake head image and scale it to the block size
snake_head_image = pygame.image.load("snake_head.png")
snake_head_image = pygame.transform.scale(snake_head_image, (block_size, block_size))

# Load the snake body segment image and scale it to the block size
snake_body_image = pygame.image.load("snake_body.png")
snake_body_image = pygame.transform.scale(snake_body_image, (block_size, block_size))

# Create the Apple class
class Apple:
    def __init__(self):
        self.image = pygame.image.load("apple.png")
        self.image = pygame.transform.scale(self.image, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, window_width // block_size - 1) * block_size
        self.rect.y = random.randint(0, window_height // block_size - 1) * block_size

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Create the snake object the player controls
class Snake:
    def __init__(self):
        self.x, self.y = block_size, block_size
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, block_size, block_size)
        self.body = [pygame.Rect(self.x - block_size, self.y, block_size, block_size)]
        self.dead = False

    def draw_head(self, surface):
        angle = 0
        if self.xdir == 1:  # Moving right
            angle = 0
        elif self.xdir == -1:  # Moving left
            angle = 180
        elif self.ydir == 1:  # Moving down
            angle = 90
        elif self.ydir == -1:  # Moving up
            angle = -90


        rotated_head = pygame.transform.rotate(snake_head_image, -1 * angle)
        surface.blit(rotated_head, self.head.topleft)
        
     

    def draw_body(self, surface):
        for i, segment in enumerate(self.body):
            angle = 0
            prev_segment = self.head if i == 0 else self.body[i-1]
            if prev_segment.x < segment.x:  # Moving left
                angle = 180
            elif prev_segment.x > segment.x:  # Moving right
                angle = 0
            elif prev_segment.y < segment.y:  # Moving up
                angle = -90
            elif prev_segment.y > segment.y:  # Moving down
                angle = 90

            rotated_body = pygame.transform.rotate(snake_body_image, angle)
            surface.blit(rotated_body, segment.topleft)

    def move(self):
        # Move the body
        self.body.insert(0, pygame.Rect(self.head.x, self.head.y, block_size, block_size))
        
        # Move the head
        self.head.x += self.xdir * block_size
        self.head.y += self.ydir * block_size

        # Screen wrapping
        if self.head.x >= window_width:
            self.head.x = 0
        elif self.head.x < 0:
            self.head.x = window_width - block_size
        if self.head.y >= window_height:
            self.head.y = 0
        elif self.head.y < 0:
            self.head.y = window_height - block_size

        # Check self-collision
        for segment in self.body[1:]:
            if self.head.colliderect(segment):
                self.dead = True
        
        # Remove last segment if not growing
        self.body.pop()

    def grow(self):
        # Just don't pop the last element to grow
        self.body.append(pygame.Rect(self.head.x, self.head.y, block_size, block_size))

snake = Snake()
apple = Apple()
score = 0

# Draw the grid for the game
def draw_grid():
    # Calculate the number of blocks that fit in the current window size
    blocks_x = window_width // block_size
    blocks_y = window_height // block_size
    
    # Calculate the offsets to center the grid
    offset_x = (window_width - (blocks_x * block_size)) // 2
    offset_y = (window_height - (blocks_y * block_size)) // 2
    
    for x in range(blocks_x):
        for y in range(blocks_y):
            rect = pygame.Rect(x * block_size + offset_x, y * block_size + offset_y, block_size, block_size)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

# Function to pause the game
def pause_game():
    pause_text = font.render("Paused", True, PAUSE_COLOR)
    screen.blit(pause_text, (window_width // 2 - pause_text.get_width() // 2, window_height // 2 - pause_text.get_height() // 2))

# Function to display the score
def display_score():
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (window_width // 2 - score_text.get_width() // 2, 20))

# Function to display game over screen
def game_over_screen():
    game_over_text = font.render("Game Over", True, GAME_OVER_COLOR)
    restart_text = small_font.render("Press 'R' to Restart", True, WHITE)
    screen.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (window_width // 2 - restart_text.get_width() // 2, window_height // 2 + game_over_text.get_height()))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_UP and snake.ydir == 0:  # Prevent 180-degree turns
                snake.xdir, snake.ydir = 0, -1
            elif event.key == pygame.K_DOWN and snake.ydir == 0:
                snake.xdir, snake.ydir = 0, 1
            elif event.key == pygame.K_LEFT and snake.xdir == 0:
                snake.xdir, snake.ydir = -1, 0
            elif event.key == pygame.K_RIGHT and snake.xdir == 0:
                snake.xdir, snake.ydir = 1, 0
            elif event.key == pygame.K_r and snake.dead:
                snake = Snake()
                apple = Apple()
                score = 0
                paused = False

        elif event.type == pygame.VIDEORESIZE:
            if not is_fullscreen:
                window_size = (event.w, event.h)
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
            window_width, window_height = window_size

    if not paused and not snake.dead:
        screen.fill(BLACK)  # Clear the screen with a black color before drawing the grid
        draw_grid()
        snake.move()
        snake.draw_head(screen)
        snake.draw_body(screen)

        # Draw the apple
        apple.draw(screen)

        # Check for collision with apple
        if snake.head.colliderect(apple.rect):
            apple = Apple()
            snake.grow()
            score += 1

        display_score()

    elif paused:
        pause_game()

    elif snake.dead:
        game_over_screen()

    pygame.display.update()
    clock.tick(6)

pygame.quit()
sys.exit()
