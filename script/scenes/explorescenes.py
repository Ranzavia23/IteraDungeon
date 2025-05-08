import pygame
from scenes.basescenes import BaseScene
from attack import Attack
from enemy import Enemy

class ExplorationScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_pos = [100, 100]
        self.player_speed = 5
        self.font = pygame.font.SysFont(None, 32)
        self.menu_active = False
        self.menu_options = ["Profile", "Skill Tree", "Options", "Exit to Main Menu"]
        self.menu_selected = 0
        self.facing = "down"
        self.sword = Attack(self)
        self.enemy = Enemy(300, 200)

    def return_to_menu(self):
        from scenes.mainmenu import MainMenuScene
        self.game.scene_manager.go_to(MainMenuScene(self.game))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.KEYDOWN:
                if self.menu_active:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        self.select_menu_option()
                    elif event.key == pygame.K_ESCAPE:
                        self.menu_active = False

                else:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_active = True

                    elif event.key == pygame.K_z:
                        from scenes.skilltree import SkillTreeScene
                        self.game.scene_manager.push(SkillTreeScene(self.game))
                    
                    elif event.key == pygame.K_x:
                        self.sword.start()

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.menu_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player_pos[0] -= self.player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player_pos[0] += self.player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player_pos[1] -= self.player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player_pos[1] += self.player_speed
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_pos[0] -= self.player_speed
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_pos[0] += self.player_speed
            self.facing = "right"                           #ini yang buat nge ambush
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_pos[1] -= self.player_speed
            self.facing = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_pos[1] += self.player_speed
            self.facing = "down"
        
        hitbox = self.sword.get_hitbox()
        if self.sword.active and hitbox and hitbox.colliderect(self.enemy.rect):
            self.start_battle(self.enemy, player_first=True)
        else:
            self.start_battle(self.enemy, player_first=False)

    def render(self):
        self.game.screen.fill((20, 20, 20))
        pygame.draw.rect(self.game.screen, (0, 200, 255), (*self.player_pos, 40, 40))

        if self.menu_active:
            overlay = pygame.Surface((300, 300))
            overlay.set_alpha(200)
            overlay.fill((50, 50, 50))
            self.game.screen.blit(overlay, (250, 150))

            for idx, item in enumerate(self.menu_options):
                color = (255, 255, 0) if idx == self.menu_selected else (255, 255, 255)
                text = self.font.render(item, True, color)
                self.game.screen.blit(text, (270, 170 + idx * 40))
        
        self.enemy.draw(self.game.screen)

    def handle_menu_selection(self):
        selected = self.menu_options[self.menu_selected]
        if selected == "Profile":
            from scenes.profilescene import ProfileScene
            self.game.scene_manager.go_to(ProfileScene(self.game))
        elif selected == "Skill Tree":
            print("Open Skill Tree (Belum dibuat)")
        elif selected == "Options":
            print("Open Options (Belum dibuat)")
        elif selected == "Main Menu":
            from scenes.mainmenu import MainMenuScene
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
        self.game.screen.blit(menu_surface, (self.game.screen.get_width() // 2 - 150, 100))

    def select_menu_option(self):
        option = self.menu_options[self.menu_selected]
        print(f"Selected: {option}")
        if option == "Profile":
            from scenes.profilescene import ProfileScene
            self.game.scene_manager.push(ProfileScene(self.game))
        elif option == "Skill Tree":
            from scenes.skilltree import SkillTreeScene
            self.game.scene_manager.go_to(SkillTreeScene(self.game))
        elif option == "Options":
            print("Buka options (belum dibuat)")
        elif option == "Exit to Main Menu":
            self.return_to_menu()

    def check_collision(self, player_pos, enemy_rect):
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 40, 40)
        return player_rect.colliderect(enemy_rect)
    
    def start_battle(self, enemy, player_first):
        from scenes.battlescene import BattleScene
        self.game.scene_manager.go_to(BattleScene(self.game, enemy, player_first))