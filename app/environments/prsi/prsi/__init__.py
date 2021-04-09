from gym.envs.registration import register

register(
    id='prsi-v0',
    entry_point='prsi.envs:PrsiEnv',
)
