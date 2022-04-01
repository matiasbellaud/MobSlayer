import pygame
import pytmx
import pyscroll
from map import MapManager
from player import Player
from dialog import DialogBox


class Game : 
    def __init__(self):
        self.screen = pygame.display.set_mode((1500,1000))
        pygame.display.set_caption("Mob Slayer - GMNC")

        self.playlist = []
        self.playlist.append('assets/sound/ilm.wav')
        
        
        pygame.mixer.music.load ( self.playlist.pop() )
        pygame.mixer.music.play()

        self.dialogbox = DialogBox()


        self.en_jeu = True
        
        tmx_data = pytmx.util_pygame.load_pygame('assets/background/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5
        
        
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)


    def handle_input(self) :
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_ESCAPE] :
            self.en_jeu = False

        if pressed[pygame.K_f] :
            self.dialogbox.next_text()

        if pressed[pygame.K_z] : 
            self.player.move_up()

        if pressed[pygame.K_s] :
            self.player.move_down()

        if pressed[pygame.K_q] :
    
            self.player.move_left()

        if pressed[pygame.K_d] :         
            self.player.move_right()

        

    def update(self) :
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()

        running = True

        
        while running :
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialogbox.render(self.screen)
            pygame.display.flip()


            if self.en_jeu == False :
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    running = False
                

            clock.tick(60)



pygame.quit()
