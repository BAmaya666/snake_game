import pygame, sys, random, asyncio
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load("head_up.png").convert_alpha()
        self.head_down = pygame.image.load("head_down.png").convert_alpha()
        self.head_right = pygame.image.load("head_right.png").convert_alpha()
        self.head_left = pygame.image.load("head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("body_horizontal.png").convert_alpha()

        self.body_tr = pygame.image.load("body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("body_bl.png").convert_alpha()
        self.crunch_sound = pygame.mixer.Sound("Sound_crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body): #to make a rectangle to position the block images
            x_pos =int(block.x * cell_size) + SIDEBAR_WIDTH
            y_pos =int(block.y * cell_size)
            block_rect =pygame.Rect(x_pos,y_pos,cell_size,cell_size) 

            if index == 0: #what direction is the face heading
                screen.blit(self.head,block_rect)
            elif index == len(self.body) -1: #the tail
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x ==-1 and next_block.y ==-1 or previous_block.y == -1 and next_block.x==-1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x ==-1 and next_block.y ==1 or previous_block.y == 1 and next_block.x==-1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x ==1 and next_block.y ==-1 or previous_block.y == -1 and next_block.x==1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x ==1 and next_block.y ==1 or previous_block.y == 1 and next_block.x==1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)  # Start moving right

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size) + SIDEBAR_WIDTH,int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0
        self.high_score = self.load_high_score()
        self.last_score = 0  # To store the final score before reset

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_sidebar()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize() # reposition the fruit
            self.snake.add_block() # add another block to the snake
            self.snake.play_crunch_sound()
            self.score = len(self.snake.body) - 3
            for block in self.snake.body[1:]: # mouse doesn't appear under snake
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        # Store final score
        self.last_score = len(self.snake.body) - 3
        
        # Update high score if needed
        if self.last_score > self.high_score:
            self.high_score = self.last_score
            self.save_high_score()
        
        # Reset game immediately
        self.snake.reset()
        self.fruit.randomize()
        self.score = 0

    def draw_grass(self):
        grass_color = (25,0,151)
        for row in range(cell_number):
            if row %2 ==0:
                for col in range(cell_number):
                    if col %2 ==0:
                        grass_rect = pygame.Rect(col * cell_size + SIDEBAR_WIDTH, row*cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col %2 !=0:
                        grass_rect = pygame.Rect(col * cell_size + SIDEBAR_WIDTH, row*cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        self.score = len(self.snake.body) - 3
        score_text = str(self.score)
        score_surface = game_font.render(score_text,True,(178,255,102))
        score_x = int(cell_size * cell_number + 100) + SIDEBAR_WIDTH
        score_y = int(cell_size * cell_number - 560)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        # apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        
        
        

    def draw_sidebar(self):
        # Draw sidebar background
        sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, (30, 30, 60), sidebar_rect)
        
        # Draw sidebar border
        pygame.draw.line(screen, (100, 100, 200), (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, SCREEN_HEIGHT), 3)
        
        # Title
        title_font = pygame.font.Font(None, 40)
        title = title_font.render("5N4KE64ME", True, (255, 255, 0))
        screen.blit(title, (SIDEBAR_WIDTH//2 - title.get_width()//2, 30))
	    
		# Current Score
        score_font = pygame.font.Font(None, 36)
        current_score = score_font.render(f"Score: {self.score}", True, (0, 255, 0))
        screen.blit(current_score, (SIDEBAR_WIDTH//2 - current_score.get_width()//2, 100))
        
        # High Score
        high_score_text = title_font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        screen.blit(high_score_text, (SIDEBAR_WIDTH//2 - high_score_text.get_width()//2, 150))
        
        # Last Score (Final score from previous game)
        if self.last_score > 0:
            last_score_text = title_font.render(f"Last Score: {self.last_score}", True, (255, 150, 150))
            screen.blit(last_score_text, (SIDEBAR_WIDTH//2 - last_score_text.get_width()//2, 200))
        
        # Instructions
        instructions_font = pygame.font.Font(None, 28)
        instructions_title = instructions_font.render("CONTROLS", True, (100, 200, 255))
        screen.blit(instructions_title, (SIDEBAR_WIDTH//2 - instructions_title.get_width()//2, 250))
        
        # Control instructions
        controls = [
            "Move: ",
            "Up:W Down:S Left:A Right:D",
            " ",
            "Volume: ",
            "-:[ +:]"
            
        ]
        
        y_offset = 290
        for line in controls:
            text = game_font.render(line, True, (220, 220, 255))
            screen.blit(text, (20, y_offset))
            y_offset += 30
        
        footer_font = pygame.font.Font(None, 24)
        footer_height = 80
        creator = footer_font.render("Brandon Amaya ©", True, (150, 200, 255))
        screen.blit(creator, (SIDEBAR_WIDTH//2 - creator.get_width()//2, SCREEN_HEIGHT - footer_height + 40))

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

# Initialize pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# Game constants
cell_size = 30
cell_number = 20
SIDEBAR_WIDTH = 300  # Width of the sidebar
SCREEN_WIDTH = cell_number * cell_size + SIDEBAR_WIDTH
SCREEN_HEIGHT = cell_number * cell_size

# Create screen with sidebar space
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
apple = pygame.image.load("mouse_chiquito.png").convert_alpha()
game_font = pygame.font.Font(None,25)

# Load and play background music
pygame.mixer.music.load("metalSlug2Desert.mp3")
pygame.mixer.music.play(-1,0.0)
vol = .5
pygame.mixer.music.set_volume(vol)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)

main_game = MAIN()

async def main():
    global vol  # ← Add this line at the very beginning
    import pygbag.aio as asyncio  # Use pygbag's asyncio
    target_fps = 30  # Lower from 60 to 30 for better performance

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: #Up
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_s: #Down
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_a: #Left
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
                if event.key == pygame.K_d: #Right
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                
                # Volume controls
                if event.key == pygame.K_LEFTBRACKET: #music go down
                    vol = max(0.0, vol - 0.1)
                    pygame.mixer.music.set_volume(vol)
                if event.key == pygame.K_RIGHTBRACKET: #music go up
                    vol = min(1.0, vol + 0.1)
                    pygame.mixer.music.set_volume(vol)
        
        # Draw everything
        screen.fill((51,0,102))  # Game area background
        main_game.draw_elements()
        pygame.display.update()
        # clock.tick(60)  # 60 frames per second
        await asyncio.sleep(1/target_fps)

asyncio.run(main())