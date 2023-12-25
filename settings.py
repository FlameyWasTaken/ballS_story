import pygame, pymunk, random

# General хуйня
width, height = 1920, 1030
clock = pygame.time.Clock() # Объект clock для задания FPS
target_fps = 60 # Наше заранее подготовленное значение FPS
delta_time = target_fps / 1000.0

# Шрифты
EpilepsySansBold = "FlameyProject/graphics/EpilepsySansBold.ttf"
MontserratBold = "FlameyProject/graphics/Montserrat-Bold.ttf"

# General 2
pygame.display.set_caption("Flamey's project") # title слева сверху
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
icon = pygame.image.load("FlameyProject/graphics/uvst.png")
pygame.display.set_icon(icon)

# Изображения
menu_background = pygame.image.load("FlameyProject/graphics/menu_background.png")
garlands = pygame.image.load("FlameyProject/graphics/garlands.png")
sinti = pygame.image.load("FlameyProject/graphics/sinti.jpg")
new_width, new_height = 600, 250
sinti_resized = pygame.transform.scale(sinti, (new_width, new_height))

# Кфг полотна
bg_color = (16, 32, 55)
multi_height = int(height / 19) # Height мультисов # 56 на 1920x1080 (54)
multi_collision = height - (multi_height * 2) # 968 на 1920x1080 (922)

score_rect = int(width / 16) # Счёт(текст) справа # 120 on 1920x1080 

obstacle_color = (190, 190, 255)
obstacle_rad = int(width / 240) # Размеры(радиус;диаметр) препясвий # 8 на 1920x1080
obstacle_pad = int(height / 19) # () # 56 на 1920x1080 | (54)
obstacle_start = (int((width / 2) - obstacle_pad), int((height - (height * 0.9)))) # (904, 108) на 1920x1080 | (906, 103)
segmentA_2 = obstacle_start

ball_rad = 16

# Словари по поводу счёта
multipliers = {
    "A+": 0,
    "A": 0,
    "B+": 0,
    "B": 0,
    "B-": 0,
    "C": 0,
    "D": 0
}

# RGB значения для множителей
multi_rgb = {
    (0, "A+"): (255, 0, 0),
    (1, "A"): (255, 30, 0),
    (2, "B+"): (255, 60, 0),
    (3, "B"): (255, 90, 0),
    (4, "B-"): (255, 120, 0),
    (5, "C"): (255, 150, 0),
    (6, "D"): (255, 180, 0),
    (7, "D"): (255, 210, 0), # Желтый side
    (8, "D"): (255, 255 ,255), # Центр
    (9, "D"): (210, 0, 255),  # Фиол side
    (10, "D"): (180, 0, 255),
    (11, "C"): (150, 0, 255), 
    (12, "B-"): (120, 0, 255),
    (13, "B"): (90, 0, 255),
    (14, "B+"): (60, 0, 255),
    (15, "A"): (30, 0, 255),
    (16, "A+"): (0, 0, 255),
}


# Кол-во множителей под спайками
num_multis = 17

# Pymunk настроечки (prevent same class collisions)
ball_category = 1
obstacle_category = 2
ball_mask = pymunk.ShapeFilter.ALL_MASKS() ^ ball_category
obstacle_mask = pymunk.ShapeFilter.ALL_MASKS()

# Аудио
pygame.mixer.init()
pygame.mixer.music.load("FlameyProject/audio/Bad Bunny - MONACO Instrumental.mp3") # Бэкграунд музяка
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1) # -1 означает бесконечное воспроизведение

click = pygame.mixer.Sound("FlameyProject/audio/click.mp3") # Звуки клика

# Звуки мультиплаеров
sound01 = pygame.mixer.Sound("FlameyProject/audio/001.mp3")
sound01.set_volume(0.1)
sound02 = pygame.mixer.Sound("FlameyProject/audio/002.mp3")
sound02.set_volume(0.3)
sound03 = pygame.mixer.Sound("FlameyProject/audio/003.mp3")
sound03.set_volume(0.4)
sound04 = pygame.mixer.Sound("FlameyProject/audio/004.mp3")
sound04.set_volume(0.5)
sound05 = pygame.mixer.Sound("FlameyProject/audio/005.mp3")
sound05.set_volume(0.6)
sound06 = pygame.mixer.Sound("FlameyProject/audio/006.mp3")
sound06.set_volume(0.7)
sound07 = pygame.mixer.Sound("FlameyProject/audio/007.mp3")
sound07.set_volume(0.8)