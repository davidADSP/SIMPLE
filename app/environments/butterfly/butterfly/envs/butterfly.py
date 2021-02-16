
import gym
import numpy as np
import random

import config

from stable_baselines import logger

from .classes import *

class ButterflyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(ButterflyEnv, self).__init__()
        self.name = 'butterfly'
        self.n_players = 3

        self.manual = manual

        self.board_size = 7
        self.squares = self.board_size * self.board_size

        self.tile_types = 11
        
        self.max_score = 100
        
        self.total_positions = self.squares + self.n_players + 1

        self.set_contents()
        self.nets = [5,7,16, 24, 32, 41, 43]
        self.total_tiles = sum([x['count'] for x in self.contents])

        self.action_space = gym.spaces.Discrete(self.total_tiles  * 2)
        self.observation_space = gym.spaces.Box(0, 1, (self.total_positions * self.total_tiles + self.squares + 4 + self.n_players + self.action_space.n ,))
        self.verbose = verbose


    def set_contents(self):
        self.contents = []

        for colour in ['R','B','G','Y']:
            for value in range(1, 6):
                self.contents.append({'tile': Butterfly, 'info': {'name': f'{colour}{value}butterfly', 'colour': colour, 'value': value}, 'count': 2} )
            self.contents.append({'tile': Butterfly, 'info': {'name': f'{colour}Xbutterfly', 'colour': colour, 'value': 0}, 'count': 1} )

        self.contents.append({'tile': Flower, 'info': {'name': 'flower'}, 'count':  13})

        for value in range(1,10):
            self.contents.append({'tile': Dragonfly, 'info': {'name': 'dragonfly', 'value': value}, 'count':  1})

        for value in range(1,10):
            self.contents.append({'tile': LightningBug,  'info': {'name': 'lightningbug', 'value': value}, 'count':  1})

        for value in range(1,10):
            self.contents.append({'tile': Cricket, 'info': {'name': 'cricket', 'value': value}, 'count':  1})

        self.contents.append({'tile': Bee, 'info': {'name': 'bee'}, 'count':  6})

        for value in range(10,16):
            self.contents.append({'tile': Honeycomb, 'info': {'name': 'honeycomb', 'value': value}, 'count':  1})
        
        for value in range(-4,-8, -1):
            self.contents.append({'tile': Wasp, 'info': {'name': 'wasp', 'value': value}, 'count':  1})

        
    @property
    def observation(self):
        obs = np.zeros(([self.total_positions, self.total_tiles]))
        player_num = self.current_player_num

        # print('Tiles')
        for s, tile in enumerate(self.board.tiles):
            if tile is not None:
                obs[s][tile.id] = 1
                # print(s, tile.id)

        # print('Positions')
        for i in range(self.n_players):
            player = self.players[player_num]

            for tile in player.position.tiles:
                obs[self.squares + i][tile.id] = 1
                # print(self.squares + i, tile.id)

            player_num = (player_num + 1) % self.n_players
        
        # print('DrawBag')
        for tile in self.drawbag.tiles:
            obs[-1][tile.id] = 1
            # print(len(obs)-1, tile.id)

        ret = obs.flatten()

        # print('Hudson')
        hudson_obs = np.zeros((self.squares, ))
        hudson_obs[self.board.hudson] = 1
        # print(len(ret) + self.board.hudson)

        ret = np.append(ret, hudson_obs)

        # print('Hudson facing')
        hudson_facing_obs = np.zeros((4, ))
        for i, x in enumerate(['U','D','L','R']):
            if self.board.hudson_facing == x:
                hudson_facing_obs[i] = 1
                # print(len(ret) + i)

        ret = np.append(ret, hudson_facing_obs)

        # print('Score')
        score_obs = np.zeros((self.n_players, ))

        player_num = self.current_player_num
        for i in range(self.n_players):
            player = self.players[player_num]
            score_obs[i] = player.position.score / self.max_score
            # print(len(ret) + i)
            # print(score_obs[i])
            player_num = (player_num + 1) % self.n_players

        ret = np.append(ret, score_obs)

        # print('Legal actions')
        # for i in range(len(self.legal_actions)):
        #     if self.legal_actions[i] == 1:
        #         print(len(ret) + i)

        ret = np.append(ret, self.legal_actions)

        return ret

    @property
    def legal_actions(self):
        legal_actions = np.zeros(self.action_space.n)

        # UP / DOWN
        for factor in [-1,1]:
            if (factor == -1 and self.board.hudson_facing == 'D') or (factor == 1 and self.board.hudson_facing == 'U'):
                pass
            else:
                current_square = self.board.hudson
                found_net = False
                for i in range(self.board_size):
                    current_square = current_square + factor * self.board_size
                    if 0 <= current_square < self.squares:
                        tile = self.board.tiles[current_square]
                        if tile is not None:
                            legal_actions[tile.id] = 1
                            if found_net:
                                legal_actions[tile.id + self.total_tiles] = 1
                        else:
                            if self.board.nets[current_square] == 1:
                                found_net = True
                    else:
                        break

        # LEFT / RIGHT
        for factor in [-1,1]:
            if (factor == -1 and self.board.hudson_facing == 'R') or (factor == 1 and self.board.hudson_facing == 'L'):
                pass
            else:
                current_square = self.board.hudson
                found_net = False
                for i in range(self.board_size):
                    current_square = current_square + factor
                    if (factor == 1 and current_square % self.board_size != 0) or (factor == -1 and current_square % self.board_size != self.board_size - 1) :
                        tile = self.board.tiles[current_square]
                        if tile is not None:
                            legal_actions[tile.id] = 1
                            if found_net:
                                legal_actions[tile.id + self.total_tiles] = 1
                        else:
                            if self.board.nets[current_square] == 1:
                                found_net = True
                    else:
                        break


        return legal_actions





    def score_game(self):
        reward = [0.0] * self.n_players
        scores = [p.position.score for p in self.players]
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


    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def convert_action(self, tile_id):
        if tile_id < self.total_tiles:
            net = False
        else:
            net = True        
            tile_id = tile_id - self.total_tiles

        square = [i for i, tile in enumerate(self.board.tiles) if tile is not None and tile.id == tile_id][0]

        return net, square


    def choose_net_tile(self):
        logger.debug(f'Player {self.current_player.id} choosing extra tile using net')
        self.current_player.position.add(self.drawbag.draw(1))

    def choose_tile(self, square):
        tile = self.board.remove(square)
        if tile is None:
            logger.debug(f"Player {self.current_player.id} trying to pick tile from square {square} but doesn't exist!")
            raise Exception('tile not found')

        logger.debug(f"Player {self.current_player.id} picking {tile.symbol}")
        self.current_player.position.add([tile])


    def place_hudson(self):
        self.board.hudson = random.randint(0, self.squares - 1)
        self.board.hudson_facing = random.choice(['U', 'D', 'L', 'R'])



    def step(self, action):
        
        reward = [0] * self.n_players
        done = False

        # check move legality
        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1
            done = True

        
        else:
            # pick the tile and optional bonus tile
            net, square = self.convert_action(action)
            
            self.choose_tile(square)

            if net:
                self.choose_net_tile()

            # move and turn hudson
            if 0 < square - self.board.hudson < self.board_size:
                self.board.hudson_facing = 'R'
            elif -self.board_size < square - self.board.hudson < 0 :
                self.board.hudson_facing = 'L'
            elif square > self.board.hudson:
                self.board.hudson_facing = 'D'
            elif square < self.board.hudson:
                self.board.hudson_facing = 'U'
            
            self.board.hudson = square

            if sum(self.legal_actions) == 0:
                reward = self.score_game()
                done = True
            else:
                self.turns_taken += 1
                self.current_player_num = (self.current_player_num + 1) % self.n_players

        self.done = done

        return self.observation, reward, done, {}


    def reset(self):
        self.drawbag = DrawBag(self.contents)
        self.players = []

        player_id = 1
        for p in range(self.n_players):
            self.players.append(Player(str(player_id)))
            player_id += 1


        self.current_player_num = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')

        self.board = Board(self.board_size)
        
        self.board.fill(self.drawbag.draw(self.squares))

        for net in self.nets:
            self.board.add_net(net)

        self.place_hudson()

        self.turns_taken = 0

        return self.observation


    def render(self, mode='human', close=False):
        
        if close:
            return

        if not self.done:
            logger.debug(f'\n\n-------TURN {self.turns_taken + 1}-----------')
            logger.debug(f"It is Player {self.current_player.id}'s turn to choose")
        else:
            logger.debug(f'\n\n-------FINAL POSITION-----------')
        
        out = '\n'
        for square in range(self.squares):
            if self.board.hudson == square:
                if self.board.hudson_facing == 'R':
                    out += '>H>\t'
                elif self.board.hudson_facing == 'L':
                    out += '<H<\t'
                elif self.board.hudson_facing == 'U':
                    out += '^H^\t'
                elif self.board.hudson_facing == 'D':
                    out += 'vHv\t'
            elif self.board.tiles[square] == None:
                if self.board.nets[square]:
                    out += '-🥅-\t'
                else:
                    out += '---\t'
            else:
                out += self.board.tiles[square].symbol + ':' + str(self.board.tiles[square].id) + '\t' 

            if square % self.board_size == self.board_size - 1:
                logger.debug(out)
                out = ''
            
        logger.debug('\n')


        for p in self.players:
            logger.debug(f'Player {p.id}\'s position')
            if p.position.size() > 0:

                out = '  '.join([tile.symbol for tile in sorted(p.position.tiles, key=lambda x: x.id) if tile.type != 'cricket'])
                out += '  ' + '  '.join([tile.symbol for tile in p.position.tiles if tile.type == 'cricket'])

                logger.debug(out)
            else:
                logger.debug('Empty')

        logger.debug(f'\n{self.drawbag.size()} tiles left in drawbag')

        if self.verbose:
            obs_sparse = [i if o == 1 else (i,o) for i,o in enumerate(self.observation) if o != 0]
            logger.debug(f'\nObservation: \n{obs_sparse}')

        if self.done:
            logger.debug(f'\n\nGAME OVER')
        else:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')
        
        logger.debug(f'\n')

        for p in self.players:
            logger.debug(f'Player {p.id} points: {p.position.score}')


    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Butterfly!')
