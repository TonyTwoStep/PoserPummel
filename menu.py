import pygame

# Fonts used throughout
score_font = pygame.font.match_font('8bitmadness', 25)
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
PLAYER_PINK = (216, 0, 255)
TITLE_COLOR = (215, 215, 215)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


def fade_out(surface, width, height, alpha):
    fade = pygame.Surface((width, height))
    fade.fill(BLACK)
    fade.set_alpha(alpha)
    surface.blit(fade, (0, 0))
    pygame.display.flip()
    alpha -= 10
    return alpha


def main_menu(surface):
    # Sentinel value for main menu while loop and starting alpha value
    done_intro = False
    alpha = 255

    while not done_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        alpha = fade_out(surface, SCREEN_WIDTH, SCREEN_HEIGHT, alpha)

        background = pygame.image.load("./resources/img/menu_bg.png").convert_alpha()
        rect = background.get_rect()
        surface.fill(PURPLE)
        surface.blit(background, rect)
        font = pygame.font.Font(score_font, 80)
        text_surface = font.render("Poser Pummel", True, PLAYER_GREEN)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (SCREEN_WIDTH / 2, 100)
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(score_font, 80)
        text_surface = font.render("Poser Pummel", True, TITLE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.midtop = ((SCREEN_WIDTH / 2) - 4, 96)
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(score_font, 40)
        text_surface = font.render("Built using Python + PyGame", True, BUTTON_INACTIVE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (SCREEN_WIDTH / 2, 160)
        surface.blit(text_surface, text_rect)

        # Menu Buttons
        # Args: screen, x, y, width, height, inactive color, hover color
        # Play
        done_intro = button(surface, "Play!", 400, 230, 200, 90, BUTTON_INACTIVE, BUTTON_ACTIVE)

        # Quit
        if button(surface, "Quit!", 400, 490, 200, 90, BUTTON_INACTIVE, BUTTON_ACTIVE):
            pygame.quit()
            quit()

        # How to play Screen (loop)
        how_to = button(surface, "How to Play", 400, 360, 200, 90, BUTTON_INACTIVE, BUTTON_ACTIVE)

        while how_to:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            background = pygame.image.load("./resources/img/how-to.png").convert_alpha()
            rect = background.get_rect()
            surface.blit(background, rect)

            if button(surface, "Back to Title", 380, 650, 240, 90, BUTTON_INACTIVE, BUTTON_ACTIVE):

                how_to = False
                done_intro = False

            pygame.display.update()

        pygame.display.update()


def button(surface, message, x, y, width, height, base_color, hover_color):
    mouse = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        if mouse_click[0] == 1:
            return True

    else:
        pygame.draw.rect(surface, base_color, (x, y, width, height))

    font = pygame.font.Font(score_font, 40)
    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    surface.blit(text_surface, text_rect)

    return False


def game_over(surface, score, levels_completed, num_killed, x, y):

    size = 90
    done_game_over = False

    while not done_game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        background = pygame.image.load("./resources/img/menu_bg.png").convert_alpha()
        rect = background.get_rect()
        surface.fill(PURPLE)
        surface.blit(background, rect)

        # Drawing the title with 3D Effect
        font = pygame.font.Font(level_font, size)
        text_surface = font.render("GAME OVER", True, RED)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
        text_surface = font.render("GAME OVER", True, TITLE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x - 4, y - 4)
        surface.blit(text_surface, text_rect)

        # Sorry Dude
        font = pygame.font.Font(level_font, round(size / 2))
        text_surface = font.render("Better luck next time dude...", True, BUTTON_INACTIVE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y + 50)
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(level_font, round(size / 1.5))
        font.set_underline(True)
        text_surface = font.render("Ending Stats", True, TITLE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y + 120)
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(level_font, round(size / 2))
        text_surface = font.render("Final Score: " + str(score), True, BUTTON_INACTIVE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y + 160)
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(level_font, round(size / 2))
        text_surface = font.render("Enemies Killed: " + str(num_killed), True, BUTTON_INACTIVE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y + 190)
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(level_font, round(size / 2))
        text_surface = font.render("Levels Completed: " + str(levels_completed), True, BUTTON_INACTIVE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y + 220)
        surface.blit(text_surface, text_rect)

        # Retry button
        retry_button = button(surface, "Retry!", 280, 370, 200, 90, BUTTON_INACTIVE, BUTTON_ACTIVE)

        if retry_button:
            done_game_over = retry_button
            return True

        # Quit button
        quit_button = button(surface, "Give Up!", 520, 370, 200, 90, BUTTON_INACTIVE, BUTTON_ACTIVE)

        if quit_button:
            pygame.quit()
            quit()

        pygame.display.flip()


