import pygame
from pygame.sprite import Sprite
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion





class Bullet(Sprite):
    def __init__(self, game: 'AlienInvasion')-> None:
        super().__init__()

        self._screen = game.screen
        self.settings = game.settings



        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.bullet_w, self.settings.bullet_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)


    def update(self) -> None:
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        self._screen.blit(self.image, self.rect)





    




