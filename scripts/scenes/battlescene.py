import pygame
from scenes.basescenes import BaseScene
class BattleScene(BaseScene):
    def __init__(self, game, enemy, player_first=True):
        super().__init__(game)
        self.enemy = enemy
        self.player_first = player_first
        self.turn = "player" if player_first else "enemy"
        self.font = pygame.font.SysFont(None, 30)
        self.done = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if self.turn == "player":
                    if event.key == pygame.K_SPACE:
                        self.enemy.hp -= 10  # Serangan dasar
                        print("Player menyerang! HP musuh:", self.enemy.hp)
                        self.turn = "enemy"
                elif self.turn == "enemy":
                    self.game.player.hp -= 5
                    print("Musuh menyerang! HP player:", self.game.player.hp)
                    self.turn = "player"

    def update(self):
        if self.enemy.hp <= 0:
            print("Menang!")
            from scenes.explorescenes import ExplorationScene
            self.game.scene_manager.go_to(ExplorationScene(self.game))
        elif self.game.player.hp <= 0:
            print("Kalah! Game over.")
            self.game.quit()

    def render(self):
        self.game.screen.fill((0, 0, 0))
        enemy_text = self.font.render(f"Enemy HP: {self.enemy.hp}", True, (255, 255, 255))
        player_text = self.font.render(f"Player HP: {self.game.player.hp}", True, (255, 255, 255))
        turn_text = self.font.render(f"Turn: {self.turn}", True, (255, 255, 0))

        self.game.screen.blit(enemy_text, (50, 50))
        self.game.screen.blit(player_text, (50, 90))
        self.game.screen.blit(turn_text, (50, 130))