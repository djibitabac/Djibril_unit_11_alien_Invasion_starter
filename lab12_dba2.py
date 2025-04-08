# Lab12_djba2.py
# Author: Djibril Ba
# Description: Combined Alien Invasion game with customized spaceship sprite.
# Date: April 8, 2025

import sys
import pygame
from pathlib import Path
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

class Settings:
    def __init__(self)-> None:
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60

        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'newspaceship.jpg'

        self.ship_w = 40
        self.ship_h = 60
        self.ship_speed = 5

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5

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

class Arsenal:
    def __init__(self, game: 'AlienInvasion')-> None:
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self)-> None:
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self) -> None:
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True

        return False

class Ship:
    def __init__(self, game: 'AlienInvasion')-> None:
        self.screen = game.screen
        self.settings = game.settings
        self.ship_image = pygame.image.load(self.settings.ship_file)
        self.ship_image = pygame.transform.scale(self.ship_image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.ship_image.get_rect()
        self.screen_rect = game.screen.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

        self.arsenal = Arsenal(game)


    def update(self)-> None:
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x
        self.arsenal.update_arsenal()

    def draw(self)-> None:
        self.screen.blit(self.ship_image, self.rect)
        self.arsenal.draw()

    def fire(self):
        return self.arsenal.fire_bullet()

class AlienInvasion:
    def __init__(self)-> None:
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
            )                              

        self.running  = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.ship = Ship(self)

    def run_game(self)-> None:
        while self.running:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _update_screen(self):
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running= False      
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event)-> None:
         if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event)-> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            self.running= False      
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
