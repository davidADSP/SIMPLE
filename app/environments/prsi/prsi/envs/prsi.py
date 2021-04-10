
import gym
import numpy as np
import config
from stable_baselines import logger
from .classes import Player, Deck


class PrsiEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False, manual=False):
        super(PrsiEnv, self).__init__()
        self.name = 'prsi'
        self.manual = manual

        self.n_players = 2
        self.cards_per_player = 5

        self.n_rounds = 3

        self.total_positions = self.n_players * 2 + 2

        self.total_cards = 32
        self.action_space = gym.spaces.Discrete(33)

        self.observation_space = gym.spaces.Box(
            0, 1, (97,))
        self.verbose = verbose

    @property
    def observation(self):
        obs = np.zeros(([97, ]))
        # player_num = self.current_player_num

        # for i in range(self.n_players):
        #     player = self.players[player_num]

        #     if self.turns_taken >= hands_seen:
        #         for card in player.hand.cards:
        #             obs[i*2][card.id] = 1

        #     for card in player.position.cards:
        #         obs[i*2+1][card.id] = 1

        #     player_num = (player_num + 1) % self.n_players
        #     hands_seen += 1

        # if self.turns_taken >= self.n_players - 1:
        #     for card in self.deck.cards:
        #         obs[6][card.id] = 1

        # for card in self.discard.cards:
        #     obs[7][card.id] = 1

        # ret = obs.flatten()
        # for p in self.players:  #  TODO this should be from reference point of the current_player
        #     ret = np.append(ret, p.score / self.max_score)
        ret = obs.flatten()
       # ret = np.append(ret, self.legal_actions)

        return ret

    @property
    def legal_actions(self):
        legal_actions = np.zeros(self.action_space.n)
        hand = self.current_player.hand.cards

        # pop action
        legal_actions[0] = 1

        for card in hand:
            if card.suit == self.tableCard.suit or card.name == self.tableCard.name:
                legal_actions[card.id] = 1
        return legal_actions

    def score_game(self):
        reward = [0.0] * self.n_players
        scores = [p.score for p in self.players]
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

    def get_limits(self, counts, type):
        counts = np.array(counts, dtype=np.float)
        if type == 'max':
            type_counts = np.nanmax(counts)
        else:
            type_counts = np.nanmin(counts)

        counts_winners = []

        for i, m in enumerate(counts):
            if m == type_counts:
                counts_winners.append(i)

        return counts_winners

    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def convert_action(self, action):
        if action < self.card_types:
            return False, action, None
        else:
            action = action - self.card_types
            first_card = action // self.card_types
            second_card = action % self.card_types
            return True, first_card, second_card

    def step(self, action):

        reward = [0] * self.n_players
        done = False

        # check move legality
        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1
            done = True

        # play the card(s)
        else:
            # pop card from deck
            if action == 0:
                self.current_player.hand.add(self.deck.pop())
            else:
                self.deck.cards.append(self.tableCard)
                self.tableCard = self.current_player.hand.pick(action)

        if len(self.current_player.hand.cards) == 0:
            reward[self.current_player_num] = 1
            done = True
        self.done = done
        self.round += 1

        return self.observation, reward, done, {}

    def reset_round(self):
        self.round += 1
        self.turns_taken = 0

    def reset(self):
        self.round = 0
        self.deck = Deck()
        self.players = []
        self.action_bank = []

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1

        for player in self.players:
            player.hand.add(self.deck.pop(5))

        self.current_player_num = 0
        self.done = False
        self.tableCard = self.deck.pop()[0]
        self.reset_round()
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def render(self, mode='human', close=False):

        if close:
            return

            logger.debug(
                f'\n\n-------ROUND {self.round}-----------')
            logger.debug(
                f"It is Player {self.current_player.id}'s turn to choose")

        for p in self.players:
            logger.debug(f'\nPlayer {p.id}\'s hand')
            for card in p.hand.cards:
                logger.debug(card.id, card.name, card.suit)

        logger.debug(
            f'\nTable card {self.tableCard.name} {self.tableCard.suit}')

        logger.debug(f'\n{self.deck.size()} cards left in deck')

        if self.verbose:
            logger.debug(
                f'\nObservation: \n{[i if o == 1 else (i,o) for i,o in enumerate(self.observation) if o != 0]}')

        if not self.done:
            logger.debug(
                f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')

        if self.done:
            logger.debug(f'\n\nGAME OVER')

        if self.turns_taken == self.cards_per_player:
            for p in self.players:
                logger.debug(f'Player {p.id} points: {p.score}')

    def rules_move(self):
        raise Exception(
            'Rules based agent is not yet implemented for Sushi Go!')
