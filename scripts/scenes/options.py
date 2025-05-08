import pygame
from scenes.basescenes import BaseScene

class OptionsScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 36)
        self.input_text = game.player.name

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.player.name = self.input_text.strip()
                    from scenes.mainmenu import MainMenuScene
                    self.game.scene_manager.go_to(MainMenuScene(self.game))
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    from scenes.mainmenu import MainMenuScene
                    self.game.scene_manager.go_to(MainMenuScene(self.game))
                else:
                    if len(self.input_text) < 20:
                        self.input_text += event.unicode

    def render(self):
        self.game.screen.fill((40, 40, 40))
        text = self.font.render("Rename Character:", True, (255, 255, 255))
        name = self.font.render(self.input_text + "|", True, (255, 255, 0))
        self.game.screen.blit(text, (100, 100))
        self.game.screen.blit(name, (100, 150))