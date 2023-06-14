import pygame

from player import Entity

class COIN(Entity):

    def __init__(self, name, nb_points, dialog1):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog1 = dialog1
        self.points = []
        self.name = name
        self.current_point = 0

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def teleport_spawn_point_two(self):
        location = self.points[1]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

class CEREAL(Entity):

    def __init__(self, name, nb_points, dialog1):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog1 = dialog1
        self.points = []
        self.name = name
        self.current_point = 0

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def teleport_spawn_point_two(self):
        location = self.points[1]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

class RING(Entity):

    def __init__(self, name, nb_points, dialog1):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog1 = dialog1
        self.points = []
        self.name = name
        self.current_point = 0

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def teleport_spawn_point_two(self):
        location = self.points[1]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

