import os
import numpy as np
import random

from utils.files import load_model, load_all_models, get_best_model_name
from utils.agents import Agent

import config

from stable_baselines import logger

def selfplay_wrapper(env):
    class SelfPlayEnv(env):
        # wrapper over the normal single player env, but loads the best self play model
        def __init__(self, opponent_type, verbose):
            super(SelfPlayEnv, self).__init__(verbose)
            self.opponent_type = opponent_type
            self.opponent_models = load_all_models(self)
            self.best_model_name = get_best_model_name(self.name)

        def setup_opponents(self):
            if self.opponent_type == 'rules':
                self.opponent_agent = Agent('rules')
            else:
                # incremental load of new model
                best_model_name = get_best_model_name(self.name)
                if self.best_model_name != best_model_name:
                    self.opponent_models.append(load_model(self, best_model_name ))
                    self.best_model_name = best_model_name

                if self.opponent_type == 'random':
                    start = 0
                    end = len(self.opponent_models) - 1
                    i = random.randint(start, end)
                    self.opponent_agent = Agent('ppo_opponent', self.opponent_models[i]) 

                elif self.opponent_type == 'best':
                    self.opponent_agent = Agent('ppo_opponent', self.opponent_models[-1])  

                elif self.opponent_type == 'mostly_best':
                    j = random.uniform(0,1)
                    if j < 0.8:
                        self.opponent_agent = Agent('ppo_opponent', self.opponent_models[-1])  
                    else:
                        start = 0
                        end = len(self.opponent_models) - 1
                        i = random.randint(start, end)
                        self.opponent_agent = Agent('ppo_opponent', self.opponent_models[i])  

                elif self.opponent_type == 'base':
                    self.opponent_agent = Agent('base', self.opponent_models[0])  

            self.agent_player_num = np.random.choice(self.n_players)
            self.agents = [self.opponent_agent] * self.n_players
            self.agents[self.agent_player_num] = None
            try:
                #if self.players is defined on the base environment
                logger.debug(f'Agent plays as Player {self.players[self.agent_player_num].id}')
            except:
                pass


        def reset(self):
            super(SelfPlayEnv, self).reset()
            self.setup_opponents()

            if self.current_player_num != self.agent_player_num:   
                self.continue_game()

            return self.observation

        @property
        def current_agent(self):
            return self.agents[self.current_player_num]

        def continue_game(self):
            observation = None
            reward = None
            done = None

            while self.current_player_num != self.agent_player_num:
                self.render()
                action = self.current_agent.choose_action(self, choose_best_action = False, mask_invalid_actions = False)
                observation, reward, done, _ = super(SelfPlayEnv, self).step(action)
                logger.debug(f'Rewards: {reward}')
                logger.debug(f'Done: {done}')
                if done:
                    break

            return observation, reward, done, None


        def step(self, action):
            self.render()
            observation, reward, done, _ = super(SelfPlayEnv, self).step(action)
            logger.debug(f'Action played by agent: {action}')
            logger.debug(f'Rewards: {reward}')
            logger.debug(f'Done: {done}')

            if not done:
                package = self.continue_game()
                if package[0] is not None:
                    observation, reward, done, _ = package


            agent_reward = reward[self.agent_player_num]
            logger.debug(f'\nReward To Agent: {agent_reward}')

            if done:
                self.render()

            return observation, agent_reward, done, {} 

    return SelfPlayEnv