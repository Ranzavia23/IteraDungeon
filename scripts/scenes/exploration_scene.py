import pygame
from scenes.base_scene import BaseScene
from attack import Attack
from floors import FirstFloor, SecondFloor, ThirdFloor


class ExplorationScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_speed = 5
        self.font = pygame.font.SysFont(None, 24)
        self.menu_active = False
        self.menu_options = ["Profile", "Skill Tree", "Options", "Exit to Main Menu"]
        self.menu_selected = 0
        self.facing = "down"
        self.sword = Attack(self)

        self.floors = [FirstFloor(), SecondFloor(), ThirdFloor()]
        self.current_floor_index = 0
        self.current_floor = self.floors[self.current_floor_index]

    def return_to_menu(self):
        from scenes.mainmenu_scene import MainMenuScene

        self.game.scene_manager.go_to(MainMenuScene(self.game))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if self.menu_active:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_RETURN:
                        self.select_menu_option()
                    elif event.key == pygame.K_ESCAPE:
                        self.menu_active = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_active = True
                    elif event.key == pygame.K_z:
                        from scenes.skilltree_scene import SkillTreeScene

                        self.game.scene_manager.push(SkillTreeScene(self.game))
                    elif event.key == pygame.K_x:
                        self.sword.start()
                       

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.menu_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.current_floor.player_pos[0] -= self.player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.current_floor.player_pos[0] += self.player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.current_floor.player_pos[1] -= self.player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.current_floor.player_pos[1] += self.player_speed

            if self.current_floor.check_portal_collision(self.current_floor.player_pos):
                if self.current_floor_index < len(self.floors) - 1:
                    self.current_floor_index += 1
                    self.current_floor = self.floors[self.current_floor_index]
                else:
                    print("Congratulations! You've completed all floors!")

            if (self.sword.active and self.current_floor.enemy not in self.current_floor.defeated_enemies):
                hitbox = self.sword.get_hitbox()
                if hitbox and hitbox.colliderect(self.current_floor.enemy.rect):
                    self.start_battle(self.current_floor.enemy, player_first=True)

    def render(self):
        self.game.screen.fill((20, 20, 20))

        if self.current_floor.returning_from_battle:
            self.current_floor.player_pos = (
                self.current_floor.last_position_before_battle.copy()
            )
            self.current_floor.returning_from_battle = False

        floor_text = self.font.render(
            f"{self.current_floor.name}", True, (255, 255, 255)
        )
        self.game.screen.blit(floor_text, (10, 10))

        pygame.draw.rect(
            self.game.screen, (0, 200, 255), (*self.current_floor.player_pos, 40, 40)
        )

        if self.menu_active:
            overlay = pygame.Surface((300, 300))
            overlay.set_alpha(200)
            overlay.fill((50, 50, 50))
            self.game.screen.blit(overlay, (250, 150))
            for idx, item in enumerate(self.menu_options):
                color = (255, 255, 0) if idx == self.menu_selected else (255, 255, 255)
                text = self.font.render(item, True, color)
                self.game.screen.blit(text, (270, 170 + idx * 30))

        if self.current_floor.enemy not in self.current_floor.defeated_enemies:
            self.current_floor.enemy.draw(self.game.screen)

        self.current_floor.draw_portal(self.game.screen)

    def handle_menu_selection(self):
        selected = self.menu_options[self.menu_selected]
        if selected == "Profile":
            from scenes.profile_scene import ProfileScene

            self.game.scene_manager.go_to(ProfileScene(self.game))
        elif selected == "Skill Tree":
            print("Open Skill Tree (Belum dibuat)")
        elif selected == "Options":
            print("Open Options (Belum dibuat)")
        elif selected == "Main Menu":
            from scenes.mainmenu_scene import MainMenuScene

            self.game.scene_manager.go_to(MainMenuScene(self.game))
        elif selected == "Exit Game":
            self.game.running = False

    def draw_menu(self):
        menu_surface = pygame.Surface((300, 200))
        menu_surface.fill((50, 50, 50))
        for idx, option in enumerate(self.menu_options):
            color = (255, 255, 0) if idx == self.menu_selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            menu_surface.blit(text, (20, 20 + idx * 40))
        self.game.screen.blit(
            menu_surface, (self.game.screen.get_width() // 2 - 150, 100)
        )

    def select_menu_option(self):
        option = self.menu_options[self.menu_selected]
        print(f"Selected: {option}")
        if option == "Profile":
            from scenes.profile_scene import ProfileScene

            self.game.scene_manager.push(ProfileScene(self.game))
        elif option == "Skill Tree":
            from scenes.skilltree_scene import SkillTreeScene

            self.game.scene_manager.go_to(SkillTreeScene(self.game))
        elif option == "Options":
            print("Buka options (belum dibuat)")
        elif option == "Exit to Main Menu":
            self.return_to_menu()

    def start_battle(self, enemy, player_first):
        from scenes.battle_scene import BattleScene

        self.current_floor.save_battle_position(self.current_floor.player_pos)
        self.current_floor.in_battle = True
        self.game.scene_manager.go_to(BattleScene(self.game, enemy, player_first, self))

    def on_battle_complete(self, enemy_defeated=False):
        if enemy_defeated:
            self.current_floor.defeat_enemy()
        self.current_floor.returning_from_battle = True
        self.current_floor.in_battle = False

        self.game.player.hp = 100
