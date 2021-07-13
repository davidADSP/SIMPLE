import numpy as np
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from tensorflow.keras.layers import BatchNormalization, Activation, Flatten, Add, Dense, Multiply, Concatenate, Lambda, Conv2D, Conv3D
import tensorflow.keras.backend as K
from stable_baselines.common.policies import ActorCriticPolicy
from stable_baselines.common.distributions import CategoricalProbabilityDistribution

ACTIONS = 29
FEATURE_SIZE = 64


class CustomPolicy(ActorCriticPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **kwargs):
        super(CustomPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=reuse, scale=True)

        with tf.variable_scope("model", reuse=reuse):

            obs, legal_actions = split_input(self.processed_obs, ACTIONS)

            extracted_features = resnet_extractor(obs, **kwargs)

            self._policy = policy_head(extracted_features, legal_actions)
            self._value_fn, self.q_value = value_head(extracted_features)
            self._proba_distribution  = CategoricalProbabilityDistribution(self._policy)

        self._setup_init()

    def step(self, obs, state=None, mask=None, deterministic=False):
        if deterministic:
            action, value, neglogp = self.sess.run([self.deterministic_action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        else:
            action, value, neglogp = self.sess.run([self.action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        return action, value, self.initial_state, neglogp

    def proba_step(self, obs, state=None, mask=None):
        return self.sess.run(self.policy_proba, {self.obs_ph: obs})

    def value(self, obs, state=None, mask=None):
        return self.sess.run(self.value_flat, {self.obs_ph: obs})


def split_input(processed_obs, split):
    obs = processed_obs[...,:-split]
    legal_actions = K.mean(processed_obs[...,-split:], axis = (1,2))
    return  obs, legal_actions 


def value_head(y):
    y = convolutional(y, 4, (1,1), batch_norm = False)
    y = Flatten()(y)
    y = dense(y,FEATURE_SIZE, batch_norm = False)

    vf = dense(y, 1, batch_norm = False, activation = 'tanh', name='vf')
    q = dense(y, ACTIONS, batch_norm = False, activation = 'tanh', name='q')
    return vf, q


def policy_head(y, legal_actions):
    y = convolutional(y, 1, (1,1), batch_norm = False)
    y = Flatten()(y)
    y = dense(y,FEATURE_SIZE, batch_norm = False)

    policy = dense(y, ACTIONS, batch_norm = False, activation = None, name='pi')
    
    mask = Lambda(lambda x: (1 - x) * -1e8)(legal_actions)   
    
    policy = Add()([policy, mask])
    return policy


def resnet_extractor(y, **kwargs):

    y = convolutional(y, FEATURE_SIZE, (3,3), batch_norm = False, strides = (2,1))
    y = residual(y, FEATURE_SIZE * 2, (3,3), batch_norm = False, strides = (2,1))
    return y


def convolutional(y, filters, kernel_size, batch_norm = False, activation = 'relu', strides = (1,1)):
    y = Conv2D(filters, kernel_size=kernel_size, strides=strides, padding='same')(y)
    if batch_norm:
        y = BatchNormalization(momentum = 0.9)(y)
    if activation:
        y = Activation('relu')(y)
    return y


def residual(y, filters, kernel_size, batch_norm, strides):
    shortcut = convolutional(y, filters, kernel_size = (1,1), batch_norm = False, strides = strides)
    shortcut = convolutional(shortcut, filters, kernel_size = (1,1), batch_norm = False, strides = strides)

    y = convolutional(y,filters, kernel_size=kernel_size, batch_norm = batch_norm, strides = strides)

    y = convolutional(y,filters, kernel_size=kernel_size, batch_norm = batch_norm, activation=None, strides = strides)
    y = Add()([shortcut, y])

    y = Activation('relu')(y)

    return y


def dense(y, filters, batch_norm = False, activation = 'relu', name = None):

    if batch_norm or activation:
        y = Dense(filters)(y)
    else:
        y = Dense(filters, name = name)(y)
    
    if batch_norm:
        if activation:
            y = BatchNormalization(momentum = 0.9)(y)
        else:
            y = BatchNormalization(momentum = 0.9, name = name)(y)

    if activation:
        y = Activation(activation, name = name)(y)
    
    return y


