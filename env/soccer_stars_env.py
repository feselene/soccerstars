import gym
from gym import spaces
import numpy as np
import math
import pygame

class SoccerStarsEnv(gym.Env):
    def __init__(self):
        super(SoccerStarsEnv, self).__init__()
        
        # Environment constants
        self.WIDTH = 800
        self.HEIGHT = 400
        self.PLAYER_RADIUS = 20
        self.BALL_RADIUS = 15

        self.observation_space = spaces.Box(
            low=0,
            high=max(self.WIDTH, self.HEIGHT),
            shape=(12,),  # 2 players x (x, y, vx, vy) + ball (x, y, vx, vy)
            dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=np.array([0, 0]),  # Angle (0-360 degrees) and Power (0-1)
            high=np.array([360, 1]),
            dtype=np.float32
        )

        self.reset()

    def reset(self):
        # Randomize positions for the two players and the ball
        self.player1_pos = [100, self.HEIGHT // 2]
        self.player2_pos = [self.WIDTH - 100, self.HEIGHT // 2]
        self.ball_pos = [self.WIDTH // 2, self.HEIGHT // 2]

        self.player1_vel = [0, 0]
        self.player2_vel = [0, 0]
        self.ball_vel = [0, 0]

        return self._get_obs()

    def step(self, action):
        """ Takes an action for player 1 and updates the environment. """
        
        # Unpack action (angle, force)
        angle, force = action
        angle_rad = np.radians(angle)

         # Apply force to player 1's velocity
        self.player1_vel[0] = force * np.cos(angle_rad) * 5  # 5 = max speed multiplier
        self.player1_vel[1] = force * np.sin(angle_rad) * 5

        # Update player positions and ball position
        self._update_position(self.player1_pos, self.player1_vel)
        self._update_position(self.player2_pos, self.player2_vel)
        self._update_position(self.ball_pos, self.ball_vel)

        # Handle collisions
        self._handle_collision(self.player1_pos, self.ball_pos)
        self._handle_collision(self.player2_pos, self.ball_pos)
        
        reward, done = self._check_goal()

        return self._get_obs(), reward, done, {}
    
    def _update_position(self, pos, vel):
        pos[0] += vel[0]
        pos[1] += vel[1]
        vel[0] *= 0.98  # Friction
        vel[1] *= 0.98  # Friction
        
        # Keep positions inside boundaries
        pos[0] = np.clip(pos[0], self.PLAYER_RADIUS, self.WIDTH - self.PLAYER_RADIUS)
        pos[1] = np.clip(pos[1], self.PLAYER_RADIUS, self.HEIGHT - self.PLAYER_RADIUS)

    def _handle_collision(self, pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < self.PLAYER_RADIUS + self.BALL_RADIUS:
            # Simple elastic collision (reverse velocity)
            pos1[0] += dx * 0.1
            pos1[1] += dy * 0.1

    def _check_goal(self):
        if self.ball_pos[0] < 10:  # Player 2 scores
            return -1, True
        elif self.ball_pos[0] > self.WIDTH - 10:  # Player 1 scores
            return 1, True
        return 0, False
    
    def _get_obs(self):
        return np.array(
            self.player1_pos + self.player1_vel +
            self.player2_pos + self.player2_vel +
            self.ball_pos + self.ball_vel
        )

    def render(self, mode='human'):
        if not hasattr(self, 'screen'):  # Only initialize Pygame if it's not already initialized
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption('Soccer Stars AI')

        # Fill the background with black
        self.screen.fill((0, 0, 0))  # Black background

        # Draw goals (left and right goal zones)
        pygame.draw.rect(self.screen, (255, 0, 0), (0, self.HEIGHT // 2 - 50, 10, 100))  # Left goal
        pygame.draw.rect(self.screen, (0, 0, 255), (self.WIDTH - 10, self.HEIGHT // 2 - 50, 10, 100))  # Right goal

        # Draw the players as circles
        pygame.draw.circle(self.screen, (0, 0, 255), (int(self.player1_pos[0]), int(self.player1_pos[1])), self.PLAYER_RADIUS)
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.player2_pos[0]), int(self.player2_pos[1])), self.PLAYER_RADIUS)

        # Draw the ball as a white circle
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.ball_pos[0]), int(self.ball_pos[1])), self.BALL_RADIUS)

        # Update the display
        pygame.display.flip()
