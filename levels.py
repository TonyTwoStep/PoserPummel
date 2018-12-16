import pygame
# from blocks import Target
from blocks import Platform
from blocks import MovingPlatform
from blocks import Wall
from blocks import Cop
from blocks import Pogomonkey
from blocks import Bikefish
import random

# Colors
PURPLE = (150, 0, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


# Generic level class that is a parent to all other levels
class Level(object):

    # Constructor, takes player arg to handle collisions
    def __init__(self, player):

        # Create lists for platforms, enemies and initialize the player
        self.platform_list = pygame.sprite.Group()
        self.target_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = pygame.image.load("./resources/city-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))
        self.rect = self.background.get_rect()

        # Starting clock for each level, used to test against game clock to calculate seconds
        self.start_clock = pygame.time.get_ticks()

        # Other level variables
        self.time_allowed = 0
        self.level_complete_bonus = 0
        self.level_complete = False
        self.score_multiplier = 0
        self.zone = ""

    # Update function for updating the platform and enemy lists
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.target_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(PURPLE)
        screen.blit(self.background, (0, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.target_list.draw(screen)

    def level_reset(self, player):
        self.__init__(player)


class LevelOne(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 20
        self.score_multiplier = 10
        self.level_complete_bonus = 200
        self.zone = "City"
        self.background = pygame.image.load("./resources/city-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[200, 30, 40, 750],
                 [500, 20, 0, 800],
                 [500, 20, 500, 800],
                 [100, 30, 0, 700],
                 [200, 30, 280, 610],
                 [200, 30, 500, 610],
                 [200, 30, 800, 705],
                 [100, 30, 0, 500],
                 [200, 30, 280, 410],
                 [200, 30, 500, 410],
                 [200, 30, 800, 515],
                 [100, 30, 900, 480],
                 [200, 30, 0, 320],
                 [200, 30, 280, 225],
                 [200, 30, 500, 225],
                 [50, 30, 950, 150],
                 [50, 30, 0, 80]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(7):

            target = Cop()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.move_end = random_plat[2] + random_plat[0]

            # Add the block to the list of objects
            self.target_list.add(target)


class LevelTwo(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 25
        self.score_multiplier = 12
        self.level_complete_bonus = 300
        self.zone = "City"
        self.background = pygame.image.load("./resources/city-bg.png").convert_alpha()

        # Array with width, height, x, and y of platform
        level = [[150, 40, 0, 720],
                 [500, 20, 0, 800],
                 [500, 20, 500, 800],
                 [150, 40, 850, 720],
                 [100, 40, 0, 640],
                 [100, 40, 900, 640],
                 [50, 40, 950, 560],
                 [50, 40, 0, 560],
                 [500, 40, 250, 480],
                 [70, 40, 930, 400],
                 [450, 40, 275, 320],
                 [100, 40, 20, 260],
                 [400, 40, 300, 180],
                 [40, 40, 380, 630],
                 [40, 40, 580, 630],
                 [50, 30, 0, 80],
                 [50, 30, 950, 80],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(10):

            target = Cop()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.move_end = random_plat[2] + random_plat[0]

            # Add the block to the list of objects
            self.target_list.add(target)


class LevelThree(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 40
        self.score_multiplier = 12
        self.level_complete_bonus = 300
        self.zone = "City"
        self.background = pygame.image.load("./resources/city-bg.png").convert_alpha()

        # Array with width, height, x, and y of platform
        level = [[100, 60, 250, 740],
                 [100, 60, 660, 740],
                 [150, 40, 190, 110],
                 [150, 40, 640, 110],
                 [150, 40, 0, 530],
                 [150, 40, 850, 530],
                 [170, 40, 0, 330],
                 [170, 40, 830, 330]]

        walls = [[30, 130, 170, 240],
                 [30, 130, 800, 240]]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(200, 40, self.zone, player)
        block.rect.x = 400
        block.rect.y = 140
        block.boundary_bottom = 705
        block.boundary_top = 115
        block.change_y = -2
        self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(10):

            target = Cop()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.move_end = random_plat[2] + random_plat[0]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Deliberate target locations for level as per design
        for i in range(6, 8):
            target = Cop()

            platform = level[i]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            plat_x = platform[2]
            plat_y = platform[3]
            target.rect.x = random.randrange(plat_x, plat_x+(platform[0] - target.width))
            target.rect.y = plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = platform[2]
            target.move_end = platform[2] + platform[0]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Generate walls after enemies so none spawn on it
        for platform in walls:
            block = Wall(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)


class LevelFour(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 25
        self.score_multiplier = 12
        self.level_complete_bonus = 300
        self.zone = "Swamp"
        self.background = pygame.image.load("./resources/swamp-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[100, 40, 700, 750],
                 [100, 40, 900, 670],
                 [380, 40, 300, 580],
                 [100, 40, 200, 540],
                 [100, 40, 0, 460],
                 [380, 40, 300, 370],
                 [100, 40, 900, 280],
                 [100, 40, 570, 190],
                 [200, 40, 200, 150],
                 [50, 40, 950, 90],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(6):

            target = Pogomonkey()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.jump_start = random_plat[3]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Deliberate target locations for level as per design
        for i in range(8, 10):
            target = Pogomonkey()

            platform = level[i]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            plat_x = platform[2]
            plat_y = platform[3]
            target.rect.x = random.randrange(plat_x, plat_x+(platform[0] - target.width))
            target.rect.y = plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = platform[2]
            target.jump_start = platform[3]

            # Add the block to the list of objects
            self.target_list.add(target)


class LevelFive(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 25
        self.score_multiplier = 12
        self.level_complete_bonus = 400
        self.zone = "Swamp"
        self.background = pygame.image.load("./resources/swamp-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[100, 40, 600, 760],
                 [150, 40, 850, 670],
                 [70, 40, 930, 580],
                 [100, 40, 600, 400],
                 [150, 40, 200, 760],
                 [150, 40, 0, 670],
                 [70, 40, 0, 580],
                 [40, 40, 0, 490],
                 [100, 40, 470, 300],
                 [250, 40, 300, 100],
                 [250, 40, 550, 100],
                 ]

        walls = [[30, 120, 570, 680],
                 [30, 120, 570, 560],
                 [30, 120, 570, 440],
                 [30, 120, 570, 320],
                 [30, 120, 570, 200],
                 [30, 100, 570, 100]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 40, self.zone, player)
        block.rect.x = 200
        block.rect.y = 450
        block.boundary_bottom = 510
        block.boundary_top = 100
        block.change_y = -1
        self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(2):

            target = Pogomonkey()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.jump_start = random_plat[3]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Deliberate target locations for level as per design
        for i in range(9):
            target = Pogomonkey()

            platform = level[i]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            plat_x = platform[2]
            plat_y = platform[3]
            target.rect.x = random.randrange(plat_x, plat_x+(platform[0] - target.width))
            target.rect.y = plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = platform[2]
            target.jump_start = platform[3]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Generate walls after enemies so none spawn on it
        for platform in walls:
            block = Wall(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)


class LevelSix(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 30
        self.score_multiplier = 12
        self.level_complete_bonus = 400
        self.zone = "Swamp"
        self.background = pygame.image.load("./resources/swamp-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[90, 70, 340, 730],
                 [90, 70, 570, 730],
                 [250, 30, 230, 540],
                 [250, 30, 520, 540],
                 [180, 30, 300, 400],  # mandatory
                 [180, 30, 520, 400],  # mandatory
                 [230, 30, 250, 140],
                 [230, 30, 520, 140],
                 [50, 30, 270, 305],
                 [50, 30, 680, 305],
                 [40, 30, 0, 115],
                 [40, 30, 960, 115]]

        walls = [[30, 95, 270, 335],
                 [30, 95, 700, 335],
                 [40, 120, 480, 310],
                 [40, 120, 480, 190],
                 [40, 120, 480, 70],
                 [40, 120, 480, -50],
                 [40, 120, 480, 430],
                 [40, 120, 480, 450]]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(140, 30, self.zone, player)
        block.rect.x = 50
        block.rect.y = 500
        block.boundary_bottom = 750
        block.boundary_top = 115
        block.change_y = -1
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(140, 30, self.zone, player)
        block.rect.x = 810
        block.rect.y = 500
        block.boundary_bottom = 750
        block.boundary_top = 115
        block.change_y = 1
        self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(10):

            target = Pogomonkey()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.jump_start = random_plat[3]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Generate walls after enemies so none spawn on it
        for platform in walls:
            block = Wall(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)


class LevelSeven(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 20
        self.score_multiplier = 12
        self.level_complete_bonus = 500
        self.zone = "Underwater"
        self.background = pygame.image.load("./resources/atlantis-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[200, 30, 800, 615],
                 [300, 30, 0, 115],
                 [300, 30, 700, 115],

                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(150, 30, self.zone, player)
        block.rect.x = 40
        block.rect.y = 710
        block.boundary_left = 40
        block.boundary_right = 600
        block.change_x = -3
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(150, 30, self.zone, player)
        block.rect.x = 100
        block.rect.y = 520
        block.boundary_left = 50
        block.boundary_right = 600
        block.change_x = -5
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(150, 30, self.zone, player)
        block.rect.x = 300
        block.rect.y = 430
        block.boundary_left = 0
        block.boundary_right = 400
        block.change_x = -1
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(150, 30, self.zone, player)
        block.rect.x = 200
        block.rect.y = 340
        block.boundary_left = 0
        block.boundary_right = 400
        block.change_x = -2
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(150, 30, self.zone, player)
        block.rect.x = 300
        block.rect.y = 250
        block.boundary_left = 200
        block.boundary_right = 400
        block.change_x = -4
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(150, 30, self.zone, player)
        block.rect.x = 500
        block.rect.y = 160
        block.boundary_left = 400
        block.boundary_right = 700
        block.change_x = -4
        self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(4):

            target = Bikefish()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.move_end = random_plat[2] + random_plat[0]

            # Add the block to the list of objects
            self.target_list.add(target)


class LevelEight(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 30
        self.score_multiplier = 12
        self.level_complete_bonus = 500
        self.zone = "Underwater"
        self.background = pygame.image.load("./resources/atlantis-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[100, 50, 0, 750],
                 [100, 50, 900, 750],
                 [100, 30, 120, 660],
                 [100, 30, 780, 660],
                 [100, 30, 260, 750],
                 [100, 30, 640, 750],
                 [100, 30, 260, 570],
                 [100, 30, 640, 570],
                 [280, 30, 200, 150],
                 [280, 30, 520, 150]]

        walls = [[40, 120, 220, 680],
                 [40, 120, 740, 680],
                 [40, 110, 220, 570],
                 [40, 110, 740, 570],
                 [40, 90, 480, 0],
                 [40, 90, 480, 90]]

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 30, self.zone, player)
        block.rect.x = 450
        block.rect.y = 660
        block.boundary_left = 370
        block.boundary_right = 530
        block.change_x = -2
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 30, self.zone, player)
        block.rect.x = 300
        block.rect.y = 480
        block.boundary_left = 150
        block.boundary_right = 750
        block.change_x = -3
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 30, self.zone, player)
        block.rect.x = 50
        block.rect.y = 300
        block.boundary_bottom = 500
        block.boundary_top = 200
        block.change_y = -1
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 30, self.zone, player)
        block.rect.x = 850
        block.rect.y = 400
        block.boundary_bottom = 500
        block.boundary_top = 200
        block.change_y = -1
        self.platform_list.add(block)

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)

        # Go through and create randomized targets for the level
        for target in range(10):

            target = Bikefish()

            # Set a random location for the block, but place it on a platform within the list
            # First select a random plat from the list in the level
            random_plat = random.randrange(len(level))
            random_plat = level[random_plat]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            random_plat_x = random_plat[2]
            random_plat_y = random_plat[3]
            target.rect.x = random.randrange(random_plat_x, random_plat_x+(random_plat[0] - target.width))
            target.rect.y = random_plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = random_plat[2]
            target.move_end = random_plat[2] + random_plat[0]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Deliberate target locations for level as per design
        for i in range(8, 10):
            target = Bikefish()

            platform = level[i]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            plat_x = platform[2]
            plat_y = platform[3]
            target.rect.x = random.randrange(plat_x, plat_x+(platform[0] - target.width))
            target.rect.y = plat_y - target.height

            # Move distance allowed for this plat
            target.move_start = platform[2]
            target.move_end = platform[2] + platform[0]

            # Add the block to the list of objects
            self.target_list.add(target)

        # Generate walls after enemies so none spawn on it
        for platform in walls:
            block = Wall(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)


class LevelNine(Level):

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.time_allowed = 40
        self.score_multiplier = 12
        self.level_complete_bonus = 600
        self.zone = "Underwater"
        self.background = pygame.image.load("./resources/atlantis-bg.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1000, 800))

        # Array with width, height, x, and y of platform
        level = [[90, 30, 0, 770],
                 [90, 30, 910, 770],
                 [90, 30, 200, 680],
                 [90, 30, 710, 680],
                 [90, 30, 0, 590],
                 [90, 30, 910, 590],
                 [90, 30, 200, 500],
                 [90, 30, 710, 500],
                 [90, 30, 0, 410],
                 [90, 30, 910, 410],
                 [90, 30, 200, 320],
                 [90, 30, 710, 320],
                 [90, 30, 0, 230],
                 [90, 30, 910, 230],
                 [90, 30, 200, 140],
                 [90, 30, 710, 140],
                 ]

        walls = [[40, 120, 290, 680],
                 [40, 120, 670, 680],
                 [40, 120, 290, 560],
                 [40, 120, 670, 560],
                 [40, 120, 290, 440],
                 [40, 120, 670, 440],
                 [40, 120, 290, 320],
                 [40, 120, 670, 320],
                 [40, 120, 290, 200],
                 [40, 120, 670, 200],
                 [40, 120, 290, 80],
                 [40, 120, 670, 80],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 30, self.zone, player)
        block.rect.x = 350
        block.rect.y = 500
        block.boundary_bottom = 800
        block.boundary_top = 50
        block.change_y = 1
        self.platform_list.add(block)

        # Moving platform construct and add to platform list
        block = MovingPlatform(100, 30, self.zone, player)
        block.rect.x = 550
        block.rect.y = 500
        block.boundary_bottom = 800
        block.boundary_top = 50
        block.change_y = -1
        self.platform_list.add(block)

        # Deliberate target locations for level as per design
        for i in range(len(level)):
            target = Bikefish()

            platform = level[i]

            # Grab it's X and Y and set this iteration of target's X and Y to be within a "standing" bound
            plat_x = platform[2]
            plat_y = platform[3]
            target.rect.x = random.randrange(plat_x, plat_x+(platform[0] - target.width))
            target.rect.y = plat_y - target.height

            # Add the block to the list of objects
            self.target_list.add(target)

        # Generate walls after enemies so none spawn on it
        for platform in walls:
            block = Wall(platform[0], platform[1], self.zone)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.zone = self.zone
            self.platform_list.add(block)
