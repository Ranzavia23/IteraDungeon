import pygame
from scenes.base_scene import BaseScene
from scene_manager import SceneManager


class SkillTreeScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 30)
        self.done = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_1:
                    self.game.player.unlock_skill("Power Strike")
                elif event.key == pygame.K_2:
                    self.game.player.unlock_skill("Swift Step")
                elif event.key == pygame.K_3:
                    self.game.player.unlock_skill("Iron Guard")

    def update(self):
        if self.done:
            self.game.scene_manager.pop()

    def render(self):
        self.game.screen.fill((20, 20, 20))
        y = 50
        for i, skill in enumerate(self.game.player.skill_tree.skills):
            status = "Unlocked" if skill.unlocked else f"Level {skill.required_level}"
            line = f"{i + 1}. {skill.name} - {skill.description} ({status})"
            text = self.font.render(line, True, (255, 255, 255))
            self.game.screen.blit(text, (50, y))
            y += 40
