import pygame

class Projectile_right(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('../sprites/projectile_right.png')
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.x = 480
        self.rect.y = 340

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        if self.rect.x > 900:
            self.remove()

class Projectile_left(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('../sprites/projectile_left.png')
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.x = 380
        self.rect.y = 340

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x -= self.velocity
        if self.rect.x == 0:
            self.remove()

class Projectile_down(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('../sprites/projectile_down.png')
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = 438
        self.rect.y = 390

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.y += self.velocity
        if self.rect.y > 700:
            self.remove()

class Projectile_up(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load('../sprites/projectile_up.png')
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = 438
        self.rect.y = 270

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.y -= self.velocity
        if self.rect.y == 0:
            self.remove()