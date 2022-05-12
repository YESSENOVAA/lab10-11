import pygame
from random import randrange
import psycopg2
from config import params

playerName = input("Enter your name:\n")

config = psycopg2.connect(**params)
current = config.cursor()

flag = False

insert_into = '''
    INSERT INTO records VALUES (%s, %s);
'''

pygame.init()

# Initializing
WIDTH = 800
HEIGHT = 600
FPS = 10

# Screen & Clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (199, 21, 133)

# Font
font = pygame.font.Font("./font/Cavorting.otf", 50)
gameOver = font.render("Game Over", True, (BLACK))
winOver = font.render("You WON!", True, (BLACK))

# Music
pygame.mixer.music.load("./music/pouyaSerpent.mp3")
pygame.mixer.music.play(-1)

cell = 40

class Food():
    def __init__(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, cell, cell))
    
    def redraw(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)

class FoodBig():
    def __init__(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)
    
    def draw(self):
        pygame.draw.rect(screen, PINK, (self.x, self.y, cell, cell))
    
    def redraw(self):
        self.x = randrange(0, WIDTH, cell)
        self.y = randrange(0, HEIGHT, cell)

class Wall():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, cell, cell))

class Snake():
    def __init__(self):
        self.body = [[80, 80]]
        self.speed = cell
        self.dx = 0
        self.dy = 0
        self.direction = ""
        self.color = GREEN

    def move(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != "right":
                    self.dx = -self.speed
                    self.dy = 0
                    self.direction = "left"
                if event.key == pygame.K_RIGHT and self.direction != "left":
                    self.dx = self.speed
                    self.dy = 0
                    self.direction = "right"
                if event.key == pygame.K_UP and self.direction != "down":
                    self.dx = 0
                    self.dy = -self.speed
                    self.direction = "up"
                if event.key == pygame.K_DOWN and self.direction != "up":
                    self.dx = 0
                    self.dy = self.speed
                    self.direction = "down"
        for i in range(len(self.body) -1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

        self.body[0][0] %= WIDTH
        self.body[0][1] %= HEIGHT
    
    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, self.color, (block[0], block[1], cell, cell))
        
    def collideFood(self, food : Food):
        if self.body[0][0] == food.x and self.body[0][1] == food.y:
            global score
            score += 1
            self.body.append([1000, 1000])
    
    def checkFood(self, food : Food):
        if [food.x, food.y] in self.body:
            food.redraw()
    
    def collideSelf(self):
        if self.body[0] in self.body[1:]:
            global running, lose
            lose = True
            running = False

restart = True
while restart:
    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(0)
    running = True
    lose = False
    pause = False
    score = 0
    level = 0
    
    snake = Snake()
    food = Food()
    foodBig = FoodBig()

    while running:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
restart = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                level += 1
                level %= 3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = True
        screen.fill(WHITE)

        wallsCoor = open(f"wall{level}.txt", 'r').readlines()
        walls = []
        for i, line in enumerate(wallsCoor):
            for j, each in enumerate(line):
                if each == '#':
                    walls.append(Wall(j * cell, i * cell))

        for i in range(0, WIDTH, cell):
            for j in range(0, HEIGHT, cell):
                pygame.draw.rect(screen, BLACK, (i, j, cell, cell), 1)
        
        food.draw()
        snake.draw()
        snake.move(events)
        snake.collideFood(food)
        snake.checkFood(food)
        snake.collideFood(foodBig)
        snake.checkFood(foodBig)
        snake.collideSelf()
        if score % 2 == 0:
            foodBig.draw()

        for wall in walls:
            wall.draw()
            if food.x == wall.x and food.y == wall.y:
                food.redraw()
            if foodBig.x == wall.x and foodBig.y == wall.y:
                foodBig.redraw()
            if snake.body[0][0] == wall.x and snake.body[0][1] == wall.y:
                running = False
                lose = True
                pygame.mixer.music.stop()

        scores = font.render(str(score), True, WHITE)
        screen.blit(scores, (10, 10))
        levelCur = font.render(str(level + 1), True, WHITE)
        screen.blit(levelCur, (WIDTH - 35, 10))
        if score == 8:
            level = 1
            FPS += 0.05
        elif score == 16:
            FPS += 0.05
            level = 2

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    restart = False
                    pause = False
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
        
        while lose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    restart = False
                    running = False
                    lose = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    restart = True
                    running = True
                    lose = False
                    FPS = 10
                    score = 0
                    level = 0
                    snake = Snake()
                    food = Food()
                    pygame.mixer.music.play(-1)
            
            if lose:
                gameOver.set_colorkey((WHITE))
                pos = gameOver.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
                screen.blit(gameOver, pos)

                text_score = font.render(f'Score: {score}', True, BLACK)
                pos = text_score.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(text_score, pos)

                ok = False
                try:
                    get = f'''
                        SELECT record FROM records WHERE name = '{playerName}';
                    '''
                    current.execute(get)
                    output = current.fetchone()
                    scorePlayer = output[0]
                    flag = True
                except:
                    pass

                if ok == False:
                    if flag == True:
                        if score > scorePlayer:
                            update = f'''
                                UPDATE records SET record = {score} WHERE name = '{playerName}';
                            '''
                            current.execute(update)
                    else:
                        current.execute(insert_into, (f'{playerName}', f'{score}'))
                ok = True

            pygame.display.flip()
        pygame.display.flip()
    pygame.display.flip()

current.close()
config.commit()
config.close()
pygame.quit()