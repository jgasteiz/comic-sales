import logging
import os

from envparse import env


def read_envfile():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_filepath = os.path.abspath(os.path.join(base_dir, os.environ["ENV_FILE"]))
        env.read_envfile(path=env_filepath)
    except Exception:
        logging.warning("Unable to read envfile")
