from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym
import numpy as np

from train_data import load_training_data

class LogReplayEnv(gym.Env):
    def __init__(self, states, rewards):
        super().__init__()
        self.states = states
        self.rewards = rewards
        self.i = 0

        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(
            low=0.0, high=1.0, shape=(4,), dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        self.i = 0
        return np.array(self.states[self.i]), {}

    def step(self, action):
        reward = self.rewards[self.i]
        self.i += 1

        terminated = self.i >= len(self.states)
        truncated = False

        obs = np.array(self.states[self.i - 1])
        return obs, reward, terminated, truncated, {}

# Load logged data
states, _, rewards = load_training_data()

env = DummyVecEnv([
    lambda: LogReplayEnv(states, rewards)
])
if not states or not rewards:
    raise RuntimeError(
        "No PPO training data found. "
        "Run executions that log router='ppo_reward' before training."
    )
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=5000)
model.save("ppo_router")

print("✅ PPO model trained and saved")
