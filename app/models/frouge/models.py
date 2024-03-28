from typing import Callable, Dict, List, Optional, Tuple, Type, Union
from collections import OrderedDict

from gymnasium import spaces

from torch import nn, cuda
from torch import reshape, flatten, cat, add, Tensor, permute

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy

ACTIONS = 29
MAX_BOARD_SIZE = 120
BOARD_CELL_DIM_SIZE = 17
FEATURE_SIZE = 64
OBS_SIZE = 6204

class CustomNetwork(nn.Module):
    """
    Custom network for policy and value function.
    It receives as input the features extracted by the features extractor.

    :param feature_dim: dimension of the features extracted with the features_extractor (e.g. features from a CNN)
    :param last_layer_dim_pi: (int) number of units for the last layer of the policy network
    :param last_layer_dim_vf: (int) number of units for the last layer of the value network
    """

    def __init__(
        self,
        feature_dim: int,
        last_layer_dim_pi: int = 64,
        last_layer_dim_vf: int = 64,
    ):
        super().__init__()

        # IMPORTANT:
        # Save output dimensions, used to create the distributions
        self.latent_dim_pi = ACTIONS
        self.latent_dim_vf = 1

        self.resnet_extractor_board = nn.Sequential(
            convolutional(BOARD_CELL_DIM_SIZE,int(FEATURE_SIZE/2), kernel_size=9, strides=1, padding=4),
            convolutional(int(FEATURE_SIZE/2), BOARD_CELL_DIM_SIZE, kernel_size=9, strides=1, padding=4),
        )
        self.resnet_extractor_final = dense(OBS_SIZE, FEATURE_SIZE)
        self.residual = nn.Sequential(
            dense(FEATURE_SIZE, FEATURE_SIZE),
            dense(FEATURE_SIZE,FEATURE_SIZE, activation = None)
        )
        self.policy_head = nn.Sequential(
            dense(FEATURE_SIZE, FEATURE_SIZE),
            dense(FEATURE_SIZE, ACTIONS, batch_norm = True, activation = None)
        )
        self.value_head_first = dense(FEATURE_SIZE, FEATURE_SIZE)
        self.value_head_f = dense(FEATURE_SIZE, 1, batch_norm = False, activation = 'tanh')

    def forward(self, features: Tensor) -> Tuple[Tensor, Tensor]:
        """
        :return: (th.Tensor, th.Tensor) latent_policy, latent_value of the specified network.
            If all layers are shared, then ``latent_policy == latent_value``
        """
        return self.forward_actor(features), self.forward_critic(features)
    
    def _common_forward(self, features: Tensor) -> Tensor:

        extracted_features = self.forward_resnet_extractor(features)

        return extracted_features

    def forward_actor(self, features: Tensor) -> Tensor:
        # Policy network
        extracted_features = self._common_forward(features)
        policy_net = self.forward_policy_head(extracted_features)
        return policy_net

    def forward_critic(self, features: Tensor) -> Tensor:
        # Value network
        extracted_features = self._common_forward(features)
        value_net = self.forward_value_head(extracted_features)
        return value_net

    def forward_resnet_extractor(self, y, **kwargs):

        board, cards = split_input(y, int(y.shape[1])-(MAX_BOARD_SIZE*3*BOARD_CELL_DIM_SIZE))
        board = reshape(board,[ -1, MAX_BOARD_SIZE, 3, BOARD_CELL_DIM_SIZE ])
        board = permute(board,(0,3,1,2))
        
        board = self.resnet_extractor_board(board)
        board = permute(board,(0,2,3,1))
        board = flatten(board,1)

        y = cat([board, cards],1)
        y = self.resnet_extractor_final(y)

        shortcut = y

        y = self.residual(y)
        y = add(shortcut, y)

        y = nn.ReLU()(y)

        return y
    
    def forward_policy_head(self, y):

        policy = self.policy_head(y)
        return policy
    
    def forward_value_head(self, y):

        y = self.value_head_first(y)
        vf = self.value_head_f(y)
        return vf


class CustomPolicy(MaskableActorCriticPolicy):
    def __init__(
        self,
        observation_space: spaces.Space,
        action_space: spaces.Space,
        lr_schedule: Callable[[float], float],
        *args,
        **kwargs,
    ):
        # Disable orthogonal initialization
        kwargs["ortho_init"] = False
        super().__init__(
            observation_space,
            action_space,
            lr_schedule,
            # Pass remaining arguments to base class
            *args,
            **kwargs,
        )


    def _build_mlp_extractor(self) -> None:
        self.mlp_extractor = CustomNetwork(self.features_dim)


def split_input(processed_obs, split):
    obs_1 = processed_obs[...,:-split]
    obs_2 = processed_obs[...,-split:]
    return  obs_1, obs_2 


def convolutional(in_channels, out_channels, kernel_size, batch_norm = False, activation = 'relu', strides = (1,1), padding= 1):
    out = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=strides, padding=padding))
    if batch_norm:
        out.append(nn.BatchNorm1d(momentum = 0.9))
    if activation != None:
        if activation == "relu":
            out.append(nn.ReLU())
        elif activation == "tanh":
            out.append(nn.Tanh())
        else:
            raise Exception(f"Unknown activation layer {activation}")
    return out


def dense(in_size, out_size, batch_norm = False, activation = 'relu'):

    out = nn.Sequential(nn.Linear(in_size,out_size))
    
    if batch_norm:
        out.append(nn.BatchNorm1d(out_size, momentum=0.9))

    if activation != None:
        if activation == "relu":
            out.append(nn.ReLU())
        elif activation == "tanh":
            out.append(nn.Tanh())
        else:
            raise Exception(f"Unknown activation layer {activation}")
    
    return out


