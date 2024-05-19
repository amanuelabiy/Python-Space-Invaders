import pygame
import os
import sys
from Player import Player
from Enemey import Enemey 

class Game: 


    lives_pic = pygame.image.load(os.path.join('Assets', 'Player.png'))

    WIDTH = 800
    HEIGHT = 600
    _FPS = 60
    _BLACK = (0, 0, 0)
    _WHITE = (255, 255, 255)
    _RED = (255, 0, 0)
    

    def __init__(self):
        pygame.init()
        self._window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self._clock = pygame.time.Clock()
        self._run = True
        self.score = 0 
        self.lives = 3
        self.player = Player(self)
        self.enemy = Enemey()
        self.game_over_font = pygame.font.SysFont('comicsans', 100)
        self.SCORE_FONT = pygame.font.SysFont('comicsans', 25)
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.jpg')), (self.WIDTH, self.HEIGHT))
        self.score = 0 
        


    def run_game(self):
        while self._run:
            dt = self._clock.tick(self._FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._run = False 
        
                    
                self.player.fire_bullet(event, self.enemy.all_aliens, self._window)

            

            
            self.player.handle_bullets()
            self.enemy.handle_bullets(self)
            self.check_aliens_dead()
            

            self.enemy.fire_bullet(dt)
            keys_pressed = pygame.key.get_pressed()
            self.draw_window(keys_pressed, event, dt)


    def draw_window(self, keys_pressed, event, dt):
        self._window.blit(self.BACKGROUND, (0, 0))
        self.player.draw_spaceship(self._window, self)
        self.player.move_spaceship(self, keys_pressed)
        
        self.check_collision()
        self.enemy.draw_aliens(self._window)
        self.enemy.move_aliens(dt, self)
        self.player.draw_bullets(self._window)
        self.enemy.draw_alien_bullets(self._window)
        self.draw_score()
        self.draw_lives()

        
        self.check_game_loss()
        pygame.display.update()


    


    def check_game_loss(self):
        if self.enemy.check_loss(self):
            self.draw_game_over()
        
        if self.lives <= 0:
            self.draw_game_over()

            
    def draw_game_over(self):
            draw_text = self.game_over_font.render('GAME OVER', 1, self._RED)
            self._window.blit(draw_text, (self.WIDTH//2 - draw_text.get_width()//2, self.HEIGHT//2 - draw_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit(0)


    def check_collision(self):
        if self.enemy.check_collision_with_bullet(self.player.bullets):
            self.score += 10

        if self.player.check_collision_with_alien(self.enemy.alien_bullets):
            self.lives -= 1
            print('Life Deduction')

    def draw_score(self):
        player_score_text = self.SCORE_FONT.render("Score: " + str(self.score), 1, self._WHITE)
        text_width, text_height = player_score_text.get_size()

        x_position = 10
        y_position = self._window.get_height() - text_height - 10

        self._window.blit(player_score_text, (x_position, y_position))


    def draw_lives(self):
         
        x_position = self.WIDTH - (self.player.width - 30)
        y_position = 10  

        for i in range(self.lives):
            self._window.blit(pygame.transform.scale(self.lives_pic, (self.player.width - 30, self.player.height - 20)), 
                            (x_position, y_position))
            x_position -= (self.player.width - 30) + 10 


    
    def check_aliens_dead(self):
        if self.enemy.check_empty_aliens():
           self.enemy.all_aliens = [
            [
                [self.enemy.alien, pygame.Rect(j * self.enemy.width, i * self.enemy.height, self.enemy.width, self.enemy.height)]
                for j in range(self.enemy.aliens_columns)
            ]
            for i in range(self.enemy.aliens_rows)
            ]
           
           if self.enemy.bullet_shoot_rate > 600:
              self.enemy.bullet_shoot_rate -= 200

           if self.enemy.update_rate > 100:
              self.enemy.update_rate -= 100


           
            
           

    



        





    
        


          

   

    









