import pygame
import random
from abc import ABC, abstractmethod

# Inisialisasi Pygame
pygame.init()

# Dimensi layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Ukuran objek
PLAYER_SIZE = (50, 50)
ENEMY_SIZE = (40, 40)
BOSS_SIZE = (100, 100)

# Memuat suara
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# Kelas dasar untuk semua objek dalam game
class GameObject(ABC):
    def __init__(self, x, y, image_path, size):
        self._x = x
        self._y = y
        self._image = pygame.transform.scale(pygame.image.load(image_path), size)
        self._width = size[0]
        self._height = size[1]

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

# Kelas Player
class Player(GameObject):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, image_path, size)
        self._speed = 5
        self._bullets = []

    def draw(self):
        screen.blit(self._image, (self._x, self._y))
        for bullet in self._bullets:
            bullet.draw()

    def move(self, keys):
        if keys[pygame.K_LEFT] and self._x > 0:
            self._x -= self._speed
        if keys[pygame.K_RIGHT] and self._x < WIDTH - self._width:
            self._x += self._speed
        if keys[pygame.K_UP] and self._y > 0:
            self._y -= self._speed
        if keys[pygame.K_DOWN] and self._y < HEIGHT - self._height:
            self._y += self._speed

    def shoot(self):
        bullet = Bullet(self._x + self._width // 2 - 2, self._y, RED, -10)
        self._bullets.append(bullet)
        shoot_sound.play()  # Mainkan suara tembakan

    def update_bullets(self):
        for bullet in self._bullets[:]:
            bullet.move()
            if bullet._y < 0:
                self._bullets.remove(bullet)

# Kelas Enemy
class Enemy(GameObject):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, image_path, size)
        self._speed = 2
        self._bullets = []
        self._shoot_timer = random.randint(30, 120)

    def draw(self):
        screen.blit(self._image, (self._x, self._y))
        for bullet in self._bullets:
            bullet.draw()

    def move(self):
        self._y += self._speed

    def shoot(self):
        if self._shoot_timer <= 0:
            bullet = Bullet(self._x + self._width // 2 - 2, self._y + self._height, WHITE, 5)
            self._bullets.append(bullet)
            self._shoot_timer = random.randint(30, 120)
        else:
            self._shoot_timer -= 1

    def update_bullets(self):
        for bullet in self._bullets[:]:
            bullet.move()
            if bullet._y > HEIGHT:
                self._bullets.remove(bullet)

# Kelas Final Boss
class FinalBoss(Enemy):
    def __init__(self, x, y, image_path, size):
        super().__init__(x, y, image_path, size)
        self._health = 10
        self._x_speed = 3
        self._y_speed = 2
        self._shoot_timer = random.randint(20, 80)  # Timer untuk menembak lebih sering

    def draw(self):
        super().draw()
        # Gambar health bar
        pygame.draw.rect(screen, RED, (self._x, self._y - 10, self._width, 5))
        pygame.draw.rect(screen, GREEN, (self._x, self._y - 10, self._width * (self._health / 10), 5))

    def move(self):
        self._x += self._x_speed
        self._y += self._y_speed

        if self._x <= 0 or self._x >= WIDTH - self._width:
            self._x_speed *= -1
        if self._y <= 0 or self._y >= HEIGHT // 2 - self._height:
            self._y_speed *= -1

    def shoot(self):
        if self._shoot_timer <= 0:
            bullet = Bullet(self._x + self._width // 2 - 2, self._y + self._height, WHITE, 5)
            self._bullets.append(bullet)
            self._shoot_timer = random.randint(20, 80)  # Reset waktu penembakan
        else:
            self._shoot_timer -= 1

    def update_bullets(self):
        self.shoot()  # Memastikan boss menembak
        for bullet in self._bullets[:]:
            bullet.move()
            if bullet._y > HEIGHT:
                self._bullets.remove(bullet)

    def take_damage(self):
        self._health -= 1

    def is_dead(self):
        return self._health <= 0

# Kelas Bullet
class Bullet:
    def __init__(self, x, y, color, speed):
        self._x = x
        self._y = y
        self._color = color
        self._speed = speed
        self._width = 4
        self._height = 10

    def draw(self):
        pygame.draw.rect(screen, self._color, (self._x, self._y, self._width, self._height))

    def move(self):
        self._y += self._speed

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

# Fungsi untuk spawn musuh dengan posisi acak
def spawn_enemy():
    x = random.randint(0, WIDTH - ENEMY_SIZE[0])
    y = random.randint(-100, -50)
    return Enemy(x, y, "enemy.png", ENEMY_SIZE)

# Fungsi untuk spawn 5 musuh jika musuh sebelumnya tertembak atau keluar layar
def check_enemy_spawn(enemies, defeated_enemies, boss_spawned):
    if not boss_spawned and defeated_enemies < 15:
        if len(enemies) == 0 or enemies[-1]._y > HEIGHT:
            for _ in range(5):
                enemies.append(spawn_enemy())

# Loop utama permainan
def main():
    running = True
    player = Player(WIDTH // 2 - PLAYER_SIZE[0] // 2, HEIGHT - 80, "spaceship.png", PLAYER_SIZE)
    enemies = []
    final_boss = None
    boss_spawned = False
    font = pygame.font.Font(None, 36)
    score = 0
    defeated_enemies = 0
    game_over = False
    win = False

    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    while running:
        clock.tick(FPS)

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not win:
                    player.shoot()
                if game_over or win:
                    if event.key == pygame.K_r:
                        main()
                    if event.key == pygame.K_q:
                        running = False

        if not game_over and not win:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update_bullets()

            check_enemy_spawn(enemies, defeated_enemies, boss_spawned)

            for enemy in enemies[:]:
                enemy.move()
                enemy.shoot()
                enemy.update_bullets()
                enemy.draw()

                if enemy.get_rect().colliderect(player.get_rect()):
                    game_over = True

                for bullet in enemy._bullets:
                    if bullet.get_rect().colliderect(player.get_rect()):
                        game_over = True

                for bullet in player._bullets[:]:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        enemies.remove(enemy)
                        player._bullets.remove(bullet)
                        score += 10
                        defeated_enemies += 1
                        hit_sound.play()

            if defeated_enemies >= 15 and not boss_spawned:
                final_boss = FinalBoss(WIDTH // 2 - BOSS_SIZE[0] // 2, 50, "final_boss.png", BOSS_SIZE)
                boss_spawned = True

            if boss_spawned:
                final_boss.move()
                final_boss.update_bullets()

                for bullet in final_boss._bullets:
                    if bullet.get_rect().colliderect(player.get_rect()):
                        game_over = True

                for bullet in player._bullets[:]:
                    if bullet.get_rect().colliderect(final_boss.get_rect()):
                        final_boss.take_damage()
                        player._bullets.remove(bullet)

                if final_boss.is_dead():
                    win = True

                final_boss.draw()

            player.draw()
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        elif game_over:
            game_over_text = font.render("GAME OVER! Press R to restart or Q to quit", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        elif win:
            win_text = font.render("YOU WIN! Press R to restart or Q to quit", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

main()
