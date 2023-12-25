import pygame

class Button:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path = None, sound_path = None): # Параметры для класса(кнопки)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path) # Задание изображения для кнопки
        self.image = pygame.transform.scale(self.image, (width, height) ) # Масштабирование от ширины, высоты
        self.hover_image = self.image # Изображение при наведении
        if hover_image_path: # Задан ли параметр изображения при наведении на кнопку
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path: # Если задан параметр звука, то проверяется файлик
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False
    
    def update_image(self, mute):
        if mute:
            self.image = pygame.image.load("FlameyProject/graphics/muteon.png")
            self.hover_image = pygame.image.load("FlameyProject/graphics/muteon_hover.png")
        else:
            self.image = pygame.image.load("FlameyProject/graphics/muteoff.png")
            self.hover_image = pygame.image.load("FlameyProject/graphics/muteoff_hover.png")
        
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.hover_image = pygame.transform.scale(self.hover_image, (self.width, self.height))

    def draw(self, screen): # Отрисовка текста и поведение при наведении курсором мышки по кнопке
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font("FlameyProject/graphics/Montserrat-Bold.ttf", 48)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos): # Проверка наведения мышки на кнопку
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event): # Обработка поведения кнопки (звук и изображение при наведении)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button = self))