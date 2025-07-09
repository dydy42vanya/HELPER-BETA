import pygame
import os
import sys
import math
import random

pygame.init()
pygame.mixer.init()

# Загрузка изображений и звуков
icon_path = os.path.join(os.path.dirname(__file__), "source", "image", "shooter.png")
player_path = os.path.join(os.path.dirname(__file__), "source", "image", "player.png")
enemy_path = os.path.join(os.path.dirname(__file__), "source", "image", "enemy.png")
bullet_hit_sound_path = os.path.join(os.path.dirname(__file__), "source", "music", "hit.mp3")
music = os.path.join(os.path.dirname(__file__), "source", "music", "music1.mp3")

# Проверка файлов
if not os.path.exists(bullet_hit_sound_path):
    print(f"Ошибка: файл звука не найден по пути {bullet_hit_sound_path}")
    pygame.quit()
    sys.exit()

# Загрузка ресурсов
icon = pygame.image.load(icon_path)
player_image_original = pygame.image.load(player_path)
enemy_image_original = pygame.image.load(enemy_path)
bullet_hit_sound = pygame.mixer.Sound(bullet_hit_sound_path)
pygame.mixer.music.load(music)

screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("shooter")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
run = True
screen_w = screen.get_width()
screen_h = screen.get_height()

# Настройки игры
INITIAL_SPAWN_RATE = 120
MIN_SPAWN_RATE = 30
SPAWN_RATE_DECREMENT = 30
KILLS_TO_DECREASE = 10
PLAYER_MAX_HP = 10  # Максимальное здоровье игрока

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 5
        self.color = (255, 255, 0)
        
        dx = target_x - x
        dy = target_y - y
        distance = max(1, math.sqrt(dx**2 + dy**2))
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return (self.x < 0 or self.x > screen_w or 
                self.y < 0 or self.y > screen_h)

class Player:
    def __init__(self):
        self.x = screen_w // 2
        self.y = screen_h // 2
        self.speed = 6
        self.size = 40
        self.hp = PLAYER_MAX_HP  # Текущее здоровье
        self.original_image = pygame.transform.scale(player_image_original, (self.size, self.size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.invincible = False  # Неуязвимость после получения урона
        self.invincible_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x = mouse_x - self.x
        rel_y = mouse_y - self.y
        
        angle = math.degrees(math.atan2(-rel_x, -rel_y))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Обработка неуязвимости
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def take_damage(self):
        if not self.invincible:
            self.hp -= 1
            self.invincible = True
            self.invincible_timer = 60  # 1 секунда неуязвимости (60 FPS)

    def draw(self):
        # Мигание при неуязвимости
        if not self.invincible or pygame.time.get_ticks() % 200 < 100:
            screen.blit(self.image, self.rect)
        
        # Отрисовка здоровья
        font = pygame.font.SysFont(None, 36)
        hp_text = font.render(f"HP: {self.hp}/{PLAYER_MAX_HP}", True, (255, 0, 0))
        screen.blit(hp_text, (screen_w - 150, 10))

class Enemy:
    def __init__(self, player):
        self.size = 40
        self.speed = 2
        self.player = player
        self.original_image = pygame.transform.scale(enemy_image_original, (self.size, self.size))
        self.image = self.original_image
        
        side = random.randint(0, 3)
        if side == 0:  # Верх
            self.x = random.randint(0, screen_w)
            self.y = -self.size
        elif side == 1:  # Право
            self.x = screen_w + self.size
            self.y = random.randint(0, screen_h)
        elif side == 2:  # Низ
            self.x = random.randint(0, screen_w)
            self.y = screen_h + self.size
        else:  # Лево
            self.x = -self.size
            self.y = random.randint(0, screen_h)
        
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = max(1, math.sqrt(dx**2 + dy**2))
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def collides_with(self, obj):
        distance = math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)
        if isinstance(obj, Bullet):
            return distance < (self.size//2 + obj.radius)
        return distance < (self.size//2 + obj.size//2)

# Инициализация игры
player = Player()
enemies = []
bullets = []
spawn_timer = 0
kills = 0
current_spawn_rate = INITIAL_SPAWN_RATE

# Настройка звука
pygame.mixer.init()
try:
    bullet_hit_sound = pygame.mixer.Sound(bullet_hit_sound_path)
    bullet_hit_sound.set_volume(0.3)
except:
    print("Не удалось загрузить звук попадания")
    bullet_hit_sound = None


pygame.mixer.music.play(loops=-1)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.append(Bullet(player.x, player.y, mouse_x, mouse_y))
    
    player.update()

    # Спавн врагов
    spawn_timer += 1
    if spawn_timer >= current_spawn_rate:
        enemies.append(Enemy(player))
        spawn_timer = 0

    # Обновление врагов
    for enemy in enemies[:]:
        enemy.update()
        
        if enemy.collides_with(player):
            player.take_damage()
            enemies.remove(enemy)
            continue
            
        for bullet in bullets[:]:
            if enemy.collides_with(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                kills += 1
                if bullet_hit_sound:
                    bullet_hit_sound.play()
                if kills % KILLS_TO_DECREASE == 0:
                    current_spawn_rate = max(MIN_SPAWN_RATE, current_spawn_rate - SPAWN_RATE_DECREMENT)
                break

    # Обновление пуль
    for bullet in bullets[:]:
        bullet.update()
        if bullet.is_off_screen():
            bullets.remove(bullet)

    # Проверка смерти игрока
    if player.hp <= 0:
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_w//2 - 150, screen_h//2 - 36))
        pygame.display.flip()
        pygame.time.wait(3000)
        run = False

    # Отрисовка
    screen.fill((20, 20, 20))
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for bullet in bullets:
        bullet.draw()
    
    # Отображение счёта
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Убито: {kills}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()