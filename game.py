import random
import pygame
import time

random.seed()

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
score = 0

# Snake piece image
snake = pygame.image.load("resources/images/snake.jpg")

# Snake image size
snake_size = 20
# Initial snake length
snake_length = 5
# Up/Left/Down/Right
keys = [False, False, False, False]
start_x = random.randint(snake_length + 3, int(width / snake_size) - snake_length - 4) * 20
start_y = random.randint(snake_length + 3, int(height / snake_size) - snake_length - 4) * 20
snake_direction = random.randint(0, 3)

# Initial snake position - X, Y, direction, direction change
snake_positions = [[start_x, start_y, snake_direction, -1]]

# Generate other snake parts
for i in range(snake_length - 1):
    position = snake_positions[i].copy()
    if snake_direction == 0:
        position[1] += 20
    elif snake_direction == 1:
        position[0] += 20
    elif snake_direction == 2:
        position[1] -= 20
    elif snake_direction == 3:
        position[0] -= 20
    snake_positions.append(position)

eat = False
edible = pygame.image.load("resources/images/edible.jpg")
collision = True
while collision:
    edible_x = random.randint(0, int(width / snake_size) - 1) * 20
    edible_y = random.randint(0, int(height / snake_size) - 1) * 20
    collision = False
    for snake_position in snake_positions:
        if snake_position[0] == edible_x and snake_position[1] == edible_y:
            collision = True

edible_item_position = [edible_x, edible_y]


def draw_edible_items(screen, edible_item_position):
    if len(edible_item_position) > 0:
        screen.blit(edible, edible_item_position)


def draw_snake(screen, snake_positions):
    for snake_position in snake_positions:
        screen.blit(snake, (snake_position[0], snake_position[1]))


def new_position(snake_position):
    speed = 1
    x = snake_position[0]
    y = snake_position[1]
    direction = snake_position[2]
    # EDIT: Here need to change if would like to achieve that snake appears on the opposite side of the game field
    if direction == 0:
        y -= speed
    elif direction == 1:
        x -= speed
    elif direction == 2:
        y += speed
    elif direction == 3:
        x += speed
    return [x, y]


def check_edible(snake_positions, eat, edible_item_position, score):
    start_eat = False

    x, y = new_position(snake_positions[0])
    if not eat and len(edible_item_position) > 0:
        edible_x, edible_y = edible_item_position
        if edible_x - snake_size + 1 <= x <= edible_x + snake_size - 1 and \
                edible_y - snake_size + 1 <= y <= edible_y + snake_size - 1:
            start_eat = True

    if start_eat:
        eat = True
        position = snake_positions[0].copy()
        snake_positions[0][3] = -1
        position[0] = x
        position[1] = y
        snake_positions.insert(0, position)
    elif eat:
        position = snake_positions[0]
        position[0] = x
        position[1] = y
        if x == edible_item_position[0] and y == edible_item_position[1]:
            eat = False
            score += 1
            print("Jānis ir izdzēris " + str(score) + " CIDO suliņas!")
            # EDIT: Here we can add a new edible item instead of clearing it
            collision = True
            while collision:
                edible_x = random.randint(0, int(width / snake_size) - 1) * 20
                edible_y = random.randint(0, int(height / snake_size) - 1) * 20
                collision = False
                for snake_position in snake_positions:
                    if snake_position[0] == edible_x and snake_position[1] == edible_y:
                        collision = True

            edible_item_position = [edible_x, edible_y]

    return [snake_positions, eat, edible_item_position, score]


def move_snake(snake_positions, eat):
    if not eat:
        for snake_position in snake_positions:
            snake_position[0], snake_position[1] = new_position(snake_position)

    return snake_positions


def check_change_direction(snake_positions, change_direction):
    # If snake is eating then don't change directions
    if eat:
        return snake_positions[0][2]

    if change_direction >= 0:
        snake_positions[0][3] = change_direction

    i = len(snake_positions) - 1
    while i >= 0:
        snake_position = snake_positions[i]
        if snake_position[3] >= 0 and snake_position[0] % snake_size == 0 and snake_position[1] % snake_size == 0:
            snake_position[2] = snake_position[3]
            if i < len(snake_positions) - 1:
                snake_positions[i + 1][3] = snake_position[3]
            snake_position[3] = -1
        i -= 1
    return snake_positions[0][2]


def get_change_direction(keys, snake_direction):
    change_direction = -1
    if keys[0] and snake_direction != 0 and snake_direction != 2:
        change_direction = 0
    elif keys[2] and snake_direction != 2 and snake_direction != 0:
        change_direction = 2
    if keys[1] and snake_direction != 1 and snake_direction != 3:
        change_direction = 1
    elif keys[3] and snake_direction != 3 and snake_direction != 1:
        change_direction = 3
    return change_direction


def process_events(keys):
    for event in pygame.event.get():
        # Check if the event is the X button
        if event.type == pygame.QUIT:
            # If it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys[0] = True
            elif event.key == pygame.K_LEFT:
                keys[1] = True
            elif event.key == pygame.K_DOWN:
                keys[2] = True
            elif event.key == pygame.K_RIGHT:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys[0] = False
            elif event.key == pygame.K_LEFT:
                keys[1] = False
            elif event.key == pygame.K_DOWN:
                keys[2] = False
            elif event.key == pygame.K_RIGHT:
                keys[3] = False
    return keys

def deathwall(snake_positions):
    x = snake_positions[0][0]
    y = snake_positions[0][1]
    if x < 0 or x > 640 or y < 0 or y > 480:
        return True
    return False

def deathsnake(snake_positions):
    x = snake_positions[0][0]
    y = snake_positions[0][1]
    for position in snake_positions[3:]:

        positionx = position[0]
        positiony = position[1]
        if positionx - snake_size + 1 <= x <= positionx + snake_size - 1 and \
                positiony - snake_size + 1 <= y <= positiony + snake_size - 1:
            return True
    return False



while True:
    # Clear the screen before drawing it again
    screen.fill(0)
    # Draw the screen elements
    draw_snake(screen, snake_positions)
    draw_edible_items(screen, edible_item_position)
    # Update the screen
    pygame.display.flip()

    # Loop through the events
    keys = process_events(keys)

    # Check whether user changed Snake direction
    change_direction = get_change_direction(keys, snake_direction)

    snake_positions, eat, edible_item_position, score = check_edible(snake_positions, eat, edible_item_position, score)

    # Change direction for all snake items
    snake_direction = check_change_direction(snake_positions, change_direction)

    # Move snake items
    snake_positions = move_snake(snake_positions, eat)
    time.sleep(0.01)
    # EDIT: Here we can check whether first snake item isn't out of bounds or crashed into the snake itself
    if deathwall(snake_positions):
        print("Jānis ieskrēja sienā! :O")
        break
    elif deathsnake(snake_positions):
        print("Jānis sevī ieskrēja! :O")
        break
