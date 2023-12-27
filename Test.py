import pygame
import sys
import random
from pygame import mixer
import time

# Starting Pygame
pygame.init()

# Screen Variables
screen_width = 1000
screen_height = 600

# Position Variables
player_x_pos = 500
player_y_pos = 300

# Player Speed
player_speed = 2

# Bullet Speed
bullet_speed = 8

# Bullet Delay
last_shot_time = 0
bullet_delay = 500

# Arrow Key Values
up_key_pressed = False
down_key_pressed = False
left_key_pressed = False
right_key_pressed = False
space_pressed = False

# Player Direction
player_direction = 'Down'

# Player Stats
player_health = 100
player_score = 0
start_time = None

# Zombie Direction
zombie_direction = 'Down'

# Zombie Speed
zombie_speed = 2.7

# Maximum Zombies On Screen
max_zombies_on_screen = 30

# Colors
display_health_color = (255, 0, 0)
title_color = (255, 0, 0)

# Font
game_font = pygame.font.Font('Minecraft copy.ttf', 25)
title_font = pygame.font.Font('Minecraft copy.ttf', 50)

# Game Sounds
player_gun = pygame.mixer.Sound('arcade-8bit-fx-159064.mp3')
player_gun.set_volume(0.8)

zombie_shot = pygame.mixer.Sound('kick-hard-8-bit-103746.mp3')
zombie_shot.set_volume(0.5)

player_hit = pygame.mixer.Sound('hurt_c_08-102842.mp3')
player_hit.set_volume(1)

thunder_noise = pygame.mixer.Sound('thunder-124463.mp3')
thunder_noise.set_volume(1)

rain_noise = pygame.mixer.Sound('rain-with-distant-thunder-112714.mp3')
rain_noise.set_volume(0.6)

night_noise = pygame.mixer.Sound('night-ambience-17064.mp3')
night_noise.set_volume(0.5)

player_death_sound = pygame.mixer.Sound('8-bit-scream_F_minor.wav')
player_death_sound.set_volume(0.7)

extra_heart = pygame.mixer.Sound('video-game-powerup-38065 copy 2.mp3')

# Lightning Variables
lightning_color = (255, 255, 255)
last_lightning = 0

# Extra Life Stats
health_min_x = 3500
health_max_x = 5000
health_min_y = 30
health_max_y = 500

health_x_pos = random.randint(health_min_x, health_max_x)
health_y_pos = random.randint(health_min_y, health_max_y)


def zombie_spawn():
    if len(zombie_group) < max_zombies_on_screen:
        for i in range(7):

            attempts = 0
            max_attempts = 10

            while True:

                # Generating the zombie x-position spawn
                while True:
                    zombie_x_pos = random.randint(-100, 1100)

                    if -50 <= zombie_x_pos <= 1050:
                        pass
                    else:
                        break

                # Generating the zombie y-position spawn
                while True:
                    zombie_y_pos = random.randint(-100, 700)

                    if -50 <= zombie_y_pos <= 650:
                        pass
                    else:
                        break

                zombie = Zombie(zombie_x_pos, zombie_y_pos)

                if not any(zombie.rect.colliderect(existing_zombie.rect) for existing_zombie in zombie_group):
                    zombie_group.add(zombie)
                    break

                attempts += 1
                if attempts >= max_attempts:
                    break


def update_zombies():
    for zombie in zombie_group:
        # Calculate the direction vector from zombie to the center of the player
        dx = player.rect.centerx - zombie.rect.centerx
        dy = player.rect.centery - zombie.rect.centery

        # Normalize the direction vector
        length = max(1, abs(dx) + abs(dy))
        direction_x = dx / length
        direction_y = dy / length

        # Update zombie position based on the normalized direction
        zombie.rect.x += direction_x * zombie_speed
        zombie.rect.y += direction_y * zombie_speed

        # Determine the direction (Up, Down, Left, Right)
        if abs(direction_x) > abs(direction_y):
            if direction_x > 0:
                zombie.update_direction('Right')
            else:
                zombie.update_direction('Left')
        else:
            if direction_y > 0:
                zombie.update_direction('Down')
            else:
                zombie.update_direction('Up')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Creating the player image and rectangle
        self.image = pygame.image.load('enemy-1/frames/enemy1.png').convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image_scaled.get_rect(center=(player_x_pos, player_y_pos))

        # Creating the different player image directions
        self.images = {
            'Down': pygame.transform.rotate(self.image_scaled, 0),
            'Up': pygame.transform.rotate(self.image_scaled, 180),
            'Left': pygame.transform.rotate(self.image_scaled, 270),
            'Right': pygame.transform.rotate(self.image_scaled, 90)
        }

        self.direction = 'Down'
        self.default_image = self.images[self.direction]
        self.mask = pygame.mask.from_surface(self.default_image)

    def create_bullet(self):
        return Bullet(self.rect.centerx, self.rect.centery, player_direction)

    def update_direction(self, direction):
        self.direction = direction
        self.default_image = self.images[self.direction]
        self.rect = self.default_image.get_rect(center=self.rect.center)

        self.mask = pygame.mask.from_surface(self.default_image)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, direction):
        super().__init__()

        # Creating the bullet image and rectangle
        self.image = pygame.Surface((10, 10))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        self.mask = pygame.mask.from_surface(self.image)

        self.direction = direction

    def update(self):

        # Update bullet position based on the direction
        if self.direction == 'Down':
            self.rect.y += bullet_speed

        elif self.direction == 'Up':
            self.rect.y -= bullet_speed

        elif self.direction == 'Left':
            self.rect.x -= bullet_speed

        elif self.direction == 'Right':
            self.rect.x += bullet_speed

        self.mask = pygame.mask.from_surface(self.image)

        # Removing the bullet from the group when it's off-screen
        for bullet in bullet_group:
            if bullet.rect.x < -100 or bullet.rect.x > 1100:
                bullet.kill()

            if bullet.rect.y < -100 or bullet.rect.y > 610:
                bullet.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        # Creating the zombie image and rectangle
        self.image = pygame.image.load('Zombie.png').convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (350, 250))
        self.rect = self.image_scaled.get_rect(center=(x_pos, y_pos))

        # Creating the different zombie image directions
        self.images = {
            'Down': pygame.transform.rotate(self.image_scaled, 0),
            'Up': pygame.transform.rotate(self.image_scaled, 180),
            'Left': pygame.transform.rotate(self.image_scaled, 270),
            'Right': pygame.transform.rotate(self.image_scaled, 90)
        }

        self.direction = 'Down'
        self.default_image = self.images[self.direction]
        self.mask = pygame.mask.from_surface(self.default_image)

    def update_direction(self, direction):
        self.direction = direction
        self.default_image = self.images[self.direction]
        self.rect = self.default_image.get_rect(center=self.rect.center)

        self.mask = pygame.mask.from_surface(self.default_image)


class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(-20, screen_height)

    def update(self):
        self.rect.y += 2
        if self.rect.y > screen_height:
            self.rect.y = random.randint(-20, -5)
            self.rect.x = random.randint(0, screen_width)


class BloodSplatter(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        # Creating the blood splatter image and rectangle
        unscaled_image = pygame.image.load('blood_splatter.png').convert_alpha()
        self.image = pygame.transform.scale(unscaled_image, (75, 75))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

        self.alpha = 255
        self.fade_speed = 2

        self.life = 100

    def update(self):
        # Fade the blood splatter
        self.alpha -= self.fade_speed
        if self.alpha < 0:
            self.alpha = 0

        # Set the alpha value of the image
        self.image.set_alpha(self.alpha)

        # Update the blood splatter position
        self.rect = self.image.get_rect(center=self.rect.center)

        self.life -= 1
        if self.life <= 0:
            self.kill()


class ExtraLife(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Creating the extra life heart
        health_powerup_surface = pygame.image.load('extra_heart.png').convert_alpha()
        self.image = pygame.transform.scale(health_powerup_surface, (80, 80))
        self.rect = self.image.get_rect(center=(health_x_pos, health_y_pos))

        self.speed = 3

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Updating the heart's position
        self.rect.x -= self.speed

        if self.rect.x < -100:
            self.rect.x = random.randint(health_min_x, health_max_x)
            self.rect.y = random.randint(health_min_y, health_max_y)

        self.mask = pygame.mask.from_surface(self.image)


def main(background):
    global last_lightning, start_time

    zombie_spawn_timer = 0

    # Creating the instance of the extra life
    extra_health = ExtraLife()
    extra_health.rect.x = health_x_pos
    extra_health.rect.y = health_y_pos
    extra_life_group.add(extra_health)

    # Loading the game music
    mixer.music.load('8-bit-halloween-story-166454.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    while True:
        lightning_delay = random.randint(20000, 50000)

        event_loop()

        current_time = pygame.time.get_ticks()

        if current_time - last_lightning > lightning_delay:
            thunder_noise.play()
            create_lightning(screen_var[1])
            last_lightning = current_time

        if current_time - zombie_spawn_timer > 2400:
            zombie_spawn()
            zombie_spawn_timer = current_time

        player_movement()
        player_shooting()

        position_check()

        if start_time is not None:
            final_time = update(screen_var[0], screen_var[1], background)
            collision_check(final_time, extra_health)

        update_zombies()


def display_menu(clock, screen, background):
    global start_time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    night_noise.stop()
                    start_time = int((pygame.time.get_ticks() / 1000))
                    main(background)

        # Playing the ambience
        night_noise.play(-1)

        # Displaying the menu graphics
        display_bg(screen, background)
        create_rain(screen)
        display_title(screen)

        pygame.display.update()

        clock.tick(60)


def display_end_screen(clock, screen, background, final_time):
    global player_score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    night_noise.stop()
                    player_score = 0
                    main(background)

        # Playing the ambience
        night_noise.play(-1)

        # Displaying the end screen graphics
        display_bg(screen, background)
        create_rain(screen)
        display_game_over(screen, final_time)

        pygame.display.update()

        clock.tick(60)


def display_time(screen):
    # Displaying the time
    actual_time = int((pygame.time.get_ticks() / 1000)) - start_time

    time_surface = game_font.render(f'Time: {actual_time}', False, title_color)
    time_rect = time_surface.get_rect(center=(940, 25))
    screen.blit(time_surface, time_rect)

    return actual_time


def display_game_over(screen, final_time):
    global player_health, player_score, player_x_pos, player_y_pos, player_direction, up_key_pressed, down_key_pressed, left_key_pressed, right_key_pressed, space_pressed, start_time

    title = title_font.render(f' You Died!', False, title_color)
    title_rect = title.get_rect(center=((screen_width / 2), (screen_height / 2) - 200))
    screen.blit(title, title_rect)

    time_surface = title_font.render(f'You Survived For {final_time} Seconds', False, title_color)
    time_rect = time_surface.get_rect(center=(screen_width / 2, (screen_height / 2)))
    screen.blit(time_surface, time_rect)

    stat_message = title_font.render(f' You killed {player_score} zombies', False, title_color)
    stat_message_rect = stat_message.get_rect(center=((screen_width / 2), (screen_height / 2) + 200))
    screen.blit(stat_message, stat_message_rect)

    # Ending the sounds
    pygame.mixer.music.stop()

    # Resetting the game
    # Player Stats
    player_health = 100
    player.rect.center = (screen_width // 2, screen_height // 2)
    player_direction = 'Down'
    start_time = int((pygame.time.get_ticks() / 1000))

    # Clearing the groups
    zombie_group.empty()
    bullet_group.empty()
    blood_splatter_group.empty()
    extra_life_group.empty()

    # Resetting the key variables
    up_key_pressed = False
    down_key_pressed = False
    left_key_pressed = False
    right_key_pressed = False
    space_pressed = False


def display_title(screen):
    # Displaying the title
    title = title_font.render(f' Survive The Horde', False, title_color)
    title_rect = title.get_rect(center=((screen_width / 2), (screen_height / 2) - 200))
    screen.blit(title, title_rect)

    play_message = title_font.render(f' Press "Space" To Play', False, title_color)
    play_message_rect = play_message.get_rect(center=((screen_width / 2), (screen_height / 2) + 200))
    screen.blit(play_message, play_message_rect)


def display_screen():
    pygame.display.set_caption('Survive The Horde')

    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    return clock, screen


def event_loop():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)

        elif event.type == pygame.KEYUP:
            handle_keyup(event)


def handle_keydown(event):
    global up_key_pressed, down_key_pressed, left_key_pressed, right_key_pressed, space_pressed

    if event.key == pygame.K_UP:
        up_key_pressed = True

    elif event.key == pygame.K_DOWN:
        down_key_pressed = True

    elif event.key == pygame.K_LEFT:
        left_key_pressed = True

    elif event.key == pygame.K_RIGHT:
        right_key_pressed = True

    elif event.key == pygame.K_SPACE:
        space_pressed = True


def handle_keyup(event):
    global up_key_pressed, down_key_pressed, left_key_pressed, right_key_pressed, space_pressed

    if event.key == pygame.K_UP:
        up_key_pressed = False

    elif event.key == pygame.K_DOWN:
        down_key_pressed = False

    elif event.key == pygame.K_LEFT:
        left_key_pressed = False

    elif event.key == pygame.K_RIGHT:
        right_key_pressed = False

    elif event.key == pygame.K_SPACE:
        space_pressed = False


def create_bg():
    # Creating the background
    width = 1000
    height = 600
    field = pygame.Surface((width, height))

    field.fill((0, 10, 15))

    # Draw rectangles for the grassy field
    for x in range(0, width, 50):
        for y in range(0, height, 50):
            # Adding some variations in shades for a more realistic look
            base_green = random.randint(5, 20)
            grass_color = (
                min(15, base_green + random.randint(-3, 3)),
                min(40, base_green + random.randint(-3, 3)),
                min(15, base_green + random.randint(-3, 3)),
            )
            pygame.draw.rect(field, grass_color, (x, y, 50, 50))

    return field


def create_rain(screen):
    # Creating the rain effect
    raindrops = pygame.sprite.Group()

    for _ in range(125):
        raindrop = Raindrop()
        raindrops.add(raindrop)

    raindrops.draw(screen)


def create_lightning(screen):
    # Creating the lightning effect
    for intensity in range(0, 256, 8):
        draw_lightning(screen, intensity)
        time.sleep(0.00001)

    for intensity in range(255, -1, -8):
        draw_lightning(screen, intensity)
        time.sleep(0.007)


def draw_lightning(screen, intensity):
    # Drawing the lightning effect
    color = (intensity, intensity, intensity)

    screen.fill(color)

    pygame.display.flip()


def display_bg(screen, background):
    # Displaying the background
    screen.blit(background, (0, 0))


def display_player(screen):
    # Drawing the player on the screen based on the direction
    if player_direction == 'Down':
        screen.blit(player.images['Down'], player.rect)

    elif player_direction == 'Up':
        screen.blit(player.images['Up'], player.rect)

    elif player_direction == 'Left':
        screen.blit(player.images['Left'], player.rect)

    elif player_direction == 'Right':
        screen.blit(player.images['Right'], player.rect)


def display_zombie(screen):
    # Drawing the zombie on the screen based on its direction
    for zombie in zombie_group:
        screen.blit(zombie.default_image, zombie.rect)


def display_health(screen):
    # Displaying the player's health
    # Loading in the images
    heart_1 = pygame.image.load('Heart_Red_1.png').convert_alpha()
    heart_1_scaled = pygame.transform.scale(heart_1, (40, 40))
    heart_1_rect = heart_1_scaled.get_rect(center=(25, 25))

    heart_2 = pygame.image.load('Heart_Red_1.png').convert_alpha()
    heart_2_scaled = pygame.transform.scale(heart_2, (40, 40))
    heart_2_rect = heart_2_scaled.get_rect(center=(55, 25))

    heart_3 = pygame.image.load('Heart_Red_1.png').convert_alpha()
    heart_3_scaled = pygame.transform.scale(heart_3, (40, 40))
    heart_3_rect = heart_3_scaled.get_rect(center=(85, 25))

    heart_4 = pygame.image.load('Heart_Red_1.png').convert_alpha()
    heart_4_scaled = pygame.transform.scale(heart_4, (40, 40))
    heart_4_rect = heart_4_scaled.get_rect(center=(115, 25))

    # Displaying the hearts on the screen
    if player_health == 100:
        screen.blit(heart_1_scaled, heart_1_rect)
        screen.blit(heart_2_scaled, heart_2_rect)
        screen.blit(heart_3_scaled, heart_3_rect)
        screen.blit(heart_4_scaled, heart_4_rect)

    elif player_health == 75:
        screen.blit(heart_1_scaled, heart_1_rect)
        screen.blit(heart_2_scaled, heart_2_rect)
        screen.blit(heart_3_scaled, heart_3_rect)

    elif player_health == 50:
        screen.blit(heart_1_scaled, heart_1_rect)
        screen.blit(heart_2_scaled, heart_2_rect)

    elif player_health == 25:
        screen.blit(heart_1_scaled, heart_1_rect)

    else:
        pass


def display_score(screen):
    # Displaying the player's score
    player_score_surface = game_font.render(f' Score: {player_score}', False, display_health_color)
    player_score_rect = player_score_surface.get_rect(center=(500, 25))
    screen.blit(player_score_surface, player_score_rect)


def player_movement():
    global player_direction

    if up_key_pressed:
        player_direction = 'Up'
        player.rect.y -= player_speed

    if down_key_pressed:
        player_direction = 'Down'
        player.rect.y += player_speed

    if left_key_pressed:
        player_direction = 'Left'
        player.rect.x -= player_speed

    if right_key_pressed:
        player_direction = 'Right'
        player.rect.x += player_speed


def player_shooting():
    global bullet_group, last_shot_time

    current_time = pygame.time.get_ticks()

    if space_pressed and current_time - last_shot_time > bullet_delay:
        bullet = player.create_bullet()
        bullet_group.add(bullet)

        player_gun.play()

        last_shot_time = current_time

        # Move the bullet to the correct starting position
        if player_direction == 'Down':
            bullet.rect.y -= bullet_speed

        elif player_direction == 'Up':
            bullet.rect.y += bullet_speed

        elif player_direction == 'Left':
            bullet.rect.x += bullet_speed

        elif player_direction == 'Right':
            bullet.rect.x -= bullet_speed


def position_check():
    # Checking the player's position and adjusting if the player goes off-screen
    if player.rect.y < -45:
        player.rect.y = -45

    if player.rect.y > 545:
        player.rect.y = 545

    if player.rect.x < -45:
        player.rect.x = -45

    if player.rect.x > 945:
        player.rect.x = 945


def collision_check(final_time, extra_health):
    global player_score, player_health, zombie_group, bullet_group, player, blood_splatter_group, extra_life_group

    # Check for collisions between bullets and zombies
    collisions = pygame.sprite.groupcollide(bullet_group, zombie_group, False, False, pygame.sprite.collide_mask)

    # Handling the collisions
    for bullet, zombies_hit in collisions.items():
        for zombie in zombies_hit:
            # Checking if the bullet's mask collides with the zombie's mask
            if pygame.sprite.collide_mask(bullet, zombie):
                zombie_group.remove(zombie)
                bullet_group.remove(bullet)

                zombie_shot.play()

                player_score += 1

                # Add blood splatter where the zombie died
                blood_splatter = BloodSplatter(zombie.rect.centerx, zombie.rect.centery)
                blood_splatter_group.add(blood_splatter)

    # Checking for collisions with the player and the zombies
    player_zombie_collisions = pygame.sprite.spritecollide(player, zombie_group, False, pygame.sprite.collide_mask)

    # Handling player and zombie collisions
    for zombie in player_zombie_collisions:
        if pygame.sprite.collide_mask(player, zombie):
            zombie_group.remove(zombie)

            player_hit.play()

            player_health -= 25

            blood_splatter = BloodSplatter(zombie.rect.centerx, zombie.rect.centery)
            blood_splatter_group.add(blood_splatter)

            if player_health == 0:
                player_death_sound.play()
                display_end_screen(screen_var[0], screen_var[1], grass, final_time)

    # Checking for collisions with the player and the extra life powerup
    extra_life_collisions = pygame.sprite.spritecollide(player, extra_life_group, False)

    for life in extra_life_collisions:
        if pygame.sprite.collide_mask(player, life):
            if player_health != 100:
                extra_heart.play()
                player_health += 25
                extra_health.rect.x = random.randint(health_min_x, health_max_x)
                extra_health.rect.y = random.randint(health_min_y, health_max_y)
            else:
                pass


def update(clock, screen, background):
    display_bg(screen_var[1], background)

    bullet_group.update()
    bullet_group.draw(screen)

    display_player(screen_var[1])
    display_zombie(screen_var[1])
    display_health(screen_var[1])
    display_score(screen_var[1])
    final_time = display_time(screen_var[1])

    blood_splatter_group.update()
    blood_splatter_group.draw(screen)

    extra_life_group.update()
    extra_life_group.draw(screen_var[1])

    create_rain(screen)

    pygame.display.update()

    clock.tick(60)

    return final_time


screen_var = display_screen()

player = Player()

bullet_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
blood_splatter_group = pygame.sprite.Group()
extra_life_group = pygame.sprite.Group()

grass = create_bg()
rain_noise.play(-1)

# Starting the game
display_menu(screen_var[0], screen_var[1], grass)
