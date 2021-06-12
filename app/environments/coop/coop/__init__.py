from gym.envs.registration import register

register(
    id='Coop-v0',
    entry_point='coop.envs:CoopEnv',
)

