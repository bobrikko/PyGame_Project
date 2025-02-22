import random
import pygame
import os
from constants import TILE_SIZE, CHIKEN_RUN_ANIM_TEXTURES, CHIKEN_RUN_ANIM_SPEED, PASSABLE_TILES, FPS, \
    TEXTURE_FOLDER, CHIKEN_IDLE_ANIM_SPEED, CHIKEN_IDLE_ANIM_TEXTURES, SOUNDS_FOLDER


class Player:
    def __init__(self, position, tile_size):
        self.anim_frames = [pygame.transform.scale(pygame.image.load(os.path.join(TEXTURE_FOLDER, img)).convert_alpha(),
                                                   (tile_size, tile_size)) for img in CHIKEN_IDLE_ANIM_TEXTURES]
        self.image = self.anim_frames[0]
        self.x, self.y = position
        self.target_x, self.target_y = self.x, self.y
        self.tile_size = tile_size
        self.game_over = False
        self.hp = 10
        self.moving = False
        self.speed = TILE_SIZE / (FPS // 3)
        self.offset_x = 0
        self.offset_y = 0
        self.move_dx = 0
        self.move_dy = 0
        self.anim_index = 0
        self.anim_timer = 0
        self.facing_right = True  # Направление спрайта

        self.plus_sound = self.load_sound("plusCell.wav")
        self.minus_sound = self.load_sound("minusCell.wav")
        self.victory_sound = self.load_sound("victorySound.mp3")
        self.step_sounds = [self.load_sound(f"Gravel_hit{i}.ogg") for i in range(1, 5)]

    def load_sound(self, file_name):
        sound_path = os.path.join(SOUNDS_FOLDER, file_name)
        if os.path.exists(sound_path):
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(0.5)  # Делаем звук тише
            return sound
        else:
            print(f"Warning: Sound file '{file_name}' not found in '{SOUNDS_FOLDER}'.")
            return None

    def play_sound(self, sound, volume):
        if sound:
            sound.set_volume(volume)
            sound.play()

    def draw(self, screen, offset_x, offset_y):
        if self.game_over:
            return
        image = pygame.transform.flip(self.image, not self.facing_right, False)  # Флип изображения
        screen.blit(image, ((self.x * self.tile_size + offset_x) + self.offset_x,
                            (self.y * self.tile_size + offset_y) + self.offset_y))

    def move(self, dx, dy, tile_map):
        if self.hp <= 0 or self.moving:  # Проверка, не закончилась ли игра и не идет ли движение
            return

        new_x = self.x + dx
        new_y = self.y + dy

        if dx < 0:
            self.facing_right = False  # Поворачиваем влево
        elif dx > 0:
            self.facing_right = True  # Поворачиваем вправо

        if 0 <= new_x < len(tile_map.tiles[0]) and 0 <= new_y < len(tile_map.tiles):
            tile_name, tile_value = tile_map.parse_tile_name(tile_map.tiles[new_y][new_x])

            if tile_name in PASSABLE_TILES or tile_name == "SeedsPack":
                self.target_x = new_x
                self.target_y = new_y
                self.moving = True
                self.move_dx = dx * self.speed
                self.move_dy = dy * self.speed
                self.anim_index = 1
                self.anim_timer = 0

                if tile_map.check_if_end((new_x, new_y)):
                    tile_map.clear_tile_value(new_x, new_y)
                    self.play_sound(self.victory_sound, 0.5)
                    return "level_complete"

                total_hp_change = tile_value if tile_value is not None else 0

                if total_hp_change > 0:
                    self.play_sound(self.plus_sound, 0.65)
                elif total_hp_change < 0:
                    self.play_sound(self.minus_sound, 0.65)

                self.change_hp(total_hp_change - 1)

                tile_map.clear_tile_value(new_x, new_y)

                if tile_name == "SeedsPack":
                    tile_map.clear_tile_value(new_x, new_y)

    def update(self):
        if self.moving:
            self.offset_x += self.move_dx
            self.offset_y += self.move_dy
            self.anim_timer += 1

            if self.anim_timer >= CHIKEN_RUN_ANIM_SPEED:
                self.anim_index = (self.anim_index + 1) % len(CHIKEN_RUN_ANIM_TEXTURES)
                self.image = pygame.transform.scale(pygame.image.load(
                    os.path.join(TEXTURE_FOLDER, CHIKEN_RUN_ANIM_TEXTURES[self.anim_index])).convert_alpha(),
                                                    (self.tile_size, self.tile_size))
                self.play_sound(random.choice(self.step_sounds), 0.07)
                self.anim_timer = 0

            if abs(self.offset_x) >= TILE_SIZE or abs(self.offset_y) >= TILE_SIZE:
                self.x = self.target_x
                self.y = self.target_y
                self.offset_x = 0
                self.offset_y = 0
                self.moving = False
                self.image = pygame.transform.scale(
                    pygame.image.load(os.path.join(TEXTURE_FOLDER, CHIKEN_IDLE_ANIM_TEXTURES[0])).convert_alpha(),
                    (self.tile_size, self.tile_size))

        else:  # Когда игрок не двигается, воспроизводим анимацию стояния
            self.anim_timer += 1
            if self.anim_timer >= CHIKEN_IDLE_ANIM_SPEED:
                self.anim_index = (self.anim_index + 1) % len(CHIKEN_IDLE_ANIM_TEXTURES)
                self.image = pygame.transform.scale(pygame.image.load(
                    os.path.join(TEXTURE_FOLDER, CHIKEN_IDLE_ANIM_TEXTURES[self.anim_index])).convert_alpha(),
                                                    (self.tile_size, self.tile_size))
                self.anim_timer = 0

    def change_hp(self, amount):
        self.hp = max(0, self.hp + amount)
        if self.hp <= 0:
            self.game_over = True
