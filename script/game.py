import pygame
from scene_manager import SceneManager

import pygame
from scene_manager import SceneManager
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Itera Dungeon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.scene_manager = SceneManager(self)

    def run(self):
        while self.running:
            self.scene_manager.handle_events()
            self.scene_manager.update()
            self.scene_manager.render()
            pygame.display.flip()
            self.clock.tick(60)

    def quit(self):
        self.running = False
        pygame.quit()