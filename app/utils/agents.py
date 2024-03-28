import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import random
import string
import logging as logger
import config
import torch

from sb3_contrib.common.maskable.utils import get_action_masks

def sample_action(action_probs):
    action = np.random.choice(len(action_probs), p = action_probs)
    return action


def mask_actions(legal_actions, action_probs):
    masked_action_probs = np.multiply(legal_actions, action_probs)
    masked_action_probs = masked_action_probs / np.sum(masked_action_probs)
    return masked_action_probs


class Agent():
  def __init__(self, name, model = None):
      self.name = name
      self.id = self.name + '_' + ''.join(random.choice(string.ascii_lowercase) for x in range(5))
      self.model = model
      self.points = 0
      if model != None:
        self.device = model.device

  def print_top_actions(self, action_probs):
    top5_action_idx = np.argsort(-action_probs)[:5]
    top5_actions = action_probs[top5_action_idx]
    logger.debug(f"Top 5 actions: {[str(i) + ': ' + str(round(a,2))[:5] for i,a in zip(top5_action_idx, top5_actions)]}")

  def choose_action(self, env, choose_best_action, mask_invalid_actions):
      if self.name == 'rules':
        action_probs = np.array(env.rules_move())
        value = None
        self.print_top_actions(action_probs)
        action = np.argmax(action_probs)
        logger.debug(f'Best action {action}')
        if not choose_best_action:
          action = sample_action(env.legal_actions / sum(env.legal_actions))
          logger.debug(f'Sampled action {action} chosen')
      else:
        action_masks = get_action_masks(env)
        action = self.model.predict(env.observation, deterministic = choose_best_action, action_masks = action_masks)[0]
        value = self.model.policy.predict_values(torch.from_numpy(np.array([env.observation])).to(self.device))[0]
        logger.debug(f'Value {float(value):.2f}')
        logger.debug(f'Best action {action}')

      return action



