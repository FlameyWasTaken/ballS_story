from multiples import *
from obstacles import *
from settings import *

class Board():
    def __init__(self, space):
        self.space = space
        self.display_surface = pygame.display.get_surface()

        # Obstacles
        self.curr_row_count = 3
        self.final_row_count = 18
        self.obstacles_list = []
        self.obstacle_sprites = pygame.sprite.Group()
        self.updated_coords = obstacle_start

        # Кнопка play
        self.play_up = pygame.image.load("graphics/play.png").convert_alpha()
        self.play_down = pygame.image.load("graphics/play_hover.png").convert_alpha()
        self.pressing_play = False
        self.play_orig_width = self.play_up.get_width()
        self.play_orig_height = self.play_up.get_height()

        # Поменьше кнопочку давай
        self.play_scaled_width = self.play_orig_width // 2
        self.play_scaled_height = self.play_orig_height // 2
        self.scaled_play_up = pygame.transform.scale(self.play_up, (self.play_scaled_width, self.play_scaled_height))
        self.scaled_play_down = pygame.transform.scale(self.play_down, (self.play_scaled_width, self.play_scaled_height))
        self.play_rect = self.scaled_play_up.get_rect(center=(width / 6, height / 2))

        # Получает вторую точку для segmentA
        self.segmentA_2 = obstacle_start
        while self.curr_row_count <= self.final_row_count:
            for i in range(self.curr_row_count):
                # Первая точка для segmentB
                if self.curr_row_count == 3 and self.updated_coords[0] > obstacle_start[0] + obstacle_pad:
                    self.segmentB_1 = self.updated_coords
                # Первая точка для segmentA
                elif self.curr_row_count == self.final_row_count and i == 0:
                    self.segmentA_1 = self.updated_coords
                # Вторая точка для segmentB
                elif self.curr_row_count == self.final_row_count and i == self.curr_row_count - 1:
                    self.segmentB_2 = self.updated_coords
                self.obstacles_list.append(self.spawn_obstacle(self.updated_coords, self.space))
                self.updated_coords = (int(self.updated_coords[0] + obstacle_pad), self.updated_coords[1])
            self.updated_coords = (int(width - self.updated_coords[0] + (.5 * obstacle_pad)), int(self.updated_coords[1] + obstacle_pad)) # x, y для новых коордов
            self.curr_row_count += 1
        self.multi_x, self.multi_y = self.updated_coords[0] + obstacle_pad, self.updated_coords[1]

        # Сегменты (граница со стороны препятствий)
        self.spawn_segments(self.segmentA_1, self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, self.segmentB_2, self.space)
        # Сегменты верхних препятствий
        self.spawn_segments((self.segmentA_2[0], 0), self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, (self.segmentB_1[0], 0), self.space)

        # Спавн мультисов
        self.spawn_multis()

    def draw_obstacles(self, obstacles): # Препятствия
        for obstacle in obstacles:
            pos_x, pos_y = int(obstacle.body.position.x), int(obstacle.body.position.y)
            pygame.draw.circle(self.display_surface, obstacle_color, (pos_x, pos_y), obstacle_rad)

    # Обводка у колонны мультисов справа 
    def draw_prev_multi_mask(self):
        multi_mask_surface = pygame.Surface((width / 4, height), pygame.SRCALPHA)
        multi_mask_surface.fill(bg_color)
        right_side_of_board = (width / 16) * 13
        right_side_pad = right_side_of_board / 130
        mask_y = (height / 4) + ((height / 4) / 9)
        pygame.draw.rect(multi_mask_surface, (0, 0, 0, 0), (right_side_pad, mask_y, score_rect, score_rect * 4), border_radius=30)
        self.display_surface.blit(multi_mask_surface, (right_side_of_board, 0))

    def spawn_multis(self):
        self.multi_amounts = [val[1] for val in multi_rgb.keys()]
        self.rgb_vals = [val for val in multi_rgb.values()]
        for i in range(num_multis):
            multi = Multi((self.multi_x, self.multi_y), self.rgb_vals[i], self.multi_amounts[i])
            multi_group.add(multi)
            self.multi_x += obstacle_pad

    def spawn_obstacle(self, pos, space):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        body.friction = 0.6 # 
        shape = pymunk.Circle(body, obstacle_rad) # Наши препятствия
        shape.elasticity = 0.4 # BOUNCE
        shape.filter = pymunk.ShapeFilter(categories=obstacle_category, mask=obstacle_mask) # Шарики с собою не касались
        self.space.add(body, shape)
        obstacle = Obstacle(body.position.x, body.position.y)
        self.obstacle_sprites.add(obstacle)
        return shape

    def spawn_segments(self, pointA, pointB, space):
        segment_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, pointA, pointB, 5) # radius = 5
        self.space.add(segment_body, segment_shape)

    def update(self):
        self.draw_obstacles(self.obstacles_list)
        multi_group.draw(self.display_surface)
        multi_group.update()
        if len(list(prev_multi_group)) > 0:
            prev_multi_group.update()
        if len(list(animation_group)) > 0:
            animation_group.update()
        self.draw_prev_multi_mask()
        if self.pressing_play:
            self.display_surface.blit(self.scaled_play_down, (width // 16, height // 3))
        else:
            self.display_surface.blit(self.scaled_play_up, (width // 16, height // 3))