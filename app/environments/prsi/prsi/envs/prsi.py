
import gym
import numpy as np

import config

from stable_baselines import logger

from .classes import *


class PrsiEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False, manual=False):
        super(PrsiEnv, self).__init__()
        self.name = 'prsi'
        self.manual = manual

        # init Game
        self.game = Game()

        self.n_players = 2
        self.cards_per_player = 5

        self.n_rounds = 3

        self.total_positions = self.n_players * 2 + 2

        self.total_cards = 32
        self.action_space = gym.spaces.Discrete(33)

        self.observation_space = gym.spaces.Box(
            0, 1, (self.total_cards * self.n_players + self.action_space.n,))
        self.verbose = verbose

    @property
    def observation(self):
        obs = np.zeros(([self.total_positions, self.total_cards]))
        player_num = self.current_player_num

        for i in range(self.n_players):
            player = self.players[player_num]

            if self.turns_taken >= hands_seen:
                for card in player.hand.cards:
                    obs[i*2][card.id] = 1

            for card in player.position.cards:
                obs[i*2+1][card.id] = 1

            player_num = (player_num + 1) % self.n_players
            hands_seen += 1

        if self.turns_taken >= self.n_players - 1:
            for card in self.deck.cards:
                obs[6][card.id] = 1

        for card in self.discard.cards:
            obs[7][card.id] = 1

        ret = obs.flatten()
        for p in self.players:  #  TODO this should be from reference point of the current_player
            ret = np.append(ret, p.score / self.max_score)

        ret = np.append(ret, self.legal_actions)

        return ret

    @property
    def legal_actions(self):
        legal_actions = np.zeros(self.action_space.n)
        hand = self.current_player.hand.cards

        # pop action
        legal_actions[0] = 1

        for i in range(len(hand)):
            if hand[i].suit == self.game.tableCard.suit or hand[i].name == self.game.tableCard.name:
                legal_actions[i] = 1
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

    def play_card(self, card_num, player):

        card_name = self.contents[card_num]['info']['name']
        card = player.hand.pick(card_name)
        if card is None:
            logger.debug(
                f"Player {player.id} trying to play {card_num} but doesn't exist!")
            raise Exception('Card not found')

        logger.debug(
            f"Player {player.id} playing {str(card.order) + ': ' + card.symbol + ': ' + str(card.id)}")
        if card.type == 'nigiri':
            for c in player.position.cards:
                if c.type == 'wasabi' and c.played_upon == False:
                    c.played_upon = True
                    card.played_on_wasabi = True
                    break

        player.position.add([card])

    def switch_hands(self):
        logger.debug(f'\nSwitching hands...')
        playernhand = self.players[-1].hand

        for i in range(self.n_players - 1, -1, -1):
            if i > 0:
                self.players[i].hand = self.players[i-1].hand

        self.players[0].hand = playernhand

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
                self.current_player.hand.pop()
                done = True

            if len(self.action_bank) == self.n_players:
                logger.debug(
                    f'\nThe chosen cards are now played simultaneously')
                for i, action in enumerate(self.action_bank):
                    player = self.players[i]

                    pickup_chopsticks, first_card, second_card = self.convert_action(
                        action)
                    self.play_card(first_card, player)

                    if pickup_chopsticks:
                        self.pickup_chopsticks(player)
                        self.play_card(second_card, player)

                self.action_bank = []
                self.switch_hands()

            self.current_player_num = (
                self.current_player_num + 1) % self.n_players

            if self.current_player_num == 0:
                self.turns_taken += 1

            if self.turns_taken == self.cards_per_player:
                self.score_round()

                if self.round >= self.n_rounds:
                    self.score_puddings()
                    reward = self.score_game()
                    done = True
                else:
                    self.render()
                    self.reset_round()

        self.done = done

        return self.observation, reward, done, {}

    def reset_round(self):

        for p in self.players:
            self.discard.add(
                [x for x in p.position.cards if x.type != 'pudding'])
            puddings = [x for x in p.position.cards if x.type == 'pudding']
            p.position = Position()
            p.position.add(puddings)
            p.hand.add(self.deck.draw(self.cards_per_player))

        self.round += 1
        self.turns_taken = 0

    def reset(self):
        self.round = 0
        self.deck = Deck(self.contents)
        self.discard = Discard()
        self.players = []
        self.action_bank = []

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1

        self.current_player_num = 0
        self.done = False
        self.reset_round()
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def render(self, mode='human', close=False):

        if close:
            return

        if self.turns_taken < self.cards_per_player:
            logger.debug(
                f'\n\n-------ROUND {self.round} : TURN {self.turns_taken + 1}-----------')
            logger.debug(
                f"It is Player {self.current_player.id}'s turn to choose")
        else:
            logger.debug(
                f'\n\n-------FINAL ROUND {self.round} POSITION-----------')

        for p in self.players:
            logger.debug(f'\nPlayer {p.id}\'s hand')
            if p.hand.size() > 0:
                logger.debug('  '.join(
                    [str(card.order) + ': ' + card.symbol for card in sorted(p.hand.cards, key=lambda x: x.id)]))
            else:
                logger.debug('Empty')

            logger.debug(f'Player {p.id}\'s position')
            if p.position.size() > 0:
                logger.debug('  '.join([str(card.order) + ': ' + card.symbol + ': ' + str(
                    card.id) for card in sorted(p.position.cards, key=lambda x: x.id)]))
            else:
                logger.debug('Empty')

        logger.debug(f'\n{self.deck.size()} cards left in deck')
        logger.debug(f'{self.discard.size()} cards discarded')

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
