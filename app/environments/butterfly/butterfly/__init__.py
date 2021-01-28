from gym.envs.registration import register

register(
    id='Butterfly-v0',
    entry_point='butterfly.envs:ButterflyEnv',
)

