import random
import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class AlienFleet:

    def __init__(self, game:'AlienInvasion')-> None:
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()

        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed


        self.create_fleet()

    def create_fleet(self)-> None:
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h



        fleet_w, fleet_h, x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, screen_h)

    
        self._create_random_formation(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_cross_formation(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """
        Builds a cross shape in the alien fleet.
        Basically puts aliens in the middle row and column
        
        """
        mid_col = fleet_w // 2
        mid_row = fleet_h // 2
        for row in range(fleet_h):
            for col in range(fleet_w):
            # only ad aliens if we're on the center row or column
                if row == mid_row or col == mid_col:
                    current_x = alien_w * col + x_offset
                    current_y = alien_h * row + y_offset
                    self._create_alien(current_x, current_y)


    def _create_random_formation(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """
        Makes a messy/random alien fleet
        Only adds an alien like 20% of the time per spot
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
            # randomly decide if this spot should get an alien
                if random.random() < 0.1:  # around 1 in 5 chance
                    current_x = alien_w * col + x_offset
                    current_y = alien_h * row + y_offset
                    self._create_alien(current_x, current_y)


    def calculate_offsets(self, alien_w, alien_h, screen_w, screen_h):
        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        half_screen = self.settings.screen_h//2 
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_w
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return fleet_w,fleet_h,x_offset,y_offset


    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h)-> any:
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h /2)//alien_h)
        if fleet_w % 2 == 0:
            fleet_w -= 1

        else:
            fleet_w -= 2
        if fleet_h % 2 ==0:
            fleet_h -= 1
        else:
            fleet_h-=2
        
        return int(fleet_w), int(fleet_h)

    def _create_alien(self, current_x: int, current_y: int)-> None:
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)


    def _check_fleet_edges(self)->None:
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()

                self.fleet_direction *= -1
                break
                
    def _drop_alien_fleet(self)-> None:
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self)-> None:
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self)-> None: 
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group)-> dict[any, list]:
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    

    def check_fleet_bottom(self)-> None:
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        return not self.fleet
       
 