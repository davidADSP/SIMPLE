
import gym
import numpy as np

import config

from stable_baselines import logger

class Player():
    def __init__(self, id):
        self.id = id

class CoopEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(CoopEnv, self).__init__()
        self.name = 'coop'
        self.manual = manual
        
        self.n_players = 1
        self.n_chickens = 1
        self.max_turns_taken = 1

        self.n_eggs = 10
        self.n_env_inputs = 1
        self.n_ear_channels = 1
        
        self.action_space = gym.spaces.Box(0, 1, (1 + self.n_ear_channels, ))
        self.observation_space = gym.spaces.Box(0, 1, (self.n_env_inputs + self.n_ear_channels, ))
        self.verbose = verbose

        
    def observation(self):
        obs = np.zeros(self.observation_space.shape)
        if self.perspective >= 0:
            obs[0] = self.env_input[0]
        else:
            obs[0] = 0
        
        obs[1] = self.speech

        return obs



    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def check_action(self,action):
        egg_selection = int(action * self.n_eggs)
        logger.debug(f'Egg chosen: {egg_selection}')
        if egg_selection == self.egg:
            return True
        else:
            return False


    def step(self, action):
        
        reward = [0] * self.n_players
        done = False

        self.action_bank.append(action)

        if len(self.action_bank) == self.n_chickens:
            logger.debug(f'\nTaking actions')
            self.speech = 0
            for i, action in enumerate(self.action_bank):

                self.speech += action[1]
                if i == 0:
                    done = self.check_action(action[0])
                logger.debug(f'Entity {i} says: {action[1]}')

            self.speech /= 2
            self.speech += np.random.uniform(-1,1) * 0.01

            self.action_bank = []
        
        self.current_player_num = (self.current_player_num + 1) % self.n_players

        if self.perspective == self.n_chickens - 1:
            self.turns_taken += 1
        self.perspective = (self.perspective + 1) % self.n_chickens

        if done:
            reward = [1] * self.n_players
        else:
            reward = [0] * self.n_players


        if self.turns_taken == self.max_turns_taken:
            done = True
 

        self.done = done

        return self.observation(), reward, done, {}



    def setup_coop(self):
        egg = 8 #np.random.randint(self.n_eggs)
        env_input = [float(egg) / self.n_eggs ]
        return egg, env_input



    def reset(self):
        self.players = []
        self.action_bank = []
        self.turns_taken = 0
        self.perspective = 0
        self.speech = np.random.uniform(-1,1) * 0.01
        self.egg, self.env_input = self.setup_coop()

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1

        self.current_player_num = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        
        return self.observation()


    def render(self, mode='human', close=False):
        
        if close:
            return

        if self.done:
            logger.debug(f'\n\nGAME OVER')
            logger.debug(f'\n{self.turns_taken} turns taken')

        else:

            logger.debug(f'\n\n-------TURN {self.turns_taken + 1} : PERSPECTIVE {self.perspective}-----------')
            logger.debug(f'Egg to find: {self.egg}')
            logger.debug(f'Observation: {self.observation()}')

        
            



    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Coop!')
