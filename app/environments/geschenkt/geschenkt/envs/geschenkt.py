
import gym
import numpy as np

import config

from stable_baselines import logger

from .classes import *

class GeschenktEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False, n_players = 3):
        super(GeschenktEnv, self).__init__()
        self.name = 'geschenkt'
        self.n_players = n_players
        self.counters_per_player = 11
        self.manual = manual

        if self.manual:
            self.cards_to_discard = 0
            self.deck_size_at_end = 9
        else:
            self.cards_to_discard = 9
            self.deck_size_at_end = 0
        
            
        
        
        self.max_score = 300
        self.max_counters = 55
        
        self.total_positions = self.n_players + 1 #each position plus the centre

        self.contents = []
        for value in range(3, 36):
            self.contents.append({'card': Card, 'info': {'value': value}, 'count': 1})

        self.total_cards = sum([x['count'] for x in self.contents])

        self.action_space = gym.spaces.Discrete(1 + 35)
        self.observation_space = gym.spaces.Box(-1, 1, (
            self.total_cards * self.total_positions # cards
            + self.total_positions # counters
            + self.n_players #scores
            + self.action_space.n  #legal_actions
            , )
        )  
        self.verbose = verbose

        
    @property
    def observation(self):
        # Cards
        obs = np.zeros(([self.total_positions, self.total_cards]))
        player_num = self.current_player_num

        for i in range(self.n_players):
            player = self.players[player_num]

            for card in player.position.cards:
                obs[i][card.id] = 1

            player_num = (player_num + 1) % self.n_players

        if self.centre_card.size() > 0:
            obs[-1][self.centre_card.cards[0].id] = 1

        ret = obs.flatten()

        # Counters

        counter_obs = np.zeros((self.n_players + 1, ))

        player_num = self.current_player_num
        for i in range(self.n_players):
            player = self.players[player_num]
            counter_obs[i] = player.counters.size() / self.max_counters
            player_num = (player_num + 1) % self.n_players

        counter_obs[-1] = self.centre_counters.size() / self.max_counters

        ret = np.append(ret, counter_obs)

        # Score
        score_obs = np.zeros((self.n_players, ))

        player_num = self.current_player_num
        for i in range(self.n_players):
            player = self.players[player_num]
            score_obs[i] = player.score / self.max_score
            player_num = (player_num + 1) % self.n_players

        ret = np.append(ret, score_obs)

        ret = np.append(ret, self.legal_actions)

        return ret

    @property
    def legal_actions(self):
        legal_actions = np.zeros(self.action_space.n)
        if self.current_player.counters.size() > 0:
            legal_actions[0] = 1
        if self.centre_card.size() > 0:
            legal_actions[self.centre_card.cards[0].value] = 1

        return legal_actions



    def score_game(self):
        reward = [0.0] * self.n_players
        scores = [p.score for p in self.players]
        min_score = min(scores)
        winners = []

        for i, s in enumerate(scores):
            if s == min_score:
                winners.append(i)

        for w in winners:
            reward[w] += 1.0 / len(winners)

        return reward


    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def step(self, action):
        
        reward = [0] * self.n_players
        done = False
        draw_card = False

        # check move legality
        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1
            done = True

        #play the card(s)
        else:
            if action == 0:
                logger.debug(f'\nPlayer chooses to play a counter')
                self.current_player.counters.remove(1)
                self.centre_counters.add(1)
                self.current_player_num = (self.current_player_num + 1) % self.n_players

            else:
                logger.debug(f'Player chooses to take card {self.centre_card.cards[0].symbol} and {self.centre_counters.size()} counters')
                self.current_player.position.add(self.centre_card.cards)
                self.current_player.counters.add(self.centre_counters.size())
                self.centre_card.reset()
                self.centre_counters.reset()

                if self.deck.size() == self.deck_size_at_end:
                    reward = self.score_game()
                    done = True
                else:
                    if self.manual:
                        next_card = input('What card is drawn?: ')
                        self.centre_card.add(self.deck.pick(next_card))
                    else:
                        self.centre_card.add(self.deck.draw(1))
                
            self.turns_taken += 1

        self.done = done

        return self.observation, reward, done, {}



    def reset(self):
        self.deck = Deck(self.contents)
        self.discard = Discard()
        self.discard.add(self.deck.draw(self.cards_to_discard))

        self.centre_card = Position()
        if self.manual:
            next_card = input('What card is drawn?: ')
            self.centre_card.add(self.deck.pick(next_card))
        else:
            self.centre_card.add(self.deck.draw(1))
        
        self.centre_counters = Counters()

        self.players = []

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1

        for p in self.players:
            p.position = Position()
            p.counters.add(self.counters_per_player)

        self.turns_taken = 0
        self.current_player_num = 0
        self.done = False

        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation


    def render(self, mode='human', close=False):
        
        if close:
            return

        if not self.done:
            logger.debug(f'\n\n-------TURN {self.turns_taken + 1}-----------')
            logger.debug(f"It is Player {self.current_player.id}'s turn to choose")
        else:
            logger.debug(f'\n\n-------FINAL POSITION-----------')
            

        for p in self.players:
            logger.debug(f'\nPlayer {p.id}: {p.counters.size()} counters')
            logger.debug([x.symbol for x in sorted(p.position.cards, key=lambda x: x.id)])

        if self.centre_card.size() > 0:
            logger.debug(f'\n{self.centre_card.cards[0].symbol} in the centre')
        else:
            logger.debug(f'No card in the centre')

        logger.debug(f'{self.centre_counters.size()} counters in the centre')

        logger.debug(f'\n{self.deck.size()} cards left in deck')
        logger.debug(f'{self.discard.size()} cards discarded')

        if self.verbose:
            logger.debug(f'\nObservation: \n{[i if o == 1 else (i,o) for i,o in enumerate(self.observation) if o != 0]}')
        
        if not self.done:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')

        if self.done:
            logger.debug(f'\n\nGAME OVER')
            for p in self.players:
                logger.debug(f'Player {p.id} points: {p.score}')


    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Geschenkt!')
