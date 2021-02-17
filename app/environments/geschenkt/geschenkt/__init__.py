from gym.envs.registration import register

register(
    id='Geschenkt-v0',
    entry_point='geschenkt.envs:GeschenktEnv',
)

