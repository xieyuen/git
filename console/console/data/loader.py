import os
import json

import yaml

from .. import logger
from .saver import \
    create_default_user_data, create_default_config, default_user_data


config: dict = {}
userdata: list[dict] = []


@logger.catch
def load_config() -> dict:
    """
    Loads the config file
    """
    global config

    if os.path.exists('./config.yml'):
        with open('./config.yml', 'r', encoding='utf-8') as cfg_file:
            config = yaml.safe_load(cfg_file)

    elif os.path.exists('./config.json'):
        logger.warning('Config file is in JSON format, converting to YAML')
        with open('./config.json', 'r') as cfg_file:
            config = json.load(cfg_file)
        with open('./config.yml', 'w', encoding='utf-8') as cfg_file:
            yaml.safe_dump(config, cfg_file, default_flow_style=False, allow_unicode=True)
        os.remove('./config.json')

    else:
        logger.error('Config file not found')
        logger.debug('Creating default config file')
        create_default_config()

    return config


@logger.catch
def load_user_data() -> list:
    """
    Loads the user data file
    """
    global userdata
    if not os.path.exists('./data/user_data.json'):
        logger.warning('User data file not found, creating new one')
        create_default_user_data()
    with open("./data/user_data.json", "r", encoding='utf-8') as jsonfile:
        userdata = json.load(jsonfile)
    for acc in userdata:
        if not default_user_data[0].keys() == acc.keys():
            logger.error('Invalid user data file')
            create_default_user_data()
            userdata = default_user_data.copy()
            break
    return userdata
