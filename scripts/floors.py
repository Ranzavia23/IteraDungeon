import pygame
from enemy import Enemy


class Floor:
    def __init__(self, name, enemy_type, enemy_x=300, enemy_y=200):
        self.name = name
        self.enemy_type = enemy_type
        self.cleared = False
        self.player_pos = [100, 100]
        self.last_position_before_battle = [100, 100]
        self.enemy = Enemy(enemy_x, enemy_y)
        self.defeated_enemies = set()
        self.returning_from_battle = False
        self.in_battle = False
        self.portal_position = [500, 300]
        self.current_turn = "player"

    def defeat_enemy(self):
        if not self.cleared:
            print(f"You have defeated the enemy: {self.enemy_type} on {self.name}!")
            self.cleared = True
            self.defeated_enemies.add(self.enemy)
        else:
            print(f"The {self.name} is already cleared.")

    def has_portal(self):
        return self.cleared

    def save_player_position(self, position):
        self.player_pos = position.copy()

    def save_battle_position(self, position):
        self.last_position_before_battle = position.copy()

    def draw_portal(self, screen):
        if self.has_portal():
            pygame.draw.rect(screen, (0, 255, 0), (*self.portal_position, 50, 80))

    def check_portal_collision(self, player_pos):
        if not self.has_portal():
            return False
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 40, 40)
        portal_rect = pygame.Rect(
            self.portal_position[0], self.portal_position[1], 50, 80
        )
        return player_rect.colliderect(portal_rect)

    def set_turn(self, turn):
        self.current_turn = turn

    def get_battle_stats(self):
        return {
            "enemy_hp": self.enemy.hp,
            "turn": self.current_turn,
            "cleared": self.cleared,
        }


class FirstFloor(Floor):
    def __init__(self):
        super().__init__("First Floor", "Goblin", 300, 200)


class SecondFloor(Floor):
    def __init__(self):
        super().__init__("Second Floor", "Orc", 400, 250)


class ThirdFloor(Floor):
    def __init__(self):
        super().__init__("Third Floor", "Dragon", 450, 300)

    def has_portal(self):
        return False
