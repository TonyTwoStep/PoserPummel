import pygame
from blocks import MovingPlatform

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Player(pygame.sprite.Sprite):

    # -- Methods
    def __init__(self):
        # Call the parent's constructor
        super().__init__()

        # Initialized and starting values
        width = 60
        height = 85
        self.direction = "R"
        self.frame = 0
        self.jumping = False

        # Image arrays for bi-directional sprite with animation
        self.player_img_array = []
        self.jump_img_right = []
        self.jump_img_left = []

        # Loading the basic images into the arrays
        player_img = pygame.image.load("./resources/seq1-right.png").convert_alpha()
        player_img = pygame.transform.scale(player_img, (width, height))
        self.player_img_array.append(player_img)

        player_img = pygame.image.load("./resources/seq1-left.png").convert_alpha()
        player_img = pygame.transform.scale(player_img, (width, height))
        self.player_img_array.append(player_img)

        # Loading right facing animated sprites into array
        for seqnum in range(2, 8):
            for i in range(6):
                player_img = pygame.image.load("./resources/seq" + str(seqnum) + "-right.png").convert_alpha()
                player_img = pygame.transform.scale(player_img, (width, height))
                self.jump_img_right.append(player_img)

        # Left facing animated sprites
        for seqnum in range(2, 8):
            for i in range(6):
                player_img = pygame.image.load("./resources/seq" + str(seqnum) + "-left.png").convert_alpha()
                player_img = pygame.transform.scale(player_img, (width, height))
                self.jump_img_left.append(player_img)

        self.image = self.player_img_array[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.rect.y = 750

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # Collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

        if not self.jumping:
            self.frame = 0
            if self.direction == "R":
                self.image = self.player_img_array[0]
            if self.direction == "L":
                self.image = self.player_img_array[1]

        if self.jumping:
            if self.frame == len(self.jump_img_right) - 1:
                self.frame = len(self.jump_img_right) - 1
            else:
                self.frame += 1

            if self.direction == "R":
                self.image = self.jump_img_right[self.frame]
            if self.direction == "L":
                self.image = self.jump_img_left[self.frame]

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # Check for grounding
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.frame = 0
            self.jumping = False

        if self.change_y >= 2.1:
            self.jumping = False

    def jump(self):

        # Check if jump is valid or if it is being blocked by a platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If jump is valid, change sprite to move upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -8
            self.jumping = True

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0
