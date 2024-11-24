import gym
from gym import spaces
import numpy as np
import math

# Constants
WIDTH, HEIGHT = 800, 400
PADDLE_RADIUS = 20
PUCK_RADIUS = 15
PUCK_FRICTION = 0.99
PADDLE_FRICTION = 0.95
BOUNDARY_MARGIN = 50
BOUNDARY_LEFT = BOUNDARY_MARGIN
BOUNDARY_RIGHT = WIDTH - BOUNDARY_MARGIN
BOUNDARY_TOP = BOUNDARY_MARGIN
BOUNDARY_BOTTOM = HEIGHT - BOUNDARY_MARGIN
GOAL_WIDTH = 10
GOAL_HEIGHT = 100
GOAL_LEFT_X = BOUNDARY_LEFT - GOAL_WIDTH
GOAL_RIGHT_X = BOUNDARY_RIGHT
GOAL_Y = HEIGHT // 2 - GOAL_HEIGHT // 2

class AirHockeyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(AirHockeyEnv, self).__init__()
        self.action_space = spaces.MultiDiscrete([3, 3, 3])  # Up, Down, Stay for 3 paddles
        self.observation_space = spaces.Box(
            low=0,
            high=max(WIDTH, HEIGHT),
            shape=(12,),  # 6 paddle positions (x, y for each), 2 puck position, 2 puck velocities
            dtype=np.float32,
        )

        # Initialize game state
        self.reset()

    def reset(self):
        self.team1_positions = [[100, HEIGHT // 4], [100, HEIGHT // 2], [100, 3 * HEIGHT // 4]]
        self.team2_positions = [[WIDTH - 100, HEIGHT // 4], [WIDTH - 100, HEIGHT // 2], [WIDTH - 100, 3 * HEIGHT // 4]]
        self.team1_velocities = [[0, 0] for _ in range(3)]
        self.team2_velocities = [[0, 0] for _ in range(3)]
        self.puck_pos = [WIDTH // 2, HEIGHT // 2]
        self.puck_vel = [0, 0]
        self.scores = [0, 0]
        self.done = False
        return self._get_obs()

    def step(self, action):
        # Apply actions to team2 (AI team)
        for i in range(3):
            if action[i] == 0:  # Up
                self.team2_velocities[i][1] = -3
            elif action[i] == 1:  # Down
                self.team2_velocities[i][1] = 3
            else:  # Stay
                self.team2_velocities[i][1] = 0

        # Update positions and velocities
        for i in range(3):
            self._update_position_with_bounds(self.team2_positions[i], self.team2_velocities[i], PADDLE_FRICTION)
            self._update_position_with_bounds(self.team1_positions[i], self.team1_velocities[i], PADDLE_FRICTION)

        self._update_position_with_bounds(self.puck_pos, self.puck_vel, PUCK_FRICTION)

        # Handle collisions
        for i in range(3):
            self._handle_paddle_collision(self.team1_positions[i], self.team1_velocities[i])
            self._handle_paddle_collision(self.team2_positions[i], self.team2_velocities[i])

        # Check for goals
        reward, self.done = self._check_goals()

        return self._get_obs(), reward, self.done, {}

    def render(self, mode='human'):
        print(f"Team 1: {self.scores[0]} | Team 2: {self.scores[1]}")

    def _get_obs(self):
        return np.array(
            self.team1_positions + self.team2_positions + [self.puck_pos] + [self.puck_vel]
        ).flatten()

    def _update_position_with_bounds(self, pos, vel, friction):
        pos[0] += vel[0]
        pos[1] += vel[1]
        vel[0] *= friction
        vel[1] *= friction

        # Constrain to boundaries
        pos[0] = np.clip(pos[0], BOUNDARY_LEFT + PADDLE_RADIUS, BOUNDARY_RIGHT - PADDLE_RADIUS)
        pos[1] = np.clip(pos[1], BOUNDARY_TOP + PADDLE_RADIUS, BOUNDARY_BOTTOM - PADDLE_RADIUS)

    def _handle_paddle_collision(self, paddle_pos, paddle_vel):
        dx = self.puck_pos[0] - paddle_pos[0]
        dy = self.puck_pos[1] - paddle_pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < PADDLE_RADIUS + PUCK_RADIUS:
            angle = math.atan2(dy, dx)
            overlap = PADDLE_RADIUS + PUCK_RADIUS - distance
            self.puck_pos[0] += overlap * math.cos(angle)
            self.puck_pos[1] += overlap * math.sin(angle)

            relative_velocity_x = self.puck_vel[0] - paddle_vel[0]
            relative_velocity_y = self.puck_vel[1] - paddle_vel[1]
            collision_velocity = (relative_velocity_x * math.cos(angle) +
                                  relative_velocity_y * math.sin(angle))

            if collision_velocity < 0:
                self.puck_vel[0] -= 2 * collision_velocity * math.cos(angle)
                self.puck_vel[1] -= 2 * collision_velocity * math.sin(angle)

    def _check_goals(self):
        if self.puck_pos[0] <= GOAL_LEFT_X:
            self.scores[1] += 1  # Team2 scores
            self._reset_puck()
            return -1, True
        elif self.puck_pos[0] >= GOAL_RIGHT_X:
            self.scores[0] += 1  # Team1 scores
            self._reset_puck()
            return 1, True
        return 0, False

    def _reset_puck(self):
        self.puck_pos = [WIDTH // 2, HEIGHT // 2]
        self.puck_vel = [0, 0]
