import gym
import numpy as np

box = gym.spaces.Box(0, 1, shape=(32, 40),)

print(box[3])
