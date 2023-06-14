import pygame
import random
from player import Player
from dialog import DialogBox
from dialog import DialogBox_Info
from intro import DialogBox_Intro
from map import MapManager

class Game:

    def __init__(self):
        # Démarrage
        self.running = True
        self.map = "world"
        # creer la fenetre du jeu
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("La Comté - Le jeu par Arthur Diquéro")
        self.myfont = pygame.font.SysFont('Calibri', 25)

        # générer un joueur
        self.name = 'player'
        self.player = Player(self.name)
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()
        self.dialog_box_intro = DialogBox_Intro()
        self.dialog_box_info = DialogBox_Info()
        self.coinimg = pygame.image.load('../img/coin1.png').convert_alpha()
        self.ringimg = pygame.image.load('../img/fire.png').convert_alpha()

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
            self.map_manager.direction_projectile = 4
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.map_manager.direction_projectile = 3
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.map_manager.direction_projectile = 2
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.map_manager.direction_projectile = 1

    def update(self, dialog_box_info):
        self.map_manager.update(dialog_box_info)

    def run(self):

        clock = pygame.time.Clock()

        # Clock

        while self.running:
            self.player.save_location()
            self.handle_input()
            self.update(self.dialog_box_info)
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.dialog_box_intro.render(self.screen)
            self.dialog_box_info.render(self.screen)
            self.screen.blit(self.coinimg, (-5, 630))
            self.screen.blit(self.ringimg, (75, 646))
            self.fire_counter = self.myfont.render(str(self.map_manager.fire), True, (255, 0, 0))
            self.screen.blit(self.fire_counter, (110, 650))
            self.counter = self.myfont.render(str(self.map_manager.coins), True, (255,215,0))
            self.screen.blit(self.counter, (50, 650))
            self.player.all_projectiles.draw(self.screen)

            pygame.display.update()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dialog_box_intro.next_text()
                        self.map_manager.check_npc_collisions(self.dialog_box)
                    if event.key == pygame.K_r:
                        self.map_manager.add_coin(self.dialog_box_info)
                        self.map_manager.take_ring(self.dialog_box_info)
                    if event.key == pygame.K_c:
                        self.map_manager.cut_cereal(self.dialog_box_info)
                    if event.key == pygame.K_f and self.map_manager.direction_projectile == 1 and self.map_manager.fire > 0:
                        self.player.launch_projectile_right()
                        self.map_manager.fire -= 1
                        pygame.mixer.init()
                        fire_sound = pygame.mixer.Sound("../song/fire_sound.mp3")
                        fire_sound.play()
                    if event.key == pygame.K_f and self.map_manager.direction_projectile == 2 and self.map_manager.fire > 0:
                        self.player.launch_projectile_left()
                        self.map_manager.fire -= 1
                        pygame.mixer.init()
                        fire_sound = pygame.mixer.Sound("../song/fire_sound.mp3")
                        fire_sound.play()
                    if event.key == pygame.K_f and self.map_manager.direction_projectile == 3 and self.map_manager.fire > 0:
                        self.player.launch_projectile_down()
                        self.map_manager.fire -= 1
                        pygame.mixer.init()
                        fire_sound = pygame.mixer.Sound("../song/fire_sound.mp3")
                        fire_sound.play()
                    if event.key == pygame.K_f and self.map_manager.direction_projectile == 4 and self.map_manager.fire > 0:
                        self.player.launch_projectile_up()
                        self.map_manager.fire -= 1
                        pygame.mixer.init()
                        fire_sound = pygame.mixer.Sound("../song/fire_sound.mp3")
                        fire_sound.play()
                    if event.key == pygame.K_p:
                        self.name = 'player'
                        pygame.display.update()

            clock.tick(60)

        pygame.quit()
