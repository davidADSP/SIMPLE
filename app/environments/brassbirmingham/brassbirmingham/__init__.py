from gym.envs.registration import register

register(
    id='BrassBirmingham-v0',
    entry_point='brassbirmingham.envs:BrassBirminghamEnv',
)

