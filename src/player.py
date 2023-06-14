import pygame

from animation import AnimateSprite
from projectile import Projectile_right
from projectile import Projectile_left
from projectile import Projectile_down
from projectile import Projectile_up

class Entity(AnimateSprite):

    def __init__(self, name, x, y,):
        super().__init__(name)

        self.image = self.get_image(0, 0)
        self.image.set_colorkey(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self):
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self):
        self.change_animation("down")
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect_topleft = self.position
        self.feet.midbottom = self.rect.midbottom

class Player(Entity):
    def __init__(self, name):
        super().__init__(f'{name}', 0, 0)
        self.all_projectiles = pygame.sprite.Group()

    def launch_projectile_right(self):
        self.all_projectiles.add(Projectile_right(self))

    def launch_projectile_left(self):
        self.all_projectiles.add(Projectile_left(self))

    def launch_projectile_down(self):
        self.all_projectiles.add(Projectile_down(self))

    def launch_projectile_up(self):
        self.all_projectiles.add(Projectile_up(self))

class NPC(Entity):

    def __init__(self, name, nb_points, dialog1, dialog2):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog1 = dialog1
        self.dialog2 = dialog2
        self.points = []
        self.name = name
        self.speed = 1
        self.current_point = 0
       # self.all_projectiles = pygame.sprite.Group()

    #def launch_projectile(self):
        #.all_projectiles.add(Projectile(self))

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def teleport_spawn_point_two(self):
        location = self.points[2]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)