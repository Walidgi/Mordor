from dataclasses import dataclass
import pygame, pytmx, pyscroll
import moviepy.editor

from player import NPC
from stuff import COIN
from stuff import CEREAL
from stuff import RING

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world : str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    coins: list[COIN]
    cereals: list[CEREAL]
    rings: list[RING]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"
        self.coins = 0
        self.cereals = 0
        self.rings = 0
        self.direction_projectile = 0
        self.fire = 200

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_mordor", target_world="mordor", teleport_point="spawn_mordor"),
            Portal(from_world="world", origin_point="enter_farm", target_world="farm", teleport_point="spawn_farm")
        ], npcs=[
            NPC(name="robin", nb_points=2, dialog1=["Moi c'est Robin", "bienvenue à la Comté"], dialog2=["test"])
        ], coins=[
            COIN(name="coin1", nb_points=2, dialog1=["Press R pour prendre la pièce"]),
            COIN(name="coin2", nb_points=2, dialog1=["ceci est un coin2"])
        ])
        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit")
        ], npcs=[
            NPC(name="gandalf", nb_points=3, dialog1=["Arthurion, je t'attendais !","ton oncle Bilbon t'a laissé un cadeau avant de partir","Il est dans ta chambre, près de ton lit.","va le chercher et reviens me voir.","mais par pitié, fais attention..."], dialog2=["Tu as mis l'anneau? Qu'as-tu vu ?","J'aurais dû te prévenir, c'est ma faute.","Je dois me rendre à Minas Tirith"])
        ], coins=[
            COIN(name="coin3", nb_points=2, dialog1=["ceci est un coin3"])
        ], rings=[
            RING(name="ring1", nb_points=2, dialog1=["Press R pour mettre l'anneau"])
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="exit_house2")
        ], npcs=[
            NPC(name="paul", nb_points=2, dialog1=["Salut Arthurion, ça va depuis la fête de Bilbon ?", "Tu veux la clé pour sortir de La Comté?", "Bien sûr, je peux te la donner.", "Au fait, tu me dois 5 pièces d'or !", "Je te donne la clé en échange de mon argent!","reviens me voir quand tu auras mes 5 pièces.","Si tu n'as pas assez de pièces dans tes coffres.","Va voir le vieux Poildepied à l'ouest de La Comté.","Il est dans son champ en train de couper du bois","Il pourra te proposer un travail bien payé.","et comme ça, tu me remboursera en échange de la clé."], dialog2=["Bien joué pour les pièces, merci !"]),
        ]),
        self.register_map("farm", portals=[
            Portal(from_world="farm", origin_point="exit_farm", target_world="world", teleport_point="farm_exit_spawn")
        ], npcs=[
            NPC(name="farmer", nb_points=3, dialog1=["Bonjour Arthurion, comment vas-tu ?", "Tu veux bien m'aider à récolter du maïs ?","en échange de quelques pièces, bien sûr !","Reviens me voir quand tu en auras récolté"], dialog2=["Merci Arthurion pour ton travail", "voici 2 pièces"])
        ], cereals=[
            CEREAL(name="cereal1", nb_points=2, dialog1=["Press C pour couper le maïs"])
        ])
        self.register_map("mordor", portals=[
            Portal(from_world="mordor", origin_point="exit_mordor", target_world="world", teleport_point="mordor_exit_spawn")
        ], npcs=[
            NPC(name="boss", nb_points=2, dialog1=["Vous auriez pas vu un anneau ?"], dialog2=["test"])
        ])

        self.teleport_player("player")
        self.teleport_npcs()
        self.teleport_coins()
        self.teleport_cereals()
        self.teleport_rings()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "paul" and self.coins < 2:
                dialog_box.execute(sprite.dialog1)
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "paul" and self.coins >= 2:
                dialog_box.execute(sprite.dialog2)
                self.coins = 0
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "robin":
                dialog_box.execute(sprite.dialog1)
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "boss":
                dialog_box.execute(sprite.dialog1)
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "farmer" and self.cereals < 1:
                dialog_box.execute(sprite.dialog1)
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "farmer" and self.cereals >= 1:
                dialog_box.execute(sprite.dialog2)
                self.cereals = 0
                pygame.mixer.init()
                coin_sound = pygame.mixer.Sound("../song/coin_sound.mp3")
                coin_sound.play()
                self.coins += 2
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "gandalf" and self.rings < 1:
                dialog_box.execute(sprite.dialog1)
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC and sprite.name == "gandalf" and self.rings >= 1:
                dialog_box.execute(sprite.dialog2)
                if dialog_box.reading == False:
                    self.teleport_gandalf_point_two()
                    pygame.mixer.init()
                    gandalf_sound = pygame.mixer.Sound("../song/gandalf.mp3")
                    gandalf_sound.play()

    def inform_player(self, dialog_box_info):
        for sprite in self.get_group().sprites():
            if type(sprite) is COIN and sprite.feet.colliderect(self.player.rect) and sprite.name == "coin1":
                dialog_box_info.execute(sprite.dialog1)
            if type(sprite) is COIN and not sprite.feet.colliderect(self.player.rect) and sprite.name == "coin1":
                dialog_box_info.not_execute()
            if type(sprite) is CEREAL and sprite.feet.colliderect(self.player.rect) and sprite.name == "cereal1":
                dialog_box_info.execute(sprite.dialog1)
            if type(sprite) is CEREAL and not sprite.feet.colliderect(self.player.rect) and sprite.name == "cereal1":
                dialog_box_info.not_execute()
            if type(sprite) is RING and sprite.feet.colliderect(self.player.rect) and sprite.name == "ring1":
                dialog_box_info.execute(sprite.dialog1)
            if type(sprite) is RING and not sprite.feet.colliderect(self.player.rect) and sprite.name == "ring1":
                dialog_box_info.not_execute()

    def add_coin(self, dialog_box_info):
        for sprite in self.get_group().sprites():
            if type(sprite) is COIN and sprite.feet.colliderect(self.player.rect) and sprite.name == "coin1":
                pygame.mixer.init()
                coin_sound = pygame.mixer.Sound("../song/coin_sound.mp3")
                coin_sound.play()
                dialog_box_info.not_execute()
                self.coins += 1
                self.teleport_coin1_point_two()
            if type(sprite) is COIN and sprite.feet.colliderect(self.player.rect) and sprite.name == "coin2":
                pygame.mixer.init()
                coin_sound = pygame.mixer.Sound("../song/coin_sound.mp3")
                coin_sound.play()
                self.coins += 1
                self.teleport_coin2_point_two()
            if type(sprite) is COIN and sprite.feet.colliderect(self.player.rect) and sprite.name == "coin3":
                pygame.mixer.init()
                coin_sound = pygame.mixer.Sound("../song/coin_sound.mp3")
                coin_sound.play()
                self.coins += 1
                self.teleport_coin3_point_two()

    def cut_cereal(self, dialog_box_info):
        for sprite in self.get_group().sprites():
            if type(sprite) is CEREAL and sprite.feet.colliderect(self.player.rect) and sprite.name == "cereal1":
                pygame.mixer.init()
                cereal_sound = pygame.mixer.Sound("../song/cereal_cut.mp3")
                cereal_sound.play()
                dialog_box_info.not_execute()
                self.cereals += 1
                self.teleport_cereal1_point_two()

    def take_ring(self, dialog_box_info):
        for sprite in self.get_group().sprites():
            if type(sprite) is RING and sprite.feet.colliderect(self.player.rect) and sprite.name == "ring1":
                dialog_box_info.not_execute()
                self.teleport_ring1_point_two()
                video = moviepy.editor.VideoFileClip("../videos/sauron.mp4")
                video.preview()
                self.screen = pygame.display.set_mode((900, 700))
                self.rings += 1
                pygame.mixer.init()
                hobbit_song = pygame.mixer.Sound("../song/hobbit_song.mp3")
                hobbit_song.play()

    def check_collisions(self):
        #portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    if portal.target_world == "mordor":
                        pygame.mixer.stop()
                        pygame.mixer.init()
                        hobbit_song = pygame.mixer.Sound("../song/shadow_of_the_past.mp3")
                        hobbit_song.play()
                    if portal.target_world == "world" and portal.teleport_point == "mordor_exit_spawn":
                        pygame.mixer.stop()
                        pygame.mixer.init()
                        hobbit_song = pygame.mixer.Sound("../song/hobbit_song.mp3")
                        hobbit_song.play()

        #collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[], coins=[], cereals=[], rings=[]):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # définir une liste qui va stocker les rectangles de collision
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        #récupérer tous les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)
        for coin in coins:
            group.add(coin)
        for cereal in cereals:
            group.add(cereal)
        for ring in rings:
            group.add(ring)

        #Enregistrer la nouvelle carte chargée
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, coins, cereals, rings)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def teleport_coins(self):
        for map in self.maps:
            map_data = self.maps[map]
            coins = map_data.coins

            for coin in coins:
                coin.load_points(map_data.tmx_data)
                coin.teleport_spawn()

    def teleport_cereals(self):
        for map in self.maps:
            map_data = self.maps[map]
            cereals = map_data.cereals

            for cereal in cereals:
                cereal.load_points(map_data.tmx_data)
                cereal.teleport_spawn()

    def teleport_rings(self):
        for map in self.maps:
            map_data = self.maps[map]
            rings = map_data.rings

            for ring in rings:
                ring.load_points(map_data.tmx_data)
                ring.teleport_spawn()

    def teleport_coin1_point_two(self):
        for map in self.maps:
            map_data = self.maps[map]
            coins = map_data.coins

            for coin in coins:
                if type(coin) is COIN and coin.name == "coin1":
                    coin.teleport_spawn_point_two()

    def teleport_coin2_point_two(self):
        for map in self.maps:
            map_data = self.maps[map]
            coins = map_data.coins

            for coin in coins:
                if type(coin) is COIN and coin.name == "coin2":
                    coin.teleport_spawn_point_two()

    def teleport_coin3_point_two(self):
        for map in self.maps:
            map_data = self.maps[map]
            coins = map_data.coins

            for coin in coins:
                if type(coin) is COIN and coin.name == "coin3":
                    coin.teleport_spawn_point_two()

    def teleport_cereal1_point_two(self):
        for map in self.maps:
            map_data = self.maps[map]
            cereals = map_data.cereals

            for cereal in cereals:
                if type(cereal) is CEREAL and cereal.name == "cereal1":
                    cereal.teleport_spawn_point_two()

    def teleport_ring1_point_two(self):
        for map in self.maps:
            map_data = self.maps[map]
            rings = map_data.rings

            for ring in rings:
                if type(ring) is RING and ring.name == "ring1":
                    ring.teleport_spawn_point_two()

    def teleport_gandalf_point_two(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                if type(npc) is NPC and npc.name == "gandalf":
                    npc.teleport_spawn_point_two()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self, dialog_box_info):
        self.get_group().update()
        self.check_collisions()
        self.inform_player(dialog_box_info)

        for npc in self.get_map().npcs:
            npc.move()

        for projectile in self.player.all_projectiles:
            projectile.move()
