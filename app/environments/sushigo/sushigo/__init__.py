from gym.envs.registration import register

register(
    id='SushiGo-v0',
    entry_point='sushigo.envs:SushiGoEnv',
)

