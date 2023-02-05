
import gym
import numpy as np
import requests

from stable_baselines import logger


BASE_URL = 'http://localhost:8765'


class RemoteEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False, manual=False):
        super(RemoteEnv, self).__init__()
        self.name = 'remote'
        self.manual = manual
        self.newgame()

        self.action_space = gym.spaces.Discrete(self.action_space_size)
        self.observation_space = gym.spaces.Box(-1, 1, (self.observation_space_size + self.action_space_size,))
        self.verbose = verbose

    @property
    def observation(self):
        return self.current_observation

    @property
    def legal_actions(self):
        return self.current_legal_actions

    def step(self, action):
        response = self.remote_call('step', data={"action": int(action)})
        self.current_player_num = response['next_player']
        self.current_observation = self.get_observation_from_payload(response)
        self.current_legal_actions = np.array(response['legal_actions'])
        return self.observation, response['reward'], response['done'], {}

    def reset(self):
        self.newgame()
        return self.observation

    def render(self, mode='human', close=False):
        # skipping extra network calls for now - uncomment to debug
        # self.remote_call('render')
        pass

    def remote_call(self, endpoint, data=None):
        url = f'{BASE_URL}/{endpoint}/{self.remote_id}'
        if data is None:
            return requests.get(url).json()
        else:
            return requests.post(url, json=data).json()

    def newgame(self):
        response = requests.get(f'{BASE_URL}/newgame').json()
        self.remote_id = response['id']
        self.action_space_size = response['action_space_size']
        self.observation_space_size = response['observation_space_size']
        self.n_players = response['player_count']
        self.current_player_num = response['current_player']
        self.current_observation = self.get_observation_from_payload(response)
        self.current_legal_actions= np.array(response['legal_actions'])

    def get_observation_from_payload(self, response):
        o = response['observation']
        if len(o) != self.observation_space_size + self.action_space_size:
            o += response['legal_actions']
        assert len(o) == self.observation_space_size + self.action_space_size, 'Observation length must be the same as observation_space_size + action_space_size'
        return np.array(o)

    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Sushi Go!')
