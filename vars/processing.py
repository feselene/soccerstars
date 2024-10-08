import numpy as np

def move(ball_position, player_positions, score):
    """
    Determines the best move based on ball position, player positions, and score.
    
    Parameters:
    ball_position (tuple): (x, y) coordinates of the ball.
    player_positions (list of tuples): List of (x, y) coordinates for each player.
    score (tuple): (team_score, opponent_score).
    
    Returns:
    list of tuples: List of (x_move, y_move) indicating the direction for each player to move.
    """
    moves = []
    team_score, opponent_score = score
    ball_x, ball_y = ball_position

    for player_x, player_y in player_positions:
        # Calculate vector to the ball
        vector_to_ball = (ball_x - player_x, ball_y - player_y)
        distance_to_ball = np.hypot(vector_to_ball[0], vector_to_ball[1])

        # Normalize movement vector to get the direction
        if distance_to_ball > 0:
            normalized_vector = (vector_to_ball[0] / distance_to_ball, vector_to_ball[1] / distance_to_ball)
        else:
            normalized_vector = (0, 0)

        # Movement strategy based on score
        if team_score <= opponent_score:
            # Offensive strategy: move towards the ball
            move_x = normalized_vector[0]
            move_y = normalized_vector[1]
        else:
            # Defensive strategy: stay between ball and goal (assuming goal at y=0 or another position)
            goal_position = (player_x, 0)  # Example goal position; adjust as needed
            vector_to_goal = (goal_position[0] - player_x, goal_position[1] - player_y)
            normalized_vector_goal = (vector_to_goal[0] / distance_to_ball, vector_to_goal[1] / distance_to_ball)

            # Combine ball and goal directions for balanced defense
            move_x = 0.5 * normalized_vector[0] + 0.5 * normalized_vector_goal[0]
            move_y = 0.5 * normalized_vector[1] + 0.5 * normalized_vector_goal[1]

        # Append the calculated move for the player
        moves.append((move_x, move_y))

    return moves

# Example usage
ball_position = (300, 200)
player_positions = [(100, 100), (120, 140), (150, 170), (180, 200), (220, 240)]
score = (2, 2)  # Tied game example

player_moves = move(ball_position, player_positions, score)
print("Player Moves:", player_moves)
