
import logging as logger
import os
import sys
import random
import csv
import time
import numpy as np


from shutil import rmtree
from sb3_contrib import MaskablePPO as PPO1

from utils.register import get_network_arch

import config


def write_results(players, game, games, episode_length):
    
    out = {'game': game
    , 'games': games
    , 'episode_length': episode_length
    , 'p1': players[0].name
    , 'p2': players[1].name
    , 'p1_points': players[0].points
    , 'p2_points': np.sum([x.points for x in players[1:]])
    }

    if not os.path.exists(config.RESULTSPATH):
        with open(config.RESULTSPATH,'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=out.keys())
            writer.writeheader()

    with open(config.RESULTSPATH,'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=out.keys())
        writer.writerow(out)

def list_model(env):
    models = list()
    for f in os.listdir(os.path.join(config.MODELDIR, env.name)):
        if not f.startswith("_") and f.endswith(".zip"):
            models.append(f[:-4])
    return models

def load_model(env, name, device):

    filename = os.path.join(config.MODELDIR, env.name, name)
    filename_pretrained = os.path.join(config.MODELDIR, "pretrained", env.name, name)
    if os.path.exists(filename):
        logger.info(f'Loading {name}')
        cont = True
        while cont:
            try:
                ppo_model = PPO1.load(filename, env=env, device=device)
                cont = False
            except Exception as e:
                time.sleep(5)
                print(e)
    
    elif os.path.exists(filename_pretrained):
        logger.info(f'Loading {name}')
        cont = True
        while cont:
            try:
                ppo_model = PPO1.load(filename_pretrained, env=env, device=device)
                cont = False
            except Exception as e:
                time.sleep(5)
                print(e)
    
    elif name == 'base.zip':
        cont = True
        while cont:
            try:
                ppo_model = PPO1(get_network_arch(env.name), env=env)
                logger.info(f'Saving base.zip PPO model...')
                ppo_model.save(os.path.join(config.MODELDIR, env.name, 'base.zip'))

                cont = False
            except IOError as e:
                sys.exit(f'Check zoo/{env.name}/ exists and read/write permission granted to user')
            except Exception as e:
                logger.error(e)
                time.sleep(2)
                
    else:
        raise Exception(f'\n{filename} not found')
    
    return ppo_model


def load_all_models(env, device):
    modellist = [f for f in os.listdir(os.path.join(config.MODELDIR, env.name)) if f.startswith("_model")]
    modellist.sort()
    models = [load_model(env, 'base.zip', device)]
    for model_name in modellist:
        models.append(load_model(env, name = model_name, device=device))
    return models


def get_best_model_name(env_name):
    modellist = [f for f in os.listdir(os.path.join(config.MODELDIR, env_name)) if f.startswith("_model")]
    
    if len(modellist)==0:
        filename = None
    else:
        modellist.sort()
        filename = modellist[-1]
        
    return filename

def get_model_stats(filename):
    if filename is None:
        generation = 0
        timesteps = 0
        best_rules_based = -np.inf
        best_reward = -np.inf
    else:
        stats = filename.split('_')
        generation = int(stats[2])
        best_rules_based = float(stats[3])
        best_reward = float(stats[4])
        timesteps = int(stats[5])
    return generation, timesteps, best_rules_based, best_reward


def reset_logs():
    try:
        filelist = [ f for f in os.listdir(config.LOGDIR) if f not in ['.gitignore']]
        for f in filelist:
            if os.path.isfile(f):  
                os.remove(os.path.join(config.LOGDIR, f))

        for i in range(100):
            if os.path.exists(os.path.join(config.LOGDIR, f'tb_{i}')):
                rmtree(os.path.join(config.LOGDIR, f'tb_{i}'))
        
        open(os.path.join(config.LOGDIR, 'log.txt'), 'a').close()
    
        
    except Exception as e :
        print(e)
        print('Reset logs failed')

def reset_models(model_dir):
    try:
        filelist = [ f for f in os.listdir(model_dir) if f not in ['.gitignore']]
        for f in filelist:
            os.remove(os.path.join(model_dir , f))
    except Exception as e :
        print(e)
        print('Reset models failed')