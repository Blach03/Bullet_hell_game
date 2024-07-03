import pygame
from config import screen_height, screen_width
import math
import random

class Player:
    def __init__(self, x, y, speed, hp, image, scale=0.5):
        self.original_image = image
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.boundary_left = 0
        self.boundary_right = screen_width - self.width
        self.boundary_top = 0
        self.boundary_bottom = screen_height - self.height
        self.attack_speed = 500
        self.main_bullet_damage = 10
        self.side_bullet_damage = 7
        self.bullet_speed = 10
        self.main_bullet_dmg_filled = 1
        self.side_bullet_dmg_filled = 1
        self.main_bullet_stage = 1
        self.side_bullet_stage = 1
        self.special_attack_charge = 0
        self.special_attack_ready = False


    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1

        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length
        
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        self.x = max(self.boundary_left, min(self.boundary_right, self.x))
        self.y = max(self.boundary_top, min(self.boundary_bottom, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(10, screen_height - bar_height - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(10, screen_height - bar_height - 10, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

        font = pygame.font.SysFont(None, 20)
        hp_text = font.render(f'HP: {round(self.hp)}/{self.max_hp}', True, (255,255,255))
        text_rect = hp_text.get_rect(center=outline_rect.center)
        screen.blit(hp_text, text_rect)

    def draw_special_attack_bar(self, screen):
        bar_width = 200
        bar_height = 20
        y_pos = screen_height - bar_height * 2 - 20
        fill = (self.special_attack_charge / 30) * bar_width
        if self.special_attack_ready:
            color = (22, 96, 30) 
            message = "Press SPACE to use"
        else:
            color = (255, 255, 0)  
            message = ""
        
        outline_rect = pygame.Rect(10, y_pos, bar_width, bar_height)
        fill_rect = pygame.Rect(10, y_pos, fill, bar_height)
        pygame.draw.rect(screen, color, fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

        font = pygame.font.SysFont(None, 20)
        if message:
            message_text = font.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=outline_rect.center)
            screen.blit(message_text, message_rect)

    def update_special_attack(self, delta_time):
        if not self.special_attack_ready:
            self.special_attack_charge += delta_time / 1000 
            if self.special_attack_charge >= 30:
                self.special_attack_charge = 30
                self.special_attack_ready = True

    def activate_special_attack(self):
        if self.special_attack_ready:
            self.special_attack_ready = False
            self.special_attack_charge = 0
            return True
        return False

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def scale(self, scale):
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.boundary_right = screen_width - self.width
        self.boundary_bottom = screen_height - self.height

    def collect_loot(self, loot):
        x = random.randint(0,5)
        if x == 0:
            if self.attack_speed > 200:
                self.attack_speed = max(200, self.attack_speed - 20)
            else:
                self.side_bullet_damage += 1
                self.main_bullet_damage += 2
        elif x == 1:
            if self.bullet_speed < 20:
                self.bullet_speed = min(20, self.bullet_speed + 1)
            else:
                self.side_bullet_damage += 1
                self.main_bullet_damage += 2
        elif x == 2:
            if self.speed < 11:
                self.speed = min(11, self.speed + 0.3)
            else:
                self.side_bullet_damage += 1
                self.main_bullet_damage += 2

        elif x == 3:
            if self.main_bullet_stage != 3 or self.main_bullet_dmg_filled != 5:
                self.increment_main_bullet_dmg()
                if self.main_bullet_dmg_filled == 0:
                    self.main_bullet_stage += 1
                    if self.main_bullet_stage == 2:
                        self.main_bullet_damage = self.main_bullet_damage * 0.5
                    if self.main_bullet_stage == 3:
                        self.main_bullet_damage = self.main_bullet_damage * 0.8
            self.main_bullet_damage += 3

        elif x == 4:
            if self.side_bullet_stage != 3 or self.side_bullet_dmg_filled != 5:
                self.increment_side_bullet_dmg()
                if self.side_bullet_dmg_filled == 0:
                    self.side_bullet_stage += 1
                    if self.side_bullet_stage == 2:
                        self.side_bullet_damage = self.side_bullet_damage * 0.7
                    if self.side_bullet_stage == 3:
                        self.side_bullet_damage = self.side_bullet_damage * 0.9
            self.side_bullet_damage += 2

        elif x == 5:
            self.max_hp += 10
            self.hp = min(self.hp + 30, self.max_hp)

    def increment_main_bullet_dmg(self):
        self.main_bullet_dmg_filled += 1
        if self.main_bullet_dmg_filled > 5:
            self.main_bullet_dmg_filled = 0
        return self.main_bullet_dmg_filled

    def increment_side_bullet_dmg(self):
        self.side_bullet_dmg_filled += 1
        if self.side_bullet_dmg_filled > 5:
            self.side_bullet_dmg_filled = 0
        return self.side_bullet_dmg_filled
    
    def special_attack_collision(self, enemy):
        attack_rect = pygame.Rect(self.x, 0, self.width, self.y)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        return attack_rect.colliderect(enemy_rect)
    
    def draw_special_attack(self, screen):
        fade_rect = pygame.Surface((self.width, self.y), pygame.SRCALPHA)      
        middle = self.width // 2
        base_color = (128, 0, 128)
        curve_height = self.y // 4 
        for x in range(self.width):
            distance = abs(x - middle)
            
            alpha = max(0, 128 - int((distance / middle) * 128))
            normalized_x = (x - middle) / middle
            curve_y = int(self.y - (curve_height * (1 - normalized_x ** 2))) 

            for y in range(curve_y):
                line_color = (*base_color, alpha)
                fade_rect.set_at((x, y), line_color)

        screen.blit(fade_rect, (self.x, 0))