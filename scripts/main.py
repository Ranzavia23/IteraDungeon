from game import Game
from scenes.mainmenu_scene import MainMenuScene


def main():
    game = Game()
    game.scene_manager.go_to(MainMenuScene(game))
    game.run()


main()
