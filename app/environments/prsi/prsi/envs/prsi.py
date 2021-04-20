import gym
import numpy as np
import config
from stable_baselines import logger
from .classes import Player, Deck, Card


class PrsiEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False, manual=False):
        super(PrsiEnv, self).__init__()
        self.name = 'prsi'
        self.manual = manual
        self.played_cards = []
        self.verbose = verbose

        self.n_players = 2
        self.cards_per_player = 5

        self.n_rounds = 3

        self.total_positions = self.n_players

        self.total_cards = 32
        self.action_space = gym.spaces.Discrete(35)

        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(280,))

        self.verbose = verbose
        self.zobrane3 = False
        self.stalsom = False
        self.menimna = False
        self.ktoryvysnik = False
        self.beres = 0

    @ property
    def observation(self):
        obs = np.zeros(([6, 35]))
        maybe = np.zeros(35)

      # moje karty
        # mojekarty = np.zeros(32)
        for card in self.current_player.hand.cards:
            obs[0][card.id] = 1
            maybe[card.id] = 1

        # # pocet mojich kariet (pozicia)
        obs[1][len(self.current_player.hand.cards)] = 1
        # karta na stole
        obs[2][self.tableCard.id] = 1
        maybe[self.tableCard.id] = 1
        # uz hrate karty
        for card in self.played_cards:
            obs[3][card.id] = 1
            maybe[card.id] = 1

        for i in range(self.n_players):
            obs[4+i][len(self.players[i].hand.cards)] = 1

        ret = obs
        ret = np.append(ret, maybe)
        ret = np.append(ret, self.legal_actions)

        return ret

    @ property
    def legal_actions(self):
        legal_actions = np.zeros(self.action_space.n)
        hand = self.current_player.hand.cards

        # pop action
        legal_actions[0] = 1

        # stojis akcia 33
        if self.tableCard.name == "Eso" and self.stalsom == False:
            legal_actions[33] = 1
            legal_actions[0] = 0
        # beres tri akcia 34
        elif self.tableCard.name == "VII" and self.zobrane3 == False:
            legal_actions[0] = 0
            legal_actions[34] = 1
            # ked mas 7 mozes prebit
            for card in hand:
                if card.name == "VII":
                    legal_actions[card.id] = 1

        else:
            for card in hand:
                if card.name == "Vysnik":
                    # TODO: opravit viac vysnikov na ruke
                    self.ktoryvysnik = card.id
                    # meni na  Gula
                    legal_actions[6] = 1
                    # meni na  Zalud
                    legal_actions[14] = 1
                    # # meni na  Zelen
                    legal_actions[22] = 1
                    # # meni na cerven
                    legal_actions[30] = 1

                elif (card.suit == self.menimna):
                    legal_actions[card.id] = 1

                elif (not self.menimna and (card.suit == self.tableCard.suit or card.name == self.tableCard.name)):
                    legal_actions[card.id] = 1

        return legal_actions

    @ property
    def current_player(self):
        return self.players[self.current_player_num]

    def step(self, action):
        reward = [0] * self.n_players
        done = False
        menimna = self.menimna

        # check if have card in deck
        if self.deck.size() == 0 or (action == 34 and self.deck.size() < 3+self.beres):
            done = True
        # check move legality
        elif self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1
            done = True

        # play the card(s)
        else:
            # pop card from deck
            if action == 0:
                self.current_player.hand.add(self.deck.pop())
            # beres tri
            elif action == 34:
                self.current_player.hand.add(self.deck.pop(3+self.beres))
                self.zobrane3 = True
                self.beres = 0
            # stojis
            elif action == 33:
                self.stalsom = True
            else:
                self.menimna = ""
                menimna = ""

                if action == 6:
                    action = self.ktoryvysnik
                    menimna = "Gula"
                elif action == 14:
                    action = self.ktoryvysnik
                    menimna = "Zalud"
                elif action == 22:
                    action = self.ktoryvysnik
                    menimna = "Zelen"
                elif action == 30:
                    action = self.ktoryvysnik
                    menimna = "Cerven"

                self.zobrane3 = False
                self.stalsom = False
                # prebijam 7
                if self.tableCard.name == "VII" and (action == 1 or action == 9 or action == 17 or action == 25):
                    self.beres = self.beres+3

                self.deck.cards.append(self.tableCard)
                self.played_cards.append(self.tableCard)
                self.tableCard = self.current_player.hand.pick(action)

        if len(self.current_player.hand.cards) == 0:
            reward[self.current_player_num] = 1
            done = True
        self.done = done
        self.round += 1

        self.current_player_num = (
            self.current_player_num + 1) % self.n_players
        self.menimna = menimna
        return self.observation, reward, done, {}

    def reset(self):
        self.round = 0
        self.deck = Deck()
        self.players = []
        self.action_bank = []
        self.played_cards = []

        self.zobrane3 = False
        self.stalsom = False
        self.zobrane3 = False
        self.stalsom = False
        self.menimna = ""
        self.ktoryvysnik = ""
        self.beres = 0

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1

        for player in self.players:
            player.hand.add(self.deck.pop(5))

        self.current_player_num = 0
        self.done = False
        self.tableCard = self.deck.pop()[0]
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
                logger.debug(card.id, "  \t", card.name, "  \t", card.suit)

        logger.debug(
            f'\nTable card: {self.tableCard.name} {self.tableCard.suit}')

        logger.debug(f'\n{self.deck.size()} cards left in deck')
        if self.menimna:
            logger.debug(f'\nMenim na {self.menimna}')

        if self.verbose:
            logger.debug(f'\n\nRound {self.round}')
            logger.debug(
                f'\nObservation: \n{[i if o == 1 else (i,o) for i,o in enumerate(self.observation) if o != 0]}')

        if not self.done:
            logger.debug(
                f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')

        if self.done:
            logger.debug(f'\n\nRound {self.round}')
            logger.debug(f'\n\nGAME OVER')

    def rules_move(self):
        raise Exception(
            'Rules based agent is not yet implemented for Sushi Go!')
