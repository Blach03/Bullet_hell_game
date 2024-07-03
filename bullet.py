import pygame
import math

class Bullet:
    def __init__(self, x, y, damage, speed, sprite_sheet, bullet_type='center'):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite_sheet = sprite_sheet
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_count = 0
        self.damage = damage
        
        if bullet_type == 'center':
            self.sprite_x = 0
            self.sprite_y = 240
        elif bullet_type == 'side':
            self.sprite_x = 0
            self.sprite_y = 256
        else:
            raise ValueError('Invalid bullet type')
        
        self.frame_width = 16
        self.frame_height = 16
        
        self.frames = []
        for i in range(5):
            frame = self.sprite_sheet.subsurface(
                (self.sprite_x + i * self.frame_width, self.sprite_y, self.frame_width, self.frame_height))
            frame = pygame.transform.rotate(frame, 90) 
            self.frames.append(frame)
    
    def update(self):
        self.y -= self.speed
        
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))



class EnemyBullet:
    def __init__(self, x, y, target_x, target_y, speed, sprite_sheet):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite_sheet = sprite_sheet
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_count = 0

        self.sprite_x = 0
        self.sprite_y = 304
        self.frame_width = 16
        self.frame_height = 16

        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))
        length = math.sqrt(dx ** 2 + dy ** 2)
        self.direction = (dx / length, dy / length)

        self.frames = []
        for i in range(5):
            frame = self.sprite_sheet.subsurface(
                (self.sprite_x + i * self.frame_width, self.sprite_y, self.frame_width, self.frame_height))
            frame = pygame.transform.rotate(frame, -self.angle)  
            self.frames.append(frame)
    
    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))
    
    def check_collision(self, player):
        bullet_rect = pygame.Rect(self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height())
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        return bullet_rect.colliderect(player_rect)
