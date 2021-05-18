from gym.envs.registration import register

register(
    id='FlammeRouge-v0',
    entry_point='frouge.envs:FlammeRougeEnv',
)

