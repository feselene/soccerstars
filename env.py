import gym
from gym import spaces
import numpy as np

class AirHockeyEnv(gym.Env):
    def __init__(self):
        super(AirHockeyEnv, self).__init__()
        self.WIDTH, self.HEIGHT = 800, 400
        self.action_space = spaces.MultiDiscrete([3, 3, 3])  # Up, Down, Stay for 3 paddles
        self.observation_space = spaces.Box(
            low=0, high=800,
            shape=(6 + 2 + 2,),  # 6 paddle positions, 2 puck position, 2 puck velocities
            dtype=np.float32
        )
        self.reset()

    def reset(self):
        # Reset positions and velocities
        self.team2_positions = [[700, 100], [700, 200], [700, 300]]
        self.team2_velocities = [[0, 0] for _ in range(3)]
        self.puck_pos = [400, 200]
        self.puck_vel = [0, 0]
        self.score = [0, 0]
        return self._get_obs()

    def step(self, action):
        # Apply actions
        for i in range(3):
            if action[i] == 0:  # Up
                self.team2_velocities[i][1] = -3
            elif action[i] == 1:  # Down
                self.team2_velocities[i][1] = 3
            else:  # Stay
                self.team2_velocities[i][1] = 0

        # Update positions (apply friction and bounds)
        for i in range(3):
            update_position_with_bounds(self.team2_positions[i], self.team2_velocities[i], PADDLE_FRICTION)
        update_position_with_bounds(self.puck_pos, self.puck_vel, PUCK_FRICTION)

        # Check for collisions and scoring
        for i in range(3):
            handle_paddle_collision(self.team2_positions[i], self.team2_velocities[i], self.puck_pos, self.puck_vel, PADDLE_RADIUS)

        if self.puck_pos[0] >= self.WIDTH - PUCK_RADIUS:
            self.score[0] += 1  # Opponent scored
            reward = -1
            done = True
        elif self.puck_pos[0] <= PUCK_RADIUS:
            self.score[1] += 1  # AI scored
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        # Return current state
        return np.array(self.team2_positions + [self.puck_pos, self.puck_vel])

    def render(self, mode='human'):
        pass  # Optional: Render with Pygame for visualization
