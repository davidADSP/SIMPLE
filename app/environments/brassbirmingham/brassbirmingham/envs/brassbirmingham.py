import random

import config
import gym
import numpy as np
from stable_baselines import logger

from .classes.board import Board


# TODO delete stuff and make stuff :)
class BrassBirminghamEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, verbose=False):
        super(BrassBirminghamEnv, self).__init__()
        self.name = "brassbirmingham"

        self.numPlayers = 2
        self.board = Board(self.numPlayers)
        self.action_space = gym.spaces.Discrete()
        self.observation_space = gym.spaces.Box()
        self.verbose = verbose

    @property
    def observation(self):
        raise Exception("observation is not yet implemented for BrassBirmingham!")

    @property
    def legal_actions(self):
        raise Exception("legal_actions is not yet implemented for BrassBirmingham!")

    def score_game(self):
        reward = [0.0] * self.numPlayers

        scores = [p.position.score for p in self.players]
        best_score = max(scores)
        worst_score = min(scores)
        winners = []
        losers = []
        for i, s in enumerate(scores):
            if s == best_score:
                winners.append(i)
            if s == worst_score:
                losers.append(i)

        for w in winners:
            reward[w] += 1.0 / len(winners)

        for l in losers:
            reward[l] -= 1.0 / len(losers)

        return reward

    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def rules_move(self):
        raise Exception("Rules based agent is not yet implemented for BrassBirmingham!")
