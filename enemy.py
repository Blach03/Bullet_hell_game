import pygame
from bullet import EnemyBullet
import random
import math
from config import screen_height, screen_width
from loot import Loot

class Enemy:
    def __init__(self, x, y, hp, atk, image, bullet_sprite_sheet, loot_image):
        self.x = x
        self.y = y
        self.hp = hp
        self.maxhp = hp
        self.atk = atk
        self.image = pygame.transform.rotate(image, -90)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.bullet_sprite_sheet = bullet_sprite_sheet
        self.bullets = []
        self.attack_speed = 600 + random.randint(0, 200)
        self.shoot_timer = 0
        self.speed = 2
        self.loot_image = loot_image
        self.loot_drop_chance = 0.3

        self.direction_timer = 0
        self.direction_change_interval = 300
        self.current_dx = 0
        self.current_dy = 0

    def update(self, player, delta_time):
        self.move(player, delta_time)
        self.shoot_timer += delta_time
        if self.shoot_timer >= self.attack_speed:
            self.shoot_timer = 0
            self.shoot(player)

        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.hp > 0:
            self.draw_health_bar(screen)
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_health_bar(self, screen):
        bar_width = 70
        bar_height = 6
        fill = (self.hp / self.maxhp) * bar_width
        outline_rect = pygame.Rect(self.x + (self.width - bar_width) // 2, self.y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.x + (self.width - bar_width) // 2, self.y - 10, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 1)

    def check_collision(self, bullet):
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.frames[0].get_width(), bullet.frames[0].get_height())
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return bullet_rect.colliderect(enemy_rect)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            return self.drop_loot()
        return None

    def is_dead(self):
        return self.hp <= 0

    def shoot(self, player):
        bullet = EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, player.x + player.width // 2, player.y + player.height // 2, 7, self.bullet_sprite_sheet)
        self.bullets.append(bullet)

    def move(self, player, delta_time):
        self.direction_timer += delta_time
        if self.direction_timer >= self.direction_change_interval:
            self.direction_timer = 0
            if random.random() < 0.4:
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if dist != 0:
                    self.current_dx = dx / dist
                    self.current_dy = dy / dist
                else:
                    self.current_dx, self.current_dy = 0, 0
            else:
                self.current_dx = random.choice([-1, 1])
                self.current_dy = random.choice([-1, 1])

        self.x += self.current_dx * self.speed
        self.y += self.current_dy * self.speed

        self.x = max(0, min(screen_width - self.width, self.x))
        self.y = max(0, min(screen_height / 2 - self.height, self.y))

    def drop_loot(self):
        if random.random() < self.loot_drop_chance:
            return Loot(self.x + self.width // 2, self.y + self.height // 2, self.loot_image)
        return None


class Enemy2(Enemy):
    def __init__(self, x, y, hp, atk, image, bullet_sprite_sheet, loot_image):
        super().__init__(x, y, hp, atk, image, bullet_sprite_sheet, loot_image)
        self.maxhp = hp
        self.rapid_fire_timer = 0
        self.rapid_fire_interval = 2900 + random.randint(0, 400)
        self.rapid_fire_bullets = 10
        self.rapid_fire_count = 0
        self.loot_drop_chance = 0.5

    def update(self, player, delta_time):
        self.move(player, delta_time)
        self.shoot_timer += delta_time
        if self.shoot_timer >= self.rapid_fire_interval:
            self.shoot_timer = 0
            self.rapid_fire_count = self.rapid_fire_bullets

        if self.rapid_fire_count > 0:
            self.rapid_fire_timer += delta_time
            if self.rapid_fire_timer >= 50:
                self.rapid_fire_timer = 0
                self.shoot(player)
                self.rapid_fire_count -= 1

        for bullet in self.bullets:
            bullet.update()


class Enemy3(Enemy):
    def __init__(self, x, y, hp, atk, image, bullet_sprite_sheet, loot_image):
        super().__init__(x, y, hp, atk, image, bullet_sprite_sheet, loot_image)
        self.maxhp = hp
        self.shoot_interval = 4500 + random.randint(0, 1000)
        self.rapid_fire_timer = 0
        self.rapid_fire_bullets = 100
        self.rapid_fire_count = 0
        self.target_acquired = False
        self.initial_player_x = 0
        self.initial_player_y = 0
        self.display_lines_timer = 0
        self.display_lines_duration = 500
        self.loot_drop_chance = 0.4

    def update(self, player, delta_time):
        self.move(player, delta_time)
        self.shoot_timer += delta_time

        if not self.target_acquired and self.shoot_timer >= self.shoot_interval - self.display_lines_duration:
            self.target_acquired = True
            self.initial_player_x = player.x
            self.initial_player_y = player.y

        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.target_acquired = False
            self.rapid_fire_count = self.rapid_fire_bullets

        if self.rapid_fire_count > 0:
            self.rapid_fire_timer += delta_time
            if self.rapid_fire_timer >= 1:
                self.rapid_fire_timer = 0
                self.shoot_parabolic()
                self.rapid_fire_count -= 1

        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        super().draw(screen)
        if self.target_acquired:
            self.draw_trajectory_lines(screen)

    def draw_trajectory_lines(self, screen):
        direction_left = (self.initial_player_x - 200 - (self.x + self.width // 2), self.initial_player_y - (self.y + self.height // 2))
        direction_right = (self.initial_player_x + 200 - (self.x + self.width // 2), self.initial_player_y - (self.y + self.height // 2))
        
        length_left = math.sqrt(direction_left[0] ** 2 + direction_left[1] ** 2)
        length_right = math.sqrt(direction_right[0] ** 2 + direction_right[1] ** 2)
        direction_left = (direction_left[0] / length_left, direction_left[1] / length_left)
        direction_right = (direction_right[0] / length_right, direction_right[1] / length_right)
        
        extend_distance = 1000
        end_left = (self.initial_player_x - 200 + direction_left[0] * extend_distance, self.initial_player_y + direction_left[1] * extend_distance)
        end_right = (self.initial_player_x + 200 + direction_right[0] * extend_distance, self.initial_player_y + direction_right[1] * extend_distance)
        
        pygame.draw.line(screen, (255, 0, 0), 
                         (self.x + self.width // 2, self.y + self.height // 2), 
                         end_left, 2)
        pygame.draw.line(screen, (255, 0, 0), 
                         (self.x + self.width // 2, self.y + self.height // 2), 
                         end_right, 2)

    def shoot_parabolic(self):
        for direction in ["left", "right"]:
            if direction == "left":
                target_x = self.initial_player_x - 200
            else:
                target_x = self.initial_player_x + 200

            bullet = EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, target_x, self.initial_player_y, 30, self.bullet_sprite_sheet)
            self.bullets.append(bullet)
            

class Boss(Enemy):
    def __init__(self, x, y, hp, atk, image, bullet_sprite_sheet, loot_image):
        super().__init__(x, y, hp, atk, image, bullet_sprite_sheet, loot_image)
        self.maxhp = hp
        self.shoot_interval1 = 4500 + random.randint(0, 1000)
        self.shoot_interval2 = 1500
        self.shoot_interval3 = 1500
        self.shoot_interval4 = 3000
        self.shoot_timer2 = 0
        self.shoot_timer3 = 750
        self.shoot_timer4 = 0
        self.rapid_fire_timer = 0
        self.rapid_fire_bullets = 100
        self.rapid_fire_count = 0
        self.target_acquired = False
        self.initial_player_x = 0
        self.initial_player_y = 0
        self.display_lines_timer = 0
        self.display_lines_duration = 500
        self.loot_drop_chance = 5
        self.rapid_fire_timer2 = 0
        self.rapid_fire_bullets2 = 10
        self.rapid_fire_count2 = 0

    def update(self, player, delta_time):
        self.move(player, delta_time)
        self.shoot_timer += delta_time
        self.shoot_timer2 += delta_time
        self.shoot_timer3 += delta_time
        self.shoot_timer4 += delta_time

        if not self.target_acquired and self.shoot_timer >= self.shoot_interval1 - self.display_lines_duration:
            self.target_acquired = True
            self.initial_player_x = player.x
            self.initial_player_y = player.y

        if self.shoot_timer >= self.shoot_interval1:
            self.shoot_timer = 0
            self.target_acquired = False
            self.rapid_fire_count = self.rapid_fire_bullets

        if self.shoot_timer2 >= self.shoot_interval2:
            self.shoot_timer2 = 0
            self.shoot_normal1(player)

        if self.shoot_timer3 >= self.shoot_interval3:
            self.shoot_timer3 = 0
            self.shoot_normal2(player)

        if self.rapid_fire_count > 0:
            self.rapid_fire_timer += delta_time
            if self.rapid_fire_timer >= 1:
                self.rapid_fire_timer = 0
                self.shoot_parabolic()
                self.rapid_fire_count -= 1

    
        if self.shoot_timer4 >= self.shoot_interval4:
            self.shoot_timer4 = 0
            self.rapid_fire_count2 = self.rapid_fire_bullets2

        if self.rapid_fire_count2 > 0:
            self.rapid_fire_timer2 += delta_time
            if self.rapid_fire_timer2 >= 50:
                self.rapid_fire_timer2 = 0
                self.shoot3(player)
                self.rapid_fire_count2 -= 1


        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        super().draw(screen)
        if self.target_acquired:
            self.draw_trajectory_lines(screen)

    def draw_trajectory_lines(self, screen):
        direction_left = (self.initial_player_x - 250 - (self.x + self.width // 2), self.initial_player_y - (self.y + self.height // 2))
        direction_right = (self.initial_player_x + 250 - (self.x + self.width // 2), self.initial_player_y - (self.y + self.height // 2))
        direction_centre = (self.initial_player_x - (self.x + self.width // 2), self.initial_player_y - (self.y + self.height // 2))

        length_left = math.sqrt(direction_left[0] ** 2 + direction_left[1] ** 2)
        length_right = math.sqrt(direction_right[0] ** 2 + direction_right[1] ** 2)
        length_centre = math.sqrt(direction_centre[0] ** 2 + direction_centre[1] ** 2)
        direction_left = (direction_left[0] / length_left, direction_left[1] / length_left)
        direction_right = (direction_right[0] / length_right, direction_right[1] / length_right)
        direction_centre = (direction_centre[0] / length_centre, direction_centre[1] / length_centre)
        
        extend_distance = 1000
        end_left = (self.initial_player_x - 250 + direction_left[0] * extend_distance, self.initial_player_y + direction_left[1] * extend_distance)
        end_right = (self.initial_player_x + 250 + direction_right[0] * extend_distance, self.initial_player_y + direction_right[1] * extend_distance)
        end_centre = (self.initial_player_x + direction_centre[0] * extend_distance, self.initial_player_y + direction_centre[1] * extend_distance)

        pygame.draw.line(screen, (255, 0, 0), 
                         (self.x + self.width // 2, self.y + self.height // 2), 
                         end_left, 2)
        pygame.draw.line(screen, (255, 0, 0), 
                         (self.x + self.width // 2, self.y + self.height // 2), 
                         end_right, 2)
        pygame.draw.line(screen, (255, 0, 0), 
                         (self.x + self.width // 2, self.y + self.height // 2), 
                         end_centre, 2)

    def shoot_parabolic(self):
        for direction in ["left", "center", "right"]:
            if direction == "left":
                target_x = self.initial_player_x - 250
            elif direction == "right":
                target_x = self.initial_player_x + 250
            else:
                target_x = self.initial_player_x
            bullet = EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, target_x, self.initial_player_y, 30, self.bullet_sprite_sheet)
            self.bullets.append(bullet)

    def shoot_normal1(self, player):
        for i in range(4):
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x - 1000, self.y + self.height // 2, 7, self.bullet_sprite_sheet))
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x + 1000, self.y + self.height // 2, 7, self.bullet_sprite_sheet))
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x + self.width // 2, self.y - 1000, 7, self.bullet_sprite_sheet))
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x + self.width // 2, self.y + 1000, 7, self.bullet_sprite_sheet))

    def shoot_normal2(self, player):
        for i in range(4):
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x - 1000, self.y + 1000, 7, self.bullet_sprite_sheet))
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x + 1000, self.y - 1000, 7, self.bullet_sprite_sheet))
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x - 1000, self.y - 1000, 7, self.bullet_sprite_sheet))
            self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, self.x + 1000, self.y + 1000, 7, self.bullet_sprite_sheet))

    def shoot3(self, player):
        self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, player.x + player.width // 2, player.y + player.height // 2, 7, self.bullet_sprite_sheet))
        self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, player.x + player.width // 2 + 400, player.y + player.height // 2, 7, self.bullet_sprite_sheet))
        self.bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height // 2, player.x + player.width // 2 - 400, player.y + player.height // 2, 7, self.bullet_sprite_sheet))
