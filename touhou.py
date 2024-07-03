import pygame
from config import screen_height, screen_width
from player import Player
from bullet import Bullet
from enemy import Enemy, Enemy2, Enemy3, Boss

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Touhou 2")

def read_levels(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    levels = []
    current_level = []

    for line in lines:
        line = line.strip()
        if line.startswith("lvl:"):
            if current_level:
                levels.append(current_level)
                current_level = []
        elif line:
            current_level.append(list(map(int, line.split(', '))))
    if current_level:
        levels.append(current_level)

    return levels

def spawn_enemies(enemy_types, y, spacing):
    global current_stage
    x = 200
    for enemy_type in enemy_types:
        if enemy_type == 1:
            enemies.append(Enemy(x, y, 30 + current_stage ** 2 * 25, 8 + current_stage * 8, enemy_image, enemy_bullet_sprite_sheet, loot_image))
        elif enemy_type == 2:
            enemies.append(Enemy2(x, y, 40 + current_stage ** 2 * 30, 4 + current_stage * 4, special_enemy_image, special_enemy_bullet_sprite_sheet, loot_image))
        elif enemy_type == 3:
            enemies.append(Enemy3(x, y, 60 + current_stage ** 2 * 50, 2 + current_stage * 2, parabolic_enemy_image, parabolic_enemy_bullet_sprite_sheet, loot_image))
        elif enemy_type == 4:
            enemies.append(Boss(x, y, 1500 + current_stage ** 2 * 1000, 3 + current_stage * 4, boss_image, parabolic_enemy_bullet_sprite_sheet, loot_image))
        x += spacing

def all_enemies_defeated():
    return len(enemies) == 0

levels = read_levels('lvls.txt')


def draw_intro_screen(screen):
    font = pygame.font.SysFont(None, 60)
    title_text = font.render('Touhou 2', True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(title_text, title_rect)

    start_button = pygame.Rect(screen_width // 2 - 140, screen_height // 2, 280, 50)
    leaderboard_button = pygame.Rect(screen_width // 2 - 140, screen_height // 2 + 70, 280, 50)

    pygame.draw.rect(screen, WHITE, start_button)
    pygame.draw.rect(screen, WHITE, leaderboard_button)

    start_text = font.render('Start', True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    leaderboard_text = font.render('Leaderboard', True, BLACK)
    leaderboard_text_rect = leaderboard_text.get_rect(center=leaderboard_button.center)
    screen.blit(leaderboard_text, leaderboard_text_rect)

    return start_button, leaderboard_button


def draw_player_info_box(screen, player):
    box_width = 200
    box_height = 210
    box_x = screen_width - box_width - 10
    box_y = screen_height - box_height - 10

    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 2)

    font = pygame.font.SysFont(None, 20)

    fire_rate_label = font.render('Fire Rate', True, WHITE)
    screen.blit(fire_rate_label, (box_x + 10, box_y + 20 - 15))
    fire_rate_fill = (1200 - player.attack_speed) / 1000 * (box_width - 20)
    pygame.draw.rect(screen, WHITE, (box_x + 10, box_y + 20, box_width - 20, 20), 2)
    pygame.draw.rect(screen, BLUE, (box_x + 11, box_y + 21, fire_rate_fill, 18))

    bullet_speed_label = font.render('Bullet Speed', True, WHITE)
    screen.blit(bullet_speed_label, (box_x + 10, box_y + 60 - 15))
    bullet_speed_fill = player.bullet_speed / 20 * (box_width - 20)
    pygame.draw.rect(screen, WHITE, (box_x + 10, box_y + 60, box_width - 20, 20), 2)
    pygame.draw.rect(screen, BLUE, (box_x + 11, box_y + 61, bullet_speed_fill, 18))

    player_speed_label = font.render('Player Speed', True, WHITE)
    screen.blit(player_speed_label, (box_x + 10, box_y + 100 - 15))
    player_speed_fill = player.speed / 13 * (box_width - 20)
    pygame.draw.rect(screen, WHITE, (box_x + 10, box_y + 100, box_width - 20, 20), 2)
    pygame.draw.rect(screen, BLUE, (box_x + 11, box_y + 101, player_speed_fill, 18))

    main_bullet_dmg_label = font.render('Main Bullet DMG', True, WHITE)
    screen.blit(main_bullet_dmg_label, (box_x + 10, box_y + 140 - 15))
    pygame.draw.rect(screen, WHITE, (box_x + 10, box_y + 140, box_width - 20, 20), 2)
    for i in range(5):
        segment_x = box_x + 10 + i * ((box_width - 20) / 5)
        pygame.draw.rect(screen, WHITE, (segment_x, box_y + 140, (box_width - 20) / 5 - 2, 20), 2)
        if i < player.main_bullet_dmg_filled:
            pygame.draw.rect(screen, BLUE, (segment_x + 1, box_y + 141, (box_width - 20) / 5 - 4, 18))

    side_bullet_dmg_label = font.render('Side Bullet DMG', True, WHITE)
    screen.blit(side_bullet_dmg_label, (box_x + 10, box_y + 180 - 15))
    pygame.draw.rect(screen, WHITE, (box_x + 10, box_y + 180, box_width - 20, 20), 2)
    for i in range(5):
        segment_x = box_x + 10 + i * ((box_width - 20) / 5)
        pygame.draw.rect(screen, WHITE, (segment_x, box_y + 180, (box_width - 20) / 5 - 2, 20), 2)
        if i < player.side_bullet_dmg_filled:
            pygame.draw.rect(screen, BLUE, (segment_x + 1, box_y + 181, (box_width - 20) / 5 - 4, 18))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (27, 169, 177)

loot_image = pygame.image.load("resources/loot.png")
character_image = pygame.image.load("resources/ship.png")
enemy_image = pygame.image.load("resources/Ship1.png")
bullet_sprite_sheet = pygame.image.load("resources/bullets_purple.png")
enemy_bullet_sprite_sheet = pygame.image.load("resources/bullets_red.png")
special_enemy_image = pygame.image.load("resources/Ship2.png")
parabolic_enemy_image = pygame.image.load("resources/Ship3.png")
boss_image = pygame.image.load("resources/Ship4.png")
special_enemy_bullet_sprite_sheet = pygame.image.load("resources/bullets_blue.png")
parabolic_enemy_bullet_sprite_sheet = pygame.image.load("resources/bullets_green.png")


def draw_level_text(screen, level, stage):
    font = pygame.font.SysFont(None, 60)
    level_text = font.render(f'Level {level + 1}', True, WHITE)
    text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 - 140))
    screen.blit(level_text, text_rect)
    level_text = font.render(f'Stage {stage + 1}', True, WHITE)
    text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))
    screen.blit(level_text, text_rect)

import sys

def display_game_over(screen, current_level_index):
    font = pygame.font.SysFont(None, 60)
    game_over_text = font.render('Game Over', True, RED)
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(game_over_text, text_rect)

    font = pygame.font.SysFont(None, 40)
    prompt_text = font.render('Enter your username:', True, WHITE)
    prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(prompt_text, prompt_rect)

    pygame.display.flip()

    username = ''
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        screen.fill(BLACK)
        screen.blit(game_over_text, text_rect)
        screen.blit(prompt_text, prompt_rect)

        input_text = font.render(username, True, WHITE)
        input_rect = input_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(input_text, input_rect)

        pygame.display.flip()

    return username

def append_score(username, score):
    with open('scores.txt', 'a') as file:
        file.write(f'{username}: {score}\n')

def draw_leaderboard_screen(screen):
    with open('scores.txt', 'r') as file:
        scores = file.readlines()

    scores = [score.strip() for score in scores]
    scores.sort(key=lambda x: int(x.split(': ')[1]), reverse=True)
    top_scores = scores[:5]

    font = pygame.font.SysFont(None, 40)
    screen.fill(BLACK)
    title_text = font.render('Top 5 Scores', True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
    screen.blit(title_text, title_rect)

    for i, score in enumerate(top_scores):
        score_text = font.render(score, True, WHITE)
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100 + i * 40))
        screen.blit(score_text, score_rect)

    back_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)
    pygame.draw.rect(screen, WHITE, back_button)
    back_text = font.render('Back', True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    return back_button

state = 'intro'
clock = pygame.time.Clock()
running = True
game_over = False
special_attack_active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'intro':
                if start_button.collidepoint(event.pos):
                    state = 'game'
                    game_over = False
                    player = Player(screen_width // 2, screen_height // 2, 7, 100, character_image)
                    loots = []
                    display_level_timer = 0
                    display_level_flag = False
                    clock = pygame.time.Clock()
                    bullets = []
                    main_bullet_timer = 0
                    side_bullet_timer = 0
                    enemies = []
                    current_level_index = 0
                    current_stage = 0
                    current_wave_index = 0
                    wave_timer = 4000
                    waiting_for_next_wave = True

                elif leaderboard_button.collidepoint(event.pos):
                    state = 'leaderboard'
            elif state == 'leaderboard' and back_button.collidepoint(event.pos):
                state = 'intro'
            elif state == 'game_over' and back_button.collidepoint(event.pos):
                state = 'intro'

    if state == 'intro':
        screen.fill(BLACK)
        start_button, leaderboard_button = draw_intro_screen(screen)
    elif state == 'leaderboard':
        screen.fill(BLACK)
        back_button = draw_leaderboard_screen(screen)
    elif state == 'game':
        if not game_over:
            delta_time = clock.get_time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            player.move(keys)

            if keys[pygame.K_SPACE]:
                if player.activate_special_attack():
                    special_attack_active = True
                    special_attack_timer = 2000 

            player.update_special_attack(delta_time)

            for bullet in bullets:
                bullet.update()

            main_bullet_timer += clock.get_time()
            if main_bullet_timer >= player.attack_speed:
                main_bullet_timer = 0
                center_x = player.x + player.width // 2 - 8
                center_y = player.y
                bullets.append(Bullet(center_x, center_y, player.main_bullet_damage, player.bullet_speed, bullet_sprite_sheet, 'center'))
                if player.main_bullet_stage > 1:
                    bullets.append(Bullet(center_x + 7, center_y + 5, player.main_bullet_damage, player.bullet_speed, bullet_sprite_sheet, 'center'))
                    bullets.append(Bullet(center_x - 7, center_y + 5, player.main_bullet_damage, player.bullet_speed, bullet_sprite_sheet, 'center'))
                if player.main_bullet_stage > 2:
                    bullets.append(Bullet(center_x + 15, center_y + 10, player.main_bullet_damage, player.bullet_speed, bullet_sprite_sheet, 'center'))
                    bullets.append(Bullet(center_x - 15, center_y + 10, player.main_bullet_damage, player.bullet_speed, bullet_sprite_sheet, 'center'))

            side_bullet_timer += clock.get_time()
            if side_bullet_timer >= player.attack_speed * 2:
                side_bullet_timer = 0
                center_x = player.x + player.width // 2 - 8
                center_y = player.y
                bullets.append(Bullet(center_x - 24, center_y + 30, player.side_bullet_damage, player.bullet_speed*7/10, bullet_sprite_sheet, 'side'))
                bullets.append(Bullet(center_x + 24, center_y + 30, player.side_bullet_damage, player.bullet_speed*7/10, bullet_sprite_sheet, 'side'))
                if player.side_bullet_stage > 1:
                    bullets.append(Bullet(center_x - 34, center_y + 30, player.side_bullet_damage, player.bullet_speed*7/10, bullet_sprite_sheet, 'side'))
                    bullets.append(Bullet(center_x + 34, center_y + 30, player.side_bullet_damage, player.bullet_speed*7/10, bullet_sprite_sheet, 'side'))
                if player.side_bullet_stage > 2:
                    bullets.append(Bullet(center_x - 29, center_y + 25, player.side_bullet_damage, player.bullet_speed*7/10, bullet_sprite_sheet, 'side'))
                    bullets.append(Bullet(center_x + 29, center_y + 25, player.side_bullet_damage, player.bullet_speed*7/10, bullet_sprite_sheet, 'side'))

            for enemy in enemies[:]:
                for bullet in bullets[:]:
                    if enemy.check_collision(bullet):
                        loot = enemy.take_damage(bullet.damage)  
                        bullets.remove(bullet)
                        if loot:
                            loots.append(loot)
                        break
                if enemy.is_dead():
                    enemies.remove(enemy)

            for loot in loots[:]:
                loot.update()
                if loot.check_collision(player):
                    player.collect_loot(loot)
                    loots.remove(loot)
                elif loot.y > screen_height:
                    loots.remove(loot)

            for enemy in enemies:
                enemy.update(player, delta_time)
                for enemy_bullet in enemy.bullets[:]:
                    if enemy_bullet.check_collision(player):
                        player.take_damage(enemy.atk)  
                        enemy.bullets.remove(enemy_bullet)  

            if player.hp <= 0:
                game_over = True
                state = 'game_over'
                username = display_game_over(screen, current_level_index)
                append_score(username, current_stage * 10 + current_level_index)
                back_button = draw_leaderboard_screen(screen)
                continue

            if waiting_for_next_wave:
                wave_timer += delta_time
                if wave_timer >= 5000: 
                    waiting_for_next_wave = False
                    wave_timer = 0
                    if current_level_index < len(levels):
                        current_level = levels[current_level_index]
                        if current_wave_index < len(current_level):
                            spawn_enemies(current_level[current_wave_index], y=100, spacing=200)
                            current_wave_index += 1
                            waiting_for_next_wave = True
                        else:
                            current_level_index += 1
                            current_wave_index = 0

                    else:
                        current_level_index = 0
                        current_stage += 1
                        current_level = levels[current_level_index]
                        if current_wave_index < len(current_level):
                            spawn_enemies(current_level[current_wave_index], y=100, spacing=200)
                            current_wave_index += 1
                            waiting_for_next_wave = True
                        else:
                            current_level_index += 1
                            current_wave_index = 0

                if all_enemies_defeated(): wave_timer = 5000

            if all_enemies_defeated() and current_wave_index == 0 and not waiting_for_next_wave:
                waiting_for_next_wave = True
                wave_timer = 5000
                display_level_flag = True
                display_level_timer = 0

            screen.fill(BLACK)

            if special_attack_active:
                special_attack_timer -= delta_time
                if special_attack_timer <= 0:
                    special_attack_active = False
                else:
                    player.draw_special_attack(screen)
                    for enemy in enemies[:]:
                        if player.special_attack_collision(enemy):
                            enemy.take_damage(player.main_bullet_stage * 2 * player.main_bullet_damage / 15)  

            player.draw(screen)
            player.draw_health_bar(screen)
            
            for bullet in bullets:
                bullet.draw(screen)
            
            for enemy in enemies:
                enemy.draw(screen)

            for loot in loots:
                loot.draw(screen)

            draw_player_info_box(screen, player)

            player.draw_special_attack_bar(screen)

            if display_level_flag:
                draw_level_text(screen, current_level_index, current_stage)
                display_level_timer += delta_time
                if display_level_timer >= 2000: 
                    display_level_flag = False

        elif state == 'game_over':
            screen.fill(BLACK)
            back_button = draw_leaderboard_screen(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
