import sys

import tensorflow as tf
import shutil
from utils.agents import Agent
from utils.files import load_model
from remote.envs.remote import RemoteEnv

TEMP_OUTPUT_DIR = 'TFLITE_OUTPUT'

model_filename = 'best_model.zip'
if len(sys.argv) > 1:
    model_filename = sys.argv[1]

env = RemoteEnv(verbose=True, manual=True)
ppo_model = load_model(env, model_filename)
ppo_agent = Agent('best_model', ppo_model)


def delete_tempdir():
    try:
        shutil.rmtree(TEMP_OUTPUT_DIR)
    except:
        pass


delete_tempdir()

try:
    with ppo_model.graph.as_default():
        tf.saved_model.simple_save(ppo_model.sess, TEMP_OUTPUT_DIR,
            inputs={"obs": ppo_model.policy_pi.obs_ph},
            outputs={"action": ppo_model.policy_pi._policy_proba,
                     "value": ppo_model.policy_pi.value_fn,
                     "q": ppo_model.policy_pi.q_value})
    converter = tf.lite.TFLiteConverter.from_saved_model(TEMP_OUTPUT_DIR)
    tflite_model = converter.convert()
    with open('best_model.tflite', 'wb') as f:
        f.write(tflite_model)
finally:
    delete_tempdir()
