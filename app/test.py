# docker-compose exec app python3 test.py -d -g 1 -a base base human -e butterfly 

import logging
import random
import argparse

from stable_baselines3.common.logger import configure
from stable_baselines3.common.utils import set_random_seed

from utils.files import load_model, write_results
from utils.register import get_environment
from utils.agents import Agent

import config
import numpy as np


def main(args):

  logger = configure(config.LOGDIR)

  render_mode = args.render_mode

  if args.seed == 0:
    seed = random.randint(0,1000)
  else:
    seed = args.seed

  if args.debug:
    logger.set_level(config.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    render_mode = 'human'
  else:
    logger.set_level(config.INFO)
    
  #make environment
  env = get_environment(args.env_name)(verbose = args.verbose, manual = args.manual, render_mode = render_mode)
  set_random_seed(seed)

  total_rewards = {}

  if args.recommend:
    ppo_model = load_model(env, 'best_model.zip')
    ppo_agent = Agent('best_model', ppo_model)
  else:
    ppo_agent = None


  agents = []

  #load the agents
  if len(args.agents) != env.n_players:
    raise Exception(f'{len(args.agents)} players specified but this is a {env.n_players} player game!')

  for i, agent in enumerate(args.agents):
    if agent == 'human':
      agent_obj = Agent('human')
    elif agent == 'rules':
      agent_obj = Agent('rules')
    elif agent == 'base':
      base_model = load_model(env, 'base.zip', args.device)
      agent_obj = Agent('base', base_model)   
    else:
      ppo_model = load_model(env, f'{agent}.zip', args.device)
      agent_obj = Agent(agent, ppo_model)
    agents.append(agent_obj)
    total_rewards[agent_obj.id] = 0
  
  #play games
  logger.info(f'\nPlaying {args.games} games...')
  for game in range(args.games):
    players = agents[:]

    if args.randomise_players:
      random.shuffle(players)

    obs = env.reset(seed = seed)
    done = False
    
    for i, p in enumerate(players):
      logger.debug(f'Player {i+1} = {p.name}')

    while not done:

      current_player = players[env.current_player_num]
      env.render()
      logger.debug(f'\nCurrent player name: {current_player.name}')

      if args.recommend and current_player.name in ['human', 'rules']:
        # show recommendation from last loaded model
        logger.debug(f'\nRecommendation by {ppo_agent.name}:')
        action = ppo_agent.choose_action(env, choose_best_action = True, mask_invalid_actions = True)

      if current_player.name == 'human':
        if hasattr(env,"handle_interactive_action") and env.handle_interactive_action == True:
          action = env.get_interactive_action()
        else:
          action = input('\nPlease choose an action: ')
          try:
            # for int actions
            action = int(action)
          except:
            # for MulitDiscrete action input as list TODO
            action = eval(action)
      elif current_player.name == 'rules':
        logger.debug(f'\n{current_player.name} model choices')
        action = current_player.choose_action(env, choose_best_action = False, mask_invalid_actions = True)
      else:
        logger.debug(f'\n{current_player.name} model choices')
        action = current_player.choose_action(env, choose_best_action = args.best, mask_invalid_actions = True)

      obs, reward, done, _ , _ = env.step(action)

      for r, player in zip(reward, players):
        total_rewards[player.id] += r
        player.points += r

      if args.cont:
        input('Press any key to continue')
    
    env.render()

    logger.info(f"Played {game + 1} games: {total_rewards}")

    if args.write_results:
      write_results(players, game, args.games, env.turns_taken)

    for p in players:
      p.points = 0

  env.close()


def cli() -> None:
  """Handles argument extraction from CLI and passing to main().
  Note that a separate function is used rather than in __name__ == '__main__'
  to allow unit testing of cli().
  """
  # Setup argparse to show defaults on help
  formatter_class = argparse.ArgumentDefaultsHelpFormatter
  parser = argparse.ArgumentParser(formatter_class=formatter_class)

  parser.add_argument("--agents","-a", nargs = '+', type=str, default = ['human', 'human']
                , help="Player Agents (human, ppo version)")
  parser.add_argument("--best", "-b", action = 'store_true', default = False
                , help="Make AI agents choose the best move (rather than sampling)")
  parser.add_argument("--games", "-g", type = int, default = 1
                , help="Number of games to play)")
  parser.add_argument("--render_mode", "-rm", type = str, default = None
                 , help="Render mode to use in game gym env")
  parser.add_argument("--debug", "-d",  action = 'store_true', default = False
            , help="Show logs to debug level")
  parser.add_argument("--verbose", "-v",  action = 'store_true', default = False
            , help="Show observation on debug logging")
  parser.add_argument("--manual", "-m",  action = 'store_true', default = False
            , help="Manual update of the game state on step")
  parser.add_argument("--randomise_players", "-r",  action = 'store_true', default = False
            , help="Randomise the player order")
  parser.add_argument("--recommend", "-re",  action = 'store_true', default = False
            , help="Make recommendations on humans turns")
  parser.add_argument("--cont", "-c",  action = 'store_true', default = False
            , help="Pause after each turn to wait for user to continue")
  parser.add_argument("--env_name", "-e",  type = str, default = 'TicTacToe'
            , help="Which game to play?")
  parser.add_argument("--write_results", "-w",  action = 'store_true', default = False
            , help="Write results to a file?")
  parser.add_argument("--seed", "-s",  type = int, default = 0
            , help="Random seed. If 0, random")
  
  parser.add_argument("--device", "-dev",  type = str, default = "cpu"
            , help="The device to use")
  # Extract args
  args = parser.parse_args()

  # Enter main
  main(args)
  return


if __name__ == '__main__':
  cli()