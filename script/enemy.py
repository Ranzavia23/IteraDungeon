import pygame

class Enemy:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.hp = 100

    
    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 50, 50), self.rect)  # Merah

    def check_hit_by(self, hitbox):
        return hitbox and self.rect.colliderect(hitbox)