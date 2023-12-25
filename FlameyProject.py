import sys # альтф4

# Свои файлеке
from button import Button # Импорт нашего класса для кнопочек
from settings import *
from multiples import *
from board import *
from ball import Ball

pygame.init() # Инициализация

# Текст в menu
font = pygame.font.FontType(EpilepsySansBold, 100) 
font2 = pygame.font.FontType(EpilepsySansBold, 48)
text = "Welcome to the main menu!"
text2 = "christmas ver."

def main_menu():
    global screen, width, height

    game_button = Button(710, 280, 530, 160, "", "FlameyProject/graphics/play_button.png", "FlameyProject/graphics/play_button_hover.png", "FlameyProject/audio/click.mp3")
    quit_button = Button(710, 590, 530, 160, "", "FlameyProject/graphics/quit.png", "FlameyProject/graphics/quit_hover.png", "FlameyProject/audio/click.mp3")
    mute_button = Button(10, 900, 100, 100 , "" , "FlameyProject/graphics/muteon.png", "FlameyProject/graphics/muteon_hover.png", "FlameyProject/audio/click.mp3")

    btns = [game_button, quit_button, mute_button] # Массив со всеми нашими кнопками

    mute = False # Музыка
    fullscreen = False # Фуллскрин типо

    running = True
    while running: # Запуск самой игры
        screen.fill((0, 0, 0))  # Заливка экрана черным цветом (предотвращает "остаточные" изображения)
        screen.blit(menu_background, (0, 0))

        screen.blit(sinti_resized, (120, 760))

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)

        text2_surface = font2.render(text2, True, (255, 255, 255))
        text2_rect = text2_surface.get_rect(center=(980, 960))
        screen.blit(text2_surface, text2_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.USEREVENT and event.button == quit_button):
                running = False
                fade()
                pygame.quit()
                sys.exit()

            # В фуллскрин и обратно
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1920, 1030), pygame.RESIZABLE)
            
            # Поведения кнопок
            if event.type == pygame.USEREVENT and event.button == game_button:
                fade()
                ball_story()

            if event.type == pygame.USEREVENT and event.button == mute_button:
                if not mute:
                    # Если музыка не в режиме паузы, поставит её на паузу
                    pygame.mixer.music.pause()
                    mute = True
                else:
                    # Если музыка находится на паузе, то возобновится воспроизведение
                    pygame.mixer.music.unpause()
                    mute = False
            mute_button.update_image(mute)

            for btn in btns: # Проход циклом для поведения наших кнопок
                btn.handle_event(event)

        for btn in btns: # Проход циклом для отрисовки наших кнопок
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip() # Обновление экрана
        clock.tick(target_fps) # Обновление экрана с поставленным FPS

def ball_story():
    class Game:
        def __init__(self):
            # General setup
            pygame.init()
            self.screen = screen
            self.clock = clock
            self.delta_time = 0

            # Pymunk
            self.space = pymunk.Space()
            self.space.gravity = (0, 1800)

            # Шар и полотно
            self.ball_group = pygame.sprite.Group()
            self.board = Board(self.space)

            # Дебаггинг
            self.balls_played = 0

        def run(self):
            back_button = Button(0, 890, 230, 100, "", "FlameyProject/graphics/exit.png", "FlameyProject/graphics/exit_hover.png", "FlameyProject/audio/click.mp3")
            btns = [back_button]

            self.start_time = pygame.time.get_ticks()

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        fade()
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Получает с юзера позицию курсора
                        mouse_pos = pygame.mouse.get_pos()

                        # Проверка мыши стоит ли на кнопке или No
                        if self.board.play_rect.collidepoint(mouse_pos):
                            self.board.pressing_play = True
                        else:
                            self.board.pressing_play = False

                    # Спавнит шарик когда отпускаешь ЛКМ
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_play:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.board.play_rect.collidepoint(mouse_pos):
                            random_x = width//2 + random.choice([random.randint(-20, -1), random.randint(1, 20)]) # Рандом спавн
                            click.play()
                            self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
                            self.ball_group.add(self.ball)
                            self.board.pressing_play = False
                        else:
                            self.board.pressing_play = False

                    for btn in btns:
                            btn.handle_event(event)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            fade()
                            running = False
                    
                    if event.type == pygame.USEREVENT and event.button == back_button:
                        fade()
                        running = False


                self.screen.fill((bg_color))

                screen.blit(garlands, (0, 0))

                # Темпорари вариабле
                self.delta_time = self.clock.tick(target_fps) / 1000.0

                # Pymunk
                self.space.step(self.delta_time)
                self.board.update()
                self.ball_group.update()

                for btn in btns: # Проход циклом для отрисовки наших кнопок
                    btn.check_hover(pygame.mouse.get_pos())
                    btn.draw(screen)

                pygame.display.update()

    if __name__ == '__main__':
        game = Game()
        game.run()

def fade():
    running = True
    fade_alpha = 0 # Уровень прозрачности для анимации

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        fade_surface = pygame.Surface((width, height))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Увеличение уровня прозрачности
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False
        
        pygame.display.flip()
        clock.tick(target_fps)

main_menu()