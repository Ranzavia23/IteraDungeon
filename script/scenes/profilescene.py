import pygame
from scenes.basescenes import BaseScene

class ProfileScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.scene_manager.pop()

    def render(self):
        self.game.screen.fill((20, 20, 20))

        player = self.game.player
        lines = [
            "---Profile---",
            f"{player.name}",
            f"Level: {player.level}",
            f"HP: {player.hp}",
            f"ATK: {player.atk}",
            f"DEF: {player.defense}",
            f"Speed: {player.speed}",
            "",
            "Press ESC to return."
        ]
        y = 50
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            self.game.screen.blit(text, (50, y))
            y += 40