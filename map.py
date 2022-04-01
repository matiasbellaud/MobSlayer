from dataclasses import dataclass
import pygame, pytmx, pyscroll

from player import Monster

@dataclass
class Map:
    name: str
    walls : list[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data:pytmx.TiledMap
    monsters:list[Monster]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "map"

        self.register_map("map", monsters=[
            Monster("stermon", nb_points = 4),
            Monster("monster", nb_points = 2)

        ])

        self.teleport_player("player")
        self.teleport_monsters()
        
    def check_collisions(self):
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1 :
                sprite.move_back() 

    def teleport_player(self, name) :
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, monsters =[]):
        tmx_data = pytmx.util_pygame.load_pygame(f'assets/background/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=5)
        self.group.add(self.player)

        for monster in monsters:
            self.group.add(monster)

        self.maps[name] = Map(name, self.walls, self.group, tmx_data, monsters)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_monsters(self):
        for map in self.maps:
            map_data = self.maps[map]
            monsters = map_data.monsters

            for monster in monsters:
                monster.load_points(self)
                monster.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for monster in self.get_map().monsters :
            monster.move()