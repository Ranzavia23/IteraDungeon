import pygame

from scene_manager import SceneManager
from game import Game
from scenes.mainmenu import MainMenuScene
from player import Player


def main():
    game = Game()
    game.scene_manager.go_to(MainMenuScene(game))
    while game.running:
        game.scene_manager.scene.handle_events()
        game.scene_manager.scene.update()
        game.scene_manager.scene.render()
        pygame.display.flip()
        game.clock.tick(60)

main()