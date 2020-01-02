import os
import sys
sys.path.append('./')

from env.MouseWalkingMaze.base_env import BaseEnv
from examples.MouseWalkingMaze.map1.custom_policy import CustomCnnLnLstmPolicy
from stable_baselines import PPO2
from stable_baselines.common.vec_env import  DummyVecEnv
from stable_baselines.common.policies import MlpLnLstmPolicy

tensorboard_folder = './tensorboard/base/'
if not os.path.isdir(tensorboard_folder):
    os.makedirs(tensorboard_folder)

env = DummyVecEnv([lambda: BaseEnv(map_name='map1')])

model = PPO2(CustomCnnLnLstmPolicy, env, verbose=0, nminibatches=1, tensorboard_log=tensorboard_folder)
model.learn(total_timesteps=2500000)

model.save("mouse_base")
del model
model = PPO2.load("mouse_base")

done = False
states = None
obs = env.reset()

while not done:
    action, states = model.predict(obs, states)
    obs, _, done, info = env.step(action)
    env.render()