import pygame

# Fonts used throughout
score_font = pygame.font.match_font('8bitmadness', 35)
level_font = pygame.font.match_font('8bitmadness', 50)
largeText = pygame.font.match_font('8bitmadness', 115)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 255)
BUTTON_ACTIVE = (150, 150, 150)
BUTTON_INACTIVE = (200, 200, 200)
PLAYER_GREEN = (0, 150, 77)


# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


# Score calculation using custom algorithm
def calculate_score(previous_score, seconds, multiplier, bonus):
    new_score = round((seconds * multiplier) + previous_score + bonus)
    return new_score


# Score drawing to screen
def draw_score(surface, text):
    font = pygame.font.Font(score_font, 35)
    text_surface = font.render("Score: " + str(text), True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (0, 0)
    surface.blit(text_surface, text_rect)


# Timer format conversion and drawing
def draw_timer(surface, seconds):
    text = "Time Remaining: "
    # Convert ticks into seconds readable
    if seconds < 10:
        text += "0:0" + str(seconds)[:1]
    elif 60 > seconds >= 10:
        text += "0:" + str(seconds)[:2]
    elif seconds >= 60:
        m = seconds / 60
        s = seconds % 60
        if s >= 10:
            text += str(m)[:1] + ":" + str(s)[:2]
        else:
            text += str(m)[:1] + ":0" + str(s)[:1]
    else:
        text = "ERROR"

    font = pygame.font.Font(score_font, 35)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (715, 0)
    surface.blit(text_surface, text_rect)


# Level title drawing at death or new level
def draw_level_title(surface, level_num, size, x, y, zone, seconds, num_lives):
    # Level Screen background
    if zone == "City":
        background = pygame.image.load("./resources/city-level.png").convert_alpha()
    elif zone == "Swamp":
        background = pygame.image.load("./resources/swamp-level.png").convert_alpha()
    elif zone == "Underwater":
        background = pygame.image.load("./resources/atlantis-level.png").convert_alpha()
    else:
        background = None
        surface.fill(BLUE)

    background = pygame.transform.scale(background, (1000, 800))
    background_rect = background.get_rect()
    surface.blit(background, background_rect)

    # Drawing the title with 3D Effect
    font = pygame.font.Font(level_font, size)
    text_surface = font.render("Level " + str(level_num + 1), True, PLAYER_GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    text_surface = font.render("Level " + str(level_num + 1), True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x - 4, y - 4)
    surface.blit(text_surface, text_rect)

    # Drawing the zone information
    font = pygame.font.Font(level_font, round(size / 2))
    text_surface = font.render("Zone: " + zone, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y + 70)
    surface.blit(text_surface, text_rect)

    # Drawing the amount of seconds for that specific level
    font = pygame.font.Font(level_font, round(size / 2))
    text_surface = font.render("You have " + str(seconds) + " seconds to clear the level.", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y + 160)
    surface.blit(text_surface, text_rect)

    # Drawing the amount of lives the player has left
    font = pygame.font.Font(level_font, round(size / 3))
    text_surface = font.render("Lives:               ", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y + 206)
    surface.blit(text_surface, text_rect)

    # Load life icon
    life_img = pygame.image.load("./resources/life.png").convert_alpha()
    life_img_rect = life_img.get_rect()
    life_img_rect.y = y + 200
    life_img_rect.x = x

    # Loop for blitting life icons
    for i in range(num_lives):

        surface.blit(life_img, life_img_rect)
        life_img_rect.x += 22

    # Render all to screen
    pygame.display.flip()

    # Wait 3 seconds while pumping the OS so the window doesn't lock up
    for i in range(100):
        pygame.time.delay(30)
        pygame.event.pump()


def draw_lives(surface, num_lives):
    size = 25
    start_y = 23
    start_x = 938
    font = pygame.font.Font(score_font, size)
    text_surface = font.render("Lives:", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (865, start_y + 5)
    surface.blit(text_surface, text_rect)

    # Load life icon
    life_img = pygame.image.load("./resources/life.png").convert_alpha()
    life_img_rect = life_img.get_rect()
    life_img_rect.y = start_y
    life_img_rect.x = start_x

    # Loop for blitting life icons
    for i in range(num_lives):

        surface.blit(life_img, life_img_rect)
        life_img_rect.x += 22

