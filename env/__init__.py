import gym
from air_hockey_env import AirHockeyEnv

env = AirHockeyEnv()
obs = env.reset()

for _ in range(100):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()
