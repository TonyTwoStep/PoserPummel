import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 255)
BUTTON_ACTIVE = (150, 150, 150)
BUTTON_INACTIVE = (200, 200, 200)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, zone):
        super().__init__()
        self.zone = zone

        # City skin
        if self.zone == "City":
            if width <= 150:
                self.image = pygame.image.load("./resources/city-plat.png").convert_alpha()
            else:
                self.image = pygame.image.load("./resources/city-plat-long.png").convert_alpha()

        # Swamp skin
        elif self.zone == "Swamp":
            if width <= 150:
                self.image = pygame.image.load("./resources/swamp-plat.png").convert_alpha()
            else:
                self.image = pygame.image.load("./resources/swamp-plat-long.png").convert_alpha()

        # Underwater skin
        elif self.zone == "Underwater":
            if width <= 150:
                self.image = pygame.image.load("./resources/underwater-plat.png").convert_alpha()
            else:
                self.image = pygame.image.load("./resources/underwater-plat-long.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    def __init__(self, width, height, zone, player):

        # Call parent constructor to skin and construct platform dimensions
        super().__init__(width, height, zone)

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.player = player

    def update(self):
        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        if self.rect.x < self.boundary_left or self.rect.x > self.boundary_right:
            self.change_x *= -1


class Wall(Platform):
    def __init__(self, width, height, zone):

        # Call parent constructor to skin and construct platform dimensions
        super().__init__(width, height, zone)
        self.zone = zone

        # City skin
        if self.zone == "City":
            self.image = pygame.image.load("./resources/city-wall.png").convert_alpha()
        elif self.zone == "Swamp":
            self.image = pygame.image.load("./resources/swamp-wall.png").convert_alpha()
        elif self.zone == "Underwater":
            self.image = pygame.image.load("./resources/underwater-wall.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (width, height))


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 4])
        self.image.fill(BLACK)
        self.direction = "R"
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        if self.direction == "R":
            self.rect.x += 9
        if self.direction == "L":
            self.rect.x -= 9


class Target(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.target_states = []
        self.width = 37
        self.height = 80
        self.direction = "R"
        self.change_x = 1
        self.change_y = 0
        self.move_start = 0
        self.move_end = 0

        target_img = pygame.image.load("./resources/initial.png").convert_alpha()
        target_img = pygame.transform.scale(target_img, (self.width, self.height))
        self.target_states.append(target_img)
        target_img = pygame.image.load("./resources/initial.png").convert_alpha()
        target_img = pygame.transform.scale(target_img, (self.width, self.height))
        self.target_states.append(target_img)

        self.image = self.target_states[0]
        self.rect = self.image.get_rect()

    def change_directions(self):
        self.change_x *= -1
        if self.direction == "R":
            self.direction = "L"
        elif self.direction == "L":
            self.direction = "R"

    def update(self):
        # Walk only between edges of current platform
        if (self.rect.x + self.width == self.move_end or self.rect.x == self.move_start) and 0 != self.change_x:
            self.change_directions()

        # Handling for spawn glitched enemies
        if self.move_end - self.move_start <= 10 + self.width:
            self.change_x = 0
        if self.rect.x < self.move_start or self.rect.x + self.width > self.move_end:
            self.change_x = 0

        # State changing based on direction
        if self.direction == "R":
            self.image = self.target_states[0]
        if self.direction == "L":
            self.image = self.target_states[1]

        # Move left/right
        self.rect.x += self.change_x
        self.rect.y += self.change_y


class Cop(Target):

        def __init__(self):
            Target.__init__(self)

            self.target_states.clear()

            target_img = pygame.image.load("./resources/cop.png").convert_alpha()
            target_img = pygame.transform.scale(target_img, (self.width, self.height))
            self.target_states.append(target_img)
            target_img = pygame.image.load("./resources/cop2.png").convert_alpha()
            target_img = pygame.transform.scale(target_img, (self.width, self.height))
            self.target_states.append(target_img)


class Pogomonkey(Target):

        def __init__(self):
            Target.__init__(self)

            self.jump_start = None
            self.target_states.clear()
            self.jump = False

            target_img = pygame.image.load("./resources/pogomonkey.png").convert_alpha()
            target_img = pygame.transform.scale(target_img, (self.width, self.height))
            self.target_states.append(target_img)
            self.target_states.append(target_img)

        def update(self):

            # Gravity
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35

            # Check for grounding
            if self.rect.y >= self.jump_start - self.rect.height:
                self.change_y = 0
                self.jump = True
                self.rect.y = self.jump_start - self.rect.height

            if self.jump:
                i = random.randrange(0, 2)
                if i == 1:
                    self.change_y = -6
                    self.jump = False

            # Walk only between edges of current platform
            # Right walk handling
            if self.rect.x + self.width == self.move_end or self.rect.x == self.move_start:
                self.change_x *= -1
                self.change_directions()
            elif self.rect.x + self.width > self.move_end or self.rect.x < self.move_start:
                self.change_x = 0

            # State changing based on direction
            if self.direction == "R":
                self.image = self.target_states[0]
            if self.direction == "L":
                self.image = self.target_states[1]

            # Move left/right
            self.rect.x += self.change_x
            self.rect.y += self.change_y


class Bikefish(Target):

        def __init__(self):
            Target.__init__(self)

            self.target_states.clear()
            self.width = 87

            target_img = pygame.image.load("./resources/bikefish.png").convert_alpha()
            target_img = pygame.transform.scale(target_img, (self.width, self.height))
            self.target_states.append(target_img)
            target_img = pygame.image.load("./resources/bikefish2.png").convert_alpha()
            target_img = pygame.transform.scale(target_img, (self.width, self.height))
            self.target_states.append(target_img)

