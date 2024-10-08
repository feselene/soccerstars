import numpy as np
import math

def move(ball_position, player_position, score):
    """
    Generates the best move for a player towards the ball.
    
    Parameters:
    ball_position (tuple): (x, y) coordinates of the ball.
    player_position (tuple): (x, y) coordinates of the player.
    score (tuple): (team_score, opponent_score).
    
    Returns:
    tuple: (angle, length) where angle is in degrees and length is the distance to move.
    """
    ball_x, ball_y = ball_position
    player_x, player_y = player_position
    team_score, opponent_score = score

    # Calculate the vector from player to ball
    dx = ball_x - player_x
    dy = ball_y - player_y

    # Calculate the angle in degrees
    angle = math.degrees(math.atan2(dy, dx))

    # Calculate the length (distance) of the arrow
    length = math.sqrt(dx**2 + dy**2)

    # Adjust length based on the score
    if team_score <= opponent_score:
        # Offensive strategy: Use full length to move directly towards the ball
        move_length = length
    else:
        # Defensive strategy: Use half the length
        move_length = length / 2

    return angle, move_length

# Example usage
ball_position = (300, 200)
player_position = (100, 100)
score = (2, 2)  # Tied game example

angle, length = move(ball_position, player_position, score)
print(f"Move Angle: {angle} degrees")
print(f"Move Length: {length}")