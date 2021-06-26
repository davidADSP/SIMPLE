
import gym
import numpy as np

import random
from functools import cmp_to_key

import config

from stable_baselines import logger

from .classes import *


#TODO network decides where to place players at start of game
#TODO need to split decision into S and R cards

PLAYER_COLOR_MAP = {
                "1" : "91",
                "2" : "92",
                "3" : "93",
                "4" : "94",
                "5" : "95",
            }

class FlammeRougeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(FlammeRougeEnv, self).__init__()
        self.name = 'frouge'
        self.manual = manual
        
        self.n_players = 5
        self.board = None
        
        card_types = len(ALL_CARDS)
        #action space = all possible couples of rouleur and sprinter cards = card_types/2 * card_types/2
        self.action_space = gym.spaces.Discrete(int(card_types*card_types/4))
        #observation space = board + current player played cards + current player discarded cards + other player played cards + current player hand (+action_space)
        self.observation_space = gym.spaces.Box(0, 1, (MAX_BOARD_SIZE, 3, (MAX_CODE + 2*self.n_players) + card_types * self.n_players + 2*card_types + self.action_space.n))
        self.verbose = verbose

        
    @property
    def observation(self):
        cell_dim_size = (MAX_CODE + 2*self.n_players)
        #add race board
        board_array = np.array(self.board.array)
        board_array = np.append(board_array,np.zeros((board_array.shape[0],3,2*self.n_players)),axis=2)
        #add current player position info
        board_array[self.current_player.r_position.col, self.current_player.r_position.row, MAX_CODE] = 1
        board_array[self.current_player.s_position.col, self.current_player.s_position.row, MAX_CODE + 1] = 1
        #add location of other players
        i = 0
        for player_num in range(self.n_players):
            if player_num != self.current_player_num:
                board_array[self.board.players[player_num].r_position.col, self.board.players[player_num].r_position.row, MAX_CODE + 2 + 2*i] = 1
                board_array[self.board.players[player_num].s_position.col, self.board.players[player_num].s_position.row, MAX_CODE + 3 + 2*i] = 1
                i += 1
        obs = board_array
        #add current player played cards
        deck = np.add(self.current_player.r_played.array(),self.current_player.s_played.array())
        deck = np.expand_dims(deck, [0,1])
        deck = np.repeat(deck, MAX_BOARD_SIZE, axis = 0)
        deck = np.repeat(deck, 3, axis = 1)
        obs = np.append(obs,deck,axis=2)
        #add other player played cards
        for player_num in range(self.n_players):
            if player_num != self.current_player_num:
                player = self.board.players[player_num]
                deck = np.add(player.r_played.array(),player.s_played.array())
                deck = np.expand_dims(deck, [0,1])
                deck = np.repeat(deck, MAX_BOARD_SIZE, axis = 0)
                deck = np.repeat(deck, 3, axis = 1)
                obs = np.append(obs,deck,axis=2)
        #add current player discarded cards
        deck = np.add(self.current_player.r_discard.array(),self.current_player.s_discard.array())
        deck = np.expand_dims(deck, [0,1])
        deck = np.repeat(deck, MAX_BOARD_SIZE, axis = 0)
        deck = np.repeat(deck, 3, axis = 1)
        obs = np.append(obs,deck,axis=2)
        #add player's hand #TODO at the moment cards are being added - better to treat S and R cards separately?
        hand = np.add(self.current_player.r_hand.array(),self.current_player.s_hand.array())
        hand = np.expand_dims(hand, [0,1])
        hand = np.repeat(hand, MAX_BOARD_SIZE, axis = 0)
        hand = np.repeat(hand, 3, axis = 1)
        obs = np.append(obs,hand,axis=2)
        #pipe legal actions
        actions = self.legal_actions
        actions = np.expand_dims(actions, [0,1])
        actions = np.repeat(actions, MAX_BOARD_SIZE, axis = 0)
        actions = np.repeat(actions, 3, axis = 1)
        obs = np.append(obs,actions,axis=2)

        return obs

    @property
    def legal_actions(self):
        my_player = self.current_player
        legal_actions = np.zeros(self.action_space.n)
        for i in range(self.action_space.n):
            r_card_index = int(i / (len(ALL_CARDS)/2)) 
            s_card_index = i % int(len(ALL_CARDS)/2)
            if my_player.r_hand.array()[r_card_index+int(len(ALL_CARDS)/2)] > 0:
                if my_player.s_hand.array()[s_card_index] > 0:
                    legal_actions[i] = 1
        return legal_actions

    def from_action_to_cards(self,action):
        r_card = ALL_CARDS[int(action / (len(ALL_CARDS)/2)) + int(len(ALL_CARDS)/2) ]
        s_card = ALL_CARDS[(action % int(len(ALL_CARDS)/2))]
        return (r_card, s_card)

    def from_cards_to_action(self,r_card,s_card):
        return (ALL_CARDS.index(r_card)-int(len(ALL_CARDS)/2))*int(len(ALL_CARDS)/2)+ALL_CARDS.index(s_card)


    def score_game(self):
        reward = [0.0] * self.n_players
        scores = [ (max((p.r_position.col*3-p.r_position.row),(p.s_position.col*3-p.s_position.row)),p) for p in self.board.players]
        scores.sort(key=lambda item: item[0])
        for i, s in enumerate(scores):
            if i < self.n_players - 1:
                reward[s[1].n - 1] = -1.0/(self.n_players - 1)
            else:
                reward[s[1].n - 1] = 1.0
        

        return reward


    @property
    def current_player(self):
        return self.board.players[self.current_player_num]

    def sort_cyclist_by_pos(self,a,b):
        if a[0].c_pos(a[1]).col > b[0].c_pos(b[1]).col:
            return 1
        if a[0].c_pos(a[1]).col < b[0].c_pos(b[1]).col:
            return -1
        if a[0].c_pos(a[1]).row > b[0].c_pos(b[1]).row:
            return -1
        if a[0].c_pos(a[1]).row < b[0].c_pos(b[1]).row:
            return 1
        return 0

    def resolve_turn(self):
        #build cyclist list
        self.cyclists.sort(key=cmp_to_key(self.sort_cyclist_by_pos),reverse=True)
        #move each cyclist
        for player, c_type in self.cyclists:
            card = player.c_chosen_card(c_type)
            #move cyclist
            self.board.move(player.n, c_type, card.value)
            #if finish, last turn
            if self.board.get_cell(player.c_pos(c_type).col, 0) == CF:
                self.last_turn = True
        #process aspiration
        self.cyclists.sort(key=cmp_to_key(self.sort_cyclist_by_pos))
        c_group = list()
        for player, c_type in self.cyclists:
            #no aspiration on rising or paved cells
            if self.board.get_cell(player.c_pos(c_type).col, 0) in [ CC, CP ]:
                c_group = list()
                continue
            #add to group
            c_group.append((player,c_type))
            #if not at right, still cyclist to add to group
            if player.c_pos(c_type).row != 0:
                continue
            if self.board.is_empty(player.c_pos(c_type).col+1,0):
                if not self.board.is_empty(player.c_pos(c_type).col+2,0):
                    if self.board.get_cell(player.c_pos(c_type).col+1, 0) in [ CC, CP ]:
                        #no aspiration on rising or paved cells
                        c_group=list()
                        continue
                    #aspiration : move group
                    for g_player, g_c_type in c_group[::-1]:
                        self.board.move(g_player.n,g_c_type,1,True)
                    continue
                else:
                    #cyclist too far, no aspiration
                    c_group = list()
                    continue
            else:
                #group not finished
                continue
        #assign penalty
        self.penalty = list()
        for player, c_type in self.cyclists:
            if self.board.is_empty(player.c_pos(c_type).col+1,0):
                self.penalty.append(str(player.n)+c_type)
                if c_type == "r":
                    player.c_discard(c_type).add((PENALTY_ROULEUR_CARD,))
                else:
                    player.c_discard(c_type).add((PENALTY_SPRINTER_CARD,))


    def step(self, action):
        
        reward = [0] * self.n_players
        done = False

        # check move legality
        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1.0
            done = True

        else:
            #record action to process them afterwards
            r_card, s_card = self.from_action_to_cards(action)
            self.current_player.r_chosen = r_card
            self.current_player.s_chosen = s_card
            #change player
            self.current_player_num += 1
            if self.current_player_num == self.n_players:
                self.resolve_turn()
                self.render_map()
                if self.last_turn:
                    #End of game
                    reward = self.score_game()
                    done = True
                    self.current_player_num = 0
                else:
                    self.finish_turn()

        self.done = done

        return self.observation, reward, done, {}

    def finish_turn(self):
        #discard cards and draw new
        for player in self.board.players:
            player.r_played.add((player.r_chosen,))
            player.s_played.add((player.s_chosen,))
            player.r_hand.cards.remove((player.r_chosen))
            player.s_hand.cards.remove((player.s_chosen))
            player.r_discard.add(player.r_hand.cards)
            player.s_discard.add(player.s_hand.cards)
            player.r_hand = Deck()
            player.s_hand = Deck()
        self.draw_card()
        #reset current player
        self.current_player_num = 0
        self.turns_taken += 1

    def set_start_positions(self):
        #build cyclists list
        self.cyclists = [ (p,"r") for p in self.board.players ] + [ (p,"s") for p in self.board.players ]
        #shuffle
        random.shuffle(self.cyclists)
        first_col = self.board.first_start_col()
        for c in self.cyclists:
            self.board.set_cycl_to_pos(c[0].n,c[1],first_col)
    
    def draw_card(self):
        for player in self.board.players:
            drawn = player.r_deck.draw(4)
            if len(drawn) < 4:
                player.r_deck.add(player.r_discard.cards)
                player.r_discard = Deck()
                player.r_deck.shuffle()
                drawn += player.r_deck.draw(4-len(drawn))
            if len(drawn) == 0:
                drawn.append(PENALTY_ROULEUR_CARD)
            player.r_hand.add(drawn)
            drawn = player.s_deck.draw(4)
            if len(drawn) < 4:
                player.s_deck.add(player.s_discard.cards)
                player.s_discard = Deck()
                player.s_deck.shuffle()
                drawn += player.s_deck.draw(4-len(drawn))
            if len(drawn) == 0:
                drawn.append(PENALTY_SPRINTER_CARD)
            player.s_hand.add(drawn)

    def reset(self):
        #pick a random board
        self.board = Board(random.choice(ALL_BOARDS))
        #reset players
        player_id = 1
        for p in range(self.n_players):
            player = Player(player_id)
            player.r_deck.shuffle()
            player.s_deck.shuffle()
            self.board.add_player(player)
            player_id += 1
        self.current_player_num = 0
        self.turns_taken = 0

        #TODO add initial position in learning
        self.set_start_positions()

        self.done = False
        self.last_turn = False
        logger.debug(f'\n\n---- NEW GAME ----')
        self.render_map(first_turn=True)
        self.draw_card()
        return self.observation

    def render_map(self,first_turn=False):

        #clear screen
        logger.debug('\033[2J')
        logger.debug('\033[0;0H')
        #display board
        line_size = 40
        for i in range(int(len(self.board.array)/line_size)):
            #print line by line
            for k in range(3):
                line = ""
                for j in range(line_size*i,line_size*(i+1)):
                    player_color = ""
                    content = self.board.get_cell_display(j,k)
                    if content == "":
                        content = "  "
                    else:
                        player_num = content[0]
                        player_color =  PLAYER_COLOR_MAP[player_num]+";"
                    cell = self.board.get_cell(j,k)
                    if cell == CV:
                        line += f'{content} '
                    else:
                        if cell == CC:
                            color = "101"
                        if cell == CD:
                            color = "44"
                        if cell == CP:
                            color = "43"
                        if cell == CSU:
                            color = "46"
                        if cell == CS:
                            color = "100"
                        if cell == CF:
                            color = "100"
                        if cell == CN:
                            color = "49"
                        line += f'\033[{player_color}{color};5m{content}\033[0m|'
                logger.debug(line)
            logger.debug("---"*line_size)
        if not first_turn:
            #display card played
            for p in self.board.players:
                penalty = ""
                for pen in self.penalty:
                    if p.n == int(pen[0]):
                        penalty += "X" + pen[1]
                logger.debug(f'\033[{PLAYER_COLOR_MAP[str(p.n)]}mPlayer {p.name} played : {p.r_chosen.name} {p.s_chosen.name}   Penalty: {penalty}\033[0m|          ')
        else:
            for i in range(len(self.board.players)):
                logger.debug(' '*line_size*3)

    def render(self, mode='human', close=False):

        if close:
            return
        if mode == "human" and not self.done:
            #move cursor
            logger.debug('\033[18;0H')
            tab_size = 20
            #display player hands
            p = self.current_player
            logger.debug(f'\033[{PLAYER_COLOR_MAP[str(p.n)]}mPlayer {p.name}\'s hand\033[0m')
            line = (" " * tab_size) + "".join([ c.name + " "*len(c.name) for c in p.r_hand.cards ])
            logger.debug(f'{line}')
            for s_card in p.s_hand.cards:
                line = s_card.name
                for r_card in p.r_hand.cards:
                    line += " "*(tab_size-4) + str(self.from_cards_to_action(r_card,s_card)) + "  "
                logger.debug(f'{line}               ')
            #clear remaining lines
            for i in range(20):
                logger.debug(' ' * MAX_BOARD_SIZE)
            logger.debug('\033[20A')

        if self.done:
            logger.debug(f'\n\nGAME OVER')
            
    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Flamme Rouge!')
