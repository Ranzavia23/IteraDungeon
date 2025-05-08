import pygame
from skill import SkillTree

class Player:
    def __init__(self):
        self.name = "Player"
        self.level = 1
        self.hp = 100
        self.atk = 10
        self.defense = 5
        self.speed = 8
        self.skill_tree = SkillTree()
        self.rect = pygame.Rect(100, 100, 32, 32)
        self.facing = "right"  # or "left", "up", "down"
        self.attack_active = False
        self.attack_timer = 0

    def attack(self):
        self.attack_active = True
        self.attack_timer = 10  # Frames attack is active

    def update(self):
        if self.attack_active:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attack_active = False

    @property
    def attack_rect(self):
        offset = 20
        if self.facing == "right":
            return pygame.Rect(self.rect.right, self.rect.top, offset, self.rect.height)
        elif self.facing == "left":
            return pygame.Rect(self.rect.left - offset, self.rect.top, offset, self.rect.height)
        elif self.facing == "up":
            return pygame.Rect(self.rect.left, self.rect.top - offset, self.rect.width, offset)
        elif self.facing == "down":
            return pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, offset)