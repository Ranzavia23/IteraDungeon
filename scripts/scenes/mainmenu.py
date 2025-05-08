import pygame
from scenes.basescenes import BaseScene
from scenes.explorescenes import ExplorationScene
from scenes.options import OptionsScene


class MainMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Start", "Rename", "Exit"]
        self.selected = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def select_option(self):
        selected_option = self.options[self.selected]
        if selected_option == "Start":
            self.game.scene_manager.go_to(ExplorationScene(self.game))
        elif selected_option == "Rename":
            self.game.scene_manager.go_to(OptionsScene(self.game))  # Pergi ke opsi
        elif selected_option == "Exit":
            self.game.running = False

    def render(self):
        self.game.screen.fill((30, 30, 30))
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.game.screen.blit(text, (100, 100 + i * 60))
