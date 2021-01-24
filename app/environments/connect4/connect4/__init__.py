from gym.envs.registration import register

register(
    id='Connect4-v0',
    entry_point='connect4.envs:Connect4Env',
)


