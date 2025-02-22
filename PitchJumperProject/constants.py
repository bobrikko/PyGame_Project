# Настройки экрана
APP_ICON = "App_Icon.png"
EXE_ICON = "Exe_Icon.ico"
SCREEN_WIDTH = 1920  # Ширина окна
SCREEN_HEIGHT = 1080  # Высота окна
FULLSCREEN = True  # Полноэкранный режим
FPS = 60  # Количество кадров в секунду

# Настройки уровня и тайлов
TILE_SIZE = 64  # Размер одной клетки тайла
LEVEL_NAMES = ["Level_1.data", "Level_2.data", "Level_3.data", "Level_4.data", "Level_5.data", "Level_6.data", "Level_7.data"]  # Файл с уровнем
TEXTURE_FOLDER = "Textures"  # Папка с текстурами
LEFT_ARROW_SPRITE = "Textures\LeftArrow.png"
TARGET_SCORES = [5, 2, 12, 10, 15, 6, 8]

FONT_SIZE = 24  # Размер пользовательского шрифта

BACKGROUND_COLOR = (91, 145, 76)  # Цвет фона экрана
PASSABLE_TILES = ["PathTile1", "PathTile2", "PathTile3"]  # Проходимые тайлы

# Настройки интерфейса
HEART_SIZE = 100  # Размер спрайта сердца
HP_TEXT_SIZE = 50  # Размер текста здоровья
HEART_TEXTURE = "Textures\Heart.png"  # Текстура сердца
FONT_PATH = "pixel.otf"  # Путь к шрифту
HEART_SOUND = "heart.collect.wav"  # Путь к шрифту

# Настройки игрока
PLAYER_TEXTURE = "ChikenIdle.png"  # Текстура персонажа

# Настройки анимаций
CHIKEN_RUN_ANIM_TEXTURES = ["ChikenRun_1.png", "ChikenRun_2.png"]
CHIKEN_RUN_ANIM_SPEED = 4.2
CHIKEN_IDLE_ANIM_TEXTURES = ["ChikenIdle.png", "ChikenIdle_1.png", "ChikenIdle_2.png", "ChikenIdle_1.png"]
CHIKEN_IDLE_ANIM_SPEED = 7

# Экран окончания
TEXT_COLOR = (255, 255, 255)
OVERLAY_COLOR = (0, 0, 0, 180)
FONT_SIZE_LARGE = 52

# Настройки ЗВУКОВ

SOUNDS_FOLDER = "Sounds"