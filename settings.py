from pathlib import Path
import pygame



class Settings:
    """
    A class to store all settings for the Alien Invasion game.
    """

    def __init__(self) -> None:
        """
        Initialize the game's static settings.
        """
        # Game title and display settings
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200  # Screen width in pixels
        self.screen_h = 800   # Screen height in pixels
        self.FPS = 60         # Frames per second

        # File paths for assets
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'purple.png'              # Background image
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'playerShip1_red.png'   # Player's ship image
        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserRed13.png'      # Bullet image
        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemyBlue1.png'       # Alien image

        # self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'            # Laser firing sound
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'alien.mp3'            # Laser firing sound
        # self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'     # Bullet impact sound
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / '524.mp3'
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'           # Score storage file

        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'SpecialGothicExpandedOne-Regular.ttf'  # Font file

        # Difficulty scaling factor
        self.difficulty_scale = 1.1

        # Ship settings
        self.ship_w = 40  # Ship width
        self.ship_h = 60  # Ship height

        # Alien settings
        self.alien_w = 40     # Alien width
        self.alien_h = 40     # Alien height
        self.fleet_direction = 1    # 1 for right, -1 for left

        # Button UI settings
        self.button_w = 25
        self.button_h = 50
        self.button_color = (0, 135, 50)  # RGB color

        # Text and font settings
        self.text_color = (255, 255, 255)  # White color for text
        self.button_font_size = 48
        self.HUD_font_size = 20

    def initialize_dynamic_Settings(self) -> None:
        """
        Initialize settings that change throughout the game.
        """
        # Ship properties
        self.ship_speed = 5
        self.starting_ship_count = 3

        # Bullet properties
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5    # Number of bullets allowed on screen
        self.bullet_speed = 7

        # Alien fleet properties
        self.fleet_speed = 2
        self.fleet_drop_speed = 40   # Distance fleet drops when hitting screen edge
        self.alien_points = 50    # Points per alien

    def increase_difficulty(self) -> None:
        """
        Increase speed settings to make the game more challenging.
        """
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale


        pygame.mouse.set_visible(False)

