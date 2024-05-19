import pygame
import random
import os

class Enemey:
    
    alien_pic = pygame.image.load(os.path.join('Assets', 'Alien.png'))

    def __init__(self):

        self._width = 50
        self._height = 40
        self._rows = 5
        self._columns = 11
        self._velocity = 20
        self._update_rate = 1000
        self._bullet_shoot_rate = 2000
        self._time_since_last_move = 0
        self._time_since_last_shot = 0
        self._direction = 'right'
        self.player_hit = pygame.USEREVENT + 2
        self.alien_bullets = []
        self.ALIEN_BULLET_VEL = 7
        self.ALIEN_BULLET_COLOR = (255, 0, 0)
        self._alien = pygame.transform.scale(self.alien_pic, (self._width, self._height))
        self._all_aliens = [
            [
                [self._alien, pygame.Rect(j * self._width, i * self._height, self._width, self._height)]
                for j in range(self._columns)
            ]
            for i in range(self._rows)
        ]

    

    def draw_aliens(self, window):
         for i in range(self._rows):
            for j in range(self._columns):
                alien, rect = self._all_aliens[i][j]
                if (alien != None or rect != None):
                    window.blit(alien, (rect.x, rect.y))


    
    def move_aliens(self, dt, game):
        if self._direction == 'right':
           self.move_aliens_right(dt, game)
        elif self._direction == 'left':
            self.move_aliens_left(dt, game)

    def move_aliens_left(self, dt, game):
        self._time_since_last_move += dt
        if (self._time_since_last_move >= self._update_rate):
            reached_left_edge = False
            for i in range(self._rows):
                for j in range(self._columns):
                    if self._all_aliens[i][j][1] != None:
                        if self._all_aliens[i][j][1].x <= 0:
                            reached_left_edge = True
                            break
                
                if reached_left_edge:
                    break
            
            if reached_left_edge:  
                self.move_aliens_down()
                self._direction = 'right'

            else: 
                for i in range(self._rows):
                    for j in range(self._columns):
                        if self._all_aliens[i][j][1] != None:
                            self._all_aliens[i][j][1].x -= self._velocity
            
            self._time_since_last_move = 0
                
    
    def move_aliens_right(self, dt, game):
        self._time_since_last_move += dt
        if (self._time_since_last_move >= self._update_rate):
            reached_right_edge = False
            for i in range(self._rows):
                for j in range(self._columns):
                    if self._all_aliens[i][j][1] != None:
                            if self._all_aliens[i][j][1].x + self._width >= game.WIDTH:
                                reached_right_edge = True
                                break
                if reached_right_edge:
                    break

            
            if reached_right_edge:
                self.move_aliens_down()
                self._direction = 'left'
            else:
                for i in range(self._rows):
                    for j in range(self._columns):
                        if self._all_aliens[i][j][1] != None:
                            self._all_aliens[i][j][1].x += self._velocity
            

            self._time_since_last_move = 0
            


    def move_aliens_down(self):
        for i in range(self._rows):
            for j in range(self._columns):
                if self._all_aliens[i][j][1] != None:
                    self._all_aliens[i][j][1].y += 30



    def check_loss(self, game):
        for i in range(self._rows):
            for j in range(self._columns):
                alien, rect = self._all_aliens[i][j]
                if alien != None and rect != None:
                    if rect.y >= game.HEIGHT - 50:
                        return True
        
        return False
    

    @property
    def all_aliens(self):
        return self._all_aliens
    
    @property
    def aliens_rows(self):
        return self._rows
    
    @property
    def aliens_columns(self):
        return self._columns 
    
    @property
    def aliens_rows(self):
        return self._rows
    
    @property
    def width(self):
        return self._width
    

    @property
    def height(self):
        return self._height 
    
   
    def set_rows(self, value):
        if value >= 0:
            self._rows = value
        else:
            raise ValueError("Rows cannot be negative ")
        
    def set_columns(self, value):
        if value >= 0:
            self._columns = value
        else:
            raise ValueError("Columns cannot be negative ")




    def check_collision_with_bullet(self, player_bullets):
        for bullet in player_bullets:
            for i in range(self._rows):
                for j in range(self._columns):
                    if self._all_aliens[i][j][1] != None:
                        if bullet.colliderect(self._all_aliens[i][j][1]):
                            player_bullets.remove(bullet) 
                            self._all_aliens[i][j][0] = None
                            self._all_aliens[i][j][1] = None
                            
                            return True
                    

        return False
    


    def fire_bullet(self, dt):
        self._time_since_last_shot += dt
        if (self._time_since_last_shot >= self._bullet_shoot_rate):
            random_alien_row = random.randrange(0, self._rows - 1)
            random_alien_column = random.randrange(0, self._columns - 1)
            if self._all_aliens[random_alien_row][random_alien_column][1] != None:
                bullet = pygame.Rect(self._all_aliens[random_alien_row][random_alien_column][1].x + (self._width//2), self._all_aliens[random_alien_row][random_alien_column][1].y, 10, 5)
                self.alien_bullets.append(bullet)

                self._time_since_last_shot = 0

    def handle_bullets(self, game):
        for bullet in self.alien_bullets:
            if bullet.y >= game.HEIGHT:
                self.alien_bullets.remove(bullet)
                
            else:
                bullet.y += self.ALIEN_BULLET_VEL

    def draw_alien_bullets(self, window):
        for bullet in self.alien_bullets:
            pygame.draw.rect(window, self.ALIEN_BULLET_COLOR, bullet)

    
    def check_empty_aliens(self):
        for i in range(self._rows):
            for j in range(self._columns):
                if self._all_aliens[i][j][0] != None or self._all_aliens[i][j][1] != None:
                    return False
        

        return True
    

    

    @all_aliens.setter
    def all_aliens(self, value):
         if not isinstance(value, list):
            raise ValueError("my_list must be set to a list")
         
         self._all_aliens = value


    @property
    def alien(self):
        return self._alien
    

    @property
    def bullet_shoot_rate(self):
        return self._bullet_shoot_rate
    

    @bullet_shoot_rate.setter
    def bullet_shoot_rate(self, value):
        self._bullet_shoot_rate = value;

    @property
    def update_rate(self):
        return self._update_rate
    

    @update_rate.setter
    def update_rate(self, value):
        self._update_rate = value

    

    
                        


       

                

        
                        








        


    





