import pygame
import sys
from entities import Entity
from map import Map
from items import Item
from characters import get_all_characters
from logger import get_last_actions
from emojis import get_emoji

pygame.init()

# Настройки экрана
COLOR = (128, 128, 128)
ZOOM_LEVELS = [16, 32, 64]  # Масштабы
ZOOM_INDEX = 1  # Текущий индекс масштаба
TILE_SIZE = ZOOM_LEVELS[ZOOM_INDEX]

# Динамическое определение размеров
WIDTH, HEIGHT = 1000, 600
GAME_WIDTH = int(WIDTH * 0.7)  # 70% для карты
INFO_WIDTH = WIDTH - GAME_WIDTH  # 30% для информации
GAME_HEIGHT = HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
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
camera_x = selected_entity.x * TILE_SIZE if selected_entity else 0
camera_y = selected_entity.y * TILE_SIZE if selected_entity else 0
camera_speed = 0.1  # Скорость скроллинга

# Переменные для ручного скроллинга
manual_scroll = False
scroll_dx = 0
scroll_dy = 0

# Переменные для масштабирования
zoom_speed = 0.05  # Скорость масштабирования

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_TAB:
                # Переключение между персонажами
                if entities:
                    index = (entities.index(selected_entity) + 1) % len(entities)
                    selected_entity = entities[index]
            elif event.key == pygame.K_UP:
                camera_y -= 10 * TILE_SIZE
            elif event.key == pygame.K_DOWN:
                camera_y += 10 * TILE_SIZE
            elif event.key == pygame.K_LEFT:
                camera_x -= 10 * TILE_SIZE
            elif event.key == pygame.K_RIGHT:
                camera_x += 10 * TILE_SIZE
            elif event.key == pygame.K_EQUALS:
                # Увеличение масштаба
                ZOOM_INDEX = (ZOOM_INDEX + 1) % len(ZOOM_LEVELS)
                TILE_SIZE = ZOOM_LEVELS[ZOOM_INDEX]
                map.TILE_SIZE = TILE_SIZE
                for entity in entities:
                    entity.emoji = get_emoji(entity.icon, (TILE_SIZE, TILE_SIZE))
            elif event.key == pygame.K_MINUS:
                # Уменьшение масштаба
                ZOOM_INDEX = (ZOOM_INDEX - 1) % len(ZOOM_LEVELS)
                TILE_SIZE = ZOOM_LEVELS[ZOOM_INDEX]
                map.TILE_SIZE = TILE_SIZE
                for entity in entities:
                    entity.emoji = get_emoji(entity.icon, (TILE_SIZE, TILE_SIZE))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            tile_x = x // TILE_SIZE
            tile_y = y // TILE_SIZE
            for entity in entities:
                if entity.x == tile_x and entity.y == tile_y:
                    selected_entity = entity
        elif event.type == pygame.VIDEORESIZE:
            # Обновление размеров окна
            WIDTH, HEIGHT = event.size
            GAME_WIDTH = int(WIDTH * 0.7)
            INFO_WIDTH = WIDTH - GAME_WIDTH
            GAME_HEIGHT = HEIGHT
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    if not paused:
        for entity in entities:
            ent_visible = 0 <= entity.x * TILE_SIZE - camera_x < GAME_WIDTH and 0 <= entity.y * TILE_SIZE - camera_y < GAME_HEIGHT
            entity.update(dt, ent_visible)

    # Логика скроллинга
    if selected_entity:
        # Плавное смещение камеры
        camera_x += (selected_entity.x * TILE_SIZE - GAME_WIDTH // 2 - camera_x) * camera_speed
        camera_y += (selected_entity.y * TILE_SIZE - GAME_HEIGHT // 2 - camera_y) * camera_speed

    # Отрисовка
    screen.fill((0, 0, 0))  # чёрный фон

    # Отрисовка игрового поля
    # Определение видимой области
    screen_rect = pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)

    # Определяем границы видимой области в координатах карты
    min_x = max(0, int((camera_x) // TILE_SIZE))
    max_x = min(map.width, int((camera_x + GAME_WIDTH) // TILE_SIZE) + 1)
    min_y = max(0, int((camera_y) // TILE_SIZE))
    max_y = min(map.height, int((camera_y + GAME_HEIGHT) // TILE_SIZE) + 1)

    # Отрисовка клеток только в видимой области
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            tile = map.get_tile(x, y)
            x_screen = x * TILE_SIZE - camera_x
            y_screen = y * TILE_SIZE - camera_y
            tile_rect = pygame.Rect(x_screen, y_screen, TILE_SIZE, TILE_SIZE)
            if screen_rect.colliderect(tile_rect):
                color = tile.get_color()
                pygame.draw.rect(screen, color, tile_rect)

    # Отображение предметов только в видимой области
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            tile = map.get_tile(x, y)
            for item in tile.items:
                x_screen = x * TILE_SIZE - camera_x
                y_screen = y * TILE_SIZE - camera_y
                if 0 <= x_screen < GAME_WIDTH and 0 <= y_screen < GAME_HEIGHT:
                    emoji = get_emoji("🪨", (TILE_SIZE, TILE_SIZE))
                    screen.blit(emoji, (x_screen, y_screen))

    # Отображение персонажей
    for entity in entities:
        x_screen = entity.x * TILE_SIZE - camera_x + entity.vx
        y_screen = entity.y * TILE_SIZE - camera_y + entity.vy
        if 0 <= x_screen < GAME_WIDTH and 0 <= y_screen < GAME_HEIGHT:
            screen.blit(entity.emoji, (x_screen, y_screen))

    # Отрисовка окна информации
    pygame.draw.rect(screen, (30, 30, 30), (GAME_WIDTH, 0, INFO_WIDTH, HEIGHT))  # тёмно-серый фон

    # Отображение информации о выбранном персонаже
    if selected_entity:
        font = pygame.font.SysFont("Arial", 14)
        info = f"""{selected_entity.name}
HP: {selected_entity.hp}
Состояние: {selected_entity.state}
x: {selected_entity.x} y: {selected_entity.y}
vx: {int(selected_entity.x * TILE_SIZE - camera_x + selected_entity.vx)} vy: {int(selected_entity.y * TILE_SIZE - camera_y + selected_entity.vy)}"""
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