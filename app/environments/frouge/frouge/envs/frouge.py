import gymnasium as gym
import numpy as np

import random
from time import sleep
import logging as logger
from functools import cmp_to_key
from typing import List

from nicegui import app

from .classes import *
from .render_web import render_web

class FlammeRougeEnv(gym.Env):
    metadata = {'render_modes': ['human', 'human_web']}

    N_PLAYERS = 5
    OBS_SIZE = MAX_BOARD_SIZE*3*(MAX_CODE + 2*N_PLAYERS) + len(ALL_CARDS) * N_PLAYERS + 2*len(ALL_CARDS) + len(ALL_CARDS) + 2 + MAX_START_SPACES

    PLAYER_COLOR_MAP = {
                "1" : "91",
                "2" : "92",
                "3" : "93",
                "4" : "94",
                "5" : "95",
            }

    ACTION_SELECT_SPRINTEUR_DECK = len(ALL_CARDS)
    ACTION_SELECT_ROULEUR_DECK = len(ALL_CARDS) + 1

    def __init__(self, verbose = False, manual = False, render_mode = None):
        super(FlammeRougeEnv, self).__init__()
        self.name = 'frouge'

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self._web_thread = None
        self.handle_interactive_action = render_mode == "human_web"
        self._interactive_action_on = False
        self._interactive_action_result = None
        
        self.n_players = 5
        self.board: Board
        self.board = None
        self.penalty = list()
        self.last_played_cards = dict()
        
        card_types = len(ALL_CARDS)
        #action space = all possible rouleur and sprinter cards = card_types
        # + 2 choices of deck, + starting space choices
        self.action_space = gym.spaces.Discrete(card_types + 2 + MAX_START_SPACES)
        #observation space = board + current player played cards + current player discarded cards + other player played cards + current player hand (+action_space)
        self.observation_space = gym.spaces.Box(0, 1, (MAX_BOARD_SIZE*3*(MAX_CODE + 2*self.n_players) + card_types * self.n_players + 2*card_types,))

        
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
        obs = board_array.reshape(MAX_BOARD_SIZE*3*cell_dim_size)
        #add current player played cards
        deck = np.add(self.current_player.r_played.array(),self.current_player.s_played.array())
        obs = np.append(obs,deck,axis=0)
        #add other player played cards
        for player_num in range(self.n_players):
            if player_num != self.current_player_num:
                player = self.board.players[player_num]
                deck = np.add(player.r_played.array(),player.s_played.array())
                obs = np.append(obs,deck,axis=0)
        #add current player discarded cards
        deck = np.add(self.current_player.r_discard.array(),self.current_player.s_discard.array())
        obs = np.append(obs,deck,axis=0)
        #add player's hand
        hand = np.add(self.current_player.r_hand.array(),self.current_player.s_hand.array())
        obs = np.append(obs,hand,axis=0)

        return obs

    def action_masks(self) -> List[bool]:
        legal_actions = np.full(self.action_space.n, False)
        if self.phase == 2:
            cyclist = self.current_player.hand_order[self.hand_number]
            for i in range(len(ALL_CARDS)):
                if self.current_player.c_hand(cyclist).array()[i] > 0:
                    legal_actions[i] = True

        elif self.phase == 1:
            legal_actions[len(ALL_CARDS):(len(ALL_CARDS)+2)] = True
        elif self.phase == 0:
            for i in range(MAX_START_SPACES):
                col = i // 3
                row = i % 3
                if self.board.get_cell(col, row) == CS and self.board.is_empty(col, row):
                    legal_actions[len(ALL_CARDS) + 2 + i] = True
        else:
            raise Exception(f'Invalid phase: {self.phase}')

        return legal_actions

    def from_action_to_card(self,action):
        card = ALL_CARDS[action]
        return card

    def from_card_to_action(self,card):
        return ALL_CARDS.index(card)


    def from_action_to_starting_position(self, action):
        action = action - len(ALL_CARDS) - 2
        
        if self.current_player.s_position.col == -1:
            c_type = 's'
        else:
            c_type = 'r'

        col = action // 3
        row = action % 3

        return c_type, col, row

    def from_action_to_hand_order(self, action):

        if action == self.ACTION_SELECT_SPRINTEUR_DECK:
            hand_order = ['s', 'r']
        else:
            hand_order = ['r', 's']

        return hand_order



    def score_game(self):
        #get progressions
        positions = [ p.r_position.col + p.s_position.col for p in self.board.players]
        #get card values spends
        spent = [ - p.s_played.sum_values() - p.r_played.sum_values() for p in self.board.players ]
        #get penalty cards number
        penalties = [ - p.nb_penalties()*2 for p in self.board.players ]

        scores = [ sum(x) for x in zip(positions, spent, penalties) ]

        #is the winner ?
        if self.done:
            #get the most advanced user
            pos = [ max((p.r_position.col*3-p.r_position.row),(p.s_position.col*3-p.s_position.row)) for p in self.board.players]
            #give reward for winner
            scores[np.argmax(pos)] = 1000

        logger.info(f"Rewards: {scores}")
        return scores


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
            #store last played card for rendering
            self.last_played_cards[(player,c_type)] = card
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
        done = False
        rewards = [0] * self.n_players

        # check move legality
        if self.action_masks()[action] == False:
            raise Exception(f'Illegal action {action} : Legal actions {self.action_masks()}')
        else:
            if self.phase == 0: # initial cyclist positioning (start with sprinter)
                c_type, col, row = self.from_action_to_starting_position(action)
                self.board.set_cycl_to_square(self.current_player.n, c_type, col, row)
                self.render_map()
                if self.current_player.r_position.col != -1:
                    #change player
                    self.current_player_num += 1

                if self.current_player_num == self.n_players:
                    self.phase = 1
                    self.current_player_num = 0
            
            elif self.phase == 1:
                self.current_player.hand_order = self.from_action_to_hand_order(action)
                #change player
                self.current_player_num += 1

                if self.current_player_num == self.n_players:
                    self.draw_cards()
                    self.render_map()
                    self.phase = 2
                    self.current_player_num = 0


            elif self.phase == 2:

                #record action to process them afterwards
                card = self.from_action_to_card(action)
                if self.current_player.hand_order[self.hand_number] == 'r':  
                    self.current_player.r_chosen = card
                else:
                    self.current_player.s_chosen = card

                #change player
                self.current_player_num += 1

                if self.current_player_num == self.n_players:
                    if self.hand_number == 0: #switch to choosing the card from the second hand
                        self.hand_number = 1
                        self.draw_cards()
                        self.current_player_num = 0
                        
                    else: #resolve the turn
                        self.hand_number = 0
                        self.phase = 1 #2
                        self.resolve_turn()
                        self.render_map()
                        if self.last_turn:
                            #End of game
                            done = True
                            self.done = done
                            self.current_player_num = 0
                        else:
                            self.finish_turn()
                        rewards = self.score_game()
                else:
                    self.render_map(first_turn=True)

            else:
                raise Exception(f'Invalid phase: {self.phase}')

        return self.observation, rewards, done, False, self._get_info()

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

        #reset current player
        self.current_player_num = 0
        # self.draw_cards()
        self.turns_taken += 1



    def set_start_positions(self):
        #build cyclists list
        self.cyclists = [ (p,"r") for p in self.board.players ] + [ (p,"s") for p in self.board.players ]
        #shuffle
        random.shuffle(self.cyclists)
        first_col = self.board.first_start_col()
        for c in self.cyclists:
            self.board.set_cycl_to_pos(c[0].n,c[1],first_col)


    
    def draw_cards(self):
        for player in self.board.players:
            if player.hand_order[self.hand_number] == 'r':
                drawn = player.r_deck.draw(4)
                if len(drawn) < 4:
                    player.r_deck.add(player.r_discard.cards)
                    player.r_discard = Deck()
                    player.r_deck.shuffle()
                    drawn += player.r_deck.draw(4-len(drawn))
                if len(drawn) == 0:
                    drawn.append(PENALTY_ROULEUR_CARD)
                player.r_hand.add(drawn)
            else:
                drawn = player.s_deck.draw(4)
                if len(drawn) < 4:
                    player.s_deck.add(player.s_discard.cards)
                    player.s_discard = Deck()
                    player.s_deck.shuffle()
                    drawn += player.s_deck.draw(4-len(drawn))
                if len(drawn) == 0:
                    drawn.append(PENALTY_SPRINTER_CARD)
                player.s_hand.add(drawn)
    
    def _get_info(self):
        return {}

    def reset(self, seed = None):
        
        super().reset(seed=seed)
        #pick a random board
        self.board = Board(self.np_random.choice(ALL_BOARDS))
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
        

        self.phase = 0 #2 # 0 = placing start players, 1 = choosing which hand, 2 = choosing which card
        self.hand_number = 0

        #build cyclists list
        self.cyclists = [ (p,"r") for p in self.board.players ] + [ (p,"s") for p in self.board.players ]
        self.last_played_cards = { c:None for c in self.cyclists }

        # self.set_start_positions()
        # self.draw_cards()

        self.done = False
        self.last_turn = False
        logger.info(f'\n\n---- NEW GAME ----')
        self.render_map(first_turn=True)

        return self.observation, self._get_info()

    def render_map(self,first_turn=False):

        if self.render_mode == 'human':
            #clear screen
            # logger.info('\033[2J')
            # logger.info('\033[0;0H')
            #display board
            logger.info('\n')
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
                            player_color =  self.PLAYER_COLOR_MAP[player_num]+";"
                        cell = self.board.get_cell(j,k)
                        if cell == CV:
                            line += f'{content} '
                        else:
                            if cell == CC: # climb
                                color = "101" # light red
                            if cell == CD: # descent
                                color = "44" # blue
                            if cell == CP: # paved
                                color = "43" # yellow
                            if cell == CSU: # supply cell
                                color = "46" # cyan
                            if cell == CS: # start
                                color = "100" # gray
                            if cell == CF: # finish
                                color = "100" # gray
                            if cell == CN: #normal
                                color = "49" # black
                            line += f'\033[{player_color}{color};5m{content}\033[0m|'
                    logger.info(line)
                logger.info("---"*line_size)
            if self.phase == 2:
                if not first_turn:
                    #display card played
                    for p in self.board.players:
                        penalty = ""
                        for pen in self.penalty:
                            if p.n == int(pen[0]):
                                penalty += "X" + pen[1]
                        logger.info(f'\033[{self.PLAYER_COLOR_MAP[str(p.n)]}mPlayer {p.name} played : {p.r_chosen.name} {p.s_chosen.name}   Penalty: {penalty}\033[0m|          ')
                else:
                    for i in range(len(self.board.players)):
                        logger.info(' '*line_size*3)


    def render(self):
        if self.render_mode == "human_web":
            render_web(self)

        if self.render_mode == "human":
            if not self.done:
                #move cursor
                # logger.info('\033[18;0H')
                tab_size = 20
                p = self.current_player

                if self.phase == 2:
                    #display player hands
                    cyclist = p.hand_order[self.hand_number]
                    logger.info(f'\033[{self.PLAYER_COLOR_MAP[str(p.n)]}mPlayer {p.name}\'s {cyclist} hand\033[0m')
                    line = (" " * tab_size) + "".join([ c.name + ' (' + str(self.from_card_to_action(c)) + ')' + " "*len(c.name) for c in p.c_hand(cyclist).cards ])
                    logger.info(f'{line}')
                elif self.phase == 1:
                    logger.info(f'\033[{self.PLAYER_COLOR_MAP[str(p.n)]}mPlayer {p.name} has to choose first hand to reveal\033[0m')
                    logger.info(f"s({len(ALL_CARDS)}) r({len(ALL_CARDS)+1})")
                elif self.phase == 0:
                    c_type = "s" if self.current_player.s_position.col == -1 else "r"
                    logger.info(f'\033[{self.PLAYER_COLOR_MAP[str(p.n)]}mPlayer {p.name} has to place cyclist {c_type}\033[0m')
                    actions = [index for index, value in enumerate(self.action_masks()) if value == True]
                    logger.info(" ".join([ f"{a - len(ALL_CARDS) - 1}({a})" for a in actions]))
            else:
                logger.info(f'\n\nGAME OVER')
    
    def get_interactive_action(self) -> int:
        self._interactive_action_on = True
        while True:
            if self._interactive_action_result != None:
                self._interactive_action_on = False
                action = self._interactive_action_result
                self._interactive_action_result = None
                return action 
            sleep(1)

            
    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Flamme Rouge!')
    
    def close(self):
        if self.render_mode == "human_web":
            #time to render last update
            sleep(2)
            app.shutdown()
