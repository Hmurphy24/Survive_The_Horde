import pygame

# Starting Pygame
pygame.init()

# Position Variables
player_x_pos = 500
player_y_pos = 300

# Player Speed
player_speed = 2.25

# Arrow Key Values
up_key_pressed = None
down_key_pressed = None
left_key_pressed = None
right_key_pressed = None

# Player Direction
player_direction = 'Down'


def main():

    while True:

        event_loop()

        display_player(screen_var[1], direction[0], direction[1], direction[2], direction[3])

        player_movement()

        position_check()

        update(screen_var[0], screen_var[1])


def display_screen():

    pygame.display.set_caption('Survive The Horde')

    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    return clock, screen


def player_assets():

    # Loading in player image
    player_image = pygame.image.load('enemy-1/frames/enemy1.png').convert_alpha()

    # Increasing the size of the player
    player_image_scaled = pygame.transform.scale(player_image, (100, 100))

    # Creating the player rectangle
    rectangle = player_image_scaled.get_rect(center=(player_x_pos, player_y_pos))

    # Different Player Directions
    face_down = pygame.transform.rotate(player_image_scaled, 0)

    face_up = pygame.transform.rotate(player_image_scaled, 180)

    face_left = pygame.transform.rotate(player_image_scaled, 270)

    face_right = pygame.transform.rotate(player_image_scaled, 90)

    return face_down, face_up, face_left, face_right, rectangle


def event_loop():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            exit()

        # Checking if the arrow key is pressed down
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                global up_key_pressed
                up_key_pressed = True

            elif event.key == pygame.K_DOWN:

                global down_key_pressed
                down_key_pressed = True

            elif event.key == pygame.K_LEFT:

                global left_key_pressed
                left_key_pressed = True

            elif event.key == pygame.K_RIGHT:

                global right_key_pressed
                right_key_pressed = True

        # Checking if the arrow key unpressed
        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:

                up_key_pressed = False

            elif event.key == pygame.K_DOWN:

                down_key_pressed = False

            elif event.key == pygame.K_LEFT:

                left_key_pressed = False

            elif event.key == pygame.K_RIGHT:

                right_key_pressed = False


def display_player(screen, down, up, left, right):

    global player_rect

    # Drawing the player on the screen based on the direction
    if player_direction == 'Down':

        screen.blit(down, player_rect)

    if player_direction == 'Up':

        screen.blit(up, player_rect)

    if player_direction == 'Left':

        screen.blit(left, player_rect)

    if player_direction == 'Right':

        screen.blit(right, player_rect)


def player_movement():

    global player_x_pos
    global player_y_pos
    global player_direction

    if up_key_pressed:

        player_direction = 'Up'

        player_rect.y -= player_speed

    if down_key_pressed:

        player_direction = 'Down'

        player_rect.y += player_speed

    if left_key_pressed:

        player_direction = 'Left'

        player_rect.x -= player_speed

    if right_key_pressed:

        player_direction = 'Right'

        player_rect.x += player_speed


def position_check():

    # Checking the player's position and adjusting if the player goes off-screen
    if player_rect.y < -45:

        player_rect.y = -45

    if player_rect.y > 545:

        player_rect.y = 545

    if player_rect.x < -45:

        player_rect.x = -45

    if player_rect.x > 945:

        player_rect.x = 945


def update(clock, screen):

    pygame.display.update()

    screen.fill('Black')

    clock.tick(60)


screen_var = display_screen()

direction = player_assets()

player_rect = direction[4]

main()
