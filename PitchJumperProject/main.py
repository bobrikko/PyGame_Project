import pygame
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, TILE_SIZE, TEXTURE_FOLDER, LEVEL_NAMES, FONT_PATH, \
    FONT_SIZE, BACKGROUND_COLOR, SOUNDS_FOLDER, APP_ICON, TARGET_SCORES, FONT_SIZE_LARGE, TEXT_COLOR
from tilemap import TileMap
from player_controller import Player
from hud import HUD
from main_menu import MainMenu
from end_screen import show_end_screen
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chicken Jump")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0,
                                              vsync=1)
        self.clock = pygame.time.Clock()
        self.current_level_id = 0
        self.running = True
        self.tile_map = None
        self.player = None
        self.hud = None
        self.camera_x = 0
        self.camera_y = 0
        self.level_complete = False
        self.victory_sound = self.load_sound("victorySound.mp3")
        self.button_click_sound = self.load_sound("button_click.wav")
        self.bg_color = BACKGROUND_COLOR

    def load_sound(self, file_name):
        sound_path = os.path.join(SOUNDS_FOLDER, file_name)
        if os.path.exists(sound_path):
            return pygame.mixer.Sound(sound_path)
        else:
            print(f"Warning: Sound file '{file_name}' not found in '{SOUNDS_FOLDER}'.")
            return None

    def play_sound(self, sound):
        if sound:
            sound.play()

    def display_main_menu(self):
        menu = MainMenu(self.screen)
        pygame.display.set_icon(pygame.image.load(os.path.join(TEXTURE_FOLDER, APP_ICON)))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                action = menu.handle_event(event)
                if action == "start_game":
                    return True
                elif action == "exit":
                    pygame.quit()
                    return False
            menu.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def load_level(self):
        if self.current_level_id == 666:
            self.tile_map = TileMap("SECRET_Level.data", TEXTURE_FOLDER, TILE_SIZE, self.screen)
            try:
                self.tile_map.set_font(FONT_PATH, FONT_SIZE)
            except FileNotFoundError as e:
                print(e)
        else:
            self.tile_map = TileMap(LEVEL_NAMES[self.current_level_id], TEXTURE_FOLDER, TILE_SIZE, self.screen)
            try:
                self.tile_map.set_font(FONT_PATH, FONT_SIZE)
            except FileNotFoundError as e:
                print(e)

        if self.tile_map.start_pos is None or self.tile_map.end_pos is None:
            print("Ошибка: Начальная или конечная позиция не указаны в уровне.")
            return False

        self.player = Player(self.tile_map.start_pos, TILE_SIZE)
        self.hud = HUD(self.screen)
        self.camera_x = self.player.x * TILE_SIZE
        self.camera_y = self.player.y * TILE_SIZE

        # Отображение целевого количества очков
        font = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
        target_score = TARGET_SCORES[self.current_level_id]
        target_score_text = font.render(f"Цель: {target_score} очков", True, TEXT_COLOR)
        self.screen.fill(self.bg_color)  # Заливка фона
        self.screen.blit(target_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Задержка для отображения сообщения

        return True

    def restart_level(self):
        return self.load_level()

    def next_level(self):
        self.current_level_id += 1
        if self.current_level_id >= len(LEVEL_NAMES):
            with open("player_results.data", "r") as file:
                if int(file.read().strip()) < 65:
                    self.play_loose_anim()
                else:
                    self.current_level_id = 666
        return self.load_level()

    def play_loose_anim(self):
        pygame.quit()
        sys.exit()

    def start_new_level(self):
        if not self.next_level():
            self.running = False

    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.camera_x += (self.player.x * TILE_SIZE + self.player.offset_x - self.camera_x) * 0.1
        self.camera_y += (self.player.y * TILE_SIZE + self.player.offset_y - self.camera_y) * 0.1
        offset_x = SCREEN_WIDTH // 2 - self.camera_x - TILE_SIZE // 2
        offset_y = SCREEN_HEIGHT // 2 - self.camera_y - TILE_SIZE // 2
        self.tile_map.draw(offset_x, offset_y)
        self.player.draw(self.screen, offset_x, offset_y)
        self.hud.draw_hp(self.player.hp)

    def draw_game(self):
        self.draw_background()
        pygame.display.flip()

    def game_loop(self):
        self.level_complete = False
        while self.running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.USEREVENT if self.level_complete:
                        target_score = TARGET_SCORES[self.current_level_id]
                        if self.player.hp >= target_score:
                            show_end_screen(self.screen, self.clock, True, self.start_new_level, self.draw_background,
                                            self.player.hp)
                        else:
                            self.restart_level()
                            self.level_complete = False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.running = False
                            case pygame.K_r:
                                self.play_sound(self.button_click_sound)
                                if not self.restart_level():
                                    return
                            case pygame.K_n if self.level_complete:
                                self.play_sound(self.button_click_sound)
                                self.start_new_level()
                                self.level_complete = False
                            case pygame.K_w | pygame.K_s | pygame.K_a | pygame.K_d:
                                moves = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0),
                                         pygame.K_d: (1, 0)}
                                if self.player.move(*moves[event.key], self.tile_map) == "level_complete":
                                    pygame.time.set_timer(pygame.USEREVENT, 500, True)
                                    self.level_complete = True

            self.player.update()

            self.draw_game()
            self.clock.tick(FPS)

    def run(self):
        if not self.display_main_menu():
            return
        if not self.load_level():
            return
        self.game_loop()


if __name__ == "__main__":
    Game().run()
