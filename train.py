import os
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from env.air_hockey_env import AirHockeyEnv  # Import your custom environment

# Constants
LOG_DIR = "./logs/"
MODELS_DIR = "./models/"
TOTAL_TIMESTEPS = 100000  # Number of timesteps to train
EVAL_FREQ = 10000         # Evaluate every N timesteps
SAVE_FREQ = 20000         # Save model checkpoint every N timesteps

def train():
    # Create directories for logs and models if they don't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Initialize the environment
    env = AirHockeyEnv()

    # Initialize the PPO agent
    model = PPO(
        policy="MlpPolicy",         # Use a Multi-Layer Perceptron policy
        env=env,                    # Pass the custom environment
        verbose=1,                  # Print training progress
        tensorboard_log=LOG_DIR     # Log data for TensorBoard
    )

    # Callbacks for evaluation and saving
    eval_env = AirHockeyEnv()  # Separate environment for evaluation
    eval_callback = EvalCallback(
        eval_env,                      # Evaluation environment
        best_model_save_path=MODELS_DIR,  # Path to save the best model
        log_path=LOG_DIR,              # Log evaluation results
        eval_freq=EVAL_FREQ,           # Frequency of evaluation
        deterministic=True,            # Use deterministic actions during evaluation
        render=False                   # Do not render during evaluation
    )
    checkpoint_callback = CheckpointCallback(
        save_freq=SAVE_FREQ, save_path=MODELS_DIR, name_prefix="ppo_air_hockey"
    )

    # Train the model
    print("Training started...")
    model.learn(
        total_timesteps=TOTAL_TIMESTEPS,
        callback=[eval_callback, checkpoint_callback]
    )
    print("Training complete!")

    # Save the final model
    model.save(os.path.join(MODELS_DIR, "ppo_air_hockey_final"))

if __name__ == "__main__":
    train()
