from settings import *

# Спрайты мультисов
multi_group = pygame.sprite.Group()
delta_time = target_fps / 1000.0

class Multi(pygame.sprite.Sprite):
    def __init__(self, position, color, multi_amt):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.FontType(MontserratBold, 28)
        self.color = color
        self.border_radius = 1000
        self.position = position
        self.rect_width, self.rect_height = obstacle_pad - (obstacle_pad / 14), multi_height # Типо расстояние между мультисами
        self.image = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, self.image.get_rect(), border_radius=self.border_radius)
        self.rect = self.image.get_rect(center=position)
        self.multi_amt = multi_amt
        self.prev_multi = int(width / 21.3)

        # Для анимации
        self.animated_frames = 0
        self.animation_frames = int(0.8 / delta_time) # Подпрыжка мультисов
        self.is_animating = False

        # Показывает множитель в rect
        self.render_multi()

    def animate(self, color, amount):
        if self.animated_frames < self.animation_frames // 2: # Up
            self.rect.bottom += 2 # Даун
        else:
            self.rect.bottom -= 2
        self.animated_frames += 2
        if self.animated_frames == (self.animation_frames // 2) * 2:
            self.is_animating = False
            self.animated_frames = 0

    def render_multi(self): # Мультисы снизу
        text_surface = self.font.render(f"{self.multi_amt}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

    def hit_sound(self): # Звучарра ежжи
        if str(self.multi_amt) == "D":
            sound01.play()
        elif str(self.multi_amt) == "C":
            sound02.play()
        elif str(self.multi_amt) == "B-":
            sound03.play()
        elif str(self.multi_amt) == "B":
            sound04.play()
        elif str(self.multi_amt) == "B+":
            sound05.play()
        elif str(self.multi_amt) == "A":
            sound06.play()
        elif str(self.multi_amt) == "A+":
            sound07.play()

    def update(self):
        if self.is_animating:
            self.animate(self.color, self.multi_amt)

# Список из последних множителей (Справа колонною)
class PrevMulti(pygame.sprite.Sprite):
    def __init__(self, multi_amt, rgb_tuple):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Сама колонна
        self.multi_amt = multi_amt
        self.font = pygame.font.FontType(MontserratBold, 52)
        self.rect_width = score_rect
        self.rect_height = score_rect
        self.prev_surf = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.rgb = rgb_tuple
        pygame.draw.rect(self.prev_surf, self.rgb, (0, 0, self.rect_width, self.rect_height))
        self.prev_rect = self.prev_surf.get_rect(midbottom=(int(width * 0.85), (height / 2) - (score_rect * 2)))

        # Анимация
        self.y_traverse = 0
        self.traveled = 0

        self.render_multi()

    def render_multi(self):
        text_surface = self.font.render(f"{self.multi_amt}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.prev_surf.get_rect().center)
        self.prev_surf.blit(text_surface, text_rect)

    def update(self):
        if self.prev_rect.bottom > (height - (score_rect * 2)): # 864 на 1080
            self.kill()

        else:
            if self.traveled < self.y_traverse:
                total_distance = score_rect
                distance_per_second = 1800
                distance_per_frame = distance_per_second * delta_time # 28 на delta_time = .016
                divisor = int(score_rect / distance_per_frame)
                distance_per_frame = score_rect / divisor
                self.prev_rect.bottom += int(distance_per_frame)
                self.traveled += int(distance_per_frame)
            self.display_surface.blit(self.prev_surf, self.prev_rect)

class PrevMultiGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        pass

    def update(self):
        super().update()

        # Последние 4 множителя справа (включая будет 5); анимация
        if len(self) > 5:
            self.remove(self.sprites().pop(0))        
        if len(self) == 1:
            self.sprites()[0].y_traverse = score_rect
        elif len(self) == 2:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse = score_rect * 2, score_rect
        elif len(self) == 3:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse, self.sprites()[2].y_traverse = score_rect * 3, score_rect * 2, score_rect
        elif len(self) == 4:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse, self.sprites()[2].y_traverse, self.sprites()[3].y_traverse = score_rect * 4, score_rect * 3, score_rect * 2, score_rect
        elif len(self) == 5:
            self.sprites()[0].y_traverse, self.sprites()[1].y_traverse, self.sprites()[2].y_traverse, self.sprites()[3].y_traverse, self.sprites()[4].y_traverse = score_rect * 5, score_rect * 4, score_rect * 3, score_rect * 2, score_rect

prev_multi_group = PrevMultiGroup()