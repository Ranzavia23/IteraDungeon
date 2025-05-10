import pygame
from scenes.base_scene import BaseScene


class BattleScene(BaseScene):
    def __init__(self, game, enemy, player_first=True, exploration_scene=None):
        super().__init__(game)
        self.enemy = enemy
        self.player_first = player_first
        if exploration_scene and exploration_scene.current_floor:
            self.turn = exploration_scene.current_floor.current_turn
        else:
            self.turn = "player" if player_first else "enemy"
        self.font = pygame.font.SysFont(None, 30)
        self.done = False
        self.exploration_scene = exploration_scene

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if self.turn == "player":
                    if event.key == pygame.K_SPACE:
                        self.enemy.hp -= 10
                        print("Player menyerang! HP musuh:", self.enemy.hp)
                        self.turn = "enemy"
                elif self.turn == "enemy":
                    self.game.player.hp -= self.enemy.damage
                    print("Musuh menyerang! HP player:", self.game.player.hp)
                    self.turn = "player"

                if self.exploration_scene and self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(self.turn)

    def update(self):
        if self.done:
            return

        if self.enemy.hp <= 0:
            print("Menang!")
            self.done = True

            if self.exploration_scene:
                if self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(self.turn)

                self.exploration_scene.on_battle_complete(enemy_defeated=True)
                self.game.scene_manager.go_to(self.exploration_scene)
            else:
                from scenes.exploration_scene import ExplorationScene

                self.game.scene_manager.go_to(ExplorationScene(self.game))

        elif self.game.player.hp <= 0:
            print("Kalah! Game over.")
            self.done = True
            self.game.quit()

    def render(self):
        self.game.screen.fill((0, 0, 0))
        enemy_text = self.font.render(
            f"Enemy HP: {self.enemy.hp}", True, (255, 255, 255)
        )
        player_text = self.font.render(
            f"Player HP: {self.game.player.hp}", True, (255, 255, 255)
        )
        turn_text = self.font.render(f"Turn: {self.turn}", True, (255, 255, 0))

        if self.exploration_scene and self.exploration_scene.current_floor:
            floor_text = self.font.render(
                f"Floor: {self.exploration_scene.current_floor.name}",
                True,
                (255, 255, 255),
            )
            self.game.screen.blit(floor_text, (50, 170))

        self.game.screen.blit(enemy_text, (50, 50))
        self.game.screen.blit(player_text, (50, 90))
        self.game.screen.blit(turn_text, (50, 130))
