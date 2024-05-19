import pygame
pygame.mixer.init()
import os


class Player:
    
    spaceship_pic = pygame.image.load(os.path.join('Assets', 'Player.png'))



    def __init__(self, game):
        
        self._width = 60 
        self._height = 30
        self._spaceship = pygame.transform.scale(self.spaceship_pic, (self._width, self._height))
        self._ship_rect = pygame.Rect((game.WIDTH // 2), (game.HEIGHT - 50), self._width, self._height)
        self.BULLET_VEL = 7 
        self._velocity = 5
        self.alien_hit = pygame.USEREVENT + 1
        self.BULLET_COLOR = (255, 255, 0)
        self.BULLET_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
        self.bullets = []
        



    def draw_spaceship(self, window, game):
       window.blit(self._spaceship, (self._ship_rect.x, self._ship_rect.y))
    
    def move_spaceship(self, game, keys_pressed):
        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self._ship_rect.x > 0:
            self._ship_rect.x -= self._velocity
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self._ship_rect.x + self._ship_rect.width < game.WIDTH:
            self._ship_rect.x += self._velocity
    

    def fire_bullet(self, event, aliens, window):
       if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(self._ship_rect.x + (self._width//2), self._ship_rect.y + self._height, 10, 5)
                self.bullets.append(bullet)
                self.BULLET_SOUND.play()
                


    def handle_bullets(self):
        for bullet in self.bullets:
            if bullet.y <= 0:
                self.bullets.remove(bullet)
                
            else:
                bullet.y -= self.BULLET_VEL



    

    def draw_bullets(self, window):
        for bullet in self.bullets:
            pygame.draw.rect(window, self.BULLET_COLOR, bullet)



  
          
    

    def check_collision_with_alien(self, alien_bullets):
        for bullet in alien_bullets:
            if bullet.colliderect(self._ship_rect):
                alien_bullets.remove(bullet)
                return True
        
    

    @property 
    def y_location(self):
        return self._ship_rect.y
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height



            

        

        


