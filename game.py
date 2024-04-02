import pygame
import random
import sys
import time



class Snake:
    def __init__(self,settings,screen,score):
        self.screen = screen
        self.settings = settings
        self.score = score
        self.color = settings.snake_color
        self.direction = settings.init_direction
        self.snake_body=[]
        for i in settings.snake_body:
            self.snake_body.append(pygame.Rect(i[0],i[1],settings.snake_size,settings.snake_size))
                              
    def update_snake(self,settings,game_over):
        self.recent_tail_position_top = self.snake_body[len(self.snake_body)-1].top
        self.recent_tail_position_left = self.snake_body[len(self.snake_body)-1].left
        
        if (self.direction=='RIGHT'):
            head = self.snake_body[0]
            for i in self.snake_body:
                if (i == head):
                    continue
                elif (i.top == head.top and i.left == head.left+10):
                    game_over(self.settings,self.screen,self.score)
            if (self.snake_body[0].x+10>=settings.frame_size_x):
                game_over(self.settings,self.screen,self.score)
            else:
                for i in range(len(self.snake_body)-1,0,-1):
                    self.snake_body[i].x = self.snake_body[i-1].x
                    self.snake_body[i].y = self.snake_body[i-1].y
                self.snake_body[0].x+=10
                
        elif (self.direction=='LEFT'):
            head = self.snake_body[0]
            for i in self.snake_body:
                if (i == head):
                    continue
                elif (i.top == head.top and i.left == head.left-10):
                    game_over(self.settings,self.screen,self.score)
            if (self.snake_body[0].x<=0):
                game_over(self.settings,self.screen,self.score)
            else:
                for i in range(len(self.snake_body)-1,0,-1):
                    self.snake_body[i].x = self.snake_body[i-1].x
                    self.snake_body[i].y = self.snake_body[i-1].y
                self.snake_body[0].x-=10
                
        elif (self.direction=='UP'):
            head = self.snake_body[0]
            for i in self.snake_body:
                if (i == head):
                    continue
                elif (i.top == head.top-10 and i.left == head.left):
                    game_over(self.settings,self.screen,self.score)
            if (self.snake_body[0].y<=0):
                game_over(self.settings,self.screen,self.score)
            else:
                for i in range(len(self.snake_body)-1,0,-1):
                    self.snake_body[i].x = self.snake_body[i-1].x
                    self.snake_body[i].y = self.snake_body[i-1].y
                self.snake_body[0].y-=10
                
        elif (self.direction=='DOWN'):
            head = self.snake_body[0]
            for i in self.snake_body:
                if (i == head):
                    continue
                elif (i.top == head.top+10 and i.left == head.left):
                    game_over(self.settings,self.screen,self.score)
            if (self.snake_body[0].y+10>=settings.frame_size_y):
                game_over(self.settings,self.screen,self.score)
            else:
                for i in range(len(self.snake_body)-1,0,-1):
                    self.snake_body[i].x = self.snake_body[i-1].x
                    self.snake_body[i].y = self.snake_body[i-1].y
                self.snake_body[0].y+=10
        
    def draw_snake(self):
        
        for i in self.snake_body:
            pygame.draw.rect(self.screen,self.color,i)

    def change_direction(self,direction):
        if (direction == 'RIGHT' and self.direction != 'LEFT'):
            self.direction = direction
        elif (direction == 'LEFT' and self.direction != 'RIGHT'):
            self.direction = direction
        elif (direction == 'UP' and self.direction != 'DOWN'):
            self.direction = direction
        elif (direction == 'DOWN' and self.direction != 'UP'):
            self.direction = direction
            
    def grow_body(self):
        curr_body = self.snake_body
        length = len(curr_body)
        self.snake_body.append(pygame.Rect(self.recent_tail_position_left,self.recent_tail_position_top,self.settings.snake_size,self.settings.snake_size))
        
    def check_food(self,food):
        
        if (self.direction == 'RIGHT' and self.snake_body[0].right>=food.get_left() and self.snake_body[0].right<=food.get_right() and self.snake_body[0].top==food.get_top()):
            food.create_food(self.settings,self)
            self.score+=1
            self.grow_body()
            
        elif (self.direction == 'LEFT' and self.snake_body[0].left<=food.get_right() and self.snake_body[0].left>=food.get_left() and self.snake_body[0].top==food.get_top()):
            food.create_food(self.settings,self)
            self.score+=1
            self.grow_body()
        
        elif (self.direction == 'UP' and self.snake_body[0].top<=food.get_bottom() and self.snake_body[0].top>=food.get_top() and self.snake_body[0].left==food.get_left()):
            food.create_food(self.settings,self)
            self.score+=1
            self.grow_body()
        elif (self.direction == 'DOWN' and self.snake_body[0].bottom>=food.get_top() and self.snake_body[0].bottom<=food.get_bottom() and self.snake_body[0].left==food.get_left()):
            food.create_food(self.settings,self)
            self.score+=1
            self.grow_body()

    def get_snake_body(self):

        return self.snake_body
    
class Settings:
    """Game Settings"""
    def __init__(self):
        #window parameters
        self.frame_size_x = 720
        self.frame_size_y = 480
        self.bg_color = (0,0,0)
        
        #parameters for snake
        self.snake_size = 10
        self.snake_pos = [100,50]
        self.snake_body = [[100,50],[90,50],[80,50]]
        self.init_direction = 'RIGHT'
        self.snake_color = (0, 255, 0)
    
        #parameters for food
        self.food_pos = [0,0]
        self.food_spawn = False

class Food:

    def __init__(self,settings,screen):
        
        self.screen = screen
        self.food = pygame.Rect(200,300,10,10)
        self.color = (255,0,0)
        
    def create_food(self,settings,snake):

        while(True):
            self.food.left = random.randrange(0,settings.frame_size_x-5,10)
            self.food.top = random.randrange(0,settings.frame_size_y-5,10)
            flag = False
            for i in snake.get_snake_body():
                if (self.food.left == i.left and self.food.top == i.top):
                   flag = True 
            if not (flag):
                break
        
    def draw_food(self):

        pygame.draw.rect(self.screen,self.color,self.food)

    def get_top(self):

        return self.food.top

    def get_left(self):

        return self.food.left

    def get_right(self):

        return self.food.right

    def get_bottom(self):

        return self.food.bottom

def check_events(screen,snake,food):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                snake.change_direction('RIGHT')
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                snake.change_direction('LEFT')
            elif (event.key == pygame.K_w or event.key == pygame.K_UP):
                snake.change_direction('UP')
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                snake.change_direction('DOWN')
                
def vaishnav_arora(settings,screen,snake,food):
    screen.fill(settings.bg_color)
    display_score(screen,snake.score)
    snake.draw_snake()
    food.draw_food()
    pygame.display.flip()

def game_over(settings,screen,score):
    #gameover 
    gameover_img = pygame.font.SysFont('timesnewroman', 60).render("YOU DIED", True, (166,16,30))
    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = settings.frame_size_x/2
    gameover_rect.centery = settings.frame_size_y/2-50

    #score
    score_img = pygame.font.SysFont('timesnewroman', 30).render("Score : "+str(score),True, (166,16,30))
    score_rect = score_img.get_rect()
    score_rect.centerx = settings.frame_size_x/2
    score_rect.centery = settings.frame_size_y/2+10
    #draw the text on the screen
    screen.fill(settings.bg_color)
    screen.blit(score_img,score_rect)
    screen.blit(gameover_img, gameover_rect)
    #display the last drawn screen
    pygame.display.flip()
    #wait for 3 seconds and then exit the game
    time.sleep(3)
    pygame.display.quit()
    sys.exit()

def display_score(screen,score):
    score_img = pygame.font.SysFont('timesnewroman', 20).render("Score : "+str(score),True, (240,240,240))
    score_rect = score_img.get_rect()
    score_rect.top = 20
    score_rect.left = 40
    screen.blit(score_img,score_rect)
    
def run_game():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.frame_size_x,settings.frame_size_y))
    fps_controller = pygame.time.Clock()
    food = Food(settings,screen)
    score = 0
    snake = Snake(settings,screen,score)
    
    while True:
        check_events(screen,snake,food)
        snake.update_snake(settings,game_over)
        snake.check_food(food)
        vaishnav_arora(settings,screen,snake,food)
        fps_controller.tick(15)

run_game()
