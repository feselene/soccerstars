import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")

# Colors
WHITE = (255, 255, 255)
RED = (254, 60, 114)  # Tinder Red
BLUE = (29, 161, 242)  # Twitter Blue
BLACK = (0, 0, 0)

# Game constants
PADDLE_RADIUS = 20
PUCK_RADIUS = 15
PUCK_FRICTION = 0.99  # Reduced friction for smoother rolling
PADDLE_FRICTION = 0.95  # Friction for the paddles

# Define bounding box (playing area for the paddles)
BOUNDARY_MARGIN = 50
BOUNDARY_LEFT = BOUNDARY_MARGIN
BOUNDARY_RIGHT = WIDTH - BOUNDARY_MARGIN
BOUNDARY_TOP = BOUNDARY_MARGIN
BOUNDARY_BOTTOM = HEIGHT - BOUNDARY_MARGIN

# Define goal areas
GOAL_WIDTH = 10
GOAL_HEIGHT = 100
GOAL_LEFT_X = BOUNDARY_LEFT - GOAL_WIDTH
GOAL_RIGHT_X = BOUNDARY_RIGHT
GOAL_Y = HEIGHT // 2 - GOAL_HEIGHT // 2

# Puck properties
puck_pos = [WIDTH // 2, HEIGHT // 2]
puck_vel = [0, 0]

# Player positions and velocities
team1_positions = [[100, HEIGHT // 4], [100, HEIGHT // 2], [100, 3 * HEIGHT // 4]]
team2_positions = [[WIDTH - 100, HEIGHT // 4], [WIDTH - 100, HEIGHT // 2], [WIDTH - 100, 3 * HEIGHT // 4]]
team1_velocities = [[0, 0] for _ in range(3)]
team2_velocities = [[0, 0] for _ in range(3)]

# Scoring
team1_score, team2_score = 0, 0
font = pygame.font.Font(None, 74)

# Variables for click-and-drag control
dragging = [False for _ in range(6)]
start_drag_pos = [None for _ in range(6)]

# Helper function to reset the puck
def reset_puck():
    global puck_pos, puck_vel
    puck_pos = [WIDTH // 2, HEIGHT // 2]
    puck_vel = [0, 0]

# Function to apply drag control to paddles
def apply_drag(index, pos, event):
    global dragging, start_drag_pos

    if event.type == pygame.MOUSEBUTTONDOWN:
        if math.dist(pos, event.pos) < PADDLE_RADIUS:
            dragging[index] = True
            start_drag_pos[index] = event.pos
    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging[index]:
            dx = event.pos[0] - start_drag_pos[index][0]
            dy = event.pos[1] - start_drag_pos[index][1]
            force = min(math.sqrt(dx ** 2 + dy ** 2) / 4, 15)  # Scale and cap force
            angle = math.atan2(dy, dx)
            vel_x = force * math.cos(angle)
            vel_y = force * math.sin(angle)

            if index < 3:
                team1_velocities[index] = [vel_x, vel_y]
            else:
                team2_velocities[index - 3] = [vel_x, vel_y]

            dragging[index] = False
            start_drag_pos[index] = None

# Function to update position with friction and keep paddles in bounds
def update_position_with_bounds(pos, vel, friction):
    pos[0] += vel[0]
    pos[1] += vel[1]
    vel[0] *= friction
    vel[1] *= friction

    # Left boundary: block paddles from entering the left goal zone
    if pos[0] - PADDLE_RADIUS < BOUNDARY_LEFT:
        # If paddle is within the vertical range of the goal, prevent it from entering the goal area
        if pos[1] < GOAL_Y or pos[1] > GOAL_Y + GOAL_HEIGHT:
            pos[0] = BOUNDARY_LEFT + PADDLE_RADIUS
            vel[0] = -vel[0]  # Reverse x-velocity to simulate a bounce

    # Right boundary: block paddles from entering the right goal zone
    elif pos[0] + PADDLE_RADIUS > BOUNDARY_RIGHT:
        # If paddle is within the vertical range of the goal, prevent it from entering the goal area
        if pos[1] < GOAL_Y or pos[1] > GOAL_Y + GOAL_HEIGHT:
            pos[0] = BOUNDARY_RIGHT - PADDLE_RADIUS
            vel[0] = -vel[0]  # Reverse x-velocity to simulate a bounce

    # Top and bottom boundaries
    if pos[1] - PADDLE_RADIUS < BOUNDARY_TOP:
        pos[1] = BOUNDARY_TOP + PADDLE_RADIUS
        vel[1] = -vel[1]  # Reverse y-velocity to simulate a bounce
    elif pos[1] + PADDLE_RADIUS > BOUNDARY_BOTTOM:
        pos[1] = BOUNDARY_BOTTOM - PADDLE_RADIUS
        vel[1] = -vel[1]  # Reverse y-velocity to simulate a bounce


def handle_paddle_collision(paddle_pos, paddle_vel, puck_pos, puck_vel, radius):
    dx = puck_pos[0] - paddle_pos[0]
    dy = puck_pos[1] - paddle_pos[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance < radius + PUCK_RADIUS:
        # Calculate collision angle
        angle = math.atan2(dy, dx)

        # Correct overlap by moving the puck fully outside the paddle
        overlap = radius + PUCK_RADIUS - distance
        puck_pos[0] += overlap * math.cos(angle)
        puck_pos[1] += overlap * math.sin(angle)

        # Calculate the relative velocity between paddle and puck along the collision angle
        relative_velocity_x = puck_vel[0] - paddle_vel[0]
        relative_velocity_y = puck_vel[1] - paddle_vel[1]

        # Calculate velocity component along the collision angle
        collision_velocity = (relative_velocity_x * math.cos(angle) +
                              relative_velocity_y * math.sin(angle))

        # Only proceed if they are moving towards each other
        if collision_velocity < 0:
            # Reflect the velocity along the collision angle to create a bounce effect
            puck_vel[0] -= 2 * collision_velocity * math.cos(angle)
            puck_vel[1] -= 2 * collision_velocity * math.sin(angle)



def handle_player_collision(pos1, vel1, pos2, vel2, radius):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Check for collision
    if distance < 2 * radius:
        # Calculate the angle of collision
        angle = math.atan2(dy, dx)
        
        # Separate the paddles to prevent overlap
        overlap = 2 * radius - distance
        pos1[0] -= overlap * math.cos(angle) / 2
        pos1[1] -= overlap * math.sin(angle) / 2
        pos2[0] += overlap * math.cos(angle) / 2
        pos2[1] += overlap * math.sin(angle) / 2

        # Swap velocities along the collision angle
        vel1[0], vel2[0] = vel2[0] * math.cos(angle), vel1[0] * math.cos(angle)
        vel1[1], vel2[1] = vel2[1] * math.sin(angle), vel1[1] * math.sin(angle)


def handle_goal_post_collision(pos, vel, radius):
    # Left goal post collision
    if pos[0] - radius < GOAL_LEFT_X + GOAL_WIDTH and GOAL_Y < pos[1] < GOAL_Y + GOAL_HEIGHT:
        pos[0] = GOAL_LEFT_X + GOAL_WIDTH + radius  # Push out of the goal area
        vel[0] = -vel[0]  # Reverse x-velocity to simulate bounce

    # Right goal post collision
    elif pos[0] + radius > GOAL_RIGHT_X and GOAL_Y < pos[1] < GOAL_Y + GOAL_HEIGHT:
        pos[0] = GOAL_RIGHT_X - radius  # Push out of the goal area
        vel[0] = -vel[0]  # Reverse x-velocity to simulate bounce


# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Draw boundary box
    pygame.draw.rect(screen, WHITE, (BOUNDARY_LEFT, BOUNDARY_TOP, WIDTH - 2 * BOUNDARY_MARGIN, HEIGHT - 2 * BOUNDARY_MARGIN), 2)

    # Draw goal areas
    pygame.draw.rect(screen, RED, (GOAL_LEFT_X, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT))
    pygame.draw.rect(screen, BLUE, (GOAL_RIGHT_X, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for i in range(3):
            apply_drag(i, team1_positions[i], event)
            apply_drag(i + 3, team2_positions[i], event)

    # Update puck position with friction
    update_position_with_bounds(puck_pos, puck_vel, PUCK_FRICTION)

    # Update each player's position with friction and keep within bounds
    for i in range(3):
        update_position_with_bounds(team1_positions[i], team1_velocities[i], PADDLE_FRICTION)
        update_position_with_bounds(team2_positions[i], team2_velocities[i], PADDLE_FRICTION)
        # Check goal post collision for each player
        handle_goal_post_collision(team1_positions[i], team1_velocities[i], PADDLE_RADIUS)
        handle_goal_post_collision(team2_positions[i], team2_velocities[i], PADDLE_RADIUS)

    # Wall collision for puck (top and bottom)
    if puck_pos[1] <= PUCK_RADIUS or puck_pos[1] >= HEIGHT - PUCK_RADIUS:
        puck_vel[1] = -puck_vel[1]

    # Goal detection
    if puck_pos[0] <= BOUNDARY_LEFT and GOAL_Y < puck_pos[1] < GOAL_Y + GOAL_HEIGHT:
        team2_score += 1
        reset_puck()
    elif puck_pos[0] >= BOUNDARY_RIGHT - PUCK_RADIUS and GOAL_Y < puck_pos[1] < GOAL_Y + GOAL_HEIGHT:
        team1_score += 1
        reset_puck()

    # Handle puck collisions with all paddles
    for i in range(3):
        handle_paddle_collision(team1_positions[i], team1_velocities[i], puck_pos, puck_vel, PADDLE_RADIUS)
        handle_paddle_collision(team2_positions[i], team2_velocities[i], puck_pos, puck_vel, PADDLE_RADIUS)

    # Player-to-player collisions within each team
    for i in range(3):
        for j in range(i + 1, 3):
            handle_player_collision(team1_positions[i], team1_velocities[i], team1_positions[j], team1_velocities[j], PADDLE_RADIUS)
            handle_player_collision(team2_positions[i], team2_velocities[i], team2_positions[j], team2_velocities[j], PADDLE_RADIUS)

    # Player-to-player collisions between teams
    for i in range(3):
        for j in range(3):
            handle_player_collision(team1_positions[i], team1_velocities[i], team2_positions[j], team2_velocities[j], PADDLE_RADIUS)


    # Draw paddles, puck, and center line
    for pos in team1_positions:
        pygame.draw.circle(screen, BLUE, (int(pos[0]), int(pos[1])), PADDLE_RADIUS)
    for pos in team2_positions:
        pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), PADDLE_RADIUS)
    pygame.draw.circle(screen, WHITE, (int(puck_pos[0]), int(puck_pos[1])), PUCK_RADIUS)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores
    team1_text = font.render(str(team1_score), True, WHITE)
    team2_text = font.render(str(team2_score), True, WHITE)
    screen.blit(team1_text, (WIDTH // 4, 20))
    screen.blit(team2_text, (3 * WIDTH // 4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
