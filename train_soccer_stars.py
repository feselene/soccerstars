import gym
from stable_baselines3 import PPO
from env.soccer_stars_env import SoccerStarsEnv

# Initialize the environment
env = SoccerStarsEnv()

# Train the agent using PPO
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)  # Train for 100k timesteps

# Save the model
model.save("soccer_stars_ppo")

from stable_baselines3 import PPO

env = SoccerStarsEnv()
model = PPO.load("soccer_stars_ppo", env=env)

for episode in range(5):
    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        env.render()  # Visualize each step
