"""
Poser Pummel
A Skateboarding Platformer / Shooter
by Anthony DiBari
"""

import pygame
from blocks import Bullet
from levels import LevelOne
from levels import LevelTwo
from levels import LevelThree
from levels import LevelFour
from levels import LevelFive
from levels import LevelSix
from levels import LevelSeven
from levels import LevelEight
from levels import LevelNine
from player import Player
from menu import main_menu
from menu import game_over
from text import calculate_score
from text import draw_level_title
from text import draw_timer
from text import draw_score
from text import draw_lives

# Global constants
# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


def main():

    # Initial values for local variables
    hits = 0
    lives = 3
    score = 0
    new_level = True

    # Sentinel value for main game loop
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Initialize Pygame and its mixer (fixes sound latency)
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    # -------- Game Set Up -----------------
    # Set the height and width and title of the pop out window
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Poser Pummel - DSA Studios")

    # Load sounds
    click_sound = pygame.mixer.Sound("./resources/snd/gun.ogg")
    song = pygame.mixer.Sound("./resources/snd/song.ogg")
    ollie = pygame.mixer.Sound("./resources/snd/ollie.ogg")
    hit = pygame.mixer.Sound("./resources/snd/hit.ogg")

    # Create the player
    player = Player()

    # Create all the levels and append them to the level_list
    level_list = [LevelOne(player),
                  LevelTwo(player),
                  LevelThree(player),
                  LevelFour(player),
                  LevelFive(player),
                  LevelSix(player),
                  LevelSeven(player),
                  LevelEight(player),
                  LevelNine(player)]

    # Set the current level to the default first level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # Create a group of active sprites
    active_sprite_list = pygame.sprite.Group()

    # Set level attribute of player to the current_level
    player.level = current_level

    # Add player to the active_sprite list
    active_sprite_list.add(player)

    # Create a group for bullet tracking
    bullet_list = pygame.sprite.Group()

    # -------- Main Menu -------------------
    song.play()
    main_menu(screen)

    # -------- Main Program Loop -----------
    while not done:

        # -------- Event Handling -----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Key Press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    player.direction = "L"
                if event.key == pygame.K_d:
                    player.go_right()
                    player.direction = "R"
                if event.key == pygame.K_w:
                    player.jump()
                    ollie.play()

            # Key Release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

            # Left Click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Fire a bullet and play the sound
                click_sound.play()
                bullet = Bullet()
                # Set the bullet so it is where the player is
                bullet.rect.y = player.rect.y + 14
                if player.direction == "R":
                    bullet.direction = "R"
                    bullet.rect.x = player.rect.x + 45
                if player.direction == "L":
                        bullet.direction = "L"
                        bullet.rect.x = player.rect.x
                # Add the bullet to the lists
                active_sprite_list.add(bullet)
                bullet_list.add(bullet)

        # -------- Game Logic -----------

        # Level progress
        # At the start of each new level: display the level title screen, clear bullets and reset the player position
        if new_level:
            draw_level_title(screen, current_level_no, 90, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100,
                             current_level.zone, current_level.time_allowed, lives)

            # Position reset
            player.rect.x = SCREEN_WIDTH / 2
            player.rect.y = 750

            # Grab level start clock
            current_level.start_clock = pygame.time.get_ticks()

            # Clear all remaining bullets from screen
            for bullet in bullet_list:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

            # Sentinel
            new_level = False

        # Update the player.
        active_sprite_list.update()

        # Update items in the level.
        current_level.update()

        # -------- Bullet Mechanics -----------
        for bullet in bullet_list:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, current_level.target_list, True)
            platform_hit_list = pygame.sprite.spritecollide(bullet, current_level.platform_list, False)

            # Enemy hit, remove enemy and bullet add to score and kills
            for target in block_hit_list:
                hit.play()
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)
                hits += 1
                score += 10

            # Platform hit, remove bullet
            for target in platform_hit_list:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

            # Remove bullet if off screen
            if bullet.rect.x > 1000:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)
            if bullet.rect.x < 0:
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

        # Don't let player go off the screen
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        if player.rect.left < 0:
            player.rect.left = 0

        # Clock handling
        seconds = current_level.time_allowed - ((pygame.time.get_ticks()-current_level.start_clock)/1000)

        # -------- Drawing Code  --------------
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        draw_score(screen, score)
        draw_timer(screen, seconds)
        draw_lives(screen, lives)
        # -------- End Drawing Code -----------

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # -------- Checks that should occur before flipping the screen -----------

        # When no targets are left in the level, go to the next level in the level_list
        if not current_level.target_list:
            current_level.level_complete = True
            score = calculate_score(score, seconds, current_level.score_multiplier, current_level.level_complete_bonus)
            current_level_no += 1
            current_level = level_list[current_level_no]
            player.level = current_level
            new_level = True

        # Death handling
        if seconds <= 0.5 and not new_level:
            current_level.level_reset(player)
            new_level = True
            lives -= 1
        if lives == 0:
            new_game = game_over(screen, score, current_level_no, hits, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 300)
            if new_game:
                for i in range(len(level_list)):
                    level_list[i].level_reset(player)
                current_level_no = 0
                current_level = level_list[current_level_no]
                player.level = current_level
                hits = 0
                lives = 3
                score = 0
                seconds = 0
                new_level = True

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


# Tells IDE to boot the main()
if __name__ == "__main__":
    main()
