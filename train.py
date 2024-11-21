from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Create the environment
env = make_vec_env(AirHockeyEnv, n_envs=1)

# Train the RL agent
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# Save the model
model.save("air_hockey_ai")
