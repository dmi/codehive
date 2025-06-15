import pygame
import sys
from pygame_emojis import load_emoji
from entities import Entity
from map import Map
from items import Item
from characters import get_all_characters
from logger import get_last_actions

pygame.init()

# Настройки экрана
COLOR = (128, 128, 128)
WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 32
GAME_WIDTH = int(WIDTH * 0.7)  # 70% для карты
INFO_WIDTH = WIDTH - GAME_WIDTH  # 30% для информации
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive")

# Создание большой карты
map = Map(width=100, height=100, TILE_SIZE=TILE_SIZE)

# Создание персонажей
entities = get_all_characters(map)

# Основной цикл игры
clock = pygame.time.Clock()
running = True
paused = False
selected_entity = entities[0] if entities else None

# Логика скроллинга
camera_x = 0
camera_y = 0
camera_speed = 0.1  # Скорость скроллинга

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            tile_x = x // TILE_SIZE
            tile_y = y // TILE_SIZE
            for entity in entities:
                if entity.x == tile_x and entity.y == tile_y:
                    selected_entity = entity

    if not paused:
        for entity in entities:
            entity.update(dt)

    # Логика скроллинга
    if selected_entity:
        # Плавное смещение камеры
        camera_x += (selected_entity.x * TILE_SIZE - camera_x) * camera_speed
        camera_y += (selected_entity.y * TILE_SIZE - camera_y) * camera_speed

    # Отрисовка
    screen.fill((0, 0, 0))  # чёрный фон

    # Отрисовка игрового поля
    for y in range(map.height):
        for x in range(map.width):
            tile = map.get_tile(x, y)
            color = tile.get_color()
            screen.blit(pygame.Surface((TILE_SIZE, TILE_SIZE)), (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
            pygame.draw.rect(screen, color, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE))

    # Отображение предметов
    for y in range(map.height):
        for x in range(map.width):
            tile = map.get_tile(x, y)
            for item in tile.items:
                if item.name == "Камень":
                    emoji = load_emoji("🪨", (TILE_SIZE, TILE_SIZE))
                    screen.blit(emoji, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))

    # Отображение персонажей
    for entity in entities:
        emoji = load_emoji(entity.icon, (TILE_SIZE, TILE_SIZE))
        screen.blit(emoji, (entity.x * TILE_SIZE - camera_x + entity.vx, entity.y * TILE_SIZE - camera_y + entity.vy))

    # Отрисовка окна информации
    pygame.draw.rect(screen, (30, 30, 30), (GAME_WIDTH, 0, INFO_WIDTH, HEIGHT))  # тёмно-серый фон

    # Отображение информации о выбранном персонаже
    if selected_entity:
        font = pygame.font.SysFont("Arial", 14)
        info = f"""{selected_entity.name}
HP: {selected_entity.hp}
Состояние: {selected_entity.state}
x: {selected_entity.x} y: {selected_entity.y}"""
        i = 0
        for l in info.split('\n'):
            info_text = font.render(l, True, COLOR)
            screen.blit(info_text, (GAME_WIDTH + 10, i * 15))
            i += 1

        # Отображение инвентаря
        inv_text = font.render("Инвентарь:", True, COLOR)
        screen.blit(inv_text, (GAME_WIDTH + 10, 75))
        for i, item in enumerate(selected_entity.inventory):
            item_text = font.render(f"{item.name} x{item.quantity}", True, COLOR)
            screen.blit(item_text, (GAME_WIDTH + 10, 50 + i * 15))

    # Отображение журнала
    font = pygame.font.SysFont("Arial", 14)
    log_text = font.render("Журнал:", True, COLOR)
    screen.blit(log_text, (GAME_WIDTH + 10, 150))
    for i, action in enumerate(get_last_actions()):
        action_text = font.render(action, True, COLOR)
        screen.blit(action_text, (GAME_WIDTH + 10, 170 + i * 15))

    pygame.display.flip()

pygame.quit()
sys.exit()