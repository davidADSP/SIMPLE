import argparse
import os
from collections import defaultdict
from random import choice

import numpy as np
import requests
import tensorflow as tf

from stable_baselines import logger


def get_move_from_nn(interpreter, input_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = np.array([input_data], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[2]['index'])
    output_by_move = [(score, move) for move, score in enumerate(output_data[0])]
    output_by_move.sort()
    return output_by_move[-1][1]


class RemoteGame:
    def __init__(self, base_url):
        self.base_url = base_url
        self.newgame()
        self.interpreter = tf.lite.Interpreter(model_path="best_model.tflite")
        self.interpreter.allocate_tensors()

    def play(self):
        done = False
        while done is False:
            moves = self.possible_moves()
            move = choice(moves)
            if self.current_player_num == 0:
                # use NN
                move = get_move_from_nn(self.interpreter, self.observation)
            _, reward, done, _ = self.step(move)
        try:
            return reward.index(1)
        except ValueError:
            # no winner
            return -1

    def possible_moves(self):
        return [i for i, x in enumerate(self.legal_actions) if x == 1]

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
        url = f'{self.base_url}/{endpoint}/{self.remote_id}'
        response = None
        try:
            if data is None:
                response = requests.get(url)
                return response.json()
            else:
                response = requests.post(url, json=data)
                return response.json()
        except:
            print(f'>>> Invalid response: {response.content}')
            raise

    def newgame(self):
        response = requests.get(f'{self.base_url}/newgame').json()
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
        raise Exception('Rules based agent is not yet implemented!')


if __name__ == "__main__":
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)

    parser.add_argument("--remote_base_url", "-rbu", type=str, default='http://localhost:5000'
            , help="Remote agent URL (see app/environments/remote/README.md)")

    args = parser.parse_args()
    winners = defaultdict(lambda: 0)
    for _ in range(10000):
        game = RemoteGame(args.remote_base_url)
        winner = game.play()
        winners[winner] += 1
        print(dict(winners))
    print(f'Final winners: {dict(winners)}')
